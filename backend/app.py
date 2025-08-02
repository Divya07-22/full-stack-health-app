# app.py (Corrected Version)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- Load All Trained Models ---
print("Loading models...")
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
    print(f"Error loading models: {e}. Please ensure all .pkl files are in the 'backend' folder.")
    exit()
print("All models loaded successfully.")


# Define the main prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives patient data, runs all three models, and returns a combined prediction.
    """
    data = request.get_json()
    print(f"Received data: {data}")

    # --- 1. Diabetes Prediction ---
    diabetes_features = pd.DataFrame({
        'Pregnancies': [0],
        'Glucose': [float(data.get('glucose', 0))],
        'BloodPressure': [float(data.get('bloodPressure', 0))],
        'SkinThickness': [0],
        'Insulin': [0],
        'BMI': [float(data.get('bmi', 0))],
        'DiabetesPedigreeFunction': [0.5],
        'Age': [int(data.get('age', 0))]
    })
    diabetes_risk_proba = diabetes_model.predict_proba(diabetes_features)[0][1]
    diabetes_risk = diabetes_risk_proba * 100
    print(f"Diabetes Prediction - Risk: {diabetes_risk:.2f}%")

    # --- 2. Heart Disease Prediction (Corrected Features) ---
    # The feature names now exactly match the columns from the training script.
    heart_features_dict = {
        'age': int(data.get('age', 0)),
        'trestbps': float(data.get('bloodPressure', 120)),
        'chol': float(data.get('cholesterol', 200)),
        'thalch': 150,
        'oldpeak': 1.0,
        'ca': 0.0,  # Corrected: 'ca' is a single numeric feature
        'sex_Male': 1 if data.get('gender') == 'male' else 0,
        'dataset_Hungary': 0, 'dataset_Switzerland': 0, 'dataset_VA Long Beach': 0,
        'cp_atypical angina': 0, 'cp_non-anginal': 1, 'cp_typical angina': 0,
        'fbs_True': 1 if float(data.get('glucose', 0)) > 120 else 0,
        'restecg_normal': 1,
        'restecg_st-t abnormality': 0, # Corrected: This feature was missing
        'exang_True': 0,
        'slope_flat': 1, 'slope_upsloping': 0,
        'thal_normal': 1, 'thal_reversable defect': 0
    }
    heart_features = pd.DataFrame([heart_features_dict])
    
    # Ensure the column order is the same as during training
    # This is a robust way to prevent future errors
    expected_heart_cols = heart_disease_model.feature_names_in_
    heart_features = heart_features.reindex(columns=expected_heart_cols, fill_value=0)

    heart_disease_risk_proba = heart_disease_model.predict_proba(heart_features)[0][1]
    heart_disease_risk = heart_disease_risk_proba * 100
    print(f"Heart Disease Prediction - Risk: {heart_disease_risk:.2f}%")

    # --- 3. Cancer Prediction (Simulated) ---
    cancer_risk_simulated = (1 if data.get('smoking') == 'yes' else 0) * 40 + \
                            (1 if data.get('alcohol') == 'yes' else 0) * 20 + \
                            (int(data.get('age', 0)) / 100) * 30 + \
                            (1 if float(data.get('bmi', 0)) > 30 else 0) * 10
    cancer_risk = min(cancer_risk_simulated, 95.0)
    print(f"Cancer Prediction (Simulated) - Risk: {cancer_risk:.2f}%")

    # --- Return Combined Response ---
    return jsonify({
        'diabetes': { 'risk': diabetes_risk },
        'heartDisease': { 'risk': heart_disease_risk },
        'cancer': { 'risk': cancer_risk }
    })

if __name__ == '__main__':
    print("Starting comprehensive Flask server...")
    app.run(debug=True, port=5000)
