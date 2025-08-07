import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import pandas as pd
import numpy as np
import openai # Import the new library

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
# Get the API key from the environment variable
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
    # ... (rest of the User model is the same) ...
    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# --- Train Models & Create DB Tables ---
# ... (Your train_models_if_needed function and model loading code is the same) ...
def train_models_if_needed():
    # ... (implementation) ...
    pass
with app.app_context():
    db.create_all()
    # train_models_if_needed() # You can comment this out after the first successful deploy to speed up restarts

# --- Load Models into Memory ---
# ... (Your model loading code is the same) ...
diabetes_model = None
heart_disease_model = None
cancer_model = None
try:
    with open('diabetes_model.pkl', 'rb') as f: diabetes_model = pickle.load(f)
    with open('heart_disease_model.pkl', 'rb') as f: heart_disease_model = pickle.load(f)
    with open('cancer_model.pkl', 'rb') as f: cancer_model = pickle.load(f)
    print("All models loaded successfully.")
except:
    print("Models not found, will be trained on first run.")


# --- Authentication Endpoints (Same as before) ---
@app.route('/signup', methods=['POST'])
def signup():
    # ... (implementation) ...
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    # ... (implementation) ...
    return jsonify(access_token="dummy_token")


# --- NEW: Chatbot Endpoint ---
@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_message = data.get('message')
    prediction_context = data.get('prediction')

    if not openai.api_key:
        return jsonify({"reply": "Sorry, the chatbot is not configured correctly. Missing API key."}), 500

    # Create a detailed prompt for the AI
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


# --- Protected Prediction Endpoint (Same as before) ---
@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    # ... (Your prediction logic is the same) ...
    return jsonify({
        'diabetes': { 'risk': 50.0 },
        'heartDisease': { 'risk': 60.0 },
        'cancer': { 'risk': 70.0 }
    })

# --- Root Endpoint (Same as before) ---
@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "ok"})

