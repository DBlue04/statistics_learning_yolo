import streamlit as st
import cv2 as cv
import numpy as np
import supervision as sv
from tempfile import NamedTemporaryFile
from ultralytics import YOLOv10

# Dashboard
st.title('Object Detector and Tracker')

# @st.cache_resource(show_spinner=False)
# # def load_model():
# #     return YOLO('yolov10l.pt')

model = YOLOv10('runs/detect/train/weights/best.pt')

with open("evaluation.txt", "r") as f:
    evaluation_metrics = f.read()

st.write("### Model Evaluation Metrics")
st.text(evaluation_metrics)

def process_and_display(img, is_video=False):
    results = model(source=img, conf=0.05)[0]
    detections = sv.Detections.from_ultralytics(results)

    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    annotated_img = bounding_box_annotator.annotate(scene=img, detections=detections)
    annotated_img = label_annotator.annotate(scene=annotated_img, detections=detections)

    return annotated_img

upload_type = st.sidebar.radio("Choose input type:", ("Upload Image", "Upload Video", "Live Track"))

if upload_type == "Upload Image":
    upload = st.sidebar.file_uploader(label='Upload image here', type=['png', 'jpg', 'jpeg'])
    if upload:
        st.sidebar.image(upload, caption='Uploaded image')
        file_bytes = np.asarray(bytearray(upload.read()), dtype=np.uint8)
        image = cv.imdecode(file_bytes, 1)

        if st.sidebar.button('Start Detection'):
            with st.spinner('Detecting...'):
                annotated_image = process_and_display(image)
                annotated_image = cv.cvtColor(annotated_image, cv.COLOR_BGR2RGB)
                st.image(annotated_image, use_column_width=True)

elif upload_type == "Upload Video":
    uploaded_file = st.sidebar.file_uploader(label='Upload video here', type=['mp4', 'mov'])
    if uploaded_file:
        st.sidebar.video(uploaded_file)
        tfile = NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        if st.sidebar.button('Start Detection'):
            vid = cv.VideoCapture(tfile.name)
            stframe = st.empty()

            while vid.isOpened():
                ret, frame = vid.read()
                if not ret:
                    break
                annotated_frame = process_and_display(frame, is_video=True)
                stframe.image(annotated_frame)

            vid.release()

elif upload_type == "Live Track":
    st.write("### Live Object Tracking with YOLOv10")

    if "recording" not in st.session_state:
        st.session_state.recording = False
    if "frames" not in st.session_state:
        st.session_state.frames = []
    if "cap" not in st.session_state:
        st.session_state.cap = None

    if st.session_state.recording:
        if st.sidebar.button('Stop Recording', key='stop_recording'):
            st.session_state.recording = False
            st.sidebar.write("Recording stopped.")
            if st.session_state.cap is not None:
                st.session_state.cap.release()  
                st.session_state.cap = None
                st.session_state.frames = []  
    else:
        if st.sidebar.button('Start Recording', key='start_recording'):
            st.session_state.recording = True
            st.sidebar.write("Recording started.")
            st.session_state.cap = cv.VideoCapture(0)  
            st.session_state.frames = []  

    if st.session_state.recording and st.session_state.cap is not None:
        if st.session_state.cap.isOpened():
            stframe = st.empty()
            while st.session_state.recording:
                ret, frame = st.session_state.cap.read()
                if not ret:
                    st.write("Error: Failed to capture frame from webcam.")
                    break
                annotated_frame = process_and_display(frame)
                stframe.image(annotated_frame, channels="RGB", use_column_width=True)
                st.session_state.frames.append(frame)
        else:
            st.write("Error: Could not access the webcam.")

    if not st.session_state.recording and st.session_state.cap is None and st.session_state.frames:
        st.session_state.frames = []  # Clear frames after processing

