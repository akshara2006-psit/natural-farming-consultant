import google.generativeai as genai
import streamlit as st

# Load key from your secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    print("--- AVAILABLE MODELS FOR YOUR KEY ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")