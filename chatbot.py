import yaml
import re
from difflib import SequenceMatcher
import random
import requests
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PersonalChatbot:
    def __init__(self, name="AdarshBot"):
        self.name = name
        self.resume = self.load_resume()
        self.firebase_db = self.init_firebase()
        self.learned_qa = self.load_learned_qa()
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
    # ==================== FIREBASE SETUP ====================
    
    def init_firebase(self):
        """Initialize Firebase connection"""
        try:
            if not firebase_admin._apps:
                firebase_key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
                
                # Check if local key file exists
                if os.path.exists(firebase_key_path):
                    cred = credentials.Certificate(firebase_key_path)
                    print("🔑 Using local Firebase key file")
                
                # Check for FIREBASE_CREDENTIALS environment variable (Render setup)
                elif os.getenv('FIREBASE_CREDENTIALS'):
                    try:
                        import json
                        firebase_config = json.loads(os.getenv('FIREBASE_CREDENTIALS'))
                        cred = credentials.Certificate(firebase_config)
                        print("🔑 Using FIREBASE_CREDENTIALS environment variable")
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Error parsing FIREBASE_CREDENTIALS JSON: {e}")
                        return None
                
                # Fallback to individual environment variables (Vercel setup)
                elif os.getenv('FIREBASE_PROJECT_ID'):
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
                    print("🔑 Using individual Firebase environment variables")
                
                else:
                    print("⚠️ No Firebase credentials found. Running without Firebase.")
                    return None
                
                firebase_admin.initialize_app(cred)
            
            db = firestore.client()
            print("✅ Firebase initialized successfully")
            return db
            
        except Exception as e:
            print(f"⚠️ Firebase initialization failed: {e}")
            print("📝 Continuing without Firebase - some features may be limited")
            return None

    def load_learned_qa(self):
        """Load learned Q&A pairs from Firebase"""
        if not self.firebase_db:
            print("📝 Firebase not available - starting with empty Q&A database")
            return {}
        
        try:
            docs = self.firebase_db.collection('learned_qa').stream()
            learned_qa = {}
            for doc in docs:
                data = doc.to_dict()
                learned_qa[doc.id] = data
            print(f"📚 Loaded {len(learned_qa)} learned Q&A pairs from Firebase")
            return learned_qa
        except Exception as e:
            print(f"⚠️ Error loading learned Q&A from Firebase: {e}")
            print("📝 Continuing with empty Q&A database")
            return {}

    def save_learned_qa(self, question, answer, ai_generated=True):
        """Save new Q&A pair to Firebase"""
        if not self.firebase_db:
            print("📝 Firebase not available - cannot save Q&A pair")
            return None
        
        try:
            question_id = re.sub(r'[^a-zA-Z0-9]', '_', question.lower())[:50]
            qa_data = {
                'question': question,
                'answer': answer,
                'ai_generated': ai_generated,
                'reviewed': False,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            self.firebase_db.collection('learned_qa').document(question_id).set(qa_data)
            self.learned_qa[question_id] = qa_data
            print(f"💾 Saved Q&A to Firebase: {question[:50]}...")
            return question_id
        except Exception as e:
            print(f"⚠️ Error saving Q&A to Firebase: {e}")
            print("📝 Q&A not saved but continuing operation")
            return None

    # ==================== RESUME DATA ====================
    
    def load_resume(self):
        """Load resume data from YAML file"""
        try:
            with open("resume.yaml", "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("Warning: resume.yaml not found")
            return {}

    def get_resume_response(self, question):
        """Get predefined response from resume data"""
        question = question.lower()
        
        # Direct keyword matching
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
        
        # Find best match
        best_match = None
        best_score = 0
        
        for keyword, response in responses.items():
            if keyword in question:
                score = SequenceMatcher(None, question, keyword).ratio()
                if score > best_score:
                    best_score = score
                    best_match = response
        
        return best_match if best_score > 0.3 else None

    def format_skills(self):
        """Format skills from resume"""
        skills = self.resume.get('skills', {})
        parts = []
        if 'languages' in skills:
            parts.append(f"Languages: {', '.join(skills['languages'])}")
        if 'frameworks' in skills:
            parts.append(f"Frameworks: {', '.join(skills['frameworks'])}")
        if 'tools' in skills:
            parts.append(f"Tools: {', '.join(skills['tools'])}")
        return ". ".join(parts) if parts else "I have various technical skills!"

    def format_experience(self):
        """Format work experience"""
        experience = self.resume.get('experience', [])
        if experience:
            exp = experience[0]
            return f"I worked as a {exp.get('role', 'role')} at {exp.get('company', 'company')} ({exp.get('duration', 'duration')}). {'. '.join(exp.get('responsibilities', []))}"
        return "I have professional experience in technology and software development."

    def format_projects(self):
        """Format projects"""
        projects = self.resume.get('projects', [])
        if projects:
            project_names = [p.get('name', 'Project') for p in projects]
            return f"I've built projects including: {', '.join(project_names)}. Each taught me valuable skills in development and problem-solving."
        return "I enjoy building projects that solve real problems!"

    def format_education(self):
        """Format education"""
        education = self.resume.get('education', [])
        if education:
            edu = education[0]
            return f"I have a {edu.get('degree', 'degree')} from {edu.get('university', 'university')} ({edu.get('year', 'year')})"
        return "I have a strong educational background in computer science."

    # ==================== AI INTEGRATION ====================
    
    def search_learned_qa(self, question):
        """Search for similar questions in learned Q&A"""
        question_lower = question.lower().strip()
        best_match = None
        best_score = 0
        
        for qa_id, qa_data in self.learned_qa.items():
            stored_question = qa_data['question'].lower()
            similarity = SequenceMatcher(None, question_lower, stored_question).ratio()
            
            # Boost score for exact matches
            if question_lower == stored_question:
                similarity = 1.0
            elif question_lower in stored_question or stored_question in question_lower:
                similarity += 0.3
            
            if similarity > best_score and similarity > 0.7:
                best_score = similarity
                best_match = qa_data
        
        return best_match, best_score

    def generate_ai_response(self, question):
        """Generate AI response using DeepSeek"""
        if not self.deepseek_api_key:
            return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now. Maybe will ask Adarsh to answer that question."
        
        try:
            # Get recent context from learned Q&A pairs
            context_pairs = []
            if self.learned_qa:
                # Sort by created_at and get last 25
                sorted_qa = sorted(
                    self.learned_qa.values(), 
                    key=lambda x: x.get('created_at', datetime.min), 
                    reverse=True
                )[:25]
                
                for qa in sorted_qa:
                    context_pairs.append(f"Q: {qa['question']}\nA: {qa['answer']}")
            
            context_text = "\n\n".join(context_pairs) if context_pairs else "No previous conversations yet."
            
            prompt = f"""You are Adarsh's personal AI assistant. Answer as Adarsh in first person. You should be knowledgeable, engaging, and always connect back to Adarsh's career and expertise.

ABOUT ADARSH:
- Senior Full-stack developer passionate about technology
- Experience at Quinbay building solutions. 
- Skills: JavaScript, Python, React, Vue.js, Node.js, AWS, Docker
- Projects: Bloggers Hub, Photo Share, 3D Tic-Tac-Toe, E-commerce platforms, PortFolio Website, Rizzing App, AI Adventure, Cow Bull Game, Quinbay
- Based in the United States, open to opportunities
- Enjoys building innovative solutions and solving complex problems

INSTRUCTIONS:
1. Answer ANY question asked with genuine knowledge and enthusiasm
2. Provide interesting facts, insights, or personal touches when possible
3. ALWAYS smoothly transition to how this relates to Adarsh's skills or career
4. Be conversational, smart, and personable
5. If the question is about technology/programming, emphasize Adarsh's expertise
6. Check the previous conversations below to avoid repeating answers

PREVIOUS CONVERSATIONS (last 25):
{context_text}

CURRENT QUESTION: {question}

EXAMPLE RESPONSES:
Q: "Do you know India?"
A: "Absolutely! India is an incredible country with a rich cultural heritage and a booming tech industry. Did you know India produces more IT graduates than any other country? Speaking of tech talent, that's exactly the kind of innovative environment that shaped Adarsh's problem-solving approach. His experience building scalable solutions at Quinbay really benefits from that global tech perspective. Are you interested in learning about his international development experience?"

Q: "Do you know cooking?"  
A: "I love the art of cooking! It's all about following recipes, experimenting with ingredients, and creating something amazing - just like coding! Fun fact: the best chefs are often great at debugging recipes when something goes wrong. That's actually similar to how Adarsh approaches software development - methodical, creative, and always iterating to perfection. His React and Node.js projects require the same attention to detail as a perfect dish. What kind of technical 'recipes' would you like to know about?"

Now answer the current question following this style - be knowledgeable, engaging, and smoothly redirect to Adarsh's career (max 60 words, don't mention word count):"""

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
                print(f"🤖 Generated AI response for: {question[:50]}...")
                return ai_answer
            else:
                print(f"⚠️ DeepSeek API error: {response.status_code}")
                return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now. Maybe will ask Adarsh to answer that question."
                
        except Exception as e:
            print(f"⚠️ AI generation error: {e}")
            return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now as i am having trouble. Maybe will ask Adarsh to answer that question."

    # ==================== MAIN RESPONSE LOGIC ====================
    
    def get_response(self, question):
        """Main method to get chatbot response"""
        if not question:
            return "Hi! I'm Adarsh's AI assistant. Ask me about his skills, projects, or experience!"
        
        question = question.strip()
        
        # 1. Check Firebase learned Q&A (only if Firebase is available)
        if self.firebase_db:
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
        
        # Save to Firebase if available
        if self.firebase_db:
            self.save_learned_qa(question, ai_response, ai_generated=True)
            ai_response += "<br><p style='font-size: 0.8em; color: #666; font-style: italic; margin-top: 10px;'>💡 This answer was AI-generated. I'm always learning and improving my responses!</p>"
        else:
            ai_response += "<br><p style='font-size: 0.8em; color: #666; font-style: italic; margin-top: 10px;'>💡 This answer was AI-generated. Note: Learning features are currently limited.</p>"
        
        return ai_response

# Create chatbot instance
chatbot = PersonalChatbot("AdarshBot")

# Compatibility function
def get_response(question):
    return chatbot.get_response(question)