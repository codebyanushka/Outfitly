import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        # Show avatar and username at the top
        if "username" in st.session_state:
            username = st.session_state["username"]
            avatar_path = f"images/avatars/{username}_avatar.png"

            if os.path.exists(avatar_path):
                st.image(avatar_path, width=120, caption=username)
            else:
                st.markdown(f"👋 Welcome, **{username}**")

        st.markdown("---")

        # Navigation links
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")
        st.page_link("main.py", label="🚪 Logout")

# Optional alias
def show_sidebar_with_avatar():
    render_sidebar()
