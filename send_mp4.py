import requests

import os

# Define the directory path
directory = 'uploads'

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

def send_mp4(file_path, endpoint):
    url = f"http://{endpoint}/upload"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    return response

if __name__ == "__main__":
    file_path = "./video/test_file.mp4"  # Replace this with the path to your MP4 video file
    endpoint = "127.0.0.1:5000"  # Replace this with the IP address and port where your microservice is running
    response = send_mp4(file_path, endpoint)
    print(response.text)
