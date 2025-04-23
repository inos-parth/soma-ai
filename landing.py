import streamlit as st

# Page config
st.set_page_config(page_title="Sōma.ai", page_icon="🧘", layout="centered")

# --- CSS for pulsing button ---
st.markdown("""
    <style>
    div.stButton > button {
        animation: pulse 2s infinite;
        border: 1px solid #91A6FF;
        padding: 0.6em 1.5em;
        font-size: 1rem;
        border-radius: 8px;
        background-color: #2d2d44;
        color: #eaeef2;
        transition: all 0.3s ease-in-out;
        margin-top: 0.5em;
    }

    div.stButton > button:hover {
        background-color: #3a3a5a;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(145, 166, 255, 0.6);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(145, 166, 255, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(145, 166, 255, 0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🧘 Welcome to Sōma.ai")
st.markdown("**Find your philosophical match. Reflect. Converse. Realign.**")
st.markdown("Sōma.ai is your personal space for meaningful conversations — guided by timeless thinkers from across the world.")

# --- Feature list ---
st.markdown("#### 🔍 What You Can Do")
st.markdown("""
- Answer a few reflective questions  
- Get matched with a philosopher based on your values  
- Chat with them like a modern mentor
""")

# --- Call to Action ---
st.markdown("### 👉 Ready to begin your journey?")

if st.button("✨ Start Reflecting"):
    st.switch_page("pages/app.py")
