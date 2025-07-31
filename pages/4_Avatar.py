import streamlit as st
import urllib.parse
import pandas as pd
import os

AVATAR_BASE = "https://avataaars.io/"

st.set_page_config(page_title="Customize Avatar", page_icon="🧑‍🎨", layout="centered")

# Sidebar Navigation
with st.sidebar:
    st.page_link("pages/1_Closet.py", label="👚 My Closet")
    st.page_link("pages/2_create_your_fit.py", label="🧠 Create Your Fit")
    st.page_link("pages/3_History.py", label="📸 Outfit History")
    st.page_link("pages/4_Avatar.py", label="🧑‍🎨 Customize Avatar")
    st.page_link("app.py", label="🏠 Home")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("app.py")

# Avatar Options
st.title("🧑‍🎨 Create Your Avatar")
st.write("Customize your avatar below:")

username = st.session_state.get("username", "")

skin = st.selectbox("Skin Color", ["Light", "Brown", "DarkBrown", "Black"])
hair = st.selectbox("Hair Style", ["ShortHairShortFlat", "LongHairStraight", "ShortHairDreads01", "Hat"])
hair_color = st.selectbox("Hair Color", ["Black", "Brown", "Blonde", "Red"])
eye = st.selectbox("Eye Type", ["Default", "Happy", "Squint", "Wink"])
mouth = st.selectbox("Mouth Type", ["Smile", "Serious", "Disbelief", "Twinkle"])
accessories = st.selectbox("Accessories", ["Blank", "Prescription01", "Round", "Kurt"])

# Create avatar URL
params = {
    "avatarStyle": "Circle",
    "skinColor": skin,
    "topType": hair,
    "hairColor": hair_color,
    "eyeType": eye,
    "mouthType": mouth,
    "accessoriesType": accessories
}
avatar_url = f"{AVATAR_BASE}?{urllib.parse.urlencode(params)}"

st.image(avatar_url, caption="Your Avatar", use_container_width=150)


if st.button("Save Avatar"):
    try:
        avatar_df = pd.DataFrame([{
            "username": username,
            "avatar_url": avatar_url
        }])
        file_exists = os.path.isfile("avatar_data.csv")
        if file_exists:
            all_avatars = pd.read_csv("avatar_data.csv")
            all_avatars = all_avatars[all_avatars["username"] != username]
            all_avatars = pd.concat([all_avatars, avatar_df], ignore_index=True)
            all_avatars.to_csv("avatar_data.csv", index=False)
        else:
            avatar_df.to_csv("avatar_data.csv", index=False)

        st.success("Avatar saved successfully!")
    except Exception as e:
        st.error(f"Failed to save avatar URL: {e}")
