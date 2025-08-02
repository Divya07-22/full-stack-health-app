# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

print("Script started...")

# 1. Load the dataset
print("Loading dataset...")
try:
    data = pd.read_csv('diabetes.csv')
    print("Dataset loaded successfully.")
    print("First 5 rows of the dataset:")
    print(data.head())
except FileNotFoundError:
    print("Error: 'diabetes.csv' not found. Make sure it's in the 'backend' folder.")
    exit()

# 2. Prepare the data
# We will predict the 'Outcome' column (0 for no diabetes, 1 for diabetes)
# All other columns are our features.
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# 3. Split the data into training and testing sets
# This allows us to evaluate the model's performance on data it hasn't seen before.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into training and testing sets.")

# 4. Initialize and train the model
# A RandomForestClassifier is a good, reliable choice for this kind of task.
print("Training the RandomForestClassifier model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# 5. Evaluate the model (optional, but good practice)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# 6. Save the trained model to a file
# We use pickle to serialize our model into a file that we can load later in our API.
print("Saving the model to 'diabetes_model.pkl'...")
with open('diabetes_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved successfully!")
print("Script finished.")
