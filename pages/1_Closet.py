import streamlit as st
import os
import pandas as pd
from PIL import Image
from util import show_sidebar_with_avatar  # 👈 Make sure util.py is in the root directory

IMAGE_DIR = "images"
USER_DATA = "user_data.csv"
CLOSET_FILE = "closet_data.csv"

# Ensure folders exist
os.makedirs(IMAGE_DIR, exist_ok=True)

# Show sidebar with avatar and navigation
show_sidebar_with_avatar()

# Stop if not logged in
if "username" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]

# Title
st.title("👚 My Closet")

# Upload section
st.subheader("Upload to your closet")
category = st.selectbox("Category", ["Top", "Bottom", "Footwear", "Outerwear"])
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    filename = f"{username}_{category}_{uploaded_file.name}"
    filepath = os.path.join(IMAGE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{category} uploaded!")

    # Save closet entry
    if os.path.exists(CLOSET_FILE):
        closet_df = pd.read_csv(CLOSET_FILE)
    else:
        closet_df = pd.DataFrame(columns=["username", "category", "filename"])

    closet_df = pd.concat([
        closet_df,
        pd.DataFrame([{"username": username, "category": category, "filename": filename}])
    ], ignore_index=True)
    closet_df.to_csv(CLOSET_FILE, index=False)

# View wardrobe
st.subheader("Your Closet")
if os.path.exists(CLOSET_FILE):
    closet_df = pd.read_csv(CLOSET_FILE)
    user_closet = closet_df[closet_df["username"] == username]

    for cat in ["Top", "Bottom", "Footwear", "Outerwear"]:
        st.markdown(f"### {cat}")
        items = user_closet[user_closet["category"] == cat]

        cols = st.columns(4)
        for i, (_, row) in enumerate(items.iterrows()):
            img_path = os.path.join(IMAGE_DIR, row["filename"])
            if os.path.exists(img_path):
                with cols[i % 4]:
                    st.image(img_path, use_container_width=True)
                    if st.button("🗑 Delete", key=f"del_{row['filename']}_{i}"):
                        os.remove(img_path)
                        closet_df = closet_df[closet_df["filename"] != row["filename"]]
                        closet_df.to_csv(CLOSET_FILE, index=False)
                        st.rerun()
else:
    st.info("No items in your closet yet.")
