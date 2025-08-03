# train_heart_model.py (Corrected for NaN values)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

print("Heart Disease Model Training Script started...")

# 1. Load the dataset
print("Loading heart disease dataset...")
try:
    data = pd.read_csv('heart_disease_dataset.csv', sep=',')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'heart_disease_dataset.csv' not found. Make sure it's in the 'backend' folder.")
    exit()

# 2. Prepare the data
print("Preprocessing data...")
# --- NEW STEP: Handle Missing Values ---
# We will fill any missing numeric values with the median of their column.
# First, select only numeric columns for median calculation
numeric_cols = data.select_dtypes(include=['number']).columns
for col in numeric_cols:
    median_val = data[col].median()
    data[col].fillna(median_val, inplace=True)
print("Missing values handled.")

# Convert all columns with object type (text) to numeric using one-hot encoding
data_processed = pd.get_dummies(data, drop_first=True)

# The target variable is 'num'. We will convert it to a binary outcome:
# 0 = no heart disease, 1 = heart disease present (if num > 0)
data_processed['target'] = (data_processed['num'] > 0).astype(int)

# Drop the original 'num' column and the 'id' column as they are not needed for prediction
X = data_processed.drop(['num', 'target', 'id'], axis=1)
y = data_processed['target']

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

# 6. Save the trained model
print("Saving the model to 'heart_disease_model.pkl'...")
with open('heart_disease_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Heart disease model saved successfully!")
print("Script finished.")
