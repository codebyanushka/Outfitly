import streamlit as st
import pandas as pd
import os
from utils import load_avatar, clear_session

# Config
st.set_page_config(page_title="Outfitly", page_icon="👗", layout="wide")
USER_DATA_FILE = "user_data.csv"

# Ensure user data CSV exists
if not os.path.exists(USER_DATA_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_DATA_FILE, index=False)

# Initialize session state
if "username" not in st.session_state:
    st.session_state["username"] = None

# ---------------- IF LOGGED IN ----------------
if st.session_state["username"]:
    username = st.session_state["username"]

    # Header
    st.markdown(
        f"<h3 style='text-align: left;'>👋 Welcome, <span style='color:#FAD02C'>{username}</span></h3>",
        unsafe_allow_html=True,
    )

    # Avatar + Logout button in top-right
    col1, col2 = st.columns([5, 1])
    with col2:
        load_avatar(username)
        st.button("🚪 Logout", on_click=clear_session)

    st.markdown("<br>", unsafe_allow_html=True)

    # Title & Description
    st.markdown("<h1 style='text-align: center;'>👗 Outfitly</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>Your AI-powered fashion assistant! Get outfit recommendations tailored to your style, body type, and occasion.</p>",
        unsafe_allow_html=True,
    )

    # Centered navigation buttons
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")

# ---------------- LOGIN / SIGNUP ----------------
else:
    st.markdown("<h1 style='text-align: center;'>👗 Outfitly</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Login or sign up to get started.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            users = pd.read_csv(USER_DATA_FILE)
            user = users[(users["username"] == username) & (users["password"] == password)]

            if not user.empty:
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.subheader("Signup")
        new_username = st.text_input("New Username", key="signup_user")
        new_password = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Signup"):
            users = pd.read_csv(USER_DATA_FILE)
            if new_username in users["username"].values:
                st.warning("Username already exists.")
            elif not new_username or not new_password:
                st.warning("Please fill in all fields.")
            else:
                new_user = pd.DataFrame([[new_username, new_password]], columns=["username", "password"])
                new_user.to_csv(USER_DATA_FILE, mode="a", header=False, index=False)
                st.success("Account created! Please log in.")
