import streamlit as st

def home_page():

    st.markdown(
        """
        <style>
            .hero {
                background: linear-gradient(90deg, #6a11cb, #2575fc);
                color: white;
                padding: 50px 20px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 40px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            }
            .hero h1 {
                font-size: 60px;
                font-weight: bold;
            }
            .hero p {
                font-size: 22px;
                margin-top: 15px;
                opacity: 0.9;
            }
            .cta-button {
                background-color: white;
                color: #6a11cb;
                font-weight: bold;
                padding: 12px 24px;
                font-size: 18px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
            }
            .cta-button:hover {
                background-color: #ddd;
            }
            .feature-card {
                background-color: #222;
                color: white;
                padding: 20px;
                border-radius: 8px;
                height: 100%;
                transition: transform 0.2s;
            }
            .feature-card:hover {
                transform: scale(1.02);
            }
            .feature-title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #9c27b0;
            }
            .about-box {
                background-color: #333;
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-top: 30px;
                font-size: 20px;
                line-height: 1.6;
            }
            .purple-black-box {
                background: linear-gradient(90deg, purple, black);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                font-size: 18px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }
            .blue-black-box {
                background: linear-gradient(90deg, royalblue, black);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                font-size: 18px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # HERO SECTION
    st.markdown("""
        <div class="hero">
            <h1>✈️ SkySatisfy</h1>
            <p>
                Your AI co-pilot for passenger satisfaction. Analyze, predict, and improve airline services with data-driven insights.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # SHORT ABOUT SECTION
    st.markdown("""
        <div class="about-box">
            <p>
                SkySatisfy is an AI-powered platform designed for airlines to gain deep insights into passenger behavior and satisfaction.
                From clustering passengers into meaningful groups, to predicting satisfaction levels, and pinpointing services that need improvement — SkySatisfy turns your data into actionable strategies.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # FEATURES SECTION
    st.markdown("## ✨ Core Features")

    cols = st.columns(3)
    features = [
        {
            "title": "AI Passenger Clustering",
            "desc": "Group passengers into insightful clusters for personalized services and targeted loyalty programs."
        },
        {
            "title": "Satisfaction Prediction",
            "desc": "Predict if a passenger will be satisfied or not — enabling proactive engagement to boost loyalty."
        },
        {
            "title": "Interactive Dashboards",
            "desc": "Visualize insights in stunning charts and dashboards to quickly spot trends and service gaps."
        }
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

    # HOW IT WORKS - BLUE TO BLACK
    st.markdown("## ⚙️ How SkySatisfy Works")

    steps = [
        "Upload your passenger data (CSV or manual inputs).",
        "Run the AI segmentation and prediction models.",
        "Explore recommendations and interactive visualizations."
    ]

    for i, step in enumerate(steps, start=1):
        st.markdown(
            f"""
            <div class="blue-black-box">
                <strong>Step {i}:</strong> {step}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # WHY AIRLINES CHOOSE - PURPLE TO BLACK
    st.markdown("## 🎯 Why Airlines Choose SkySatisfy")

    benefits = [
        "Increase passenger loyalty and satisfaction.",
        "Identify and improve service gaps efficiently.",
        "Make fast, data-driven decisions to stay ahead of competitors."
    ]

    for benefit in benefits:
        st.markdown(
            f"""
            <div class="purple-black-box">
                ✅ {benefit}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # FINAL ABOUT BOX
    st.markdown("""
        <div class="about-box">
            <h3>ℹ️ About SkySatisfy</h3>
            <p>
                SkySatisfy combines powerful machine learning with beautiful data visualizations to help airlines unlock passenger insights like never before.
                From clustering and satisfaction prediction to tailored service recommendations, SkySatisfy empowers airlines to enhance customer experience and boost revenue.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
