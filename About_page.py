import streamlit as st

def about_page():
    st.markdown(
        """
        <style>
            /* Wider container for a full-page look */
            .block-container {
                max-width: 95% !important;
                padding-left: 2rem;
                padding-right: 2rem;
            }

            /* INFO BOXES */
            .info-box {
                background-color: #a9d6e5; /* purple gradient-ish color */
                color: #333333;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.35);
                margin-bottom: 18px;
                font-size: 16px;
                line-height: 1.6;
                transition: transform 0.2s ease, box-shadow 0.3s ease;
            }

            .info-box:hover {
                transform: scale(1.02);
                box-shadow: 0 6px 20px rgba(0,0,0,0.45);
            }

            /* SECTION HEADINGS */
            h2 {
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                margin-top: 20px;
                margin-bottom: 15px;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # PAGE TITLE
    st.markdown("<h2>About Haze</h2>", unsafe_allow_html=True)

    # ABOUT CONTENT
    about_texts = [
        "Haze is your AI-powered companion for monitoring weather and air quality in real-time.",
        "Our mission is to empower individuals and communities with actionable insights to stay safe, plan daily activities, and support environmental awareness.",
        "We integrate IoT sensors, government data, and predictive AI models to provide accurate forecasts, heat alerts, and pollution insights.",
        "Haze is designed to be intuitive, interactive, and informative for citizens, authorities, and researchers alike.",
        "Our team at UrbanX is committed to advancing smart city initiatives and promoting healthier urban living."
    ]

    for text in about_texts:
        st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
