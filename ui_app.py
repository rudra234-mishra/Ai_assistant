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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }

/* ── Background ── */
.stApp { background: #0f0f0f; }

.block-container {
    background: transparent !important;
    padding-top: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #1f1f1f !important;
}
section[data-testid="stSidebar"] * { color: #a1a1aa !important; }

section[data-testid="stSidebar"] .stButton > button {
    background: #1a0505 !important;
    color: #f87171 !important;
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

/* ── Title ── */
.title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f97316, #fb923c, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.3;
    padding: 0.3rem 0 0.2rem;
}

/* ── Subtitle ── */
.subtitle {
    text-align: center;
    color: #52525b !important;
    font-size: 0.88rem;
    margin-bottom: 0.3rem;
    line-height: 1.6;
}
.subtitle b { color: #f97316 !important; }

/* ── Developer badge ── */
.dev-wrapper { text-align: center; margin: 0.4rem 0 0.6rem; }
.dev-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f97316, #ef4444);
    color: #fff !important;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 7px 22px;
    border-radius: 999px;
    letter-spacing: 0.3px;
    animation: badge-pulse 2.5s ease-in-out infinite;
}
@keyframes badge-pulse {
    0%,100% { box-shadow: 0 0 0 3px rgba(249,115,22,0.2), 0 4px 16px rgba(249,115,22,0.3); }
    50%      { box-shadow: 0 0 0 6px rgba(249,115,22,0.15), 0 6px 28px rgba(249,115,22,0.5); }
}

/* ── User bubble ── */
div[data-testid="stChatMessage"]:has(img[alt="🧑"]),
div[data-testid="stChatMessage"]:nth-of-type(odd) {
    background: #1c1007 !important;
    border: 1px solid #f97316 !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 0 12px rgba(249,115,22,0.1);
}

/* ── Assistant bubble ── */
div[data-testid="stChatMessage"]:has(img[alt="🤖"]) {
    background: #111111 !important;
    border: 1px solid #292929 !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.3);
}

/* ── All chat text ── */
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] div {
    color: #e4e4e7 !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
}

/* ── Chat input ── */
div[data-testid="stChatInput"] {
    background: #1a1a1a !important;
    border: 1.5px solid #292929 !important;
    border-radius: 14px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #f97316 !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.12) !important;
}
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #f4f4f5 !important;
    font-size: 0.95rem !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #f97316 !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #3f3f46 !important;
    opacity: 1 !important;
}
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #f97316, #ef4444) !important;
    border: none !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"] button:hover {
    opacity: 0.85 !important;
    transform: scale(1.07) !important;
}

/* ── Topic pills ── */
.pill {
    display: inline-block;
    background: #1c1007;
    border: 1px solid #f9731633;
    color: #fb923c !important;
    border-radius: 8px;
    padding: 4px 10px;
    margin: 3px 2px;
    font-size: 0.75rem;
    font-weight: 500;
}

/* ── General text ── */
p, label, span { color: #71717a !important; }
hr { border-color: #1f1f1f !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.4rem 0 0.8rem;'>
        <div style='font-size:2.4rem;'>🎓</div>
        <div style='font-size:1rem;font-weight:700;
                    background:linear-gradient(90deg,#f97316,#fbbf24);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    margin-top:6px;'>College AI Assistant</div>
        <div style='font-size:0.72rem;color:#3f3f46;margin-top:3px;'>
            Udayanath Autonomous College
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        "<p style='font-size:0.7rem;color:#3f3f46;letter-spacing:0.6px;'>📚 SUPPORTED TOPICS</p>",
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
        <div style='flex:1;background:#1c1007;border:1px solid #f9731655;
                    border-radius:10px;padding:10px 6px;text-align:center;'>
            <div style='font-size:1.4rem;font-weight:800;color:#f97316;'>{asked}</div>
            <div style='font-size:0.68rem;color:#3f3f46;margin-top:2px;'>Asked</div>
        </div>
        <div style='flex:1;background:#1c1007;border:1px solid #f9731655;
                    border-radius:10px;padding:10px 6px;text-align:center;'>
            <div style='font-size:1.4rem;font-weight:800;color:#fbbf24;'>{asked}</div>
            <div style='font-size:0.68rem;color:#3f3f46;margin-top:2px;'>Answered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── Header ──
st.markdown("""
<div style='text-align:center;padding-top:0.4rem;'>
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
    <div style='text-align:center;padding:3rem 1rem;
                background:#111111;
                border-top:2px solid #f97316;
                border-bottom:2px solid #fbbf24;
                border-left:1px solid #1f1f1f;
                border-right:1px solid #1f1f1f;
                border-radius:16px;margin:0.5rem 0 1.5rem;'>
        <div style='font-size:2.5rem;margin-bottom:10px;'>💬</div>
        <div style='font-size:1rem;font-weight:600;color:#e4e4e7;margin-bottom:6px;'>
            Ask me anything about Udayanath College!
        </div>
        <div style='font-size:0.85rem;color:#3f3f46;'>
            Type your question below to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──
# ✅ FIX: pass avatar= explicitly so no "face"/"smart_toy" text appears
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ──
question = st.chat_input("Ask a question about the college...")

if question:

    # User message — ✅ emoji avatar
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    # Assistant streaming — ✅ emoji avatar
    with st.chat_message("assistant", avatar="🤖"):
        streamed_answer = st.write_stream(ask_question_stream(question))

    st.session_state.messages.append({"role": "assistant", "content": streamed_answer})
