#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import speech_recognition as sr
import pyttsx3
import language_tool_python
from textblob import TextBlob

# Initialize NLP tools
recognizer = sr.Recognizer()
tool = language_tool_python.LanguageToolPublicAPI('en-US')
tts_engine = pyttsx3.init()

def analyze_text(text):
    matches = tool.check(text)
    corrections = [match.message for match in matches]
    sentiment = TextBlob(text).sentiment
    return corrections, sentiment

def speak_response(response):
    tts_engine.say(response)
    tts_engine.runAndWait()

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
        speak_response(response)
    except Exception as e:
        st.error("Could not recognize speech. Please try again.")


# In[ ]:




