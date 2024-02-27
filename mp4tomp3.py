from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

UPLOADS_DIR = 'uploads'

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def process_video(file_path):
    # Paths for the processed files
    video_no_audio_path = os.path.join(UPLOADS_DIR, 'video_no_audio.mp4')
    audio_path = os.path.join(UPLOADS_DIR, 'audio.mp3')

    # Remove audio from the video
    subprocess.call(['ffmpeg', '-i', file_path, '-an', video_no_audio_path])

    # Extract audio from the video
    subprocess.call(['ffmpeg', '-i', file_path, audio_path])

    return video_no_audio_path, audio_path

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.mp4'):
        # Save the uploaded file temporarily
        temp_path = os.path.join(UPLOADS_DIR, 'temp_' + file.filename)
        file.save(temp_path)

        # Process the video: remove audio and extract audio
        video_no_audio_path, audio_path = process_video(temp_path)

        # Optionally, delete the temporary file after processing
        os.remove(temp_path)

        return jsonify({
            'message': 'Video processed successfully',
            'video_no_audio_path': video_no_audio_path,
            'audio_path': audio_path
        }), 200
    else:
        return jsonify({'error': 'Unsupported file format'}), 400


if __name__ == '__main__':
    app.run(debug=True)
