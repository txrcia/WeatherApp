import streamlit as st

def custom_navigation(pages):
    st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: space-around;  /* evenly spread the links */
        background-color: #4A90E2;  /* navbar background */
        padding: 14px 25px;
        border-radius: 10px;
        margin: 10px auto 30px auto;  /* reduce top margin to bring navbar closer */
        width: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }

    .nav-item {
        margin: 0 18px;
        padding: 10px 24px;
        color: #ffffff !important;  /* white text */
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: 700;
        font-size: 20px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
        background-color: transparent;
    }

    .nav-item:hover {
        border: 2px solid #ffffff;  /* white border on hover */
        color: #ffffff !important;
    }

    .nav-item.active {
        border: 2px solid #ffffff;  /* border for active page */
        color: #ffffff !important;  /* active page text stays white */
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get current page from query params
    query_params = st.query_params
    current_page_list = query_params.get("page", [list(pages.keys())[0]])
    current_page = current_page_list[0] if isinstance(current_page_list, list) else current_page_list

    # Build links
    links = ""
    for key, label in pages.items():
        active = "active" if current_page == key else ""
        links += f'<a href="?page={key}" class="nav-item {active}">{label}</a>'

    st.markdown(f'<div class="nav-container">{links}</div>', unsafe_allow_html=True)
    return current_page
