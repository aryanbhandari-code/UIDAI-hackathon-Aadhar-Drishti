from sklearn.ensemble import IsolationForest
from prophet import Prophet
import pandas as pd

def run_intelligence_engine(df):
    """
    Runs Isolation Forest for anomaly detection and prepares profile data.
    """
    # 1. Create District Profile (Aggregated View)
    profile = df.groupby('district').agg({
        'migration_score': 'mean', 
        'total_vol': 'sum', 
        'state': 'first',
        'bio_update_child': 'sum',
        'enrol_newborn': 'sum'
    }).reset_index()
    
    # 2. Anomaly Detection (Isolation Forest)
    iso = IsolationForest(contamination=0.05, random_state=42)
    profile['anomaly_score'] = iso.fit_predict(profile[['migration_score', 'total_vol']])
    profile['status'] = profile['anomaly_score'].apply(lambda x: 'Critical' if x == -1 else 'Normal')
    
    # 3. Logic-Based Reasoning (Explainable AI)
    means = profile.mean(numeric_only=True)
    
    def generate_reasoning(row):
        reasons = []
        if row['migration_score'] > means['migration_score'] * 1.5:
            reasons.append("High Migration Intensity")
        if row['total_vol'] > means['total_vol'] * 2:
            reasons.append("Extreme Workload")
        if row['bio_update_child'] < means['bio_update_child'] * 0.5:
            reasons.append("Low Child Compliance")
        return " | ".join(reasons) if reasons else "Statistical Deviation"
    
    profile['ai_reasoning'] = profile.apply(generate_reasoning, axis=1)
    
    return profile

def run_forecast(df, district_name):
    """
    Runs Facebook Prophet for Time-Series Forecasting.
    """
    subset = df[df['district'] == district_name].copy()
    if len(subset) < 10: return None
    
    # Prepare for Prophet
    prophet_df = subset.groupby('date')['total_vol'].sum().reset_index()
    prophet_df.columns = ['ds', 'y']
    
    m = Prophet(daily_seasonality=True)
    m.fit(prophet_df)
    
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast