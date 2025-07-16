import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

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

def categorize_age(age):
    if age <= 30:
        return 'Young'
    elif age <= 55:
        return 'Middle-aged'
    else:
        return 'Old'

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

def plot_services_interactive(df, cluster_num, top=True, height=300, font_size=16):
    cluster_df = df[df['Assigned Cluster'] == cluster_num]
    if cluster_df.empty:
        st.info(f"No passengers in Cluster {cluster_num} for visualization.")
        return
    mean_scores = cluster_df[service_cols].mean()
    selected = mean_scores.sort_values(ascending=not top).head(5)
    fig = go.Figure(go.Bar(
        x=selected.values[::-1],
        y=selected.index[::-1],
        orientation='h',
        marker=dict(color=px.colors.sequential.Plasma[:len(selected)]),
        hovertemplate='%{y}: %{x:.2f}<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text=""),
        xaxis=dict(
            title='Average Satisfaction Score',
            range=[0, 5],
            gridcolor='gray',
            tickfont=dict(size=font_size, color='white'),
            titlefont=dict(size=font_size+2, color='white')
        ),
        yaxis=dict(
            title='Service Feature',
            tickfont=dict(size=font_size, color='white'),
            titlefont=dict(size=font_size+2, color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(l=90, r=20, t=40, b=30),
        height=height
    )
    st.plotly_chart(fig, use_container_width=True)

def segment_page():
    # CSS styling
    st.markdown("""
        <style>
            .main-scale { transform: scale(0.9); transform-origin: top left; }
            html, body, div, p, span, li, label, select, input, button {
                font-size: 20px !important; color: white !important;
            }
            .streamlit-expanderHeader { font-size: 32px !important; font-weight: bold; color: white !important; }
            .st-expanderContent { background-color: black !important; }
            .box-content { font-size: 22px !important; color: white !important; line-height: 1.6; }
            h1, h2, h3, h4 { color: white !important; }
            .big-heading { font-size: 60px; font-weight: bold; color: white; text-align: center; }
            section[data-testid="stSidebar"] *:not(h1):not(h2):not(h3):not(.stHeading) {
                font-size: 20px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="main-scale">
            <h1 class='big-heading'>👥 Passenger Segmentation</h1>
            <hr style='border: 1px solid #DDD;'>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("""
        <h2 style='font-size: 30px; margin-bottom: 0px;'>🎛️ Filter Options</h2>
        <hr style='border: 1px solid #CCC; margin-top: 5px; margin-bottom: 15px;'>
    """, unsafe_allow_html=True)

    st.sidebar.header("🧾 Data Input Method")
    mode = st.sidebar.radio("Choose data source:", ["Use Manual Inputs", "Upload CSV File"])
    st.sidebar.caption("Select how you want to provide data for analysis.")

    # If clustering results exist, compute metrics
    if "segmentation_df" in st.session_state:
        df = st.session_state["segmentation_df"]
        cluster_features = ["Customer Type", "Type of Travel", "Class", "AgeGroup", "FlightCategory"]

        if all(col in df.columns for col in cluster_features + ["Assigned Cluster"]):
            df_encoded = df.copy()
            df_encoded["Customer Type"] = le_dict["Customer Type"].transform(df["Customer Type"])
            df_encoded["Type of Travel"] = le_dict["Type of Travel"].transform(df["Type of Travel"])
            df_encoded["Class"] = le_dict["Class"].transform(df["Class"])
            df_encoded["AgeGroup"] = le_dict["AgeGroup"].transform(df["AgeGroup"])
            df_encoded["FlightCategory"] = le_dict["FlightCategory"].transform(df["FlightCategory"])

            X_clustered = df_encoded[cluster_features]
            labels = df["Assigned Cluster"]

            sil_score = silhouette_score(X_clustered, labels)
            db_score = davies_bouldin_score(X_clustered, labels)
            ch_score = calinski_harabasz_score(X_clustered, labels)

            st.sidebar.markdown("---")
            st.sidebar.markdown("### 📈 Clustering Quality Metrics")
            st.sidebar.markdown(
                f"""
                <div style="background-color:#222; padding:10px; border-radius:10px; color:white; font-size:16px;">
                    <p><strong>Silhouette Score:</strong> {sil_score:.4f} (higher is better)</p>
                    <p><strong>Davies–Bouldin Index:</strong> {db_score:.4f} (lower is better)</p>
                    <p><strong>Calinski–Harabasz Score:</strong> {ch_score:.2f} (higher is better)</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.sidebar.markdown("---")
    st.sidebar.header("📊 Visualization Options")
    show_viz = st.sidebar.checkbox("Show Visualizations")
    st.sidebar.caption("Enable to explore top or bottom service ratings for clusters.")

    viz_top5 = False
    viz_bottom5 = False
    if show_viz:
        viz_top5 = st.sidebar.checkbox("Top 5 Services", value=True)
        viz_bottom5 = st.sidebar.checkbox("Bottom 5 Services", value=False)

    # Remaining body logic (manual input, CSV upload, results) stays unchanged
    # You can keep your existing code here for manual inputs, CSV processing,
    # visualization, recommendations, etc.
