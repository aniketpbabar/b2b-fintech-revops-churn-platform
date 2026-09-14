import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import joblib

def generate_sample_b2b_data(samples=5000):
    """Generates synthetic B2B merchant data matching Kaggle schemas for local testing."""
    np.random.seed(42)
    merchant_ids = [f"MCH-{10000 + i}" for i in range(samples)]
    gpv_monthly = np.random.exponential(scale=50000, size=samples) + 5000
    quota_attainment = np.random.uniform(0.4, 1.5, size=samples)
    tenure_months = np.random.randint(1, 60, size=samples)
    support_tickets = np.random.poisson(lam=2, size=samples)
    failed_payouts = np.random.poisson(lam=0.5, size=samples)
    tier = np.random.choice(['SMB', 'Mid-Market', 'Enterprise'], size=samples, p=[0.6, 0.3, 0.1])
    
    # Calculate churn probability based on synthetic features
    churn_prob = 1 / (1 + np.exp(-(-2.0 - 0.00001*gpv_monthly - 1.5*quota_attainment + 0.3*support_tickets + 0.8*failed_payouts - 0.03*tenure_months)))
    churn_label = (churn_prob > np.random.uniform(0, 1, size=samples)).astype(int)

    df = pd.DataFrame({
        'merchant_id': merchant_ids,
        'gpv_monthly': gpv_monthly,
        'quota_attainment': quota_attainment,
        'tenure_months': tenure_months,
        'support_tickets_30d': support_tickets,
        'failed_payouts_30d': failed_payouts,
        'merchant_tier': tier,
        'churned': churn_label
    })
    return df

def train_pipeline(df):
    X = df.drop(columns=['merchant_id', 'churned'])
    y = df['churned']

    num_cols = ['gpv_monthly', 'quota_attainment', 'tenure_months', 'support_tickets_30d', 'failed_payouts_30d']
    cat_cols = ['merchant_tier']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42, eval_metric='logloss'))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model.fit(X_train, y_train)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"Model Training Completed. ROC-AUC Score: {auc_score:.4f}")
    assert auc_score >= 0.78, "ROC-AUC target of 0.78 not met."

    joblib.dump(model, 'models/xgboost_churn_model.pkl')
    print("Model successfully saved to models/xgboost_churn_model.pkl")

if __name__ == "__main__":
    data = generate_sample_b2b_data()
    data.to_csv('data/merchant_data.csv', index=False)
    train_pipeline(data)
