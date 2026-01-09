import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    data = {
        'case_id': [f'C{i:04d}' for i in range(1, num_samples+1)],
        'amount_owed': np.random.randint(100, 50000, num_samples),
        'days_overdue': np.random.randint(10, 365, num_samples),
        'customer_type': np.random.choice(['Enterprise', 'SMB', 'Individual'], num_samples, p=[0.2, 0.5, 0.3]),
        'payment_history': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], num_samples, p=[0.1, 0.3, 0.4, 0.2]),
        'contact_attempts': np.random.randint(0, 10, num_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West'], num_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Simulate Recovery Likelihood (Logic-based ground truth for training)
    # High likelihood if: Low amount, Low overdue, Good history
    # Low likelihood if: High amount, High overdue, Poor history
    
    def calculate_recovery_likelihood(row):
        score = 0
        
        # Amount factor
        if row['amount_owed'] < 1000: score += 20
        elif row['amount_owed'] < 5000: score += 10
        elif row['amount_owed'] > 20000: score -= 10
        
        # Days Overdue factor
        if row['days_overdue'] < 30: score += 30
        elif row['days_overdue'] < 60: score += 20
        elif row['days_overdue'] > 120: score -= 20
        elif row['days_overdue'] > 180: score -= 30
        
        # Payment History factor
        if row['payment_history'] == 'Excellent': score += 30
        elif row['payment_history'] == 'Good': score += 10
        elif row['payment_history'] == 'Poor': score -= 20
        
        # Contact attempts
        if row['contact_attempts'] > 5: score -= 10 # Annoyed customer or unreachable
        
        # Determine label
        if score >= 40: return 'High'
        elif score >= 10: return 'Medium'
        else: return 'Low'

    df['recovery_likelihood'] = df.apply(calculate_recovery_likelihood, axis=1)
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(1000)
    df.to_csv('training_data.csv', index=False)
    print("Syntehtic data generated: training_data.csv (1000 records)")
