from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized:", text)

        target_lang = request.form['language']

        translated = translator.translate(text, dest=target_lang)

        tts = gTTS(translated.text, lang=target_lang)
        audio_file = "static/output.mp3"
        tts.save(audio_file)

        return jsonify({
            "original": text,
            "translated": translated.text,
            "audio": audio_file
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
