# 💳 B2B FinTech RevOps & Merchant Churn Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![dbt](https://img.shields.io/badge/dbt-Core%201.7-orange.svg)](https://www.getdbt.com/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-green.svg)](https://xgboost.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end B2B payments analytics platform designed to predict merchant churn, quantify Gross Payment Volume (GPV) at risk, and provide dynamic commercial scenario controls for Revenue Operations (RevOps) and Customer Success leadership.

---

## 🚀 Key Business Outcomes

* **Predictive Churn Scoring**: Trains an XGBoost classifier achieving **ROC-AUC > 0.78** to catch high-risk merchant accounts prior to contract expiration.
* **GPV at Risk Visibility**: Automatically isolates and quantifies monthly Gross Payment Volume at risk across SMB, Mid-Market, and Enterprise merchant tiers.
* **Commercial Scenario Control**: Interactively models revenue retention outcomes based on proposed fee discounts and support SLA upgrades.
* **Structured Analytics Layer**: Implements standard software engineering pattern data modeling (Staging $\rightarrow$ Intermediate $\rightarrow$ Marts) via dbt.

---

## 📊 Dashboard Preview

<img width="937" height="541" alt="Screenshot 2026-09-14 164205" src="https://github.com/user-attachments/assets/44d16c65-e162-4cb8-b771-18e10d3ccfad" />


---

## 🏗️ System Architecture

```text
                                  ┌─────────────────────────────────────────┐
                                  │      Raw B2B Merchant Dataset           │
                                  └────────────────────┬────────────────────┘
                                                       │
                                                       ▼
                                  ┌─────────────────────────────────────────┐
                                  │           dbt Modeling Layer            │
                                  │  • stg_merchants                        │
                                  │  • int_merchant_metrics                 │
                                  │  • mart_revops_churn_intelligence       │
                                  └────────────────────┬────────────────────┘
                                                       │
                                                       ▼
                                  ┌─────────────────────────────────────────┐
                                  │         XGBoost ML Pipeline             │
                                  │  • ColumnTransformer (Scaling & OHE)    │
                                  │  • Risk Scoring Engine (ROC-AUC > 0.78)  │
                                  └────────────────────┬────────────────────┘
                                                       │
                                                       ▼
                                  ┌─────────────────────────────────────────┐
                                  │      Streamlit Operational Dashboard    │
                                  │  • Risk Distribution & Metrics          │
                                  │  • Real-time Scenario Controls          │
                                  └─────────────────────────────────────────┘
