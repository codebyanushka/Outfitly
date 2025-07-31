import streamlit as st
import pandas as pd
import os
from utils import render_sidebar  # Avatar & sidebar display logic

# Streamlit setup
st.set_page_config(page_title="Outfitly", page_icon="👗", layout="wide")

# File paths
USER_DATA_FILE = "user_data.csv"
AVATAR_DATA_FILE = "avatar_data.csv"

# Ensure required CSVs exist
if not os.path.exists(USER_DATA_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_DATA_FILE, index=False)
if not os.path.exists(AVATAR_DATA_FILE):
    pd.DataFrame(columns=["username", "avatar_url"]).to_csv(AVATAR_DATA_FILE, index=False)

# Initialize session state
if "username" not in st.session_state:
    st.session_state["username"] = None

# ----------------- IF LOGGED IN -----------------
if st.session_state["username"]:
    render_sidebar()

    st.markdown("<h1 style='text-align: center;'>👗 Outfitly</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Welcome back, <b>{st.session_state['username']}</b>! Get outfit recommendations tailored to your style, body type, and occasion.</p>", unsafe_allow_html=True)

# ----------------- LOGIN / SIGNUP FLOW -----------------
else:
    st.markdown("<h1 style='text-align: center;'>👗 Outfitly</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your AI-powered fashion assistant! Login or signup to get started.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Signup"])

    # ---- Login ----
    with tab1:
        st.subheader("Login to your account")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            users = pd.read_csv(USER_DATA_FILE)
            user = users[(users["username"] == username) & (users["password"] == password)]

            if not user.empty:
                st.session_state["username"] = username
                st.success("Login successful!")
                st.switch_page("pages/1_Closet.py")  # ✅ redirect to main page
            else:
                st.error("Invalid username or password.")

    # ---- Signup ----
    with tab2:
        st.subheader("Create a new account")
        new_username = st.text_input("New Username", key="signup_user")
        new_password = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Signup"):
            users = pd.read_csv(USER_DATA_FILE)

            if new_username in users["username"].values:
                st.warning("Username already exists.")
            elif new_username == "" or new_password == "":
                st.warning("Please fill in all fields.")
            else:
                new_user = pd.DataFrame([[new_username, new_password]], columns=["username", "password"])
                new_user.to_csv(USER_DATA_FILE, mode="a", header=False, index=False)
                st.success("Account created! Please log in.")
