import streamlit as st
import os
import random
import pandas as pd
from datetime import datetime

IMAGE_DIR = "images"
CLOSET_FILE = "closet_data.csv"
HISTORY_FILE = "outfit_history.csv"

# Show avatar if logged in
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
    st.page_link("pages/3_History.py", label="📸 Outfit History")
    st.page_link("pages/4_Avatar.py", label="🧑 Customize Avatar")
    if st.button("🚪 Logout"):
        st.session_state.logout = True
        st.switch_page("app.py")

# Stop if not logged in
if "username" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]

# Title
st.title("🧠 Create Your Fit")

# Load user's closet
if not os.path.exists(CLOSET_FILE):
    st.error("No closet found. Please upload clothes in My Closet page.")
    st.stop()

closet_df = pd.read_csv(CLOSET_FILE)
user_closet = closet_df[closet_df["username"] == username]

if user_closet.empty:
    st.info("No clothes found. Please add some to your closet.")
    st.stop()

# Occasion and Weather
occasion = st.selectbox("📅 Occasion", ["Casual", "Formal", "Party", "Sporty", "Work", "Date"])
weather = st.selectbox("🌤️ Weather", ["Sunny", "Rainy", "Cold", "Hot", "Windy"])

# Generate outfit
if st.button("✨ Generate Outfit"):
    selected = {}
    for cat in ["Top", "Bottom", "Footwear", "Outerwear"]:
        items = user_closet[user_closet["category"] == cat]
        if not items.empty:
            selected[cat] = items.sample(1)["filename"].values[0]
        else:
            selected[cat] = None

    # Display
    cols = st.columns(4)
    for i, cat in enumerate(["Top", "Bottom", "Footwear", "Outerwear"]):
        if selected[cat]:
            cols[i].image(os.path.join(IMAGE_DIR, selected[cat]), caption=cat, use_container_width=True)
        else:
            cols[i].markdown(f"*No {cat} available*")

    # Save history
    history_entry = {
        "username": username,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top": selected.get("Top"),
        "bottom": selected.get("Bottom"),
        "footwear": selected.get("Footwear"),
        "outerwear": selected.get("Outerwear"),
        "occasion": occasion,
        "weather": weather,
        "favorite": False
    }

    if os.path.exists(HISTORY_FILE):
        history_df = pd.read_csv(HISTORY_FILE)
        history_df = pd.concat([history_df, pd.DataFrame([history_entry])], ignore_index=True)
    else:
        history_df = pd.DataFrame([history_entry])

    history_df.to_csv(HISTORY_FILE, index=False)
    st.success("Outfit saved to history!")

else:
    st.info("Click 'Generate Outfit' to get a styled look.")

