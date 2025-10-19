import streamlit as st

def home_page():
    st.markdown(
        """
        <style>
            /* Wider container for a full-page look */
            .block-container {
                max-width: 95% !important;
                padding-left: 2rem;
                padding-right: 2rem;
            }

            .hero p {
                font-size: 17px;
                margin-top: 10px;
                opacity: 0.95;
            }

            /* INFO + FEATURE BOXES */
            .info-box, .feature-card {
                background-color: #a9d6e5; /* bluish-grey */
                color: black;
                padding: 18px;
                border-radius: 10px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.35);
                margin-bottom: 18px;
                font-size: 15px;
                line-height: 1.6;
                transition: transform 0.2s ease, box-shadow 0.3s ease;
            }

            .info-box:hover, .feature-card:hover {
                transform: scale(1.02);
                box-shadow: 0 6px 20px rgba(0,0,0,0.45);
            }

            /* FEATURE CARD TEXT */
            .feature-card {
                height: 100%;
                text-align: left;
            }

            .feature-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333333; /* darker text for contrast */
            }

            /* SECTION HEADINGS */
            h2 {
                color: #2c3e50;
                font-size: 28px;
                font-weight: 700;
                margin-top: 30px;
                margin-bottom: 20px;
                padding-bottom: 6px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # PROBLEM STATEMENT
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 0;">
        <h4 style="line-height: 1.5;">
            Urban air pollution and heat islands pose significant risks to health and comfort.
            Many citizens lack access to real-time air quality insights, leading to unawareness of hazardous conditions.
            <strong>Haze</strong> empowers individuals and authorities with actionable, real-time environmental intelligence.
        </h4>
    </div>
    """, unsafe_allow_html=True)


    # FEATURES SECTION
    st.markdown("## Key Features")

    cols = st.columns(4)
    features = [
        {"title": "Live Pollution Maps", "desc": "Visualize real-time AQI levels and stay away from high-risk zones."},
        {"title": "Urban Heat Alerts", "desc": "Monitor temperature anomalies and identify heat islands instantly."},
        {"title": "AI-Based Forecasting", "desc": "Predict upcoming pollution surges and take preventive actions."},
        {"title": "Insightful Dashboards", "desc": "Analyze air quality trends with interactive data visualizations."}
    ]

    for col, feature in zip(cols, features):
        col.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">{feature['title']}</div>
                <div>{feature['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # HOW IT WORKS
    st.markdown("## How Haze Works")

    steps = [
        "Collects real-time weather and pollution data from IoT sensors and APIs.",
        "Processes and predicts environmental risks using AI and statistical models.",
        "Provides personalized alerts, maps, and dashboards for users and authorities."
    ]

    for i, step in enumerate(steps, start=1):
        st.markdown(
            f"""
            <div class="info-box">
                <strong>Step {i}:</strong> {step}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # BENEFITS
    st.markdown("## Why Choose Haze")

    benefits = [
        "Get timely alerts for pollution and heat risks.",
        "Plan daily routines safely with reliable insights.",
        "Support smart city initiatives through data transparency."
    ]

    for benefit in benefits:
        st.markdown(
            f"""
            <div class="info-box">
                {benefit}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ABOUT
    st.markdown("## About Haze")
    st.markdown("""
        <div class="info-box">
            Haze blends AI, IoT, and weather science to provide a unified view of urban air health.
            Its intuitive design and predictive intelligence empower both citizens and policymakers to
            make informed, health-conscious decisions every day.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
