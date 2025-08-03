# app.py (Cloud Training Version)

import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

# --- New Logic: Train Models on the Server if They Don't Exist ---
# This code runs once when the server starts up.
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
            # We use os.system to execute the training script from the command line
            result = os.system(f"python {script_file}")
            if result != 0:
                print(f"!!! Error running {script_file}. Deployment will fail.")
                # Exit if a training script fails
                exit(1)
            print(f"Successfully ran {script_file}.")
        else:
            print(f"'{model_file}' already exists. Skipping training.")

# --- Run the Training Check ---
print("--- Starting Server Initialization ---")
train_models_if_needed()
print("--- Model check/training complete ---")


# --- Initialize Flask App and Load Models (Same as before) ---
app = Flask(__name__)
CORS(app)

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


# --- Prediction Endpoint (Same as before) ---
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # ... (The rest of your prediction logic is the same) ...
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

    # --- 3. Cancer Prediction (Simulated) ---
    cancer_risk_simulated = (1 if data.get('smoking') == 'yes' else 0) * 40 + \
                            (1 if data.get('alcohol') == 'yes' else 0) * 20 + \
                            (int(data.get('age', 0)) / 100) * 30 + \
                            (1 if float(data.get('bmi', 0)) > 30 else 0) * 10
    cancer_risk = min(cancer_risk_simulated, 95.0)

    return jsonify({
        'diabetes': { 'risk': diabetes_risk }, 'heartDisease': { 'risk': heart_disease_risk }, 'cancer': { 'risk': cancer_risk }
    })

print("--- Server setup complete. Ready for requests. ---")
