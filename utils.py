import streamlit as st
import os
from PIL import Image, UnidentifiedImageError

def render_sidebar():
    if "username" not in st.session_state:
        return  # Nothing to show if not logged in

    st.sidebar.markdown("## Navigation")
    st.sidebar.page_link("pages/1_Closet.py", label="👚 My Closet")
    st.sidebar.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
    st.sidebar.page_link("pages/3_History.py", label="📸 Outfit History")
    st.sidebar.page_link("pages/4_Avatar.py", label="🧍 Customize Avatar")

    if "avatar_path" in st.session_state:
        st.sidebar.image(st.session_state["avatar_path"], width=100, caption="Your Avatar")

    if st.sidebar.button("Logout 🔒"):
        st.session_state.clear()
        st.experimental_rerun()


        # Navigation links
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")

        # Logout button
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
