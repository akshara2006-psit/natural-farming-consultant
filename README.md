

#  Kisan-Mitra: Multilevel Natural Farming AI Consultant
### *Empowering the transition to chemical-free agriculture through Voice-First Intelligence.*


##  Project Vision
Transitioning from chemical to **Natural Farming (ZBNF/KNF)** is a high-risk journey for farmers. Lack of immediate guidance during pest attacks often leads them back to harmful chemicals. **Kisan-Mitra** (Farmer's Friend) provides a voice-first, multi-modal AI consultant that delivers instant, organic solutions based on real-time weather, market trends, and visual crop diagnostics.



##  Core Features (Selected Requirements)

### 1.  Voice-First Natural Farming Education
*   **The Problem:** Farmers in the field cannot type complex queries.
*   **The Solution:** Integrated **Groq Whisper-v3** for ultra-fast Speech-to-Text (STT) and **gTTS** for localized voice feedback.
*   **Intelligence:** Explains multilevel cropping strategies and organic sowing techniques (e.g., **Beejamrutham**) in the farmer's native language.

### 2.  AI Disease Identification (Vision)
*   **The Problem:** Delayed pest identification ruins entire harvests.
*   **The Solution:** Leveraging **Gemini 2.0 Flash Lite** to analyze crop photos.
*   **Organic Guardrails:** The AI strictly identifies organic remedies (e.g., **Neem Astra**, **Dashaparni Ark**) and refuses to recommend synthetic pesticides.

### 3.  Real-Time Weather & Mandi Intelligence
*   **Weather-Aware Advice:** Fetches live data via **OpenWeatherMap API**. If it's 38°C, the AI proactively suggests mulching to retain moisture.
*   **Dynamic Market Intelligence:** Simulates live Mandi fluctuations based on real 2024-25 MSP data, helping farmers decide whether to sell or store their harvest.

---

##  Technical Excellence (Evaluation: 40%)
To ensure high performance and reliability, I implemented a **Hybrid Multi-Model Architecture**:

| Component | Technology | Why? |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Responsive UI optimized for "Smart Boards" and mobile. |
| **Logic/Voice** | **Groq (Llama 3.3 70B)** | 5x faster than GPT-4; provides instant "Voice-to-Voice" feel. |
| **Transcription**| **Whisper-v3 (via Groq)** | Industry-leading accuracy in noisy farm environments. |
| **Vision** | **Gemini 2.0 Flash Lite** | State-of-the-art botanical image analysis. |
| **APIs** | OpenWeather & Mandi Engine | Dynamic data prevents "Static Content" fatigue. |

---

##  AI Prompt Design & Guardrails (Evaluation: 30%)
The system utilizes **Strict Prompt Engineering** to ensure agricultural safety:
*   **Negative Constraints:** The model is strictly forbidden from suggesting Urea, DAP, or chemical fungicides.
*   **Contextual Injection:** Every AI response is automatically "injected" with local weather and market data, making the advice hyper-local.
*   **Formatting for Mobile:** The AI is instructed to use **bullet points (•)** and **bold text** for key ingredients, ensuring readability on small screens.

---

##  Empathy & UX (Evaluation: 30%)
*   **Multilingual by Default:** The app automatically detects Hindi vs. English speech and responds in the same language.
*   **Low-Literacy Friendly:** Large buttons, high-contrast icons, and voice-autoplay ensure that the app is usable by all farmers.
*   **Smart Dashboard:** Uses `st.metric` cards to provide a "cockpit" view of the farm's environment at a glance.

---

##  Installation & Setup

1. **Clone the Project:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kisan-mitra.git
   cd kisan-mitra
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Secrets:**
   Create `.streamlit/secrets.toml` (Local only):
   ```toml
   GEMINI_API_KEY = "your_key"
   GROQ_API_KEY = "your_key"
   WEATHER_API_KEY = "your_key"
   ```

4. **Run App:**
   ```bash
   python -m streamlit run app.py
   ```

---


