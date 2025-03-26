from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename

import os

from genai import genai_analysis

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            files.append(filename)
            print(filename)
    files.sort(reverse=True)
    return files

@app.route('/')
def index():
    files = get_files()
    print(files)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_data' not in request.files:
        flash('No audio data')
        return redirect(request.url)
    file = request.files['audio_data']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        # filename = secure_filename(file.filename)
        filename = datetime.now().strftime("%Y%m%d-%I%M%S%p") + '.wav'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(file_path)

        #
        #
        # Modify this block to call the speech to text API
        # Save transcript to same filename but .txt
        #
        #

        # Calling the goole generative AI API using the function from our external file
        genai_analysis(filename = file_path)

    return redirect('/') #success

@app.route('/upload/<filename>')
def get_file(filename):
    return send_file(filename)

    
# @app.route('/upload_text', methods=['POST'])
# def upload_text():
#     text = request.form['text']
#     print(text)
#     #
#     #
#     # Modify this block to call the stext to speech API
#     # Save the output as a audio file in the 'tts' directory 
#     # Display the audio files at the bottom and allow the user to listen to them
#     #

#     # Creating the audio file 
#     filename = datetime.now().strftime("%Y%m%d-%I%M%S%p") + '.wav'
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#     # Calling the Text to Speech API using the function of our external file
#     text_to_speech(text=text, speech_file_path= file_path)

#     # Saving the text file
#     text_file_path = file_path + '.txt'
#     file = open(text_file_path, "a")
#     file.write(text)
#     file.close()

#     # Saving the sentiment text file
#     sentiment_file_path = file_path + '_sentiment.txt'
#     file_sentiment = open(sentiment_file_path, "w")
#     file_sentiment.write("Sentiment Type: " + sentiment_type(text))
#     file_sentiment.close() 

#     return redirect('/') #success

@app.route('/script.js',methods=['GET'])
def scripts_js():
    return send_file('./script.js')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
