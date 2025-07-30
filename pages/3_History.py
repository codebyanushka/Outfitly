import streamlit as st
import pandas as pd
import os
from datetime import datetime

AVATAR_FOLDER = "avatars"
HISTORY_FILE = "outfit_history.csv"
IMAGE_DIR = "images"

# ✅ Show avatar on top-right if logged in
if "username" in st.session_state:
    username = st.session_state["username"]
    avatar_path = os.path.join(AVATAR_FOLDER, f"{username}.png")
    if os.path.exists(avatar_path):
        _, avatar_col = st.columns([11, 1])
        with avatar_col:
            st.image(avatar_path, width=60, caption=username)

# Sidebar navigation
with st.sidebar:
    st.page_link("pages/1_Closet.py", label="👚 My Closet")
    st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
    st.page_link("pages/3_History.py", label="📸 Outfit History")
    if st.button("🚪 Logout"):
        st.session_state.logout = True
        st.switch_page("app.py")

# ✅ Stop if not logged in
if "username" not in st.session_state:
    st.warning("Please login through the onboarding page.")
    st.stop()

username = st.session_state["username"]

# ✅ Ensure history file exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        f.write("username,date_time,top,bottom,footwear,outerwear,occasion,weather,favorite\n")

# Title
st.title("📸 Outfit History")

# Load outfit history
history_df = pd.read_csv(HISTORY_FILE)

# Filter by current user
user_history = history_df[history_df["username"] == username]

# Show if no outfits yet
if user_history.empty:
    st.info("No outfits generated yet.")
    st.stop()

# Show favorites toggle
show_favorites_only = st.checkbox("⭐ Show Favorites Only")
if show_favorites_only:
    user_history = user_history[user_history["favorite"] == True]

# Display each outfit
for idx, row in user_history.iterrows():
    st.markdown(f"### 📅 {row['date_time']}")
    st.markdown(f"**Occasion:** {row.get('occasion', 'N/A')} &nbsp;&nbsp;&nbsp;&nbsp; **Weather:** {row.get('weather', 'N/A')}")

    cols = st.columns(4)

    if pd.notna(row["top"]):
        cols[0].image(os.path.join(IMAGE_DIR, row["top"]), caption="Top", use_container_width=True)
    if pd.notna(row["bottom"]):
        cols[1].image(os.path.join(IMAGE_DIR, row["bottom"]), caption="Bottom", use_container_width=True)
    if pd.notna(row["footwear"]):
        cols[2].image(os.path.join(IMAGE_DIR, row["footwear"]), caption="Footwear", use_container_width=True)
    if pd.notna(row["outerwear"]):
        cols[3].image(os.path.join(IMAGE_DIR, row["outerwear"]), caption="Outerwear", use_container_width=True)

    # Toggle favorite
    if not row["favorite"]:
        if st.button("💖 Mark as Favorite", key=f"fav_{idx}"):
            history_df.at[idx, "favorite"] = True
            history_df.to_csv(HISTORY_FILE, index=False)
            st.success("Added to favorites!")
            st.rerun()
    else:
        st.markdown("✅ Already marked as favorite")

    st.markdown("---")
