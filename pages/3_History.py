import streamlit as st
import os
import pandas as pd
from utils import render_sidebar

IMAGE_DIR = "images"
HISTORY_FILE = "outfit_history.csv"

if "username" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]
render_sidebar()

st.title("📸 Outfit History")

if os.path.exists(HISTORY_FILE):
    history_df = pd.read_csv(HISTORY_FILE)
    user_history = history_df[history_df["username"] == username]

    if user_history.empty:
        st.info("You haven't generated any outfits yet.")
    else:
        for i, row in user_history[::-1].iterrows():
            st.markdown(f"**Date:** {row['date_time']}")
            st.markdown(f"**Occasion:** {row['occasion']}  |  **Weather:** {row['weather']}")
            cols = st.columns(4)
            for idx, category in enumerate(["top", "bottom", "footwear", "outerwear"]):
                if pd.notna(row[category]):
                    image_path = os.path.join(IMAGE_DIR, row[category])
                    cols[idx].image(image_path, caption=category.capitalize(), use_container_width=True)
            st.markdown("---")
else:
    st.info("No outfit history available.")
