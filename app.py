import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Robust Regression Engine", page_icon="🏠", layout="wide")

MODEL_PATH = Path("models/best_model.joblib")
FEATURE_PATH = Path("models/feature_columns.json")

st.title("🏠 Robust Regression Engine")
st.caption("Real Estate House Price Prediction | Regularization • Cross-Validation • Tree Models • SVR")

if not MODEL_PATH.exists() or not FEATURE_PATH.exists():
    st.error("Trained model files are missing. Run the Jupyter notebook first to create models/best_model.joblib and models/feature_columns.json.")
    st.stop()

model = joblib.load(MODEL_PATH)
with open(FEATURE_PATH, "r") as f:
    feature_columns = json.load(f)

st.sidebar.header("Property Details")
area_sqft = st.sidebar.number_input("Area (sqft)", min_value=100, max_value=10000, value=1800, step=50)
bedrooms = st.sidebar.number_input("Bedrooms", min_value=1, max_value=10, value=3, step=1)
bathrooms = st.sidebar.number_input("Bathrooms", min_value=1, max_value=10, value=2, step=1)
location_score = st.sidebar.number_input("Location Score", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
property_age = st.sidebar.number_input("Property Age (years)", min_value=0, max_value=100, value=15, step=1)
distance_city_km = st.sidebar.number_input("Distance from City (km)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
near_school = st.sidebar.selectbox("Near School", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
near_metro = st.sidebar.selectbox("Near Metro", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
crime_rate_index = st.sidebar.number_input("Crime Rate Index", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
sale_year = st.sidebar.number_input("Sale Year", min_value=2010, max_value=2035, value=2023, step=1)
sale_month = st.sidebar.selectbox("Sale Month", list(range(1, 13)), index=0)

input_data = pd.DataFrame([{
    "area_sqft": area_sqft,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "location_score": location_score,
    "property_age": property_age,
    "distance_city_km": distance_city_km,
    "near_school": near_school,
    "near_metro": near_metro,
    "crime_rate_index": crime_rate_index,
    "sale_year": sale_year,
    "sale_month": sale_month,
}])[feature_columns]

st.subheader("Prediction")
if st.button("💰 Predict House Price", type="primary", use_container_width=True):
    prediction = float(model.predict(input_data)[0])
    c1, c2 = st.columns(2)
    c1.metric("Estimated House Price", f"₹{prediction:,.0f}")
    c2.metric("Estimated Price (Crore)", f"₹{prediction/1e7:.2f} Cr")

st.divider()
st.subheader("📋 Input Summary")
st.dataframe(input_data.T.rename(columns={0: "Value"}), use_container_width=True)

st.info("This application uses the trained model saved by the project notebook. It is intended for educational/project demonstration and should be revalidated with current market data before production use.")
