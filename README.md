# 🤖 SHΛi - AI Productivity Workspace

SHΛi is a futuristic AI-powered productivity assistant built using Streamlit and OpenRouter API. It provides a ChatGPT-style interface with file reading, AI memory, multi-model support, and modern UI.

---

## 🚀 Features

- 💬 AI Chat (Multiple Models)
- 🧠 AI Memory (context retention)
- 📄 PDF File Reader
- 📑 DOCX File Reader
- 📊 CSV Viewer
- 📋 TXT File Support
- 🎙️ Voice Output (Text-to-Speech)
- 📤 Export Chat as PDF
- 🎨 Modern ChatGPT-like UI
- ⚡ Fast and responsive design

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit ⚡
- OpenRouter / OpenAI API 🤖
- Pandas 📊
- PyPDF2 📄
- python-docx 📑
- FPDF 📤
- pyttsx3 🎙️

---

## 📁 Project Structure
SHAi-Productivity-AI/
│
├── app.py # Main Streamlit application
├── requirements.txt # Dependencies
├── logo.png # App logo
├── README.md # Project documentation

---
## ⚙️ Installation & Setup

Clone the repository```bashgit clone https://github.com/your-username/shai-productivity-ai.gitcd shai-productivity-ai

## Install dependencies

pip install -r requirements.txt

##Set API Key (IMPORTANT)

👉 NEVER hardcode API key in code

Mac / Linux:
export OPENROUTER_API_KEY="your_api_key_here"

Windows:
set OPENROUTER_API_KEY="your_api_key_here"

## Run the app

streamlit run app.py

## ☁️ Deployment (Streamlit Cloud)

1. Push project to GitHub

2. Go to https://share.streamlit.io

3. Select repository

4. Add secret in settings:

OPENROUTER_API_KEY="your_api_key_here"

5. Click Deploy 🚀


## 🔐 Security Rules

-Never expose API keys in code

-Use environment variables or Streamlit secrets

-keep repo clean from sensitive data



## 👨‍💻 Author

Harshika Agrawal

## ⭐ Future Improvements

🎤 Voice input (Speech-to-Text)

🖼️ Image generation support

⚡ Streaming AI responses

💾 Chat history database
