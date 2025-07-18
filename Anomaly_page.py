import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

def anomaly_detection():
    
    st.title("🛑 Airline Passenger Anomaly Detection Dashboard")
    st.markdown("""
    Detect unusual passenger behavior or feedback patterns based on service ratings, delays, and loyalty status.
    Upload a CSV and select an anomaly detection method to get started.
    """)

    # Sidebar explanations and options
    st.sidebar.markdown("""
        <hr style='border: 1px solid #CCC; margin-top: 30px; margin-bottom: 1px;'>
        <h2 style='font-size: 23px; color: grey; margin-top: 5px; margin-bottom: 0px;'>🎛️ Filter Options</h2>
        <hr style='border: 1px solid #CCC; margin-top: 5px; margin-bottom: 15px;'>
        <p style='font-size: 14px; color: grey;'>
        <strong>🔍 Method:</strong><br>
        • <b>Isolation Forest</b>: Efficient for large datasets; isolates anomalies based on random splits.<br>
        • <b>Local Outlier Factor</b>: Compares density of points; good for local, smaller anomalies.<br><br>
        <strong>🎚️ Outlier Percentage:</strong><br>
        Use the slider below to set how many points you expect to be anomalies (1%–20%).
        Higher values mark more data as outliers.
        </p>
    """, unsafe_allow_html=True)

    method = st.sidebar.radio("Select Method", ["Isolation Forest", "Local Outlier Factor"])
    contamination = st.sidebar.slider("Expected Outlier Percentage", 0.01, 0.2, 0.05)

    # File upload
    uploaded_file = st.file_uploader("📁 Upload passenger satisfaction CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df_original = df.copy()

        st.subheader("📊 Raw Data Preview")
        st.dataframe(df.head(10))

        # Encode categorical columns
        cat_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction']
        encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le

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

        # Apply selected method
        if method == "Isolation Forest":
            clf = IsolationForest(contamination=contamination, random_state=42)
            df['anomaly'] = clf.fit_predict(X)
        else:
            clf = LocalOutlierFactor(n_neighbors=20, contamination=contamination)
            df['anomaly'] = clf.fit_predict(X)

        df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})

        st.subheader("🚩 Anomaly Summary")
        st.write(df['anomaly'].value_counts())

        # Show only anomalies
        anomalies = df[df['anomaly'] == 'Anomaly']
        st.subheader("🔍 Top Anomalies")
        st.dataframe(anomalies[[
            'Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
            'Flight Distance', 'Departure Delay in Minutes',
            'Arrival Delay in Minutes', 'satisfaction'
        ]].head(10))

        # Visualization 1: Scatter
        st.subheader("📈 Flight Distance vs Delay (Colored by Anomaly)")
        fig = px.scatter(df, x="Flight Distance", y="Departure Delay in Minutes",
                         color="anomaly", hover_data=['Age', 'satisfaction', 'Customer Type'])
        st.plotly_chart(fig, use_container_width=True)

        # Visualization 2: Boxplot
        st.subheader("📦 Delay Distribution by Anomaly Status")
        fig2 = px.box(df, x='anomaly', y='Arrival Delay in Minutes', points='all', color='anomaly')
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("📤 Please upload a CSV file to begin anomaly detection.")

if __name__ == "__main__":
    anomaly_detection()
