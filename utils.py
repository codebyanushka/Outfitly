import streamlit as st
import os
from PIL import Image

# Directory where avatars are saved
AVATAR_DIR = "images/avatars"

def load_avatar(username):
    """
    Display the user's avatar image if it exists.
    """
    avatar_path = os.path.join(AVATAR_DIR, f"{username}_avatar.png")
    if os.path.exists(avatar_path):
        st.image(avatar_path, width=80, caption="Your Avatar")
    else:
        st.write("No avatar found.")

def clear_session():
    """
    Logs the user out by clearing all Streamlit session state values.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def render_sidebar():
    """
    Render the sidebar with avatar and navigation links if the user is logged in.
    """
    with st.sidebar:
        if "username" in st.session_state and st.session_state["username"]:
            username = st.session_state["username"]
            st.markdown(f"### 👤 {username}")
            load_avatar(username)
            st.page_link("pages/1_Closet.py", label="👚 My Closet")
            st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
            st.page_link("pages/3_History.py", label="📸 Outfit History")
            st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")
            st.button("🚪 Logout", on_click=clear_session)
