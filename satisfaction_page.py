import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# -----------------------------------------------------
# Load trained model and encoders
# -----------------------------------------------------

@st.cache_resource
def load_model_and_encoders():
    with open("rf_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
    return model, label_encoders

model, label_encoders = load_model_and_encoders()

# -----------------------------------------------------
# Load data to get columns
# -----------------------------------------------------

@st.cache_data
def load_data():
    df_train = pd.read_csv("train.csv")

    # Drop unused columns
    drop_cols = ['Unnamed: 0', 'id', 'Gender']
    df_train.drop(columns=[col for col in drop_cols if col in df_train.columns], inplace=True)


    # Fill missing values
    df_train['Arrival Delay in Minutes'].fillna(0, inplace=True)

    # Encode categorical columns
    categorical_cols = df_train.select_dtypes(include=['object']).columns.tolist()
    categorical_cols.remove('satisfaction')  # keep target separate

    for col in categorical_cols:
        le = label_encoders[col]
        df_train[col] = le.transform(df_train[col])

    # Encode target
    df_train['satisfaction'] = df_train['satisfaction'].map({'neutral or dissatisfied': 0, 'satisfied': 1})

    X = df_train.drop('satisfaction', axis=1)
    y = df_train['satisfaction']

    return df_train, X, y, categorical_cols

df_train, X, y, categorical_cols = load_data()

# -----------------------------------------------------
# Streamlit UI
# -----------------------------------------------------

def satisfaction_prediction_page():

    st.markdown("""
    <style>
        .big-heading {
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            color: white;
        }
        .description-box {
            background-color: #444444;
            padding: 12px;
            border-radius: 8px;
            color: white;
            font-size: 15px;
            margin-bottom: 15px;
        }
        .result-box {
            background-color: #222222;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 18px;
            color: white;
        }
        .st-expanderContent {
            background-color: #222222 !important;
        }
    </style>
""", unsafe_allow_html=True)

    # ------------------------------
    # Page Title
    # ------------------------------
    st.markdown("""
    <h1 style='
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        color: white;
    '>
        😊 Passenger Satisfaction Prediction
    </h1>
    """, unsafe_allow_html=True)

      # NEW: Collapsible Info Box
    with st.expander("ℹ️ How this works", expanded=False):
        st.markdown("""
        - This app predicts whether a passenger is likely to be **Satisfied** or **Neutral/Dissatisfied** based on their travel details.
        - You can **manually enter inputs** for one passenger or **upload a CSV** file with multiple records.
        - The model used is a Random Forest Classifier trained on airline passenger satisfaction data.
        - After prediction, you’ll see the **result summary** and **feature importance** plot to understand key influences.
        """)

    st.markdown("<hr style='border: 0.5px solid #DDD;'>", unsafe_allow_html=True)

    # ------------------------------
    # Sidebar
    # ------------------------------

    st.sidebar.markdown("""
        <hr style='border: 1px solid #CCC; margin-top: 50px; margin-bottom: 1px;'>
        <h2 style='font-size: 23px; margin-top: 5px; margin-bottom: 0px;'>🎛️ Filter Options</h2>
        <hr style='border: 1px solid #CCC; margin-top: 5px; margin-bottom: 15px;'>
    """, unsafe_allow_html=True)

    st.sidebar.header("🧾 Data Input Methods")
    mode = st.sidebar.radio("Choose data source:", ["Use Manual Inputs", "Upload CSV File"])
    st.sidebar.caption("Select how you want to provide data for analysis.")

    st.sidebar.markdown("---")


    # ------------------------------
    # Description Box
    # ------------------------------

    st.markdown("""
        <div class="description-box">
            Enter passenger details manually or upload a CSV file to predict whether
            passengers are likely to be <strong>Satisfied</strong> or
            <strong>Neutral/Dissatisfied</strong>.
        </div>
    """, unsafe_allow_html=True)

    # ------------------------------
    # Manual Input
    # ------------------------------

    if mode == "Use Manual Inputs":
        with st.form("manual_input_form"):
            user_data = {}

            service_cols = [
                'Inflight wifi service',
                'Departure/Arrival time convenient',
                'Ease of Online booking',
                'Gate location',
                'Food and drink',
                'Online boarding',
                'Seat comfort',
                'Inflight entertainment',
                'On-board service',
                'Leg room service',
                'Baggage handling',
                'Checkin service',
                'Inflight service',
                'Cleanliness'
            ]

            for feature in X.columns:
                if feature in categorical_cols:
                    le = label_encoders[feature]
                    options = list(le.classes_)
                    selected = st.selectbox(f"**{feature}**", options=options)
                    encoded_value = le.transform([selected])[0]
                    user_data[feature] = encoded_value
                elif feature in service_cols:
                    val = st.select_slider(
                        f"**{feature}** (1 = Poor, 5 = Excellent)",
                        options=[1, 2, 3, 4, 5],
                        value=3
                    )
                    user_data[feature] = val
                else:
                    if feature == "Age":
                        val = st.slider(
                            "**Age**", 
                            min_value=0,
                            max_value=90,
                            value=35,
                            step=1
                        )
                        user_data[feature] = val

                    elif feature == "Flight Distance":
                        val = st.slider(
                            "**Flight Distance (km)**",
                            min_value=100,
                            max_value=5000,
                            value=1000,
                            step=10
                        )
                        user_data[feature] = val

                    elif feature == "Departure Delay":
                        val = st.slider(
                            "**Departure Delay (minutes)**", 
                            min_value=0, 
                            max_value=300, 
                            value=0,
                            step=1
                        )
                        user_data[feature] = val

                    elif feature == "Arrival Delay":
                        val = st.slider(
                            "**Arrival Delay (minutes)**", 
                            min_value=0, 
                            max_value=300, 
                            value=0,
                            step=1
                        )
                        user_data[feature] = val

                    else:
                        val = st.slider(feature, 0, 3000)
                        user_data[feature] = val



            submitted = st.form_submit_button("🚀 Predict")

        if submitted:
            input_df = pd.DataFrame([user_data])
            pred = model.predict(input_df)[0]
            pred_text = "✅ The passenger is likely to be Satisfied." if pred == 1 else "⚠️ The passenger is likely Neutral or Dissatisfied."

            st.markdown(f"""
                <div class='result-box'>
                    {pred_text}
                </div>
            """, unsafe_allow_html=True)

            # Feature importance
            feature_importances = model.feature_importances_
            feat_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': feature_importances
            }).sort_values(by='Importance', ascending=False)

            st.markdown("<h3 style='color:white;'>🔎 Feature Importance</h3>", unsafe_allow_html=True)
            fig2 = px.bar(
                feat_df.head(10),
                x="Importance",
                y="Feature",
                orientation='h',
                title="Top 10 Important Features",
                color="Importance",
                color_continuous_scale="Plasma"
            )
            fig2.update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ------------------------------
    # Upload CSV
    # ------------------------------

    elif mode == "Upload CSV File":
        uploaded_file = st.file_uploader("Upload CSV", type="csv")

        if uploaded_file:
            df_uploaded = pd.read_csv(uploaded_file)

            drop_cols = ['Unnamed: 0', 'id', 'satisfaction','Gender']
            df_uploaded = df_uploaded.drop(columns=[col for col in drop_cols if col in df_uploaded.columns], errors='ignore')

            required_cols = list(X.columns)
            missing_cols = [c for c in required_cols if c not in df_uploaded.columns]

            if missing_cols:
                st.error(f"❌ Missing required columns:\n{missing_cols}")
            else:
                for col in categorical_cols:
                    le = label_encoders[col]
                    df_uploaded[col] = le.transform(df_uploaded[col])

                df_uploaded = df_uploaded[X.columns]

                preds = model.predict(df_uploaded)
                df_uploaded["Predicted Satisfaction"] = preds
                df_uploaded["Predicted Satisfaction Label"] = df_uploaded["Predicted Satisfaction"].map({
                    0: "Neutral or Dissatisfied",
                    1: "Satisfied"
                })

                csv_out = df_uploaded.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Download Predictions CSV",
                    csv_out,
                    file_name="satisfaction_predictions.csv"
                )

                summary_counts = df_uploaded["Predicted Satisfaction Label"].value_counts()
                num_satisfied = summary_counts.get("Satisfied", 0)
                num_dissatisfied = summary_counts.get("Neutral or Dissatisfied", 0)

                with st.expander("📊 View Prediction Summary", expanded=False):
                    st.markdown(f"""
                        <div class="result-box">
                            <p><strong>✅ Satisfied:</strong> {num_satisfied}</p>
                            <p><strong>⚠️ Neutral or Dissatisfied:</strong> {num_dissatisfied}</p>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br><br>", unsafe_allow_html=True)

                st.dataframe(df_uploaded.head())

                feature_importances = model.feature_importances_
                feat_df = pd.DataFrame({
                    'Feature': X.columns,
                    'Importance': feature_importances
                }).sort_values(by='Importance', ascending=False)

                st.markdown("<h3 style='color:white;'>🔎 Feature Importance</h3>", unsafe_allow_html=True)
                fig = px.bar(
                    feat_df.head(10),
                    x="Importance",
                    y="Feature",
                    orientation='h',
                    title="Top 10 Important Features",
                    color="Importance",
                    color_continuous_scale="Plasma"
                )
                fig.update_layout(
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    font=dict(color='white'),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    satisfaction_prediction_page()

