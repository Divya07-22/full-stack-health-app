# train_cancer_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

print("Cancer Model Training Script started...")

# 1. Load the dataset
print("Loading cancer dataset...")
try:
    data = pd.read_csv('data.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'data.csv' not found. Make sure it's in the 'backend' folder.")
    exit()

# 2. Prepare the data
# Drop unnecessary columns
if 'Unnamed: 32' in data.columns:
    data = data.drop(['id', 'Unnamed: 32'], axis=1)
else:
    data = data.drop('id', axis=1)

# The target variable is 'diagnosis'. It's categorical (M = malignant, B = benign).
# We need to convert it to a numeric format.
le = LabelEncoder()
data['diagnosis'] = le.fit_transform(data['diagnosis']) # M becomes 1, B becomes 0

X = data.drop('diagnosis', axis=1)
y = data['diagnosis']

print("First 5 rows of the processed data:")
print(X.head())

# 3. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into training and testing sets.")

# 4. Initialize and train the RandomForestClassifier model
print("Training the model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# 5. Evaluate the model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# 6. Save the trained model and the label encoder
print("Saving the model to 'cancer_model.pkl'...")
with open('cancer_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Cancer model saved successfully!")
print("Script finished.")
