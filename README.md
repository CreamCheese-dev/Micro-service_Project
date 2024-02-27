Communication Contract

Requesting Data
To request data processing (i.e., video processing) from the microservice, you'll need to send a POST request with the MP4 file. Here's an example using Python's requests module:

```python
import requests

def send_video_for_processing(file_path):
    url = "http://127.0.0.1:5000/upload"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    return response.json()  # Assumes the response is in JSON format

# Example usage
file_path = "path/to/your/video.mp4"
response = send_video_for_processing(file_path)
print(response)

```


Receiving Data
Upon successful processing, the microservice will return a JSON response containing paths to the processed video file (without audio) and the extracted audio file. The response will look something like this:

    {
    "message": "Video processed successfully",
    "video_no_audio_path": "uploads/video_no_audio.mp4",
    "audio_path": "uploads/audio.mp3"
    }

Basic UML Sequence Diagram:
```
[Client] --POST /upload (MP4 file)--> [MP4TOMP3 Microservice]
[MP4TOMP3 Microservice] --Extract & Store--> [UPLOADS folder]
[musicPlayer Application] --Check & Play--> [End User]
