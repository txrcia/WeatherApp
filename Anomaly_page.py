# anomaly_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

def anomaly_detection():
    st.set_page_config(page_title="Passenger Anomaly Detection", layout="wide")

    st.title("🛑 Airline Passenger Anomaly Detection Dashboard")
    st.markdown("Detect unusual passenger feedback based on delays, ratings, and loyalty status.")

    uploaded_file = st.file_uploader("📂 Upload passenger satisfaction CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df_original = df.copy()

            st.success("✅ File uploaded and scanned successfully!")

            st.subheader("📊 Raw Data Sample")
            st.dataframe(df.head(10), use_container_width=True)

            # Encode categorical columns
            cat_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction']
            encoders = {}
            for col in cat_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                encoders[col] = le

            # Features for detection
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

            # Sidebar settings
            st.sidebar.header("🔎 Anomaly Detection Settings")
            method = st.sidebar.radio("Select Detection Method", ["Isolation Forest", "Local Outlier Factor"])
            contamination = st.sidebar.slider("Expected Outlier Fraction", 0.01, 0.2, 0.05)

            # Anomaly detection
            if method == "Isolation Forest":
                clf = IsolationForest(contamination=contamination, random_state=42)
                df['anomaly'] = clf.fit_predict(X)
            else:
                clf = LocalOutlierFactor(n_neighbors=20, contamination=contamination)
                df['anomaly'] = clf.fit_predict(X)

            df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

            st.subheader("🚩 Anomaly Summary")
            st.write(df['anomaly'].value_counts())

            # Display anomalies
            anomalies = df[df['anomaly'] == 'Anomaly']
            st.subheader("🔍 Top 10 Anomalous Passengers")
            st.dataframe(anomalies[[
                'Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
                'Flight Distance', 'Departure Delay in Minutes',
                'Arrival Delay in Minutes', 'satisfaction'
            ]].head(10), use_container_width=True)

            # Download anomalies
            st.download_button("📥 Download Anomalies CSV", anomalies.to_csv(index=False), file_name="anomalies.csv")

            # Charts
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
            st.error(f"❌ Error processing file: {e}")

    else:
        st.info("👆 Please upload a CSV file to begin.")

# Entry point
if __name__ == "__main__":
    anomaly_detection()
