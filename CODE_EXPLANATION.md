# Personal Chatbot - Complete Code Explanation

## Overview
This personal chatbot is a Flask-based web application that serves as an AI-powered resume assistant for Adarsh Gella. It integrates multiple technologies to provide intelligent responses about Adarsh's background, skills, and experience.

## Architecture
- **Backend**: Flask (Python) with Firebase integration
- **Frontend**: Modern HTML/CSS/JavaScript chat interface
- **AI**: DeepSeek API for intelligent response generation
- **Database**: Firebase Firestore for learned Q&A storage
- **Data**: YAML-based resume information

## File Structure
```
personal-chatbot/
├── app.py                 # Flask web server (main entry point)
├── chatbot.py            # Core chatbot logic and AI integration
├── resume.yaml           # Structured personal data
├── requirements.txt      # Python dependencies
├── vercel.json          # Deployment configuration
├── env.example          # Environment variables template
├── templates/
│   ├── index.html       # Main chat interface
│   └── admin/           # Admin panel templates
│       ├── login.html
│       ├── dashboard.html
│       ├── add.html
│       ├── edit.html
│       ├── stats.html
│       └── error.html
└── firebase-key.json   # Firebase credentials (not in repo)
```

---

## 1. app.py - Flask Web Server

### Imports and Setup (Lines 1-12)
```python
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from chatbot import chatbot, get_response
from datetime import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)
app.secret_key = 'chatbot-admin-secret-key-2024'

# Admin password
ADMIN_PASSWORD = 'Adarsh232774'
```

**Explanation:**
- **Line 1**: Imports Flask framework components for HTTP handling, JSON responses, templates, redirects, flash messages, and sessions
- **Line 2**: Imports CORS to allow cross-origin requests from different domains
- **Line 3**: Imports chatbot logic from the `chatbot.py` module
- **Line 4**: Imports datetime for timestamp handling
- **Line 5**: Imports wraps decorator for creating function decorators
- **Line 7**: Creates Flask application instance
- **Line 8**: Enables CORS for all routes
- **Line 9**: Sets secret key for session encryption and security
- **Line 12**: Hard-coded admin password (not ideal for production)

### Authentication System (Lines 14-43)

#### Login Required Decorator (Lines 14-22)
```python
def login_required(f):
    """Decorator to require login for admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
```

**Purpose**: Creates a decorator that protects admin routes by checking if user is logged in.
- **Line 17**: Preserves original function metadata using `@wraps`
- **Line 19**: Checks if 'admin_logged_in' exists in session
- **Line 20**: Redirects to login if not authenticated
- **Line 21**: Executes original function if authenticated

#### Admin Login Route (Lines 24-36)
```python
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login page"""
    if request.method == "POST":
        password = request.form.get("password", "")
        
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Successfully logged in!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid password!", "error")
    
    return render_template("admin/login.html")
```

**Purpose**: Handles both displaying login form (GET) and processing login (POST).
- **Line 27**: Checks if request is POST (form submission)
- **Line 28**: Extracts password from form data
- **Line 30-33**: Validates password and sets session variable
- **Line 35**: Shows error for invalid password
- **Line 37**: Renders login template for GET requests

#### Admin Logout Route (Lines 38-43)
```python
@app.route("/admin/logout")
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash("Successfully logged out!", "success")
    return redirect(url_for("admin_login"))
```

**Purpose**: Logs out admin user by removing session variable.

### Main Chat Routes (Lines 47-58)

#### Homepage Route (Lines 47-50)
```python
@app.route("/")
def index():
    """Main chat interface"""
    return render_template("index.html")
```

**Purpose**: Serves the main chat interface HTML page.

#### Chat API Endpoint (Lines 52-58)
```python
@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    question = data.get("question", "")
    response = get_response(question)
    return jsonify({"response": response})
```

**Purpose**: API endpoint that processes chat messages and returns responses.
- **Line 55**: Extracts JSON data from request
- **Line 56**: Gets question from JSON payload
- **Line 57**: Calls chatbot logic to generate response
- **Line 58**: Returns response as JSON

### Admin Management Routes (Lines 60-220)

#### Firebase Error Handling (Lines 60-65)
```python
def handle_firebase_error():
    """Handle Firebase connection errors"""
    if not chatbot.firebase_db:
        return render_template("admin/error.html", error="Firebase not connected")
    return None
```

