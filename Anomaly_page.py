# anomaly_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

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
    st.markdown("""
    <h1 style='
        font-size: 37px;
        font-weight: bold;
        text-align: center;
        color: white;
    '>
        🛑 Airline Passenger Anomaly Detection
    </h1>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ How this works", expanded=False):
        st.markdown("""
        - This tool detects **unusual passenger records** using anomaly detection.
        - You can choose between **Isolation Forest** or **Local Outlier Factor** methods.
        - Upload your CSV with passenger data to begin the analysis.
        - Adjust the **Contamination slider** to control how strict the anomaly detection is.
        """)


    st.markdown("Detect anomalies in passenger feedback using Isolation Forest or Local Outlier Factor.")

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

                st.sidebar.markdown("""
                    <hr style='border: 1px solid #CCC; margin-top: 50px; margin-bottom: 1px;'>
                    <h2 style='font-size: 23px; margin-top: 5px; margin-bottom: 0px;'>🎛️ Filter Options</h2>
                    <hr style='border: 1px solid #CCC; margin-top: 5px; margin-bottom: 15px;'>
                """, unsafe_allow_html=True)

                # Method selection
                st.sidebar.markdown(
                    "<span style='color: grey;'>🔍 Choose method for anomaly detection:</span>",
                    unsafe_allow_html=True
                )
                method = st.sidebar.radio("Method", ["Isolation Forest", "Local Outlier Factor"])

                # Method usage description
                if method == "Isolation Forest":
                    st.sidebar.markdown(
                        "<span style='color: grey;'>✅ Good for high-dimensional data. Detects points that are 'isolated' from the rest.</span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.sidebar.markdown(
                        "<span style='color: grey;'>✅ Good for dense clusters. Flags points with few close neighbors as outliers.</span>",
                        unsafe_allow_html=True
                    )

                # Contamination slider
                st.sidebar.markdown(
                    "<span style='color: grey;'>📉 Select the percentage of expected anomalies. More = stricter detection.</span>",
                    unsafe_allow_html=True
                )
                contamination = st.sidebar.slider("Contamination", 0.01, 0.2, 0.05)

                # Execute detection
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
