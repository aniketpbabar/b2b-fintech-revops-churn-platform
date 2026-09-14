import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

st.set_page_config(page_title="FinTech RevOps & Churn Platform", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("models/xgboost_churn_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("data/merchant_data.csv")

try:
    model = load_model()
    df = load_data()

    st.title("💳 RevOps Merchant Churn & Retention Intelligence")
    st.markdown("Proactive merchant risk modeling, GPV impact analysis, and strategy controls.")

    # Sidebar Controls
    st.sidebar.header("Scenario Controls")
    discount_offer = st.sidebar.slider("Intervention Fee Discount (%)", 0, 50, 15)
    support_sla_boost = st.sidebar.selectbox("Support SLA Upgrade", ["None", "Priority Routing", "Dedicated CSM"])

    # Scoring & Predictions
    preds_proba = model.predict_proba(df[['gpv_monthly', 'quota_attainment', 'tenure_months', 'support_tickets_30d', 'failed_payouts_30d', 'merchant_tier']])[:, 1]
    df['churn_risk'] = preds_proba
    df['risk_category'] = pd.cut(df['churn_risk'], bins=[0, 0.3, 0.6, 1.0], labels=['Low', 'Medium', 'High'])

    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Active GPV", f"${df['gpv_monthly'].sum():,.0f}")
    col2.metric("High-Risk Merchants", f"{len(df[df['risk_category']=='High'])}")
    col3.metric("GPV at Risk", f"${df[df['risk_category']=='High']['gpv_monthly'].sum():,.0f}")
    col4.metric("Avg Quota Attainment", f"{df['quota_attainment'].mean()*100:.1f}%")

    st.divider()

    # Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("GPV Distribution by Churn Risk Category")
        fig1 = px.histogram(df, x="gpv_monthly", color="risk_category", barmode="overlay", title="Monthly GPV vs Risk Category")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Risk vs Quota Attainment")
        fig2 = px.scatter(df, x="quota_attainment", y="churn_risk", color="merchant_tier", size="gpv_monthly", title="Quota Attainment vs Risk Score")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Merchant High Risk Queue & Action Plan")
    high_risk_df = df[df['risk_category'] == 'High'].sort_values(by='gpv_monthly', ascending=False)
    st.dataframe(high_risk_df[['merchant_id', 'merchant_tier', 'gpv_monthly', 'quota_attainment', 'churn_risk']], use_container_width=True)

except Exception as e:
    st.info("Please run `python models/train_model.py` to generate sample data and the ML model first.")
    st.error(str(e))