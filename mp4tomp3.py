from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

UPLOADS_DIR = 'uploads'

def remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.mp4'):
        # Save the uploaded file
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        file.save(file_path)

        # Extract audio from the video
        audio_path = os.path.join(UPLOADS_DIR, 'audio.mp3')
        subprocess.call(['ffmpeg', '-i', file_path, audio_path])

        # Remove audio from the video
        video_no_audio_path = os.path.join(UPLOADS_DIR, 'video_no_audio.mp4')
        subprocess.call(['ffmpeg', '-i', file_path, '-an', video_no_audio_path])

        # Return both file paths in the response
        response = jsonify({
            'message': 'Audio extracted and video with no audio created',
            'audio': audio_path,
            'video_no_audio': video_no_audio_path
        })

        return response, 200

    return jsonify({'error': 'Invalid file format, please upload an MP4 video'}), 400

if __name__ == '__main__':
    app.run(debug=True)
