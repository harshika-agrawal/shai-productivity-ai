import streamlit as st
from openai import OpenAI
import PyPDF2
import pandas as pd
from docx import Document
import pyttsx3
from fpdf import FPDF
import base64
import time
import os

# ---------------- PAGE SETTINGS ---------------- #

st.set_page_config(
    page_title="SHAi",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* MAIN APP */
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
    color: white;
}

/* TITLE */
h1 {
    font-size: 52px !important;
    font-weight: bold !important;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* SUBTITLE */
h3 {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}

/* CHAT INPUT */
.stChatInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 15px !important;
    border: 1px solid #334155 !important;
    padding: 14px !important;
}

/* BUTTON */
.stButton button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: bold;
}

/* CHAT MESSAGE */
[data-testid="stChatMessage"] {
    background-color: rgba(30, 41, 59, 0.6);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    backdrop-filter: blur(10px);
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- OPENROUTER ---------------- #

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---------------- HEADER ---------------- #
st.markdown("""
<h1>SHΛi</h1>
<h3>Your futuristic AI workspace 🚀</h3>
""", unsafe_allow_html=True)

# ---------------- SESSION ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = []

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("⚡ SHΛi Features")

    st.write("💬 AI Chat")
    st.write("👾 Multi AI Models")
    st.write("📄 PDF Reader")
    st.write("📑 DOCX Reader")
    st.write("📃 CSV Reader")
    st.write("📋 TXT Reader")
    st.write("🎙️ Voice Output")
    st.write("📤 Chat Export")
    st.write("🧐 AI Memory")

    st.markdown("---")

    # AI MODEL
    model_choice = st.selectbox(
        "🤖 Choose AI Model",
        [
            "openai/gpt-3.5-turbo",
            "openai/gpt-4o-mini",
            "deepseek/deepseek-chat",
            "anthropic/claude-3-haiku"
        ]
    )

    st.markdown("---")

    # AI MODE
    ai_mode = st.selectbox(
        "🧠 AI Mode",
        [
            "General AI",
            "Coding Expert",
            "Study Assistant",
            "Resume Builder",
            "Productivity Coach"
        ]
    )

    st.markdown("---")

    # FILE UPLOADER
    uploaded_file = st.file_uploader(
        "📂 Upload File",
        type=["pdf", "txt", "csv", "docx"]
    )

    st.markdown("---")

    # CLEAR CHAT
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- FILE READING ---------------- #

file_text = ""

if uploaded_file is not None:

    # PDF
    if uploaded_file.type == "application/pdf":

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                file_text += text

    # TXT
    elif uploaded_file.type == "text/plain":

        file_text = uploaded_file.read().decode("utf-8")

    # CSV
    elif uploaded_file.type == "text/csv":

        df = pd.read_csv(uploaded_file)

        st.dataframe(df)

        file_text = df.to_string()

    # DOCX
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

        doc = Document(uploaded_file)

        for para in doc.paragraphs:

            file_text += para.text + "\n"

    st.success("✅ File Uploaded Successfully")

# ---------------- SYSTEM PROMPT ---------------- #

system_prompt = ""

if ai_mode == "General AI":

    system_prompt = "You are SHΛi, a futuristic AI assistant."

elif ai_mode == "Coding Expert":

    system_prompt = "You are an expert coding assistant helping with coding, debugging, DSA and development."

elif ai_mode == "Study Assistant":

    system_prompt = "Explain concepts in very simple student-friendly language."

elif ai_mode == "Resume Builder":

    system_prompt = "Help users build strong resumes and projects."

elif ai_mode == "Productivity Coach":

    system_prompt = "Help users improve focus, goals, productivity and routines."

# ---------------- SHOW OLD MESSAGES ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- USER INPUT ---------------- #

user_input = st.chat_input("Ask SHAi anything...")

if user_input:

    # MEMORY SAVE
    st.session_state.memory.append(user_input)

    # USER MESSAGE
    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        completion = client.chat.completions.create(

            model=model_choice,

            messages=[
                {
                    "role": "system",
                    "content": f"""
                    {system_prompt}

                    User Memory:
                    {st.session_state.memory}

                    Uploaded File Content:
                    {file_text}
                    """
                },

                *st.session_state.messages
            ]
        )

        ai_reply = completion.choices[0].message.content

    except Exception as e:

        ai_reply = f"❌ Error: {e}"

    # ---------------- AI RESPONSE ---------------- #

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        for word in ai_reply.split():

            full_response += word + " "

            time.sleep(0.01)

            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # SAVE AI MESSAGE
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    # ---------------- VOICE OUTPUT ---------------- #

    try:

        engine = pyttsx3.init()

        engine.say("Your response is ready")

        engine.runAndWait()

    except:
        pass

# ---------------- EXPORT CHAT ---------------- #

st.markdown("---")

if st.button("📥 Export Chat as PDF"):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for msg in st.session_state.messages:

        pdf.multi_cell(
            0,
            10,
            f"{msg['role'].upper()}: {msg['content']}"
        )

    pdf.output("SHΛi_Chat.pdf")

    with open("SHΛi_Chat.pdf", "rb") as file:

        st.download_button(
            label="⬇ Download PDF",
            data=file,
            file_name="SHΛi_Chat.pdf",
            mime="application/pdf"
        )

# ---------------- FOOTER ---------------- #

st.markdown("""
<hr>

<center>
Made with ❤️ BY HARSHIKA AGRAWAL
</center>
""", unsafe_allow_html=True)