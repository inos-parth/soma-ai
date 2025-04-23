import streamlit as st
import google.generativeai as genai

# Setup
st.set_page_config(page_title="Sōma.ai - Reflect", layout="centered")
st.title("🧭 Self-Reflection")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Philosopher matching
q1 = st.radio("1. What do you value more?", ["Truth", "Happiness"], key="q1")
q2 = st.radio("2. What guides your decisions?", ["Logic", "Emotion"], key="q2")
q3 = st.radio("3. What feels more important to you?", ["Freedom", "Stability"], key="q3")
q4 = st.radio("4. Do people shape their destiny?", ["Yes, entirely", "No, fate rules"], key="q4")
q5 = st.radio("5. Which feels more meaningful?", ["Understanding life", "Enjoying life"], key="q5")

match_placeholder = st.empty()

if st.button("🔮 Match Me"):
    with st.spinner("✨ Analyzing your values..."):
        prompt = f"""
You are a philosophical reasoning engine. Based on the following user answers, identify which philosopher their values most align with.

Choose from: Socrates, Plato, Aristotle, Nietzsche, Confucius, Simone de Beauvoir.

Respond in this format:
[Philosopher Name]
[1–2 sentence explanation why]

Answers:
1. Value: {q1}
2. Decisions guided by: {q2}
3. Importance: {q3}
4. Destiny belief: {q4}
5. Life meaning: {q5}
"""
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(prompt)
            text = response.text.strip()
            lines = text.split("\n")
            philosopher = lines[0].strip() if lines else "Unknown"
            explanation = "\n".join(lines[1:]) if len(lines) > 1 else "No explanation provided."

            st.session_state.philosopher = philosopher
            st.session_state.explanation = explanation
            st.session_state.matched = True
            st.session_state.history = []  # clear previous history

            st.switch_page("pages/chat.py")

        except Exception as e:
            match_placeholder.error(f"❌ Matching failed: {e}")
