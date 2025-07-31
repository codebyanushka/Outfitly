import streamlit as st
import os
import pandas as pd
from utils import render_sidebar

# Constants
IMAGE_DIR = "images"
CLOSET_FILE = "closet_data.csv"

# Stop if not logged in
if "username" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]
render_sidebar()

st.title("👚 My Closet")

uploaded_files = st.file_uploader("Upload clothes", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if uploaded_files:
    for file in uploaded_files:
        save_path = os.path.join(IMAGE_DIR, file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        if os.path.exists(CLOSET_FILE):
            closet_df = pd.read_csv(CLOSET_FILE)
        else:
            closet_df = pd.DataFrame(columns=["username", "filename", "category"])

        new_row = {"username": username, "filename": file.name, "category": ""}
        closet_df = pd.concat([closet_df, pd.DataFrame([new_row])], ignore_index=True)
        closet_df.to_csv(CLOSET_FILE, index=False)

    st.success("Images uploaded. Set categories below.")

# Display user closet
if os.path.exists(CLOSET_FILE):
    closet_df = pd.read_csv(CLOSET_FILE)
    user_closet = closet_df[closet_df["username"] == username]

    if not user_closet.empty:
        st.subheader("Your Closet")
        for idx, row in user_closet.iterrows():
            col1, col2 = st.columns([1, 2])
            image_path = os.path.join(IMAGE_DIR, row["filename"])
            col1.image(image_path, width=100)

            category = col2.selectbox(
                f"Category for {row['filename']}",
                ["Top", "Bottom", "Footwear", "Outerwear"],
                key=row["filename"],
                index=["Top", "Bottom", "Footwear", "Outerwear"].index(row["category"]) if row["category"] in ["Top", "Bottom", "Footwear", "Outerwear"] else 0
            )

            closet_df.loc[(closet_df["username"] == username) & (closet_df["filename"] == row["filename"]), "category"] = category

        closet_df.to_csv(CLOSET_FILE, index=False)
    else:
        st.info("No items in your closet yet.")
