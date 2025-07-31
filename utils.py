import streamlit as st
import os
from PIL import Image, UnidentifiedImageError

def render_sidebar():
    with st.sidebar:
        # Avatar section
        st.markdown("## 👤 Profile")

        if "username" in st.session_state:
            username = st.session_state["username"]
            avatar_path = f"images/avatars/{username}_avatar.png"
            if os.path.exists(avatar_path) and os.path.getsize(avatar_path) > 0:
                try:
                    image = Image.open(avatar_path)
                    st.image(image, width=120, caption=username)
                except UnidentifiedImageError:
                    st.warning("⚠️ Unable to load avatar image. Please recreate it.")
            else:
                st.info("🧑 No avatar found. Please create one.")

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
