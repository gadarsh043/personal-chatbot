# Adarsh's Personal AI Chatbot

An intelligent, self-learning personal chatbot designed to serve as an interactive resume and portfolio assistant. Built with Flask, Firebase, and Groq (LLaMA 3.1), this chatbot can answer questions about Adarsh's skills, experience, and projects while continuously learning from interactions.

## 🌟 Features

- **Groq AI Integration**: Powered by `llama-3.1-70b-versatile` through Groq for blazing fast, high-quality responses.
- **Dynamic Context**: Prompt is dynamically built from `resume.yaml` including career goals and personal facts.
- **Progressive Learning**: 
  - Automatically saves new Q&A pairs to Firebase
  - Reviews past interactions to avoid repeating answers
  - Admin dashboard to review, edit, and curate learned responses
- **3-Tier Response System**:
  1. Fast cache (Firebase learned Q&A)
  2. Rule-based matching (Resume YAML parser)
  3. AI Generation (Groq API fallback)
- **Rich Markdown Rendering**: Uses `marked.js` to render beautiful tables, lists, and code blocks directly in the chat UI.
- **Modern UI Edge**: Glassmorphism design, responsive layout, typing indicators, and suggested questions.

## 🚀 Quick Start

1. **Clone and Install**
```bash
git clone https://github.com/gadarsh043/personal-chatbot.yaml
cd personal-chatbot
pip install -r requirements.txt
```

2. **Configuration**
Create a `.env` file in the root directory:
```env
# Server Secret
FLASK_SECRET_KEY=your_secret_key_here

# Admin Password (for /admin dashboard)
ADMIN_PASSWORD=your_secure_password_here

# Groq API
GROQ_API_KEY=your_groq_api_key

# Firebase (Local dev)
FIREBASE_KEY_PATH=firebase-key.json
```

3. **Run Locally**
```bash
python app.py
```
Visit `http://localhost:8080` in your browser.

## 📊 Admin Dashboard

Access the admin panel at `http://localhost:8080/admin/login` using your configured `ADMIN_PASSWORD`. Here you can:
- View all questions asked by visitors
- See how the AI responded
- Edit answers for better accuracy
- Delete irrelevant or spam questions
- Mark AI-generated answers as "Reviewed"

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Groq API (LLaMA 3.1)
- **Frontend**: Vanilla HTML/CSS/JS, marked.js
- **Database**: Firebase Firestore
- **Data Source**: Custom YAML parsing (`resume.yaml`)
- **Deployment**: Render / Vercel compatible

## 🌍 Portfolio Integration Options

This chatbot is designed to be embedded in a portfolio website via an iframe:

```html
<iframe 
    src="https://your-chatbot-url.onrender.com" 
    width="400" 
    height="600" 
    style="border:none; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);"
></iframe>
```

---
*Built by [Adarsh Gella](https://adarshgella.com)*
