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

            /* PAGE HEADING */
            h1 {
                color: #ffffff;
                font-size: 36px;
                font-weight: 700;
                margin-top: 20px;
                margin-bottom: 20px;
                text-align: center;
            }

            /* Paragraphs as smaller text and centered */
            p {
                color: #ffffff;
                font-size: 16px;
                font-weight: 400;
                line-height: 1.5;
                margin-bottom: 12px;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # PAGE TITLE
    st.markdown("<h1>About Haze</h1>", unsafe_allow_html=True)

    # ABOUT CONTENT
    about_text = (
        "Haze is your AI-powered companion for monitoring weather and air quality in real-time. "
        "Our mission is to empower individuals and communities with actionable insights to stay safe, "
        "plan daily activities, and support environmental awareness. "
        "We integrate IoT sensors, government data, and predictive AI models to provide accurate forecasts, "
        "heat alerts, and pollution insights. "
        "Haze is designed to be intuitive, interactive, and informative for citizens, authorities, and researchers alike. "
        "Our team at UrbanX is committed to advancing smart city initiatives and promoting healthier urban living."
    )

    st.markdown(f'<p>{about_text}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
