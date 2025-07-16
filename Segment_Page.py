import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# Load pre-trained model and encoders
# -----------------------------------------------------
@st.cache_resource
def load_data():
    with open("kmeans_model.pkl", "rb") as f:
        kmeans = pickle.load(f)
    with open("supporting_data.pkl", "rb") as f:
        data = pickle.load(f)
    le_dict = data['encoders']
    median_distance = data['median_distance']
    return kmeans, le_dict, median_distance

kmeans, le_dict, median_distance = load_data()

service_cols = [
    'Inflight wifi service', 'Departure/Arrival time convenient', 'Ease of Online booking',
    'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
    'Inflight entertainment', 'On-board service', 'Leg room service',
    'Baggage handling', 'Checkin service', 'Inflight service', 'Cleanliness'
]

# -----------------------------------------------------
# Helper to categorize age
# -----------------------------------------------------
def categorize_age(age):
    if age <= 30:
        return 'Young'
    elif age <= 55:
        return 'Middle-aged'
    else:
        return 'Old'

# -----------------------------------------------------
# Prediction function
# -----------------------------------------------------
def predict_cluster(age, customer_type, travel_type, travel_class, flight_distance,
                    kmeans, le_dict, median_distance):
    age_group = categorize_age(age)
    flight_cat = 'Short' if flight_distance <= median_distance else 'Long'

    ct = le_dict['Customer Type'].transform([customer_type])[0]
    tt = le_dict['Type of Travel'].transform([travel_type])[0]
    cl = le_dict['Class'].transform([travel_class])[0]
    ag = le_dict['AgeGroup'].transform([age_group])[0]
    fc = le_dict['FlightCategory'].transform([flight_cat])[0]

    input_array = np.array([[ct, tt, cl, ag, fc]])
    cluster = kmeans.predict(input_array)[0]

    return cluster, age_group, flight_cat

# -----------------------------------------------------
# Recommendation function for one cluster
# -----------------------------------------------------
def get_cluster_recommendation(df, cluster_num):
    cluster_df = df[df['Assigned Cluster'] == cluster_num]
    if cluster_df.empty:
        return f"⚠️ No passengers found in Cluster {cluster_num}."

    means = cluster_df[service_cols].mean()
    lowest_5 = means.sort_values().head(5)
    rec = f"🎯 Cluster **{cluster_num}** — Based on passengers in this cluster:\n"
    rec += "**Airline should improve these 5 services:**\n"
    for i, (feature, score) in enumerate(lowest_5.items(), start=1):
        rec += f"  {i}. {feature} — avg. score: {score:.2f}\n"
    return rec

