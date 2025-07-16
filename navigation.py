import streamlit as st

def custom_navigation(pages):
    st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: center;
        background: linear-gradient(90deg, purple, navy);
        padding: 14px 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }

    .nav-item {
        margin: 0 18px;
        padding: 10px 24px;
        color: #ffffffcc;
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }

    .nav-item:hover {
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        border-color: #ffffff55;
        text-decoration: none !important;
    }

    .nav-item.active {
        background-color: #ffffff;
        color: purple !important;
        font-weight: 800;
        border-color: #ffffff;
        text-decoration: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    query_params = st.query_params
    current_page = query_params.get("page", list(pages.keys())[0])

    links = ""
    for key, label in pages.items():
        active = "active" if current_page == key else ""
        links += f'<a href="?page={key}" class="nav-item {active}">{label}</a>'

    st.markdown(f'<div class="nav-container">{links}</div>', unsafe_allow_html=True)
    return current_page
