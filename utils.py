import streamlit as st
import os
from PIL import Image, UnidentifiedImageError

def render_sidebar():
    with st.sidebar:
        st.markdown("### 📂 Navigation")
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")

        st.markdown("---")

        # Show avatar if available
        if "username" in st.session_state and st.session_state["username"]:
            username = st.session_state["username"]
            avatar_path = f"images/avatars/{username}_avatar.png"
            if os.path.exists(avatar_path) and os.path.getsize(avatar_path) > 0:
                try:
                    image = Image.open(avatar_path)
                    st.image(image, width=120, caption=username)
                except UnidentifiedImageError:
                    st.warning("⚠️ Can't preview avatar. Please recreate it.")
            else:
                st.info("🧑 No avatar found. Visit 'Customize Avatar' to create one.")

        st.markdown("---")

        # Logout button
        if st.button("🚪 Logout"):
            st.session_state["username"] = None
            st.switch_page("app.py")
