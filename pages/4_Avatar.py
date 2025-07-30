import streamlit as st
import urllib.parse
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import os

st.set_page_config(page_title="Avatar", page_icon="🧍")

# Sidebar navigation
with st.sidebar:
    st.page_link("pages/1_Closet.py", label="👚 My Closet")
    st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
    st.page_link("pages/3_History.py", label="📸 Outfit History")
    st.page_link("app.py", label="🔙 Logout")

# 🔙 Back button to dashboard (optional but useful)
st.markdown("### 🧍 Customize Your Avatar")
if st.button("🔙 Back to Dashboard"):
    st.switch_page("app.py")  # Streamlit v1.30+ needed

username = st.session_state.get("username", "")

AVATAR_BASE = "https://avataaars.io/"
avatar_dir = "images/avatars"
os.makedirs(avatar_dir, exist_ok=True)

# Avatar customization options
skin_colors = ["Light", "Brown", "DarkBrown", "Black", "Yellow", "Pale"]
top_types = ["ShortHairShortFlat", "LongHairStraight", "Hat", "Hijab", "Eyepatch", "NoHair"]
hair_colors = ["Brown", "Black", "Blonde", "Red"]
eye_types = ["Default", "Happy", "Squint", "Surprised", "Wink"]
mouth_types = ["Smile", "Serious", "Twinkle", "Sad"]
accessories = ["Blank", "Round", "Sunglasses", "Prescription01", "Kurt"]

st.write("### 🎨 Customize Your Avatar")

# Pick options
skin = st.selectbox("Skin Color", skin_colors)
top = st.selectbox("Top Type", top_types)
hair = st.selectbox("Hair Color", hair_colors)
eyes = st.selectbox("Eye Type", eye_types)
mouth = st.selectbox("Mouth Type", mouth_types)
accessory = st.selectbox("Accessories", accessories)

# Generate avatar URL
params = {
    "avatarStyle": "Transparent",
    "skinColor": skin,
    "topType": top,
    "hairColor": hair,
    "eyeType": eyes,
    "mouthType": mouth,
    "accessoriesType": accessory
}
avatar_url = f"{AVATAR_BASE}?{urllib.parse.urlencode(params)}"

st.write("### 🖼️ Avatar Preview")
st.image(avatar_url, width=250,caption="Your Avatar")
st.code(avatar_url, language="markdown")

# Save avatar
if st.button("✅ Save Avatar"):
    try:
        response = requests.get(avatar_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        avatar_path = os.path.join(avatar_dir, f"{username}_avatar.png")
        img.save(avatar_path)
        st.success("Avatar saved successfully!")

        # Update user_data.csv
        df = pd.read_csv("user_data.csv")
        if "avatar_url" not in df.columns:
            df["avatar_url"] = ""

        df.loc[df["username"] == username, "avatar_url"] = avatar_url
        df.to_csv("user_data.csv", index=False)

    except Exception as e:
        st.error(f"Failed to save avatar: {e}")
