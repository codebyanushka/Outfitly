import streamlit as st
import pandas as pd
import os
from PIL import Image
import urllib.parse

# Streamlit page setup
st.set_page_config(page_title="Outfitly", page_icon="👗", layout="wide")

# Load user data
USER_DATA_FILE = "user_data.csv"
if not os.path.exists(USER_DATA_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_DATA_FILE, index=False)

# Load avatar data
AVATAR_DATA_FILE = "avatar_data.csv"
if not os.path.exists(AVATAR_DATA_FILE):
    pd.DataFrame(columns=["username", "avatar_url"]).to_csv(AVATAR_DATA_FILE, index=False)

# Initialize session state
if "username" not in st.session_state:
    st.session_state["username"] = None

# Sidebar with avatar and navigation
if st.session_state["username"]:
    with st.sidebar:
        st.header(f"👋 Welcome, {st.session_state['username']}")

        # Load avatar if exists
        avatar_url = None
        avatar_df = pd.read_csv(AVATAR_DATA_FILE)
        avatar_row = avatar_df[avatar_df["username"] == st.session_state["username"]]
        if not avatar_row.empty:
            avatar_url = avatar_row.iloc[0]["avatar_url"]

        if avatar_url:
            st.image(avatar_url, width=100)
        else:
            st.info("No avatar yet. Go to 'Customize Avatar' 👇")

        # Navigation links
        st.markdown("### 📂 Navigation")
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")

        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state["username"] = None
            st.success("Logged out successfully.")
            st.rerun()

# Main content
st.markdown("<h1 style='text-align: center;'>👗 Outfitly</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your AI-powered fashion assistant! Get outfit recommendations tailored to your style, body type, and occasion.</p>", unsafe_allow_html=True)

# Login/Signup form
if not st.session_state["username"]:
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Signup"])

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
                st.rerun()
            else:
                st.error("Invalid username or password.")

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
