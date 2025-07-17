# predictive_dashboard.py

import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.express as px

# ------------------------------
# Load or generate time-series data
# ------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")  # Replace with your actual training dataset

    # If you don't have date info, simulate it
    if 'date' not in df.columns:
        df['date'] = pd.date_range(start='2022-01-01', periods=len(df), freq='D')
    
    return df[['date', 'satisfaction']]

# ------------------------------
# Prophet Forecasting
# ------------------------------

def build_forecast(df):
    df_prophet = df.rename(columns={'date': 'ds', 'satisfaction': 'y'})
    
    # Group by date in case of duplicates
    df_prophet = df_prophet.groupby('ds').mean().reset_index()

    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=30)  # Forecast 30 days ahead
    forecast = model.predict(future)
    
    return model, forecast

# ------------------------------
# Streamlit UI
# ------------------------------

def forecast_dashboard():
    st.title("📈 Predictive Analytics Dashboard")
    st.markdown("### Forecasting Satisfaction Trends with AI (Prophet)")

    df = load_data()
    
    st.markdown("#### Raw Satisfaction Over Time")
    st.line_chart(df.set_index('date'))

    st.markdown("---")
    st.markdown("#### ⏳ Forecasting with Facebook Prophet")

    model, forecast = build_forecast(df)

    st.plotly_chart(plot_plotly(model, forecast), use_container_width=True)
    
    st.markdown("#### 📊 Trend and Seasonality Components")
    st.plotly_chart(plot_components_plotly(model, forecast), use_container_width=True)

    st.markdown("##### Interpretation Tips:")
    st.markdown("- **Trend** shows the long-term satisfaction trajectory.")
    st.markdown("- **Weekly/Yearly seasonality** shows regular fluctuations.")
    st.markdown("- **Forecast plot** highlights expected future satisfaction scores.")

# ------------------------------
# Run app
# ------------------------------

if __name__ == "__main__":
    forecast_dashboard()
 