import streamlit as st
import os

def show_sidebar_with_avatar():
    with st.sidebar:
        # Show avatar if user is logged in
        if "username" in st.session_state:
            username = st.session_state["username"]
            avatar_path = os.path.join("images/avatars", f"{username}_avatar.png")
            if os.path.exists(avatar_path):
                st.image(avatar_path, width=100)
                st.markdown(f"**{username}**")

        # Navigation Links
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑 Customize Avatar")

        # Logout Button
        if st.button("🚪 Logout"):
            st.session_state.logout = True
            st.switch_page("app.py")
