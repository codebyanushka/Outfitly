import streamlit as st
import os

def render_sidebar():
    # ✅ Show avatar on top-right if logged in
    if "username" in st.session_state:
        username = st.session_state["username"]
        avatar_path = os.path.join("avatars", f"{username}.png")
        if os.path.exists(avatar_path):
            _, avatar_col = st.columns([11, 1])
            with avatar_col:
                st.image(avatar_path, width=60, caption=username)

    # Sidebar navigation
    with st.sidebar:
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧍‍♀️ Create Avatar")
        if st.button("🚪 Logout"):
            st.session_state.logout = True
            st.switch_page("app.py")
