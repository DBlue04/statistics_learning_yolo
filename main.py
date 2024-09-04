import streamlit as st
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import supervision as sv
from ultralytics import YOLO

# Dashboard
st.title('Object Detector')
upload = st.sidebar.file_uploader(label='Upload image here', type=['png', 'jpg', 'jpeg'])

# Cache the model to ensure it loads only once
@st.cache_resource(show_spinner=False)
def load_model():
    return YOLO('yolov10l.pt')

model = load_model()

if upload:
    st.sidebar.image(upload, caption='Uploaded image')
    file_bytes = np.asarray(bytearray(upload.read()), dtype=np.uint8)
    image = cv.imdecode(file_bytes, 1)

    # Button to start the detection process
    if st.sidebar.button('Start Detection'):
        with st.spinner('Detecting...'):
            results = model.predict(source=image, imgsz=416)
            annotated_image = results[0].plot()

            # Ensure the image is converted correctly to RGB
            annotated_image = cv.cvtColor(annotated_image, cv.COLOR_BGR2RGB)

            # Display the annotated image
            st.image(annotated_image, use_column_width=True)
            
            # Display metrics
            st.write("Precision:")
