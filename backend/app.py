# app.py (Final Production Version with explicit CORS)

import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Configure CORS ---
# This is the crucial change. We are explicitly allowing all origins
# to make requests to our /predict endpoint.
CORS(app, resources={r"/predict": {"origins": "*"}})


# --- NEW: Root Endpoint ---
# This endpoint is for checking the server's status.
@app.route('/', methods=['GET'])
def index():
    """
    A simple endpoint to confirm that the API is live.
    """
    return jsonify({
        "status": "ok",
        "message": "Chronic Disease Predictor API is running successfully."
    })


# --- Train Models on the Server if They Don't Exist ---
def train_models_if_needed():
    """
    Checks for the existence of .pkl files. If not found, it runs the
    corresponding training script to generate them on the server.
    """
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
        else:
            print(f"'{model_file}' already exists. Skipping training.")

# --- Run the Training Check ---
print("--- Starting Server Initialization ---")
train_models_if_needed()
print("--- Model check/training complete ---")


# --- Load Models into Memory ---
print("Loading models into memory...")
try:
    with open('diabetes_model.pkl', 'rb') as f:
        diabetes_model = pickle.load(f)
    print("Diabetes model loaded.")

    with open('heart_disease_model.pkl', 'rb') as f:
        heart_disease_model = pickle.load(f)
    print("Heart disease model loaded.")

    with open('cancer_model.pkl', 'rb') as f:
        cancer_model = pickle.load(f)
    print("Cancer model loaded.")
except FileNotFoundError as e:
    print(f"!!! Error loading models after training: {e}.")
    exit(1)
print("All models loaded successfully.")


# --- Prediction Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
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
    # NOTE: The UI form does not collect the 30 specific features needed for this model.
    # We are using a set of average, default values for a baseline prediction.
    # A future improvement would be to create a more detailed form to collect this data.
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
        'diabetes': { 'risk': diabetes_risk }, 'heartDisease': { 'risk': heart_disease_risk }, 'cancer': { 'risk': cancer_risk }
    })

print("--- Server setup complete. Ready for requests. ---")
