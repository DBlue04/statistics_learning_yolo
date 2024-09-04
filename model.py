# Download pre-trained model

import os
import urllib.request

# Define the current directory as the destination
current_dir = os.getcwd()

# URL of the file to download
url = "https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10l.pt"

# Define the file path to save the downloaded file
file_path = os.path.join(current_dir, "yolov10l.pt")

# Download the file
urllib.request.urlretrieve(url, file_path)

print(f"Downloaded {file_path}")