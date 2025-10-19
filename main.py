import streamlit as st
from Home_Page import home_page
from About_page import about_page
from Map_Page import map_page
from navigation import custom_navigation
import base64

st.set_page_config(
    page_title="Haze - Where air meets intelligence",
    layout="wide"
)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #003566, #A06CD5);  /* gradient from blue to purple */
    background-attachment: fixed;
    min-height: 100vh;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Center content wrapper */
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# CENTERED LOGO
# --------------------------
# --------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("Logo3.png")

st.markdown(f"""
<div style="text-align: center; margin-top: -150px;">
    <img src="data:image/png;base64,{logo_base64}" width="300">
</div>
<div style="text-align: center; font-style: italic; margin-top: -100px; margin-bottom: 10px;">
    <h3>Where air meets intelligence</h3>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# NAVIGATION MENU
# ----------------------------------
pages = {
    "main": "Home",
    "map": "Map",
    "about": "About"
}

current_page = custom_navigation(pages)

# ----------------------------------
# RENDER SELECTED PAGE
# ----------------------------------
if current_page == "main":
    home_page()
elif current_page == "map":
    map_page()
elif current_page == "about":
    about_page()
# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("""
<hr style="border: 1px solid #ffffff; margin-top: 50px; margin-bottom: 10px;">
<div style="text-align: center; color: #ffffff; padding: 10px; font-size: 14px;">
    © 2025 Haze by UrbanX. All rights reserved.
</div>
""", unsafe_allow_html=True)
