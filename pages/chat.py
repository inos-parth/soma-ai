import streamlit as st
import google.generativeai as genai
import time
import requests

st.set_page_config(page_title="Sōma.ai - Chat", layout="centered")

# ---------------- Weather Context ----------------
def get_weather_summary():
    try:
        lat, lon = 40.7128, -74.0060  # NYC fallback
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url).json()
        temp = response["current_weather"]["temperature"]
        code = response["current_weather"]["weathercode"]
        condition_map = {
            0: "clear skies", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
            45: "foggy", 48: "misty", 51: "light drizzle", 61: "rain showers", 80: "heavy showers"
        }
        condition = condition_map.get(code, "some weather")
        return f"It's currently {temp}°C with {condition}."
    except:
        return "Weather information is currently unavailable."

# ---------------- Page Redirect Guard ----------------
if "philosopher" not in st.session_state:
    st.warning("No philosopher matched yet. Redirecting...")
    st.switch_page("pages/app.py")

philosopher = st.session_state.philosopher
explanation = st.session_state.explanation

# ---------------- Styles ----------------
st.markdown(f"""
<style>
.user-bubble {{
    background-color: #cce5ff;
    color: black;
    padding: 0.7em 1em;
    margin: 0.5em 0;
    border-radius: 12px;
    max-width: 80%;
    margin-left: auto;
    text-align: right;
}}
.bot-bubble {{
    background-color: #f0f0f0;
    color: black;
    padding: 0.7em 1em;
    margin: 0.5em 0;
    border-radius: 12px;
    max-width: 80%;
    margin-right: auto;
    text-align: left;
}}
.fade-cursor {{
    animation: blink 1s steps(2, start) infinite;
    font-weight: bold;
}}
@keyframes blink {{
    to {{ visibility: hidden; }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.subheader(f"💬 Chat with {philosopher}")
if st.button("🔁 Go Back to Reflection"):
    st.switch_page("pages/app.py")

with st.expander("🔍 Why this philosopher?"):
    st.markdown(f"🧠 {explanation}")

# ---------------- Gemini ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

if "chat" not in st.session_state:
    intro_prompt = f"You are {philosopher}. Respond thoughtfully in their philosophical tone and worldview."
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    st.session_state.chat = model.start_chat(history=[{"role": "user", "parts": [intro_prompt]}])

# ---------------- Chat History ----------------
for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(f'<div class="user-bubble">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble"><strong>{speaker}:</strong> {msg}</div>', unsafe_allow_html=True)

# ---------------- Chat Input ----------------
user_input = st.chat_input("Ask your question...")

if user_input:
    with st.spinner("Thinking..."):
        try:
            weather_context = get_weather_summary()
            tone_instruction = (
                f"{weather_context} Please consider this environmental context while responding."
            )

            st.session_state.chat.send_message(tone_instruction)
            reply = st.session_state.chat.send_message(user_input)

            st.session_state.history.append(("You", user_input))
            st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)

            status = st.empty()
            status.markdown(f"🧠 *{philosopher} is thinking...*")

            display_text = ""
            typing_placeholder = st.empty()
            for char in reply.text:
                display_text += char
                typing_placeholder.markdown(
                    f'<div class="bot-bubble"><strong>{philosopher}:</strong> {display_text}<span class="fade-cursor">▌</span></div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.015)

            status.empty()
            typing_placeholder.markdown(
                f'<div class="bot-bubble"><strong>{philosopher}:</strong> {display_text}</div>',
                unsafe_allow_html=True
            )

            st.session_state.history.append((philosopher, reply.text))

        except Exception as e:
            st.error(f"❌ Error: {e}")
