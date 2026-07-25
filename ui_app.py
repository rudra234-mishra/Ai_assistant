import streamlit as st
from chat import ask_question

st.set_page_config(
    page_title="Udayanath College AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*:not([data-testid="stIconMaterial"]) { font-family: 'Inter', sans-serif !important; }

/* ── Background ── */
.stApp { background: #f9fafb; }

/* ── Remove top padding so title has room ── */
.block-container {
    background: transparent !important;
    padding-top: 2.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1e1b4b !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * { color: #c7d2fe !important; }

/* ── Sidebar clear button ── */
section[data-testid="stSidebar"] .stButton > button {
    background: #312e81 !important;
    color: #fca5a5 !important;
    border: 1.5px solid #ef4444 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #ef4444 !important;
    color: #fff !important;
}

/* ── Title — big, clear, full width ── */
.title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    color: #1e1b4b;
    letter-spacing: -0.4px;
    line-height: 1.3;
    padding: 0.5rem 0 0.2rem;
    -webkit-text-fill-color: #1e1b4b !important;
}

/* ── Subtitle ── */
.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
    line-height: 1.6;
}
.subtitle b { color: #4338ca !important; }

/* ── Developer badge ── */
.dev-wrapper { text-align: center; margin: 0.5rem 0 0.8rem; }
.dev-badge {
    display: inline-block;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff !important;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 7px 22px;
    border-radius: 999px;
    letter-spacing: 0.3px;
    box-shadow: 0 0 0 4px rgba(79,70,229,0.15), 0 4px 18px rgba(79,70,229,0.4);
    animation: badge-pulse 2.5s ease-in-out infinite;
}
@keyframes badge-pulse {
    0%,100% { box-shadow: 0 0 0 4px rgba(79,70,229,0.15), 0 4px 18px rgba(79,70,229,0.3); }
    50%      { box-shadow: 0 0 0 8px rgba(79,70,229,0.2), 0 6px 30px rgba(79,70,229,0.55); }
}

/* ── User bubble ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #ede9fe !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 1px 6px rgba(109,40,217,0.08);
}

/* ── Assistant bubble ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #ffffff !important;
    border: 1px solid #e0e7ff !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}

/* ── User text ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) div {
    color: #3730a3 !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

/* ── Assistant text ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) span,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) div {
    color: #111827 !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

/* ── Avatars ── */
div[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    border-radius: 50% !important;
}
div[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    border-radius: 50% !important;
}

/* ── Chat input — FIX: light background, dark visible text ── */
div[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1.5px solid #c7d2fe !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
/* FIX: make textarea text dark and visible */
div[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #111827 !important;
    font-size: 0.95rem !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #4f46e5 !important;
}
/* FIX: make placeholder clearly visible */
div[data-testid="stChatInput"] textarea::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
}
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    border: none !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"] button:hover {
    opacity: 0.88 !important;
    transform: scale(1.07) !important;
}

/* ── Topic pills ── */
.pill {
    display: inline-block;
    background: #312e81;
    color: #c7d2fe !important;
    border-radius: 8px;
    padding: 4px 10px;
    margin: 3px 2px;
    font-size: 0.76rem;
    font-weight: 500;
}

/* ── General text ── */
p, label, span { color: #374151 !important; }

hr { border-color: #e5e7eb !important; }
</style>
""", unsafe_allow_html=True)


# ── Avatars used throughout the app (emoji avoids Material Symbols font issues) ──
USER_AVATAR = "🧑"
ASSISTANT_AVATAR = "🤖"


# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.4rem 0 0.8rem;'>
        <div style='font-size:2.4rem;'>🎓</div>
        <div style='font-size:1rem;font-weight:700;color:#e0e7ff;margin-top:6px;'>
            College AI Assistant
        </div>
        <div style='font-size:0.72rem;color:#6366f1;margin-top:3px;'>
            Udayanath Autonomous College
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<p style='font-size:0.72rem;color:#6366f1;letter-spacing:0.6px;'>📚 SUPPORTED TOPICS</p>",
                unsafe_allow_html=True)

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
        <div style='flex:1;background:#312e81;border:1px solid #4338ca;
                    border-radius:10px;padding:10px 6px;text-align:center;'>
            <div style='font-size:1.3rem;font-weight:700;color:#a5b4fc;'>{asked}</div>
            <div style='font-size:0.68rem;color:#818cf8;margin-top:2px;'>Asked</div>
        </div>
        <div style='flex:1;background:#312e81;border:1px solid #4338ca;
                    border-radius:10px;padding:10px 6px;text-align:center;'>
            <div style='font-size:1.3rem;font-weight:700;color:#a5b4fc;'>{asked}</div>
            <div style='font-size:0.68rem;color:#818cf8;margin-top:2px;'>Answered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── Header — split into two lines so it never clips ──
st.markdown("""
<div style='text-align:center;padding-top:0.5rem;'>
    <div style='font-size:2.2rem;margin-bottom:4px;'>🎓</div>
    <div class='title'>Udayanath Autonomous College<br>AI Assistant</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
    Ask about <b>Location · History · Principal · Director · Courses · Placements · Facilities · Sports · Campus</b>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='dev-wrapper'>
    <span class='dev-badge'>👨‍💻 Developed by Rudra</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Empty state ──
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:3rem 1rem;background:#fff;
                border:1px solid #e0e7ff;border-radius:16px;
                margin:0.5rem 0 1.5rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);'>
        <div style='font-size:2.5rem;margin-bottom:10px;'>💬</div>
        <div style='font-size:1rem;font-weight:600;color:#1e1b4b;margin-bottom:6px;'>
            Ask me anything about Udayanath College!
        </div>
        <div style='font-size:0.85rem;color:#9ca3af;'>
            Type your question below to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──
for msg in st.session_state.messages:
    avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ──
question = st.chat_input("Ask a question about the college...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(question)

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        with st.spinner("Searching college knowledge base..."):
            answer = ask_question(question)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
