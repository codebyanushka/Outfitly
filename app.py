import streamlit as st
import pandas as pd
import os

# File paths
USER_DATA_FILE = "user_data.csv"
AVATAR_DATA_FILE = "avatar_data.csv"
AVATAR_FOLDER = "avatars"

# Page config
st.set_page_config(page_title="Outfitly - Your AI Stylist", layout="centered")

# Create necessary folders
os.makedirs(AVATAR_FOLDER, exist_ok=True)

# Initialize session state
if "username" not in st.session_state:
    st.session_state["username"] = None

# Load user data
if os.path.exists(USER_DATA_FILE):
    user_df = pd.read_csv(USER_DATA_FILE)
else:
    user_df = pd.DataFrame(columns=["username", "password", "gender", "body_type", "wardrobe_name"])

# Sidebar navigation if user is logged in
if st.session_state["username"]:
    with st.sidebar:
        st.header("👋 Welcome, " + st.session_state["username"])

        # Show avatar from avatar_data.csv
        if os.path.exists(AVATAR_DATA_FILE):
            avatar_df = pd.read_csv(AVATAR_DATA_FILE)
            avatar_row = avatar_df[avatar_df["username"] == st.session_state["username"]]
            if not avatar_row.empty:
                avatar_url = avatar_row.iloc[0]["avatar_url"]
                st.image(avatar_url, width=100)

        # Page links
        st.page_link("pages/1_Closet.py", label="👚 My Closet")
        st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
        st.page_link("pages/3_History.py", label="📸 Outfit History")
        st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")

        # Logout
        if st.button("🚪 Logout"):
            st.session_state["username"] = None
            st.success("Logged out successfully.")
            st.rerun()

# Main App Content
st.title("👗 Outfitly")
st.markdown("Your AI-powered fashion assistant! Get outfit recommendations tailored to your style, body type, and occasion.")

# Show login/signup if not logged in
if not st.session_state["username"]:
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab1:
        st.subheader("Login")
        uname = st.text_input("Username", key="login_username")
        pwd = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            match = user_df[(user_df["username"] == uname) & (user_df["password"] == pwd)]
            if not match.empty:
                st.session_state["username"] = uname
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.subheader("Sign Up")
        new_uname = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type="password")
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        body_type = st.selectbox("Body Type", ["Hourglass", "Pear", "Apple", "Rectangle", "Triangle"])
        wardrobe_name = st.text_input("Name Your Wardrobe")

        if st.button("Create Account"):
            if new_uname in user_df["username"].values:
                st.error("Username already exists. Please choose another.")
            else:
                new_row = pd.DataFrame([{
                    "username": new_uname,
                    "password": new_pwd,
                    "gender": gender,
                    "body_type": body_type,
                    "wardrobe_name": wardrobe_name
                }])
                user_df = pd.concat([user_df, new_row], ignore_index=True)
                user_df.to_csv(USER_DATA_FILE, index=False)
                st.success("Account created! Please log in.")
                st.session_state["username"] = new_uname
                st.rerun()
