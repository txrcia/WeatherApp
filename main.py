import streamlit as st

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------
st.set_page_config(
    page_title="SkySatisfy - Airline Satisfaction AI",
    layout="wide"
)

# --------------------------------------------------------
# GLOBAL STYLING
# --------------------------------------------------------
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            font-size: 14px !important;
        }

        /* Reduce overall page zoom slightly for a smaller look */
        [data-testid="stApp"] {
            zoom: 90%;
            margin: 0 auto;
            max-width: 1400px;
        }

        /* Center main content area */
        .block-container {
            margin-left: auto;
            margin-right: auto;
            max-width: 1200px;
        }

        /* Sidebar font sizes */
        section[data-testid="stSidebar"] {
            font-size: 16px !important;
        }
        
        /* Smaller expander headers */
        .streamlit-expanderHeader {
            font-size: 16px !important;
        }

        /* Smaller DataFrame text */
        .stDataFrame th, .stDataFrame td {
            font-size: 12px !important;
        }

        /* Reduce the header logo/title size */
        h1 {
            font-size: 36px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# REST OF YOUR APP
# --------------------------------------------------------

from navigation import custom_navigation
from Home_Page import home_page
from satisfaction_page import satisfaction_prediction_page
from Segment_Page import segment_page
from About_page import about_page

# --- Header Section: Logo Left, Title Centered ---

col1, col2, col3 = st.columns([2, 8, 2])

with col1:
    st.image("Logo3.png", width=200)

with col2:
    st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        ">
            <h1 style="
                font-size: 36px;
                font-weight: bold;
                color: white;
                text-shadow: 2px 2px 5px black;
                margin: 0;
            ">
                SkySatisfy
            </h1>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.empty()

# --- Navigation and Page Rendering ---

pages = {
    "main": "🏠 Home",
    "satisfaction": "😊 Satisfaction Prediction",
    "segment": "👥 Passenger Segmentation",
    "about": "ℹ️ About SkySatisfy"
}

current_page = custom_navigation(pages)

if current_page == "main":
    home_page()
elif current_page == "satisfaction":
    satisfaction_prediction_page()
elif current_page == "segment":
    segment_page()
elif current_page == "about":
    about_page()
