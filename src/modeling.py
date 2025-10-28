"""
Machine learning modeling module
"""
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import pandas as pd

def train_delay_predictor(df):
    """Train ML model to predict delivery delays"""
    
    # Prepare features for model
    df_model = df.dropna(subset=['Is_Delayed', 'Distance_KM', 'Total_Cost'])
    
    # Select features
    feature_cols = [
        'Distance_KM', 
        'Traffic_Delay_Minutes', 
        'Total_Cost', 
        'Order_Value_INR', 
        'Promised_Delivery_Days'
    ]
    
    X = df_model[feature_cols]
    y = df_model['Is_Delayed']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100, 
        random_state=42, 
        max_depth=5
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    # Feature importance
    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    return model, feature_cols, accuracy, roc_auc, importances
