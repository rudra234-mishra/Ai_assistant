import streamlit as st
from chat import ask_question_stream

st.set_page_config(
    page_title="Udayanath College AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }

/* ── Background: clean white ── */
.stApp { background: #f0f4ff; }

/* ── Hide Streamlit default black header ── */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu                       { display: none !important; }
footer                          { display: none !important; }

.block-container {
    background: transparent !important;
    padding-top: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1e3a8a !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(30,58,138,0.3);
}
section[data-testid="stSidebar"] * { color: #bfdbfe !important; }

section[data-testid="stSidebar"] .stButton > button {
    background: rgba(239,68,68,0.15) !important;
    color: #fca5a5 !important;
    border: 1.5px solid rgba(239,68,68,0.5) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #ef4444 !important;
    color: #fff !important;
    border-color: #ef4444 !important;
}

/* ── Title ── */
.title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #1d4ed8, #0ea5e9, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.25;
    letter-spacing: -0.5px;
}

/* ── Subtitle ── */
.subtitle {
    text-align: center;
    color: #64748b !important;
    font-size: 0.88rem;
    margin-bottom: 0.5rem;
    line-height: 1.7;
}
.subtitle b { color: #1d4ed8 !important; }

/* ── Developer badge — STYLISH ── */
.dev-wrapper {
    text-align: center;
    margin: 0.6rem 0 0.8rem;
}
.dev-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
    color: #fff !important;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 9px 24px;
    border-radius: 999px;
    letter-spacing: 0.4px;
    box-shadow:
        0 0 0 3px rgba(14,165,233,0.2),
        0 4px 20px rgba(29,78,216,0.4),
        inset 0 1px 0 rgba(255,255,255,0.2);
    animation: badge-shine 2.5s ease-in-out infinite;
    position: relative;
    overflow: hidden;
}
.dev-badge::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -60%;
    width: 40%;
    height: 200%;
    background: rgba(255,255,255,0.25);
    transform: skewX(-20deg);
    animation: shine-sweep 2.5s ease-in-out infinite;
}
@keyframes badge-shine {
    0%,100% {
        box-shadow: 0 0 0 3px rgba(14,165,233,0.2),
                    0 4px 20px rgba(29,78,216,0.35);
    }
    50% {
        box-shadow: 0 0 0 6px rgba(14,165,233,0.15),
                    0 6px 32px rgba(29,78,216,0.55),
                    0 0 48px rgba(14,165,233,0.2);
    }
}
@keyframes shine-sweep {
    0%   { left: -60%; }
    60%  { left: 140%; }
    100% { left: 140%; }
}

/* ── User bubble ── */
div[data-testid="stChatMessage"]:has(img[alt="🧑"]) {
    background: linear-gradient(135deg, #dbeafe, #e0f2fe) !important;
    border: 1px solid #93c5fd !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 2px 10px rgba(29,78,216,0.08);
}

/* ── Assistant bubble ── */
div[data-testid="stChatMessage"]:has(img[alt="🤖"]) {
    background: #ffffff !important;
    border: 1px solid #e0e7ff !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

/* ── User text ── */
div[data-testid="stChatMessage"]:has(img[alt="🧑"]) p,
div[data-testid="stChatMessage"]:has(img[alt="🧑"]) span,
div[data-testid="stChatMessage"]:has(img[alt="🧑"]) div {
    color: #1e3a8a !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
    font-weight: 500 !important;
}

/* ── Assistant text ── */
div[data-testid="stChatMessage"]:has(img[alt="🤖"]) p,
div[data-testid="stChatMessage"]:has(img[alt="🤖"]) span,
div[data-testid="stChatMessage"]:has(img[alt="🤖"]) div {
    color: #1e293b !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
}

/* ── Chat input ── */
div[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1.5px solid #bfdbfe !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 10px rgba(29,78,216,0.08) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.12),
                0 4px 16px rgba(29,78,216,0.1) !important;
}
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #0f172a !important;
    font-size: 0.95rem !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #1d4ed8 !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
    border: none !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"] button:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 4px 14px rgba(29,78,216,0.4) !important;
}

/* ── Topic pills ── */
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(191,219,254,0.3);
    color: #bfdbfe !important;
    border-radius: 8px;
    padding: 4px 10px;
    margin: 3px 2px;
    font-size: 0.74rem;
    font-weight: 500;
    transition: all 0.2s ease;
}
.pill:hover {
    background: rgba(255,255,255,0.2) !important;
    border-color: rgba(191,219,254,0.6) !important;
}

/* ── General text ── */
p, label, span { color: #475569 !important; }
hr { border-color: #e0e7ff !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.6rem 0 1rem;'>
        <div style='
            width:64px;height:64px;margin:0 auto 10px;
            background:linear-gradient(135deg,rgba(255,255,255,0.2),rgba(255,255,255,0.05));
            border:2px solid rgba(191,219,254,0.4);
            border-radius:18px;display:flex;align-items:center;justify-content:center;
            font-size:2rem;backdrop-filter:blur(8px);'>🎓</div>
        <div style='font-size:1rem;font-weight:700;color:#fff;margin-top:4px;'>
            College AI Assistant
        </div>
        <div style='font-size:0.72rem;color:rgba(191,219,254,0.6);margin-top:3px;'>
            Udayanath Autonomous College
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        "<p style='font-size:0.7rem;color:rgba(191,219,254,0.5);letter-spacing:0.8px;'>📚 TOPICS</p>",
        unsafe_allow_html=True
    )

    topics = ["📍 Location", "🏛️ History", "👩‍🏫 Principal", "👨‍💼 Director",
              "🎓 Courses", "💼 Placements", "🏟️ Stadium",
              "🏫 Facilities", "🌳 Environment", "📖 General Info"]

    st.markdown(
        "<div style='line-height:2.2;'>" +
        "".join([f"<span class='pill'>{t}</span>" for t in topics]) +
        "</div>", unsafe_allow_html=True
    )

    st.divider()

    asked = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.markdown(f"""
    <div style='display:flex;gap:8px;margin-bottom:12px;'>
        <div style='flex:1;background:rgba(255,255,255,0.08);
                    border:1px solid rgba(191,219,254,0.2);
                    border-radius:12px;padding:12px 6px;text-align:center;'>
            <div style='font-size:1.5rem;font-weight:800;color:#fff;'>{asked}</div>
            <div style='font-size:0.68rem;color:rgba(191,219,254,0.5);margin-top:2px;'>Asked</div>
        </div>
        <div style='flex:1;background:rgba(255,255,255,0.08);
                    border:1px solid rgba(191,219,254,0.2);
                    border-radius:12px;padding:12px 6px;text-align:center;'>
            <div style='font-size:1.5rem;font-weight:800;color:#7dd3fc;'>{asked}</div>
            <div style='font-size:0.68rem;color:rgba(191,219,254,0.5);margin-top:2px;'>Answered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── Header ──
st.markdown("""
<div style='text-align:center;padding:0.8rem 0 0.3rem;'>
    <div style='font-size:2.5rem;margin-bottom:6px;
                filter:drop-shadow(0 4px 8px rgba(29,78,216,0.3));'>🎓</div>
    <div class='title'>Udayanath Autonomous College<br>AI Assistant</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
    Ask about <b>Location · History · Principal · Director · Courses · Placements · Facilities · Sports · Campus</b>
</div>
""", unsafe_allow_html=True)

# ── Stylish Developer Badge ──
st.markdown("""
<div class='dev-wrapper'>
    <span class='dev-badge'>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
             xmlns="http://www.w3.org/2000/svg"
             style="display:inline;vertical-align:middle;margin-right:2px;">
            <path d="M16 18L22 12L16 6M8 6L2 12L8 18"
                  stroke="white" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Developed by Rudra
    </span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Empty state ──
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:3.5rem 1.5rem;
                background:#ffffff;
                border:1px solid #e0e7ff;
                border-top:3px solid #1d4ed8;
                border-radius:16px;margin:0.5rem 0 1.5rem;
                box-shadow:0 4px 24px rgba(29,78,216,0.08);'>
        <div style='font-size:3rem;margin-bottom:12px;'>💬</div>
        <div style='font-size:1.05rem;font-weight:700;color:#1e3a8a;margin-bottom:6px;'>
            Ask me anything about Udayanath College!
        </div>
        <div style='font-size:0.84rem;color:#94a3b8;'>
            Type your question below to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ──
question = st.chat_input("Ask a question about the college...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🤖"):
        streamed_answer = st.write_stream(ask_question_stream(question))

    st.session_state.messages.append({"role": "assistant", "content": streamed_answer})