import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt


#Dashboard
st.title('Object Detector')
upload = st.file_uploader(label='Upload image here', type=['png','jpg', 'jpeg'])

if upload:
    img = Image.open(upload)
    