#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import language_tool_python
from textblob import TextBlob

# Initialize NLP tools
recognizer = sr.Recognizer()
tool = language_tool_python.LanguageToolPublicAPI('en-US')

def analyze_text(text):
    matches = tool.check(text)
    corrections = [match.message for match in matches]
    sentiment = TextBlob(text).sentiment
    return corrections, sentiment

def generate_audio(response_text):
    tts = gTTS(text=response_text, lang="en")
    tts.save("response.mp3")
    return "response.mp3"

st.title("AI Chatbot for Tone & Language Improvement")
st.write("Speak into the microphone and get feedback on tone and language!")

if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        spoken_text = recognizer.recognize_google(audio)
        st.write("You said:", spoken_text)

        corrections, sentiment = analyze_text(spoken_text)

        response = ""
        if corrections:
            response += "I noticed some improvements you can make:\n" + "\n".join(corrections)
        else:
            response += "Your speech was clear and grammatically correct."

        response += f"\nSentiment Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}"

        st.write(response)

        # Generate and play response audio
        audio_file = generate_audio(response)
        st.audio(audio_file, format="audio/mp3")

    except Exception as e:
        st.error("Could not recognize speech. Please try again.")