# -----------------------------------------------------
# Interactive Plotly Visualization helper
# -----------------------------------------------------
def plot_services_interactive(df, cluster_num, top=True, height=300, font_size=16):
    try:
        cluster_df = df[df['Assigned Cluster'] == cluster_num]
        if cluster_df.empty:
            st.info(f"No passengers in Cluster {cluster_num} for visualization.")
            return

        mean_scores = cluster_df[service_cols].mean()
        selected = mean_scores.sort_values(ascending=not top).head(5)

        if selected.empty:
            st.warning(f"No service data available for Cluster {cluster_num}. Cannot plot.")
            return

        n_bars = len(selected)
        colors = px.colors.sequential.Plasma[-n_bars:][::-1] if n_bars > 1 else ["#636efa"] * n_bars

        fig = go.Figure(go.Bar(
            x=selected.values[::-1],
            y=selected.index[::-1],
            orientation='h',
            marker=dict(color=colors),
            hovertemplate='%{y}: %{x:.2f}<extra></extra>'
        ))

        fig.update_layout(
            xaxis=dict(range=[0, 5]),
            height=height,
            margin=dict(l=90, r=20, t=40, b=30),
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white', size=font_size)
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Plotly crashed: {e}")
        import traceback
        st.text(traceback.format_exc())

# -----------------------------------------------------
# Streamlit UI
# -----------------------------------------------------
def segment_page():
    # CSS
    st.markdown("""
        <style>
            html, body, div, p, span, li, label, select, input, button {
                font-size: 15px !important;
                color: white !important;
            }
            .streamlit-expanderHeader {
                font-size: 28px !important;
                font-weight: bold;
                color: white !important;
            }
            .st-expanderContent {
                background-color: black !important;
            }
            .box-content {
                font-size: 16px !important;
                color: white !important;
                line-height: 1.5;
            }
            h1, h2, h3, h4 {
                color: white !important;
            }
            .big-heading {
                font-size: 50px;
                font-weight: bold;
                color: white;
                text-align: center;
            }
            section[data-testid="stSidebar"] *:not(h1):not(h2):not(h3):not(.stHeading) {
                font-size: 15px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='
        font-size: 37px;
        font-weight: bold;
        text-align: center;
        color: white;
    '>
        👥 Passenger Segmentation
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 0.5px solid #DDD;'>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("""
        <hr style='border: 1px solid #CCC; margin-top: 50px; margin-bottom: 1px;'>
        <h2 style='font-size: 23px; margin-top: 5px; margin-bottom: 0px;'>🎛️ Filter Options</h2>
        <hr style='border: 1px solid #CCC; margin-top: 5px; margin-bottom: 15px;'>
    """, unsafe_allow_html=True)

    st.sidebar.header("🧾 Data Input Methods")
    mode = st.sidebar.radio("Choose data source:", ["Use Manual Inputs", "Upload CSV File"], key="data_mode")
    st.sidebar.caption("Select how you want to provide data for analysis.")
    st.sidebar.markdown("---")

    st.sidebar.header("📊 Visualization Options")
    show_viz = st.sidebar.checkbox("Show Visualizations")
    st.sidebar.caption("Enable to explore top or bottom service ratings for clusters.")

    viz_top5 = False
    viz_bottom5 = False
    if show_viz:
        viz_top5 = st.sidebar.checkbox("Top 5 Services", value=True)
        viz_bottom5 = st.sidebar.checkbox("Bottom 5 Services", value=False)

    # Clear state if switching modes
    if "prev_mode" not in st.session_state:
        st.session_state["prev_mode"] = mode
    if st.session_state["prev_mode"] != mode:
        st.session_state["prev_mode"] = mode
        st.session_state.pop("segmentation_df", None)
        st.session_state.pop("segmentation_clusters", None)

    if mode == "Use Manual Inputs":
        st.markdown("""
            <h2 style='font-size:30px;'>Manual Passenger Entry</h2>
            <div style='background-color: #444444; color: rgba(255,255,255,0.7); padding: 10px 15px; border-radius: 8px; margin-top: 8px; font-size: 18px;'>
                Fill in the passenger details manually to predict which cluster they belong to.
            </div>
        """, unsafe_allow_html=True)

        age = st.slider("Passenger Age", 18, 80, 35)
        customer_type = st.selectbox("Customer Type", options=le_dict['Customer Type'].classes_)
        travel_type = st.selectbox("Type of Travel", options=le_dict['Type of Travel'].classes_)
        travel_class = st.selectbox("Travel Class", options=le_dict['Class'].classes_)
        flight_distance = st.slider("Flight Distance (km)", 100, 5000, 500, step=50)

        if st.button("🚀 Predict Cluster"):
            with st.spinner("Predicting cluster..."):
                cluster, age_group, flight_cat = predict_cluster(
                    age, customer_type, travel_type, travel_class, flight_distance,
                    kmeans, le_dict, median_distance
                )

                dummy_data = {
                    "Age": [age],
                    "Customer Type": [customer_type],
                    "Type of Travel": [travel_type],
                    "Class": [travel_class],
                    "Flight Distance": [flight_distance],
                    "AgeGroup": [age_group],
                    "FlightCategory": [flight_cat],
                    "Assigned Cluster": [cluster],
                }
                for col in service_cols:
                    dummy_data[col] = [np.random.uniform(2, 5)]

                manual_df = pd.DataFrame(dummy_data)

                st.session_state["segmentation_df"] = manual_df
                st.session_state["segmentation_clusters"] = [cluster]

    elif mode == "Upload CSV File":
        st.markdown("""
            <h2 style='font-size:36px;'>📂 Upload Passenger Data CSV</h2>
            <div style='background-color: #444444; color: rgba(255,255,255,0.7); padding: 10px 15px; border-radius: 8px; margin-top: 8px; font-size: 18px;'>
                Upload a CSV file with passenger details to predict clusters in bulk.
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Choose CSV file", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

            required_cols = ["Age", "Customer Type", "Type of Travel", "Class", "Flight Distance"]
            if all(col in df.columns for col in required_cols):
                df["AgeGroup"] = df["Age"].apply(categorize_age)
                df["FlightCategory"] = df["Flight Distance"].apply(
                    lambda x: "Short" if x <= median_distance else "Long"
                )

                df_encoded = df.copy()
                df_encoded["Customer Type"] = le_dict["Customer Type"].transform(df["Customer Type"])
                df_encoded["Type of Travel"] = le_dict["Type of Travel"].transform(df["Type of Travel"])
                df_encoded["Class"] = le_dict["Class"].transform(df["Class"])
                df_encoded["AgeGroup"] = le_dict["AgeGroup"].transform(df["AgeGroup"])
                df_encoded["FlightCategory"] = le_dict["FlightCategory"].transform(df["FlightCategory"])

                X = df_encoded[["Customer Type", "Type of Travel", "Class", "AgeGroup", "FlightCategory"]]
                df["Assigned Cluster"] = kmeans.predict(X)

                for col in service_cols:
                    df[col] = np.random.uniform(2, 5, size=len(df))

                st.session_state["segmentation_df"] = df
                st.session_state["segmentation_clusters"] = sorted(df["Assigned Cluster"].unique())
                st.success("✅ Clusters predicted for uploaded CSV!")

                csv_download = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download Segmentation Results CSV", csv_download, file_name="segmentation_results.csv")

            else:
                st.error(f"CSV missing required columns: {required_cols}")

    # --------------------------------------------------
    # Show results if available
    # --------------------------------------------------
    if "segmentation_df" in st.session_state:
        df = st.session_state["segmentation_df"]
        clusters = st.session_state["segmentation_clusters"]

        st.markdown("<hr style='margin: 25px 0;'>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 2])

        if mode == "Use Manual Inputs":
            with col1:
                st.markdown("### 👤 Passenger Details")
                passenger = df.iloc[0]
                details_md = (
                    f"**Age:** {passenger['Age']}  \n"
                    f"**Customer Type:** {passenger['Customer Type']}  \n"
                    f"**Type of Travel:** {passenger['Type of Travel']}  \n"
                    f"**Class:** {passenger['Class']}  \n"
                    f"**Flight Distance:** {passenger['Flight Distance']} km  \n"
                    f"**Age Group:** {passenger['AgeGroup']}  \n"
                    f"**Flight Category:** {passenger['FlightCategory']}  \n"
                )
                st.markdown(details_md)

            with col2:
                st.markdown("### 📊 Cluster Info")
                cluster_num = clusters[0]
                st.markdown(f"**Cluster {cluster_num}** assigned to passenger")

            with col3:
                st.markdown("### ✈️ Airline Recommendations")
                cluster_num = clusters[0]
                rec_text = get_cluster_recommendation(df, cluster_num)
                st.markdown(f"<div class='box-content' style='min-height: 250px;'>{rec_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

            st.markdown("## 🔎 Visualization")
            if show_viz:
                cluster_num = clusters[0]
                if viz_top5:
                    st.markdown(f"#### Top 5 Services - Cluster {cluster_num}")
                    plot_services_interactive(df, cluster_num, top=True, height=300, font_size=16)
                if viz_bottom5:
                    st.markdown(f"#### Bottom 5 Services - Cluster {cluster_num}")
                    plot_services_interactive(df, cluster_num, top=False, height=300, font_size=16)

        elif mode == "Upload CSV File":
            with col1:
                st.markdown("### 📊 Cluster Info")
                cluster_counts = df["Assigned Cluster"].value_counts().sort_index()
                for cluster_num, count in cluster_counts.items():
                    st.markdown(f"**Cluster {cluster_num}:** {count} passengers")

            with col2:
                st.markdown("### ✈️ Airline Recommendations")
                for cluster_num in clusters:
                    rec_text = get_cluster_recommendation(df, cluster_num)
                    st.markdown(f"<div class='box-content' style='min-height: 250px;'>{rec_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("### (Empty for CSV mode)")

            st.markdown("## 🔎 Visualization")
            if show_viz:
                for cluster_num in clusters:
                    if viz_top5:
                        st.markdown(f"#### Top 5 Services - Cluster {cluster_num}")
                        plot_services_interactive(df, cluster_num, top=True, height=300, font_size=16)
                    if viz_bottom5:
                        st.markdown(f"#### Bottom 5 Services - Cluster {cluster_num}")
                        plot_services_interactive(df, cluster_num, top=False, height=300, font_size=16)

    else:
        if show_viz:
            st.warning("⚠️ Please predict a cluster or upload CSV first to see visualizations.")

if __name__ == "__main__":
    segment_page()
