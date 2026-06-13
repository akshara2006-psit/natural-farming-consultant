from google import genai
from google.genai import types
from groq import Groq
import io



def query_farming_expert(api_keys, audio_bytes, image_file, weather_data, market_data):
    groq_client = Groq(api_key=api_keys['groq'])
    
    
    w_ctx = f"{weather_data['temp']}°C, {weather_data['desc']}"
    m_ctx = ", ".join([f"{k}: ₹{v}" for k, v in market_data.items()])

 
    user_query = ""
    if audio_bytes:
        try:
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "input.wav"
            user_query = groq_client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="text"
            )
        except:
            user_query = ""

    
    system_prompt = f"""
You are an expert Natural Farming Consultant.
Respond ONLY in Hindi (Devanagari script).

FORMATTING RULES:
1. Use very few asterisks. Only bold the most important words.
2. Do not use complex markdown symbols.
3. Use simple bullet points (•) for steps.
4. If you see an image, identify the disease and give a natural cure in Hindi.

Context: Weather {w_ctx}, Market {m_ctx}.
"""


    if image_file:
        client = genai.Client(api_key=api_keys['gemini'])
        model_options = ["gemini-flash-lite-latest", "gemini-3.1-flash-lite", "gemini-flash-latest"]
        
        for model_id in model_options:
            try:
                
                response = client.models.generate_content(
                    model=model_id,
                    contents=[
                        system_prompt,
                        "Kripya is photo ko dekhein aur bimari ka upchaar HINDI mein batayein:", 
                        types.Part.from_bytes(data=image_file.getvalue(), mime_type="image/jpeg")
                    ]
                )
                return response.text, "Image Analysis"
            except Exception as e:
                if "429" in str(e): continue
                else: return f"Error: {str(e)}", "Image Analysis"
        
        return "Shama karein, AI abhi vyast hai. Neem ka tel use karein.", "Image Analysis"


    else:
        try:
            groq_client = Groq(api_key=api_keys['groq'])
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}],
                temperature=0.2
            )
            return completion.choices[0].message.content, user_query
        except:
            return "AI Expert is busy. Please use Jeevamrutham for soil health.", "General Query"