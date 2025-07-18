import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet

# --------------------------------------------------------
# Functions
# --------------------------------------------------------

def prepare_time_series(df):
    if 'Flight Date' not in df.columns or 'satisfaction' not in df.columns:
        st.error("❌ Required columns not found. Make sure the CSV has 'Flight Date' and 'satisfaction'.")
        st.stop()

    df['Flight Date'] = pd.to_datetime(df['Flight Date'])
    df['satisfaction_numeric'] = df['satisfaction'].map({
        'satisfied': 1,
        'neutral or dissatisfied': 0
    })

    ts_df = df.groupby('Flight Date')['satisfaction_numeric'].mean().reset_index()
    ts_df.columns = ['ds', 'y']  # Prophet expects 'ds' and 'y'
    return ts_df

def generate_forecast(ts_df, periods=6):
    model = Prophet()
    model.fit(ts_df)
    future = model.make_future_dataframe(periods=periods * 30)  # approx 30 days per month
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], model

def forecast_dashboard():
    st.set_page_config(page_title="Passenger Satisfaction Forecast", layout="wide")
    st.title("📈 Forecasting Passenger Satisfaction Trends")

    uploaded_file = st.file_uploader("Upload Cleaned Passenger Data (with 'Flight Date' and 'satisfaction')", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Satisfaction Over Time")
        ts_df = prepare_time_series(df)
        st.dataframe(ts_df.rename(columns={'ds': 'Date', 'y': 'Avg Satisfaction'}), use_container_width=True)

        fig1 = px.line(ts_df, x='ds', y='y', title="Average Satisfaction Over Time", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("🔮 Forecast Settings")
        periods = st.slider("Months to Forecast Ahead", min_value=1, max_value=12, value=6)
        forecast, model = generate_forecast(ts_df, periods=periods)

        st.subheader("📈 Forecasted Satisfaction")
        fig2 = px.line(forecast, x='ds', y='yhat', title="Forecasted Satisfaction", labels={'yhat': 'Forecasted Satisfaction'})
        fig2.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot'))
        fig2.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot'))
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📋 Summary")
        last_known = ts_df.iloc[-1]['y']
        last_forecast = forecast.iloc[-periods:]['yhat'].mean()

        if last_forecast > last_known:
            trend = "increasing 📈"
        elif last_forecast < last_known:
            trend = "decreasing 📉"
        else:
            trend = "stable ➖"

        st.success(f"The model forecasts that passenger satisfaction is **{trend}** over the next {periods} months.")
    else:
        st.info("👆 Please upload a CSV file to begin forecasting.")

# --------------------------------------------------------
# Launch
# --------------------------------------------------------

if __name__ == "__main__":
    forecast_dashboard()