**Purpose**: Centralized Firebase connection error handling.

#### Admin Dashboard (Lines 67-88)
```python
@app.route("/admin")
@login_required
def admin_dashboard():
    """Admin dashboard - view all Q&A pairs"""
    error = handle_firebase_error()
    if error:
        return error
    
    try:
        docs = chatbot.firebase_db.collection('learned_qa').stream()
        qa_pairs = []
        
        for doc in docs:
            data = doc.to_dict()
            qa_pairs.append({
                'id': doc.id,
                'question': data.get('question', ''),
                'answer': data.get('answer', ''),
                'ai_generated': data.get('ai_generated', False),
                'reviewed': data.get('reviewed', False),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            })
        
        qa_pairs.sort(key=lambda x: x.get('created_at') or datetime.min, reverse=True)
        return render_template("admin/dashboard.html", qa_pairs=qa_pairs)
    
    except Exception as e:
        return render_template("admin/error.html", error=f"Error: {str(e)}")
```

**Purpose**: Displays all learned Q&A pairs in admin dashboard.
- **Line 72**: Retrieves all documents from 'learned_qa' collection
- **Lines 75-84**: Converts documents to structured data
- **Line 86**: Sorts by creation date (newest first)

#### Add Q&A Route (Lines 90-125)
```python
@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def admin_add():
    """Add new Q&A pair"""
    if request.method == "GET":
        return render_template("admin/add.html")
    
    # POST request handling
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()
    
    if not question or not answer:
        flash("Both question and answer are required!", "error")
        return redirect(url_for("admin_add"))
    
    error = handle_firebase_error()
    if error:
        flash("Firebase not connected!", "error")
        return redirect(url_for("admin_add"))
    
    try:
        doc_id = question.lower().replace(" ", "_").replace("?", "").replace("!", "")[:50]
        qa_data = {
            'question': question,
            'answer': answer,
            'ai_generated': False,
            'reviewed': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        chatbot.firebase_db.collection('learned_qa').document(doc_id).set(qa_data)
        flash("Q&A pair added successfully!", "success")
        return redirect(url_for("admin_dashboard"))
        
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("admin_add"))
```

**Purpose**: Handles adding new Q&A pairs manually.
- **Line 111**: Creates document ID from question text
- **Lines 112-118**: Structures Q&A data with metadata
- **Line 120**: Saves to Firebase collection

### Application Startup (Lines 222-223)
```python
if __name__ == "__main__":
    app.run(debug=True, port=5002)
```

**Purpose**: Starts Flask development server when file is run directly.

---

## 2. chatbot.py - Core Chatbot Logic

### Class Initialization (Lines 15-21)
```python
class PersonalChatbot:
    def __init__(self, name="AdarshBot"):
        self.name = name
        self.resume = self.load_resume()
        self.firebase_db = self.init_firebase()
        self.learned_qa = self.load_learned_qa()
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
```

**Purpose**: Initializes chatbot with all necessary components.
- **Line 18**: Loads resume data from YAML file
- **Line 19**: Establishes Firebase connection
- **Line 20**: Loads existing Q&A pairs from Firebase
- **Line 21**: Gets AI API key from environment

### Firebase Integration (Lines 25-68)

#### Firebase Initialization (Lines 25-50)
```python
def init_firebase(self):
    """Initialize Firebase connection"""
    try:
        if not firebase_admin._apps:
            firebase_key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
            if os.path.exists(firebase_key_path):
                cred = credentials.Certificate(firebase_key_path)
            else:
                # Production environment variables
                firebase_config = {
                    "type": "service_account",
                    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
                }
                cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ Firebase initialized successfully")
        return db
    except Exception as e:
        print(f"⚠️ Firebase initialization failed: {e}")
        return None
```

**Purpose**: Handles both local development (key file) and production (environment variables) Firebase setup.
- **Line 28**: Checks if Firebase app already initialized
- **Line 29-31**: Uses local key file if available
- **Line 32-44**: Creates config from environment variables for production
- **Line 37**: Handles escaped newlines in private key

### Response Generation System

#### Resume Data Processing (Lines 93-167)
The system processes structured resume data from YAML:

