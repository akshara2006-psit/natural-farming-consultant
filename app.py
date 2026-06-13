import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
from data_utils import get_weather, get_market_prices
from farming_logic import query_farming_expert

# 1. SECURE KEY RETRIEVAL
try:
    api_keys = {
        "gemini": st.secrets["GEMINI_API_KEY"],
        "weather": st.secrets["WEATHER_API_KEY"],
        "groq": st.secrets["GROQ_API_KEY"]
    }
except Exception:
    st.error("Secrets not found! Check .streamlit/secrets.toml")
    st.stop()

# --- UI STYLING ---
st.set_page_config(page_title="Natural Farming AI", page_icon="🌱")
st.markdown("<style>.stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; }</style>", unsafe_allow_html=True)

st.title("🌱 Natural Farming Consultant")

# --- SIDEBAR (Smart Dashboard) ---
with st.sidebar:
    st.header("📍 Dashboard")
    city = st.text_input("Enter City", value="Lucknow")
    
    # FETCH DATA
    w_info = get_weather(city, api_keys["weather"])
    m_info = get_market_prices(city)

    # DISPLAY METRICS
    st.metric("Temperature", f"{w_info['temp']}°C", delta=w_info['desc'])
    st.subheader("📊 Mandi Prices")
    for crop, price in m_info.items():
        st.write(f"**{crop}**: ₹{price}/q")

# --- MAIN INTERFACE ---
tab1, tab2 = st.tabs(["🎙️ ASK BY VOICE", "📸 DISEASE IDENTIFIER"])

with tab1:
    audio = mic_recorder(start_prompt="Speak Now 🎙️", stop_prompt="Stop ⏹️", key='recorder')

with tab2:
    img_file = st.camera_input("Scan Crop")

# --- CROP ROTATION (Extra Requirement) ---
with st.expander("🔄 Multilevel Cropping Advice"):
    st.write("Suggested: Layer 1: Papaya | Layer 2: Turmeric | Layer 3: Ginger")

# --- PROCESSING ---

# --- PROCESSING LOGIC ---
# --- PROCESSING LOGIC (Around line 55 in your file) ---
# --- app.py ke andar PROCESSING block mein ---

if (audio or img_file):
    with st.spinner("AI soch raha hai..."):
        audio_bits = audio['bytes'] if audio else None
        response_text, transcribed_text = query_farming_expert(api_keys, audio_bits, img_file, w_info, m_info)
        
        if transcribed_text and transcribed_text != "Image Analysis":
            st.info(f"👂 What I heard: {transcribed_text}")
        
        st.subheader("Consultant's Advice:")
        st.success(response_text) # Yahan text bold dikhega (Markdown support)
        
        # --- VOICE CLEANUP START ---
        # Voice ke liye asterisks (*) ko hata dete hain taaki wo "star" na bole
        clean_voice_text = response_text.replace("*", "") 
        # --- VOICE CLEANUP END ---

        try:
            lang = 'hi' if any('\u0900' <= c <= '\u097F' for c in response_text) else 'en'
            # CLEAN text use kijiye voice ke liye
            tts = gTTS(text=clean_voice_text, lang=lang) 
            speech_fp = io.BytesIO()
            tts.write_to_fp(speech_fp)
            st.audio(speech_fp, format='audio/mp3', autoplay=True)
        except:
            pass