import streamlit as st

def about_page():
    st.markdown("""
        <style>
            .about-hero {
                background: linear-gradient(90deg, #6a11cb, #2575fc);
                padding: 40px 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            .about-hero h1 {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            .about-hero p {
                font-size: 18px;
                margin-top: 8px;
                opacity: 0.9;
            }
            .about-section {
                background: #222;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 25px;
                color: #fff;
                font-size: 16px;
                line-height: 1.6;
            }
            .about-section h2 {
                color: #ff4081;
                font-size: 24px;
                margin-bottom: 15px;
            }
            .feature-box {
                background: linear-gradient(90deg, #9c27b0, #673ab7);
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                color: white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                font-size: 15px;
            }
            .feature-box h3 {
                margin-top: 0;
                margin-bottom: 8px;
                font-size: 20px;
            }
            .vision-box {
                background: linear-gradient(90deg, #ff9800, #ff5722);
                padding: 20px;
                border-radius: 10px;
                margin-top: 25px;
                color: white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                font-size: 16px;
            }
            .vision-box h2 {
                font-size: 22px;
                margin-bottom: 12px;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
        <div class="about-hero">
            <h1>✈️ SkySatisfy</h1>
            <p>Your AI Co-Pilot for Passenger Satisfaction</p>
        </div>
    """, unsafe_allow_html=True)

    # Introduction
    st.markdown("""
        <div class="about-section">
            <p>
                <strong>SkySatisfy</strong> is a smart, AI-driven platform built to help airlines deeply understand passenger satisfaction and behavior. 
                By combining machine learning, rich analytics, and user-friendly dashboards, SkySatisfy enables data-driven decision-making to enhance 
                customer experience, optimize operations, and drive loyalty.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <div class="about-section">
            <h2>🚀 What SkySatisfy Offers</h2>

            <div class="feature-box">
                <h3>👥 Passenger Segmentation</h3>
                <p>Clusters passengers based on demographic profiles, travel behavior, and preferences to support targeted service and personalized campaigns.</p>
            </div>

            <div class="feature-box">
                <h3>😊 Satisfaction Prediction</h3>
                <p>Uses machine learning to predict whether a passenger is likely to be satisfied or dissatisfied, enabling proactive service adjustments.</p>
            </div>

            <div class="feature-box">
                <h3>🔎 Service Insights & Recommendations</h3>
                <p>Highlights which services most impact satisfaction. Guides improvements by identifying pain points specific to passenger clusters.</p>
            </div>

            <div class="feature-box">
                <h3>📊 Interactive Dashboards</h3>
                <p>Explore real-time visualizations, trends, and correlations through intuitive dashboards designed for fast, impactful decision-making.</p>
            </div>

            <div class="feature-box">
                <h3>🚨 Anomaly Detection</h3>
                <p>
                    Automatically detects outliers in passenger data using statistical methods. 
                    SkySatisfy flags scores that deviate by more than two standard deviations from the cluster mean, identifying unusual patterns or 
                    service failures. Alerts are integrated into the recommendation engine for timely action.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Vision Statement
    st.markdown("""
        <div class="vision-box">
            <h2>🌐 Our Vision</h2>
            <p>
                At SkySatisfy, we envision a world where airlines don’t just react to customer feedback—they anticipate it. 
                By transforming raw data into actionable insight, SkySatisfy enables smarter strategy, greater efficiency, 
                and elevated passenger satisfaction. Let us be your AI co-pilot on the journey toward excellence.
            </p>
        </div>
    """, unsafe_allow_html=True)
