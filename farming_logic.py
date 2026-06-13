from google import genai
from google.genai import types
from groq import Groq
import io

def query_farming_expert(api_keys, audio_bytes, image_file, weather_data, market_data):
    groq_client = Groq(api_key=api_keys['groq'])
    
    # Context data for the AI
    w_ctx = f"{weather_data['temp']}°C, {weather_data['desc']}"
    m_ctx = ", ".join([f"{k}: ₹{v}" for k, v in market_data.items()])

    # 1. Transcription (Voice to Text)
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
        except Exception as e:
            user_query = "Audio recording error."

    if not user_query and not image_file:
        return "I didn't hear a question. Please click the mic and speak clearly.", ""

    # 2. UPDATED SYSTEM PROMPT WITH FORMATTING RULES
    system_prompt = f"""
    You are an expert Natural Farming Consultant.
    
    FARMER'S QUESTION: "{user_query}"
    
    CONTEXT:
    - Weather: {w_ctx}
    - Market Prices: {m_ctx}

    INSTRUCTIONS:
    1. Only suggest natural/organic farming (Jeevamrutham, Neem Astra, etc.).
    2. Answer the farmer's question directly. 
    
    FORMATTING RULES (IMPORTANT FOR MOBILE):
    - Use bullet points (•) for any steps, ingredients, or lists.
    - Use **bold text** for key organic terms (e.g., **Jeevamrutham**, **Bijamrutham**).
    - Keep paragraphs short and use simple language.
    - Respond in the language the farmer used (Hindi or English).
    """

    # 3. Generate AI Response
    try:
        if image_file:
            # Gemini for Vision
            gemini_client = genai.Client(api_key=api_keys['gemini'])
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=[system_prompt, types.Part.from_bytes(data=image_file.getvalue(), mime_type="image/jpeg")]
            )
            return response.text, "Image Analysis"
        else:
            # Groq for Voice
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.2
            )
            return completion.choices[0].message.content, user_query
            
    except Exception as e:
        return f"AI Error: {str(e)}", user_query