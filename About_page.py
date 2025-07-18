import streamlit as st

def about_page():
    # Injects custom CSS styles for layout, colors, and fonts
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

    # Displays the hero title and subtitle section at the top
    st.markdown("""
        <div class="about-hero">
            <h1>✈️ SkySatisfy</h1>
            <p>Your AI Co-Pilot for Passenger Satisfaction</p>
        </div>
    """, unsafe_allow_html=True)

    # Main description about the app's purpose and philosophy
    st.markdown("""
        <div class="about-section">
            <p>
                <strong>SkySatisfy</strong> is a modern, AI-powered platform that helps airlines unlock deep insights into passenger satisfaction and behavior.
                We believe that understanding customers is the key to building loyalty, improving services, and staying competitive in the aviation industry.
                SkySatisfy combines advanced machine learning, intuitive visualizations, and user-friendly tools to empower airlines with data-driven decisions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # List of platform features, each in its own styled box
    st.markdown("""
        <div class="about-section">
            <h2>🚀 What SkySatisfy Offers</h2>
            <div class="feature-box">
                <h3>👥 Passenger Segmentation</h3>
                <p>Automatically groups passengers into meaningful clusters based on demographics, travel patterns, and behaviors. Helps airlines tailor services and marketing to each segment’s needs.</p>
            </div>
            <div class="feature-box">
                <h3>😊 Satisfaction Prediction</h3>
                <p>Predicts whether a passenger is likely to be satisfied or dissatisfied based on their travel experience. Allows proactive action to improve loyalty and reduce churn.</p>
            </div>
            <div class="feature-box">
                <h3>🔎 Service Insights & Recommendations</h3>
                <p>Identifies which services matter most to each passenger group. Pinpoints low-rated services that need improvement to enhance overall experience.</p>
            </div>
            <div class="feature-box">
                <h3>📊 Interactive Dashboards</h3>
                <p>Provides visual analytics, charts, and easy-to-understand insights. Supports quick exploration of trends and patterns in passenger satisfaction.</p>
            </div>
            <div class="feature-box">
                <h3>🚨 Anomaly Detection</h3>
                <p>Detects unusual or suspicious passenger behavior and service patterns using advanced AI algorithms. Helps identify operational issues and improve safety and quality control.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Company vision and final message
    st.markdown("""
        <div class="vision-box">
            <h2>🌐 Our Vision</h2>
            <p>
                At SkySatisfy, our mission is to help airlines transform raw data into meaningful strategies. By revealing what truly drives passenger satisfaction, we enable airlines to optimize operations, elevate service quality, and increase profitability.
                <br><br>
                SkySatisfy is your co-pilot on the journey to higher customer loyalty and a better flying experience.
            </p>
        </div>
    """, unsafe_allow_html=True)
