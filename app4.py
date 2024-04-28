import streamlit as st
import speech_recognition as sr # type: ignore
from googletrans import Translator # type: ignore
from gtts import gTTS
import tempfile
import os
import base64
# import pyaudio



# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio, language="en-US")
            st.write("You said:", text)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, could not understand audio.")
            return ""
        except sr.RequestError as e:
            st.error("Error fetching results; {0}".format(e))
            return ""

# Function to translate text
def translate_text(text, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=dest_lang)
    return translated_text.text

# Function to convert text to Hindi speech
def text_to_hindi_speech(text):
    tts = gTTS(text, lang='hi')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file_path = temp_file.name
        tts.save(temp_file_path)
    return temp_file_path

def main():
    st.title("Speech Translator")

    # Language selection dropdown
    dest_lang = st.selectbox("Select Destination Language", ["Hindi", "Spanish", "French"])

    if st.button("Start Recording"):
        speech_text = recognize_speech()
        if speech_text:
            st.write("Translated text:")
            translated_text = translate_text(speech_text, dest_lang.lower())
            st.write(translated_text)
            st.write("Speaking translated text...")
            wav_file = text_to_hindi_speech(translated_text)
            st.audio(wav_file, format='audio/wav', start_time=0)
            st.markdown(get_binary_file_downloader_html(wav_file, 'Download Translated Speech'), unsafe_allow_html=True)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href

if __name__ == "__main__":
    main()
