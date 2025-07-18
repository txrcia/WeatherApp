# anomaly_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import io

def preprocess_data(df):
    try:
        cat_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction']
        encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
        return df, encoders
    except Exception as e:
        st.error(f"Error in preprocessing: {e}")
        return None, None

def anomaly_detection():
    
    st.title("🛑 Airline Passenger Anomaly Detection Dashboard")

    st.markdown("""
    Detect unusual passenger behavior or feedback patterns using Isolation Forest or Local Outlier Factor.
    Upload your CSV to begin.
    """)

    # Sample CSV download
    sample_df = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Customer Type': ['Loyal Customer', 'disloyal Customer'],
        'Age': [34, 45],
        'Type of Travel': ['Business travel', 'Personal Travel'],
        'Class': ['Eco', 'Business'],
        'Flight Distance': [1234, 567],
        'Inflight wifi service': [3, 2],
        'Departure/Arrival time convenient': [3, 1],
        'Ease of Online booking': [4, 2],
        'Gate location': [2, 4],
        'Food and drink': [3, 2],
        'Online boarding': [4, 3],
        'Seat comfort': [3, 2],
        'Inflight entertainment': [4, 2],
        'On-board service': [4, 3],
        'Leg room service': [3, 2],
        'Baggage handling': [4, 3],
        'Checkin service': [4, 2],
        'Inflight service': [4, 3],
        'Cleanliness': [5, 3],
        'Departure Delay in Minutes': [5, 0],
        'Arrival Delay in Minutes': [0, 3],
        'satisfaction': ['satisfied', 'neutral or dissatisfied']
    })

    st.download_button("📥 Download Sample CSV", sample_df.to_csv(index=False), "sample_passenger_data.csv")

    # File uploader
    uploaded_file = st.file_uploader("📂 Upload passenger satisfaction CSV", type=["csv"])

    if uploaded_file:
        try:
            with st.spinner("Processing data..."):
                df = pd.read_csv(uploaded_file)
                df_original = df.copy()
                st.subheader("📊 Raw Data Sample")
                st.dataframe(df.head(10))

                df, encoders = preprocess_data(df)
                if df is None:
                    return

                features = [
                    'Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance',
                    'Inflight wifi service', 'Departure/Arrival time convenient',
                    'Ease of Online booking', 'Gate location', 'Food and drink',
                    'Online boarding', 'Seat comfort', 'Inflight entertainment',
                    'On-board service', 'Leg room service', 'Baggage handling',
                    'Checkin service', 'Inflight service', 'Cleanliness',
                    'Departure Delay in Minutes', 'Arrival Delay in Minutes',
                    'satisfaction'
                ]
                X = df[features]

                st.sidebar.header("🔎 Anomaly Detection Settings")
                method = st.sidebar.radio("Select Method", ["Isolation Forest", "Local Outlier Factor"])
                contamination = st.sidebar.slider("Expected Outlier Percentage", 0.01, 0.2, 0.05)

                if method == "Isolation Forest":
                    clf = IsolationForest(contamination=contamination, random_state=42)
                    df['anomaly'] = clf.fit_predict(X)
                else:
                    clf = LocalOutlierFactor(n_neighbors=20, contamination=contamination)
                    df['anomaly'] = clf.fit_predict(X)

                df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

                st.subheader("🚩 Anomaly Summary")
                st.write(df['anomaly'].value_counts())

                anomalies = df[df['anomaly'] == 'Anomaly']
                st.subheader("🔍 Top 10 Anomalous Passengers")
                st.dataframe(anomalies[['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
                                        'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes',
                                        'satisfaction']].head(10))

                st.download_button("📥 Download Anomalies CSV", anomalies.to_csv(index=False), file_name="anomalies.csv")

                st.subheader("📈 Visualizations")
                col1, col2 = st.columns(2)

                with col1:
                    fig1 = px.scatter(
                        df,
                        x="Flight Distance",
                        y="Departure Delay in Minutes",
                        color="anomaly",
                        hover_data=['Age', 'satisfaction', 'Customer Type'],
                        title="Flight Distance vs. Departure Delay"
                    )
                    st.plotly_chart(fig1, use_container_width=True)

                with col2:
                    fig2 = px.box(
                        df,
                        x="anomaly",
                        y="Arrival Delay in Minutes",
                        color="anomaly",
                        points="all",
                        title="Arrival Delay by Anomaly Status"
                    )
                    st.plotly_chart(fig2, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    else:
        st.info("👆 Upload a valid CSV file with passenger satisfaction data to begin.")

if __name__ == "__main__":
    anomaly_detection()
