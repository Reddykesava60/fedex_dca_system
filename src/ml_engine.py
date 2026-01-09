import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

MODEL_PATH = 'model.pkl'
ENCODERS_PATH = 'encoders.pkl'

class MLEngine:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.accuracy = 0.0

    def train_model(self, data_path):
        df = pd.read_csv(data_path)
        
        # Features and Target
        X = df[['amount_owed', 'days_overdue', 'customer_type', 'payment_history', 'contact_attempts']]
        y = df['recovery_likelihood']
        
        # Encode Categorical Features
        self.encoders = {}
        cat_cols = ['customer_type', 'payment_history']
        
        for col in cat_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.encoders[col] = le
            
        # Split Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Model
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Trained. Accuracy: {self.accuracy:.2f}")
        print(classification_report(y_test, y_pred))
        
        # Save Artifacts
        self.save_model()
        
    def predict_cases(self, df):
        """
        Takes a DataFrame of new cases and adds 'predicted_recovery' and 'confidence_score' columns.
        """
        if not self.model:
            self.load_model()
            
        # Prepare data for prediction
        X_pred = df[['amount_owed', 'days_overdue', 'customer_type', 'payment_history', 'contact_attempts']].copy()
        
        for col, le in self.encoders.items():
            # Handle unknown categories gracefully (if possible, otherwise let it error or fillna)
            # For simplicity, we assume valid categories or map to a default if needed.
            # Here we map carefully.
            X_pred[col] = X_pred[col].map(lambda s: self._safe_transform(le, s))
            
        predictions = self.model.predict(X_pred)
        probs = self.model.predict_proba(X_pred)
        
        df['predicted_recovery'] = predictions
        df['confidence_score'] = [max(p) for p in probs]
        
        return df

    def _safe_transform(self, encoder, value):
        try:
            return encoder.transform([value])[0]
        except ValueError:
            return 0 # Fallback for unseen labels

    def save_model(self):
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.encoders, ENCODERS_PATH)
        print("Model and encoders saved.")

    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.encoders = joblib.load(ENCODERS_PATH)
            return True
        return False

# Standalone training execution
if __name__ == "__main__":
    engine = MLEngine()
    if os.path.exists('training_data.csv'):
        engine.train_model('training_data.csv')
    else:
        print("training_data.csv not found!")
