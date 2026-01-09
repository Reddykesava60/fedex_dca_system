import pandas as pd
import numpy as np

# Mock Database of DCAs
DCAS = [
    {"name": "Alpha Collections", "region": "North", "specialty": "High", "performance": 0.85},
    {"name": "Beta Recovery", "region": "South", "specialty": "General", "performance": 0.72},
    {"name": "Gamma Partners", "region": "East", "specialty": "High", "performance": 0.78},
    {"name": "Delta Agency", "region": "West", "specialty": "Low", "performance": 0.65},  # Handles difficult cases
    {"name": "Epsilon Group", "region": "North", "specialty": "General", "performance": 0.70},
    {"name": "Zeta Solutions", "region": "East", "specialty": "Low", "performance": 0.60},
]

class DCAAssigner:
    @staticmethod
    def assign_case(row):
        """
        Assigns a DCA based on Region and Predicted Recovery / Difficulty.
        """
        region = row['region']
        likelihood = row.get('recovery_likelihood', 'Medium') # Ground truth or predicted
        
        # Rule 1: High potential -> Top performers in Region
        if likelihood == 'High':
            candidates = [d for d in DCAS if d['region'] == region and d['performance'] > 0.75]
            if not candidates:
                candidates = [d for d in DCAS if d['region'] == region] # Fallback
                
        # Rule 2: Low potential (Difficult) -> Specialists or Spread load
        elif likelihood == 'Low':
            candidates = [d for d in DCAS if d['specialty'] == 'Low' and d['region'] == region]
            if not candidates:
                 # If no specialist in region, pick any generalist in region
                candidates = [d for d in DCAS if d['region'] == region]

        # Rule 3: Medium -> General pool in Region
        else:
            candidates = [d for d in DCAS if d['region'] == region]

        # Fallback if no match in region (very rare with this data)
        if not candidates:
             candidates = DCAS

        # Load Balancing (Random choice among candidates for now)
        chosen = np.random.choice(candidates)
        return chosen['name']

class CaseManager:
    def __init__(self):
        self.cases_df = pd.DataFrame()

    def load_cases(self, df):
        """
        Loads new cases, keeps existing ones (simple append or replace for demo).
        For this prototype, we'll replace or append if we want state.
        """
        self.cases_df = df
        
    def get_cases(self):
        return self.cases_df

    def get_summary_stats(self):
        if self.cases_df.empty:
            return {}
        
        return {
            "total_cases": len(self.cases_df),
            "total_amount": self.cases_df['amount_owed'].sum(),
            "avg_recovery_rate": 68, # Mocked historical
            "high_priority_count": len(self.cases_df[self.cases_df['priority_score'] > 7]) if 'priority_score' in self.cases_df else 0
        }

class AnalyticsService:
    @staticmethod
    def calculate_dca_performance(df):
        if df.empty or 'dca_assigned' not in df.columns:
            return pd.DataFrame()
            
        # Mocking 'resolved' status to calculate performance
        # In a real app, we'd have a status column.
        # We will group by DCA and count assignments.
        stats = df.groupby('dca_assigned').agg(
            cases_assigned=('case_id', 'count'),
            total_amount=('amount_owed', 'sum'),
            avg_likelihood_score=('confidence_score', 'mean') if 'confidence_score' in df.columns else ('amount_owed', 'count') # fallback
        ).reset_index()
        
        return stats
