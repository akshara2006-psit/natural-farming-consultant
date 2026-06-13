import streamlit as st
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
from data_utils import get_weather, get_market_prices
from farming_logic import query_farming_expert


try:
    api_keys = {
        "gemini": st.secrets["GEMINI_API_KEY"],
        "weather": st.secrets["WEATHER_API_KEY"],
        "groq": st.secrets["GROQ_API_KEY"]
    }
except Exception:
    st.error("Secrets not found! Check .streamlit/secrets.toml")
    st.stop()


st.set_page_config(page_title="Natural Farming AI", page_icon="🌱")
st.markdown("<style>.stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; }</style>", unsafe_allow_html=True)

st.title("🌱 Natural Farming Consultant")


with st.sidebar:
    st.header("📍 Dashboard")
    city = st.text_input("Enter City", value="Lucknow")
    
   
    w_info = get_weather(city, api_keys["weather"])
    m_info = get_market_prices(city)

   
    st.metric("Temperature", f"{w_info['temp']}°C", delta=w_info['desc'])
    st.subheader("📊 Mandi Prices")
    for crop, price in m_info.items():
        st.write(f"**{crop}**: ₹{price}/q")


tab1, tab2 = st.tabs(["🎙️ ASK BY VOICE", "📸 DISEASE IDENTIFIER"])

with tab1:
    audio = mic_recorder(start_prompt="Speak Now 🎙️", stop_prompt="Stop ⏹️", key='recorder')

with tab2:
    img_file = st.camera_input("Scan Crop")


with st.expander("🔄 Multilevel Cropping Advice"):
    st.write("Suggested: Layer 1: Papaya | Layer 2: Turmeric | Layer 3: Ginger")


if (audio or img_file):
    with st.spinner("AI soch raha hai..."):
        audio_bits = audio['bytes'] if audio else None
        
        response_text, transcribed_text = query_farming_expert(api_keys, audio_bits, img_file, w_info, m_info)
        
        if transcribed_text and transcribed_text != "Image Analysis":
            st.info(f"👂 What I heard: {transcribed_text}")
        
        
        st.subheader("Consultant's Advice:")
        st.success(response_text) 

   
        try:
            
            clean_voice_text = response_text.replace("*", "").replace("#", "")
            
            lang = 'hi' if any('\u0900' <= c <= '\u097F' for c in clean_voice_text) else 'en'
            
            if clean_voice_text.strip():
              
                tts = gTTS(text=clean_voice_text, lang=lang) 
                speech_fp = io.BytesIO()
                tts.write_to_fp(speech_fp)
                
               
                st.audio(speech_fp, format='audio/mp3', autoplay=True)
        except Exception as e:
           
            st.error(f"Awaaz mein samasya: {e}")
    