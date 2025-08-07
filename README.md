Full-Stack Chronic Disease Predictor 🩺
This is a full-stack web application designed for the early prediction of chronic diseases. By leveraging machine learning, it provides users with a risk assessment for Diabetes, Heart Disease, and Cancer based on their health metrics.

The goal is to empower individuals to take proactive steps toward their health by providing accessible, data-driven insights.

✨ Key Features
Intuitive User Interface: A clean, responsive form built with React and Tailwind CSS makes data entry simple and fast on any device.

AI-Powered Predictions: The Python Flask backend uses pre-trained Scikit-learn models to analyze user data and predict disease risk in real-time.

Actionable Insights: Displays prediction results in an easy-to-understand bar chart (using Recharts) and provides personalized health recommendations based on the risk profile.

Multi-Disease Support: Includes dedicated models for three of the most common chronic diseases.
🚀 Live Demo
Check out the live application here:

Frontend (Netlify): https://spectacular-faun-929149.netlify.app/

Backend (Render): https://health-predictor-backend.onrender.com/

🛠️ Tech Stack
Component	Technology
Frontend	React, Tailwind CSS, Recharts
Backend	Python, Flask, Pandas, Scikit-learn
Deployment	Netlify (Frontend), Render (Backend)

Export to Sheets
⚙️ How It Works
The application follows a simple, robust workflow:

Data Input: The user enters their health metrics into the React frontend.

API Request: The frontend sends the data to the Flask backend via an API call.

Data Processing: The Flask server receives the data and uses Pandas to format it into the structure required by the ML models.

Prediction: The appropriate Scikit-learn model (.pkl file) is loaded to predict the disease risk.

API Response: The backend sends the prediction results (risk percentages) back to the frontend.

Visualization: The React app displays the results in a bar chart and shows personalized recommendations.

Local Setup Guide
To get a local copy up and running, follow these steps.

Prerequisites
Node.js & npm: Download & Install Node.js

Python 3: Download & Install Python

Git: Download & Install Git

Installation
Clone the repository:

Bash

git clone <your-repository-url>
cd <repository-folder>
Backend Setup (Flask):
Open a terminal in the project's root directory.

Bash

# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
# For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
.\venv\Scripts\activate

# Install the required Python packages
pip install flask pandas scikit-learn flask-cors

# Run the Flask server
python app.py
Your backend will now be running on http://127.0.0.1:5000.

Frontend Setup (React):
Open a new terminal in the project's root directory.

Bash

# Navigate to the frontend directory
cd frontend

# Install NPM packages
npm install

# Run the React development server
npm start
Your frontend will open automatically in your browser at http://localhost:3000.

You can now use the application locally!

🗺️ Future Roadmap
User Authentication: Add user accounts to save and track prediction history.

Expand Disease Models: Integrate models for other conditions like kidney disease or stroke.

Containerization: Add Docker support for easier setup and deployment.

Data Sources: Provide links and information about the datasets used to train the models.
