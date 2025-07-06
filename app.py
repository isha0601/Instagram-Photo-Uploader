import streamlit as st
from instagrapi import Client
import os
import json
from io import BytesIO
from PIL import Image

SESSION_FILE = "ig_session.json"

# ---- Streamlit page config ----
st.set_page_config(page_title="Instagram Photo Uploader Pro", page_icon="✨")

st.title("📸 Instagram Photo Uploader Pro")

# ---- IG Credentials ----
st.sidebar.header("Login")

username = st.sidebar.text_input("Instagram Username")
password = st.sidebar.text_input("Instagram Password", type="password")

# ---- Image upload ----
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Preview", use_column_width=True)

caption = st.text_area("Write your caption here:")

# ---- Hashtag Suggestion ----
if st.button("Suggest Hashtags"):
    if caption:
        # Dummy hashtag generator — can replace with real trending data later
        keywords = ["travel", "food", "nature", "selfie", "fun", "coding"]
        suggested = [f"#{kw}" for kw in keywords if kw in caption.lower()]
        st.write("Suggested Hashtags:", " ".join(suggested) or "#awesome #instagood")
    else:
        st.warning("Write a caption first!")

# ---- Post Button ----
if st.button("Post to Instagram"):
    if not username or not password:
        st.warning("Please enter your Instagram credentials.")
    elif not uploaded_file:
        st.warning("Please upload an image.")
    elif not caption:
        st.warning("Please write a caption.")
    else:
        with st.spinner("Logging in and posting..."):
            try:
                cl = Client()

                # Try to reuse session
                if os.path.exists(SESSION_FILE):
                    cl.load_settings(SESSION_FILE)

                cl.login(username, password)

                # Save session for next time
                cl.dump_settings(SESSION_FILE)

                temp_file = f"temp_{uploaded_file.name}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                media = cl.photo_upload(temp_file, caption)

                os.remove(temp_file)

                st.success(f"✅ Posted successfully! Media ID: {media.dict().get('id')}")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
