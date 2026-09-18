import streamlit as st
from openai import OpenAI
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="RogueGPT-Monolith-V3", page_icon="🕋", layout="wide")

# --- THE MONOLITH UI (GRAND & POWERFUL) ---
st.markdown("""
    <style>
    /* Deep Space Canvas */
    .stApp { 
        background-color: #05070a; 
        color: #f0f6fc; 
        font-family: 'Inter', system-ui, sans-serif; 
    }
    
    /* Monolithic Centered Layout */
    .main .block-container { 
        max-width: 900px; 
        padding-top: 5rem; 
    }

    /* Cinematic Chat Flow */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: none !important;
        border-left: 4px solid transparent;
        margin-bottom: 1rem !important;
        padding: 2.5rem !important;
        transition: all 0.4s ease;
    }
    
    /* Highlight User Messages with Monolith Blue */
    [data-testid="stChatMessage"][data-testid="user-message"] {
        border-left: 4px solid #58a6ff;
        background-color: rgba(88, 166, 255, 0.03) !important;
    }

    /* Sidebar - Heavy & Solid */
    section[data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 2px solid #161b22;
        width: 320px !important;
    }

    /* Power Buttons */
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-radius: 4px !important;
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #58a6ff !important;
    }
    .stButton > button:hover {
        border-color: #58a6ff !important;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.2);
    }

    /* The Monolith Input */
    .stChatInputContainer {
        border-top: 1px solid #30363d !important;
        background-color: #05070a !important;
        padding: 2rem 0 !important;
    }
    
    /* Footer Signature */
    .signature-box {
        margin-top: 100px;
        padding: 20px;
        border-top: 1px solid #30363d;
        text-align: center;
    }
    .signature-text {
        font-size: 0.75rem;
        letter-spacing: 2px;
        color: #8b949e;
        text-transform: uppercase;
    }
    .author-highlight {
        color: #f0f6fc;
        font-weight: 800;
        display: block;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE RESET LOGIC ---
def purge_session():
    st.session_state.messages = []

# --- CORE INITIALIZATION ---
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("SYSTEM CRITICAL: OPENROUTER_API_KEY missing.")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- THE COMMAND CENTER (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='letter-spacing:2px; color: #58a6ff;'>RogueGPT</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='letter-spacing:4px; margin-top:-15px;'>MONOLITH</h4>", unsafe_allow_html=True)
    st.caption("V3 // ADVANCED NEURAL ARCHITECTURE")
    
    st.divider()
    
    model_engines = {
        "Nvidia Nemotron 3 Nano Omni": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "Liquid LFM 2.5": "liquid/lfm-2.5-2.6b:free",
        "Poolside Laguna XS": "poolside/laguna-xs-2.1:free",
        "Nex-AGI Nex N2.5 Mini": "nex-agi/nex-n2.5-mini:free",
        "Cohere North Mini Code": "cohere/north-mini-code:free",
        "Google Lyria 3 Pro": "google/lyria-3-pro-preview",
        "Google Gemma 4 26B": "google/gemma-4-26b-a4b-it:free"
    }
    
    selected_name = st.selectbox(
        "CORE ENGINE", 
        options=list(model_engines.keys()),
        on_change=purge_session,
        key="engine_selector"
    )
    ACTIVE_ENGINE = model_engines[selected_name]
    
    st.divider()
    
    if st.button("PURGE & RESET"):
        purge_session()
        st.rerun()

    if st.session_state.messages:
        data = json.dumps(st.session_state.messages, indent=2)
        st.download_button("EXTRACT TRANSCRIPT", data, file_name="roguegpt_monolith_v3.json")
    
    # SIGNATURE
    st.markdown(
        f"""
        <div class="signature-box">
            <div class="signature-text">
                ENGINEERED BY
                <span class="author-highlight">CHINMAY V CHATRADAMATH</span>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- THE INTERFACE ---
if not st.session_state.messages:
    # Grand Branding
    st.markdown("<h3 style='text-align: center; color: #58a6ff; letter-spacing: 5px; margin-top: 50px;'>ROGUEGPT</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 5rem; letter-spacing: -3px; margin-top: -20px;'>MONOLITH</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #8b949e; font-weight: 600; letter-spacing: 2px;'>V3 // {selected_name.upper()}</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Input Command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp_box = st.empty()
        full_resp = ""
        
        try:
            completion = client.chat.completions.create(
                model=ACTIVE_ENGINE,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                extra_headers={
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "RogueGPT-Monolith-V3"
                },
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_resp += chunk.choices[0].delta.content
                    resp_box.markdown(full_resp + "█")
            
            resp_box.markdown(full_resp)
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
                
        except Exception as e:
            st.error(f"ENGINE ERROR: {str(e)}")
