import streamlit as st
import pandas as pd
from prophet import Prophet
import numpy as np

# ----------------------------
# Load and preprocess dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("satisfaction_data.csv")  # Your dataset must include 'date' and 'satisfaction'
    df['date'] = pd.to_datetime(df['date'])
    df['satisfaction_binary'] = df['satisfaction'].apply(lambda x: 1 if x == "satisfied" else 0)
    df = df.groupby('date')["satisfaction_binary"].mean().reset_index()
    df.columns = ['ds', 'y']
    return df

# ----------------------------
# Anomaly Detection Function
# ----------------------------
def detect_anomalies(df, window=7, threshold=2.5):
    df['rolling_mean'] = df['y'].rolling(window, center=True).mean()
    df['rolling_std'] = df['y'].rolling(window, center=True).std()
    df['anomaly'] = np.abs(df['y'] - df['rolling_mean']) > threshold * df['rolling_std']
    return df

# ----------------------------
# Forecast Function
# ----------------------------
def run_forecast(df, periods=30):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast, model

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="✈️ AI Satisfaction Dashboard", layout="wide")
st.title("✈️ Airline Passenger Satisfaction AI Dashboard")
st.markdown("This dashboard detects anomalies and forecasts future satisfaction rates using AI.")

option = st.sidebar.selectbox("Select Dashboard", ["Forecast Satisfaction", "Anomaly Detection"])

# Load data
data = load_data()

if option == "Forecast Satisfaction":
    st.subheader("📈 Forecasting Satisfaction Trends")
    future_days = st.slider("Select how many days to forecast", 7, 60, 30)
    forecast, model = run_forecast(data, periods=future_days)
    fig1 = model.plot(forecast)
    st.write("### Forecast Plot")
    st.pyplot(fig1)
    st.write("### Forecast Components")
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)

elif option == "Anomaly Detection":
    st.subheader("🚨 Anomaly Detection in Daily Satisfaction")
    window_size = st.slider("Rolling Window Size", 3, 30, 7)
    threshold = st.slider("Anomaly Threshold (std dev)", 1.0, 4.0, 2.5)
    anomalies_df = detect_anomalies(data.copy(), window=window_size, threshold=threshold)
    st.line_chart(anomalies_df.set_index('ds')[['y', 'rolling_mean']])
    st.write("### Detected Anomalies")
    st.dataframe(anomalies_df[anomalies_df['anomaly'] == True])

# ------------------------------
# Run app
# ------------------------------

if __name__ == "__main__":
    forecast_dashboard()
 