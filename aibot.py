#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import language_tool_python
from textblob import TextBlob
from pydub import AudioSegment
import ffmpeg
import shutil

#  Ensure ffmpeg is available
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path:
    AudioSegment.converter = ffmpeg_path
else:
    raise FileNotFoundError("FFmpeg not found! Ensure it's installed properly.")

# NLP Tools
recognizer = sr.Recognizer()
tool = language_tool_python.LanguageToolPublicAPI('en-US')

# Function to analyze text for improvements
def analyze_text(text):
    matches = tool.check(text)
    corrections = [match.message for match in matches]
    sentiment = TextBlob(text).sentiment
    return corrections, sentiment

#Function to generate AI audio response
def generate_audio(response_text):
    tts = gTTS(text=response_text, lang="en")
    audio_path = "response.mp3"
    tts.save(audio_path)
    return audio_path

# Streamlit UI
st.title("🎙 AI Chatbot for Tone & Language Improvement")
st.write("Upload an audio file, and get AI feedback on your tone and language!")

uploaded_file = st.file_uploader("📂 Upload an audio file (MP3/WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    audio_path = "uploaded_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Convert to WAV if needed
    audio = AudioSegment.from_file(audio_path)
    audio.export("converted_audio.wav", format="wav")

    with sr.AudioFile("converted_audio.wav") as source:
        st.write("🔄 Processing...")
        audio_data = recognizer.record(source)

    try:
        spoken_text = recognizer.recognize_google(audio_data)
        st.write("🗣 You said:", spoken_text)

        #  Get grammar corrections & sentiment analysis
        corrections, sentiment = analyze_text(spoken_text)

        response = ""
        if corrections:
            response += "📝 I noticed some improvements you can make:\n" + "\n".join(corrections)
        else:
            response += "✅ Your speech was clear and grammatically correct."

        response += f"\n📊 Sentiment Polarity: {sentiment.polarity:.2f}, Subjectivity: {sentiment.subjectivity:.2f}"

        st.write(response)

        # ✅ Generate & play AI voice response
        audio_file = generate_audio(response)
        st.audio(audio_file, format="audio/mp3")

    except Exception as e:
        st.error("❌ Could not recognize speech. Please try again.")







