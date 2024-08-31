import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from tempfile import NamedTemporaryFile
import requests
from io import BytesIO
from pytube import YouTube

# Title
st.title('Object Detector')

upload_option = st.radio("Choose an option:", ("Upload File", "Paste Link"))

if upload_option == "Upload File":
    upload_type = st.radio("Choose upload type:", ("Image", "Video"))

    if upload_type == "Image":
        uploaded_file = st.file_uploader(label='Upload image here', type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", use_column_width=True)

    elif upload_type == "Video":
        uploaded_file = st.file_uploader(label='Upload video here', type=['mp4', 'mov'])
        if uploaded_file:
            tfile = NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())

            vid = cv2.VideoCapture(tfile.name)

            st.write("Uploaded Video")
            stframe = st.empty()

            while vid.isOpened():
                ret, frame = vid.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame)

            vid.release()

elif upload_option == "Paste Link":
    link = st.text_input("Paste image or video link here")
    if link:
        try:
            response = requests.get(link)
            response.raise_for_status() 

            content_type = response.headers.get('content-type')

            if 'image' in content_type:
                img = Image.open(BytesIO(response.content))
                st.image(img, caption="Image from Link", use_column_width=True)

            elif 'video' in content_type:
                if not any(ext in link for ext in ['.mp4', '.mov', '.avi']):
                    st.error("Unsupported video format. Please provide a direct link to an MP4, MOV, or AVI video.")
                else:
                    st.write("Video from Link (implementation needed)")

            elif "youtube.com" in link or "youtu.be" in link:
                try:
                    yt = YouTube(link)
                    stream = yt.streams.get_highest_resolution()

                    with NamedTemporaryFile(delete=False) as tfile:
                        stream.download(output_path="", filename=tfile.name)
                        video_path = tfile.name

                    vid = cv2.VideoCapture(video_path)
                    st.write("Video from YouTube")
                    stframe = st.empty()

                    while vid.isOpened():
                        ret, frame = vid.read()
                        if not ret:
                            print("Can't receive frame (stream end?). Exiting ...")
                            break
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        stframe.image(frame)

                    vid.release()

                except Exception as e:
                    st.error(f"Error processing YouTube video: {e}")

            else:
                st.error("Invalid link. Please provide a valid image or video link.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching content: {e}")