```python
def get_resume_response(self, question):
    """Get predefined response from resume data"""
    question = question.lower()
    
    responses = {
        'name': f"Hi! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')} 👋",
        'location': f"I'm based in {self.resume.get('personal', {}).get('location', 'the US')}",
        'email': f"You can reach me at {self.resume.get('personal', {}).get('email', 'my email')}",
        'skills': self.format_skills(),
        'experience': self.format_experience(),
        'projects': self.format_projects(),
        'education': self.format_education(),
        'contact': f"Email: {self.resume.get('personal', {}).get('email', '')} | Phone: {self.resume.get('personal', {}).get('phone', '')}",
    }
    
    # Find best match using string similarity
    best_match = None
    best_score = 0
    
    for keyword, response in responses.items():
        if keyword in question:
            score = SequenceMatcher(None, question, keyword).ratio()
            if score > best_score:
                best_score = score
                best_match = response
    
    return best_match if best_score > 0.3 else None
```

**Purpose**: Maps keywords to structured resume responses with similarity matching.

#### AI Response Generation (Lines 192-267)
```python
def generate_ai_response(self, question):
    """Generate AI response using DeepSeek"""
    if not self.deepseek_api_key:
        return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now. Maybe will ask Adarsh to answer that question."
    
    try:
        # Build context from recent Q&A pairs
        context_pairs = []
        if self.learned_qa:
            sorted_qa = sorted(
                self.learned_qa.values(), 
                key=lambda x: x.get('created_at', datetime.min), 
                reverse=True
            )[:25]
            
            for qa in sorted_qa:
                context_pairs.append(f"Q: {qa['question']}\nA: {qa['answer']}")
        
        context_text = "\n\n".join(context_pairs) if context_pairs else "No previous conversations yet."
        
        prompt = f"""You are Adarsh's personal AI assistant. Answer as Adarsh in first person...
        
CURRENT QUESTION: {question}

Now answer the current question following this style - be knowledgeable, engaging, and smoothly redirect to Adarsh's career (max 60 words):"""

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-chat',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 400,
                'temperature': 0.8
            },
            timeout=15
        )
        
        if response.status_code == 200:
            ai_answer = response.json()['choices'][0]['message']['content'].strip()
            return ai_answer
        else:
            return fallback_message
            
    except Exception as e:
        return fallback_message
```

**Purpose**: Generates contextual AI responses using DeepSeek API with conversation history.

#### Main Response Logic (Lines 271-296)
```python
def get_response(self, question):
    """Main method to get chatbot response"""
    if not question:
        return "Hi! I'm Adarsh's AI assistant. Ask me about his skills, projects, or experience!"
    
    question = question.strip()
    
    # 1. Check Firebase learned Q&A
    learned_match, score = self.search_learned_qa(question)
    if learned_match and score > 0.7:
        response = learned_match['answer']
        if learned_match.get('ai_generated') and not learned_match.get('reviewed'):
            response += "<br><p style='font-size: 0.8em; color: #666; font-style: italic; margin-top: 10px;'>💡 This answer was AI-generated and may be updated as I learn more!</p>"
        return response
    
    # 2. Check resume-based responses
    resume_response = self.get_resume_response(question)
    if resume_response:
        return resume_response
    
    # 3. Generate AI response
    ai_response = self.generate_ai_response(question)
    self.save_learned_qa(question, ai_response, ai_generated=True)
    ai_response += "<br><p style='font-size: 0.8em; color: #666; font-style: italic; margin-top: 10px;'>💡 This answer was AI-generated. I'm always learning and improving my responses!</p>"
    
    return ai_response
```

**Purpose**: Implements priority-based response system:
1. **First**: Check learned Q&A pairs (Firebase)
2. **Second**: Check resume-based responses (YAML)
3. **Third**: Generate AI response and save it

---

## 3. templates/index.html - Chat Interface

### Document Structure and Styling

#### CSS Variables and Reset (Lines 9-29)
```css
:root {
    --primary-color: #2ecc71; /* Emerald Green */
    --secondary-color: #008080; /* Deep Teal */
    --dark-neutral: #2c3e50; /* Charcoal Grey */
    --light-neutral: #f7f9f9; /* Soft Ivory */
    --highlight-color: #f1c40f; /* Amber Yellow */
    --error-color: #e74c3c; /* Burnt Orange */
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: transparent;
}
```

**Purpose**: Establishes design system with consistent colors and typography.

