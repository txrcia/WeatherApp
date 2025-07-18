import streamlit as st

# This function shows the About page of the SkySatisfy app.
# It explains what the app does and why it's useful.
def about_page():
    # Custom CSS to make the page look nicer (colors, layout, fonts, etc.)
    st.markdown("""
        <style>
            /* Top banner with title and tagline */
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

            /* Sections that explain the app */
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

            /* Boxes that list features */
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

            /* Box for the vision/mission section */
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

    # App name and short tagline at the top
    st.markdown("""
        <div class="about-hero">
            <h1>✈️ SkySatisfy</h1>
            <p>Your AI Co-Pilot for Passenger Satisfaction</p>
        </div>
    """, unsafe_allow_html=True)

    # Short intro explaining what the app does and why it’s helpful
    st.markdown("""
        <div class="about-section">
            <p>
                <strong>SkySatisfy</strong> is an AI tool that helps airlines understand and improve passenger satisfaction.
                It gives useful insights so airlines can make better decisions and keep their customers happy.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # List of features and what they do
    st.markdown("""
        <div class="about-section">
            <h2>🚀 What SkySatisfy Offers</h2>
            <div class="feature-box">
                <h3>👥 Passenger Segmentation</h3>
                <p>Groups passengers based on behavior and preferences to help airlines serve them better.</p>
            </div>
            <div class="feature-box">
                <h3>😊 Satisfaction Prediction</h3>
                <p>Predicts if a passenger will be satisfied or not based on their journey experience.</p>
            </div>
            <div class="feature-box">
                <h3>🔎 Service Insights & Recommendations</h3>
                <p>Shows which services matter most and which need improvement.</p>
            </div>
            <div class="feature-box">
                <h3>📊 Interactive Dashboards</h3>
                <p>Displays easy-to-understand charts and graphs to explore satisfaction trends.</p>
            </div>
            <div class="feature-box">
                <h3>⚠️ Anomaly Detection</h3>
                <p>Identifies unusual patterns in passenger data to uncover hidden issues or outliers that could affect satisfaction or operations.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Final box showing the app’s mission and vision
    st.markdown("""
        <div class="vision-box">
            <h2>🌐 Our Vision</h2>
            <p>
                SkySatisfy helps airlines turn data into smart strategies. We want to make flying better for passengers
                and more profitable for airlines.
                <br><br>
                Think of us as your co-pilot for improving customer experience.
            </p>
        </div>
    """, unsafe_allow_html=True)
