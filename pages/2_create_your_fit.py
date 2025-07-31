import streamlit as st
import os
import random
import pandas as pd
from datetime import datetime
from utils import render_sidebar  # ✅ Use render_sidebar

# Constants
IMAGE_DIR = "images"
CLOSET_FILE = "closet_data.csv"
HISTORY_FILE = "outfit_history.csv"

# Stop if not logged in
if "username" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]

# Sidebar with avatar
render_sidebar()

# Page title
st.title("🧠 Create Your Fit")

# Load closet
if not os.path.exists(CLOSET_FILE):
    st.error("No closet found. Please upload clothes in My Closet page.")
    st.stop()

closet_df = pd.read_csv(CLOSET_FILE)
user_closet = closet_df[closet_df["username"] == username]

if user_closet.empty:
    st.info("No clothes found. Please add some to your closet.")
    st.stop()

# Occasion and weather selection
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

    # Display selected outfit
    cols = st.columns(4)
    for i, cat in enumerate(["Top", "Bottom", "Footwear", "Outerwear"]):
        if selected[cat]:
            cols[i].image(os.path.join(IMAGE_DIR, selected[cat]), caption=cat, use_container_width=True)
        else:
            cols[i].markdown(f"*No {cat} available*")

    # Save to history
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
