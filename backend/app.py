import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import pandas as pd
import numpy as np
import openai

# --- Initialize App and Extensions ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Database Configuration ---
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_url = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- JWT Configuration ---
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-key-for-dev')

# --- OpenAI Configuration ---
openai.api_key = os.environ.get('OPENAI_API_KEY')
if not openai.api_key:
    print("Warning: OPENAI_API_KEY not found. Chatbot will not work.")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# --- Database Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# --- Train Models on the Server if They Don't Exist ---
def train_models_if_needed():
    training_map = {
        'diabetes_model.pkl': 'train_model.py',
        'heart_disease_model.pkl': 'train_heart_model.py',
        'cancer_model.pkl': 'train_cancer_model.py'
    }
    for model_file, script_file in training_map.items():
        if not os.path.exists(model_file):
            print(f"'{model_file}' not found. Running training script: {script_file}")
            result = os.system(f"python {script_file}")
            if result != 0:
                print(f"!!! Error running {script_file}. Deployment will fail.")
                exit(1)
            print(f"Successfully ran {script_file}.")

# --- Create DB tables and run training check within app context ---
with app.app_context():
    db.create_all()
    train_models_if_needed()

# --- Load Models into Memory ---
print("Loading models into memory...")
with open('diabetes_model.pkl', 'rb') as f:
    diabetes_model = pickle.load(f)
with open('heart_disease_model.pkl', 'rb') as f:
    heart_disease_model = pickle.load(f)
with open('cancer_model.pkl', 'rb') as f:
    cancer_model = pickle.load(f)
print("All models loaded successfully.")


# --- Authentication Endpoints ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'email': user.email, 'id': user.id})
        return jsonify(access_token=access_token)
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# --- Chatbot Endpoint ---
@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_message = data.get('message')
    prediction_context = data.get('prediction')
    if not openai.api_key:
        return jsonify({"reply": "Sorry, the chatbot is not configured correctly. Missing API key."}), 500
    system_prompt = "You are a helpful and empathetic AI health assistant. Your role is to explain health risks in a clear and simple way. Do not provide a diagnosis or medical advice. Always encourage the user to consult a real doctor."
    user_prompt = f"Here is my latest health risk assessment:\n"
    if prediction_context:
        user_prompt += f"- Diabetes Risk: {prediction_context['diabetes']['risk']}%\n"
        user_prompt += f"- Heart Disease Risk: {prediction_context['heartDisease']['risk']}%\n"
        user_prompt += f"- Cancer Risk: {prediction_context['cancer']['risk']}%\n\n"
    else:
        user_prompt += "No prediction has been run yet.\n\n"
    user_prompt += f"Based on this, please answer my question: '{user_message}'"
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return jsonify({"reply": "Sorry, I encountered an error while generating a response."}), 500


# --- Protected Prediction Endpoint ---
@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    current_user = get_jwt_identity()
    print(f"Prediction request from user: {current_user['email']}")
    data = request.get_json()
    
    # --- 1. Diabetes Prediction ---
    diabetes_features = pd.DataFrame({
        'Pregnancies': [0], 'Glucose': [float(data.get('glucose', 0))], 'BloodPressure': [float(data.get('bloodPressure', 0))],
        'SkinThickness': [0], 'Insulin': [0], 'BMI': [float(data.get('bmi', 0))],
        'DiabetesPedigreeFunction': [0.5], 'Age': [int(data.get('age', 0))]
    })
    diabetes_risk_proba = diabetes_model.predict_proba(diabetes_features)[0][1]
    diabetes_risk = diabetes_risk_proba * 100

    # --- 2. Heart Disease Prediction ---
    heart_features_dict = {
        'age': int(data.get('age', 0)), 'trestbps': float(data.get('bloodPressure', 120)), 'chol': float(data.get('cholesterol', 200)),
        'thalch': 150, 'oldpeak': 1.0, 'ca': 0.0, 'sex_Male': 1 if data.get('gender') == 'male' else 0,
        'dataset_Hungary': 0, 'dataset_Switzerland': 0, 'dataset_VA Long Beach': 0, 'cp_atypical angina': 0,
        'cp_non-anginal': 1, 'cp_typical angina': 0, 'fbs_True': 1 if float(data.get('glucose', 0)) > 120 else 0,
        'restecg_normal': 1, 'restecg_st-t abnormality': 0, 'exang_True': 0, 'slope_flat': 1, 'slope_upsloping': 0,
        'thal_normal': 1, 'thal_reversable defect': 0
    }
    heart_features = pd.DataFrame([heart_features_dict])
    expected_heart_cols = heart_disease_model.feature_names_in_
    heart_features = heart_features.reindex(columns=expected_heart_cols, fill_value=0)
    heart_disease_risk_proba = heart_disease_model.predict_proba(heart_features)[0][1]
    heart_disease_risk = heart_disease_risk_proba * 100

    # --- 3. Cancer Prediction (Using Real Model) ---
    cancer_features_dict = {
        'radius_mean': 14.1, 'texture_mean': 19.2, 'perimeter_mean': 91.9, 'area_mean': 654.8,
        'smoothness_mean': 0.096, 'compactness_mean': 0.104, 'concavity_mean': 0.088,
        'concave points_mean': 0.048, 'symmetry_mean': 0.181, 'fractal_dimension_mean': 0.062,
        'radius_se': 0.405, 'texture_se': 1.21, 'perimeter_se': 2.86, 'area_se': 40.3,
        'smoothness_se': 0.007, 'compactness_se': 0.025, 'concavity_se': 0.031,
        'concave points_se': 0.011, 'symmetry_se': 0.020, 'fractal_dimension_se': 0.003,
        'radius_worst': 16.2, 'texture_worst': 25.6, 'perimeter_worst': 107.2, 'area_worst': 880.5,
        'smoothness_worst': 0.132, 'compactness_worst': 0.254, 'concavity_worst': 0.272,
        'concave points_worst': 0.114, 'symmetry_worst': 0.290, 'fractal_dimension_worst': 0.083
    }
    cancer_features = pd.DataFrame([cancer_features_dict])
    expected_cancer_cols = cancer_model.feature_names_in_
    cancer_features = cancer_features.reindex(columns=expected_cancer_cols, fill_value=0)
    cancer_risk_proba = cancer_model.predict_proba(cancer_features)[0][1]
    cancer_risk = cancer_risk_proba * 100

    return jsonify({
        'diabetes': { 'risk': diabetes_risk },
        'heartDisease': { 'risk': heart_disease_risk },
        'cancer': { 'risk': cancer_risk }
    })

# --- Root Endpoint ---
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "message": "Chronic Disease Predictor API is running successfully."
    })
