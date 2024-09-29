import os
from flask import Flask, request, render_template
import whisper

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():

    if 'audioFile' not in request.files:
        return "No file uploaded", 400
    
    audio_file = request.files['audioFile']

    if audio_file.filename == '':
        return "No file selected", 400

    # Save the file in the current working directory
    upload_folder = os.path.join(os.getcwd(), 'uploads')  # Create uploads folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    audio_path = os.path.join(upload_folder, audio_file.filename)
    
    audio_file.save(audio_path)

    # Load the Whisper model and transcribe
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="ar")
    transcription = result['text']

    return render_template('transcription.html', transcription=transcription)

if __name__ == '__main__':
    app.run(debug=True)
