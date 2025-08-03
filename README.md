# Full-Stack Chronic Disease Predictor 🩺

This is a full-stack web application that predicts the risk of chronic diseases like diabetes, heart disease, and cancer. The frontend is built with React, and the backend is a Python Flask server that uses pre-trained machine learning models to make predictions.

## Screenshot 📸

![Chronic Disease Predictor Screenshot](https://i.ibb.co/9g0y1fP/Screenshot-2024-05-23-at-12-44-15-PM.png)

## Features ✨

* **Interactive Frontend:** A user-friendly form to input health data.
* **Machine Learning Backend:** A Python Flask server that uses trained models to predict disease risk.
* **Multiple Disease Models:** Includes separate models for predicting Diabetes, Heart Disease, and Cancer.
* **Risk Analysis:** Visual representation of disease risks in a bar chart.
* **Personalized Recommendations:** Provides health recommendations based on the prediction results.
* **Responsive Design:** Fully responsive and works on various devices.

## Technologies Used 💻

* **Frontend:**
    * React
    * Tailwind CSS
    * Recharts
* **Backend:**
    * Python
    * Flask
    * Pandas
    * Scikit-learn

## Getting Started 🚀

To get a local copy up and running, you need to set up both the backend and the frontend.

### Prerequisites

* **Node.js & npm:** For the frontend. Download from [nodejs.org](https://nodejs.org/).
* **Python 3:** For the backend. Download from [python.org](https://www.python.org/).
* **pip:** Python package installer.

### Backend Setup

1.  **Navigate to the backend directory:**
    ```sh
    cd backend
    ```
2.  **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` file from the imported libraries in `app.py` if one doesn't exist. The main libraries are `flask`, `pandas`, `scikit-learn`, `flask-cors`)*

3.  **Run the Flask server:**
    ```sh
    python app.py
    ```
    The backend server will start on `http://127.0.0.1:5000`.

### Frontend Setup

1.  **Navigate to the frontend directory in a new terminal:**
    ```sh
    cd frontend
    ```
2.  **Install NPM packages:**
    ```sh
    npm install
    ```
3.  **Run the React app:**
    ```sh
    npm start
    ```
    The frontend development server will start, usually on [http://localhost:3000](http://localhost:3000).

Once both the backend and frontend servers are running, you can open your browser to `http://localhost:3000` to use the application.