#### Container and Layout (Lines 30-106)
```css
.container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    width: 100%;
    max-width: 450px;
    height: 600px;
    display: flex;
    flex-direction: column;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

**Purpose**: Creates glassmorphism design with modern aesthetics.
- **Line 31**: Semi-transparent background
- **Line 32**: Backdrop blur effect
- **Line 40-41**: Flexbox column layout for proper chat structure

### Interactive Elements

#### Message System (Lines 127-196)
```css
.message {
    margin-bottom: 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

**Purpose**: Smooth message animations and layout.

#### Typing Indicator (Lines 292-332)
```css
.typing-indicator {
    display: none;
    padding: 12px 16px;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    border-bottom-left-radius: 4px;
    max-width: 75%;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.typing-dots span {
    width: 6px;
    height: 6px;
    background: var(--secondary-color);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
    }
    30% {
        transform: translateY(-8px);
        opacity: 1;
    }
}
```

**Purpose**: Animated typing indicator with bouncing dots.

### JavaScript Functionality

#### Message Sending (Lines 432-462)
```javascript
async function sendMessage() {
    const input = document.getElementById("input");
    const messages = document.getElementById("messages");
    const question = input.value.trim();
    
    if (question === "") return;

    // Add user message
    addMessage(question, 'user');
    input.value = "";

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send question to Flask backend
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        // Hide typing indicator and add bot response
        hideTypingIndicator();
        addMessage(data.response, 'bot');
        
    } catch (error) {
        hideTypingIndicator();
        addMessage("Sorry, I'm having trouble connecting right now. Please try again!", 'bot');
    }
}
```

**Purpose**: Handles complete message flow with error handling.

#### Dynamic Message Creation (Lines 464-484)
```javascript
function addMessage(text, sender) {
    const messages = document.getElementById("messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = sender === 'user' ? 'Y' : 'A';
    
    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messages.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    setTimeout(() => {
        messages.scrollTop = messages.scrollHeight;
    }, 100);
}
```

**Purpose**: Dynamically creates message elements with proper styling and auto-scroll.

---

## 4. Configuration Files

### resume.yaml - Structured Data
```yaml
personal:
  name: Adarsh Gella
  email: g.adarsh043@gmail.com
  phone: 469-347-2862
  portfolio: https://adarshgella.com
  github: https://github.com/gadarsh043
  linkedin: https://linkedin.com/in/g-adarsh-sonu
  location: United States

skills:
  languages:
    - JavaScript (ES5/ES6)
    - TypeScript
    - Python
    - Java
  frameworks:
    - Express
    - Node.js
    - React.js
    - Vue.js
  tools:
    - Git
    - AWS
    - Docker
    - Kubernetes
```

**Purpose**: Provides structured, easily maintainable personal data.

### requirements.txt - Dependencies
```
flask==3.0.0
flask-cors==4.0.0
pyyaml==6.0.1
firebase-admin==6.4.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

**Purpose**: Specifies exact Python package versions for reproducible deployments.

### vercel.json - Deployment Configuration
```json
{
    "version": 2,
    "builds": [
      {
        "src": "app.py",
        "use": "@vercel/python",
        "config": {
          "maxLambdaSize": "15mb"
        }
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "app.py"
      }
    ],
    "functions": {
      "app.py": {
        "maxDuration": 30
      }
    }
}
```

**Purpose**: Configures serverless deployment on Vercel platform.

---

## 5. System Architecture

### Data Flow
1. **User Input** → Frontend captures question
2. **AJAX Request** → JavaScript sends POST to `/chat`
3. **Flask Routing** → app.py routes to chatbot logic
4. **Response Processing** → chatbot.py processes through:
   - Firebase learned Q&A search
   - Resume YAML matching
   - AI generation via DeepSeek
5. **Response Storage** → New AI responses saved to Firebase
6. **JSON Response** → Flask returns structured response
7. **UI Update** → JavaScript updates chat interface

### Key Features
- **Progressive Learning**: System learns from interactions
- **Multi-source Responses**: Resume, learned, and AI-generated
- **Admin Interface**: Full CRUD for response management
- **Modern UI**: Responsive with smooth animations
- **Error Handling**: Graceful fallbacks for failures
- **Authentication**: Session-based admin access
- **Cloud Integration**: Firebase + Vercel deployment

### Security Considerations
- Session-based authentication for admin
- Environment variables for sensitive data
- Input validation and sanitization
- Error handling without exposing internals
- CORS configuration for API access

This system creates a sophisticated personal assistant that intelligently responds about Adarsh's background while continuously learning and improving through AI generation and admin curation. 