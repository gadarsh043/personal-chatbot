import yaml
import re
from difflib import SequenceMatcher
import random
import requests
import os
from datetime import datetime, timezone
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
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
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
        if 'tools_and_technologies' in skills:
            parts.append(f"Tools: {', '.join(skills['tools_and_technologies'])}")
        return " | ".join(parts) if parts else "I have various technical skills!"

    def format_experience(self):
        """Format work experience"""
        experience = self.resume.get('experience', [])
        if experience:
            # Show the most recent experience (first in list)
            exp = experience[0]
            role = exp.get('role', 'Developer')
            company = exp.get('company', 'company')
            duration = exp.get('duration', 'duration')
            responsibilities = exp.get('responsibilities', [])
            
            if responsibilities:
                return f"I'm currently working as a {role} at {company} ({duration}). {'. '.join(responsibilities[:2])}."
            return f"I'm currently working as a {role} at {company} ({duration})."
        return "I have professional experience in technology and software development."

    def format_projects(self):
        """Format projects"""
        projects = self.resume.get('projects', [])
        if projects:
            project_names = [p.get('name', 'Project') for p in projects[:5]]
            return f"I've built projects including: {', '.join(project_names)}. Each taught me valuable skills in development and problem-solving."
        return "I enjoy building projects that solve real problems!"

    def format_education(self):
        """Format education"""
        education = self.resume.get('education', [])
        if education:
            # Show the most recent education (Master's degree)
            edu = education[0]
            degree = edu.get('degree', 'degree')
            university = edu.get('university', 'university')
            year = edu.get('year', 'year')
            gpa = edu.get('gpa', '')
            location = edu.get('location', '')
            
            if gpa and gpa != 'Pursuing':
                return f"I'm pursuing a {degree} from {university} in {location} ({year}) with a GPA of {gpa}."
            return f"I'm pursuing a {degree} from {university} in {location} ({year})."
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

    def get_dynamic_prompt_context(self):
        """Build a dynamic prompt context from resume YAML"""
        # Personal
        personal = self.resume.get('personal', {})
        bio = personal.get('summary', '')
        
        # Education
        education = self.resume.get('education', [{}])[0]
        edu_str = f"{education.get('degree')} at {education.get('university')} ({education.get('year')})"
        
        # Experience
        experience = self.resume.get('experience', [{}])[0]
        exp_str = f"{experience.get('role')} at {experience.get('company')}"
        
        # Projects (Top 5)
        projects = self.resume.get('projects', [])[:5]
        projects_str = "\n".join([f"- {p.get('name')}: {p.get('description')} (Live: {p.get('live', 'N/A')})" for p in projects])
        
        # Skills
        skills = self.resume.get('skills', {})
        langs = ", ".join(skills.get('languages', []))
        frameworks = ", ".join(skills.get('frameworks', []))
        tools = ", ".join(skills.get('tools_and_technologies', []))
        
        # Personal Facts
        facts = self.resume.get('personal_facts', {})
        facts_str = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in facts.items()])
        
        # Career Goals
        goals = self.resume.get('career_goals', {})
        goals_str = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in goals.items()])
        
        return f"""
ABOUT ADARSH:
- {bio}
- Current Education: {edu_str}
- Latest Experience: {exp_str}

TOP 5 PROJECTS:
{projects_str}

CORE SKILLS:
- Languages: {langs}
- Frameworks: {frameworks}
- Tools: {tools}

PERSONAL FACTS ABOUT ADARSH:
{facts_str}

CAREER GOALS:
{goals_str}
"""

    def generate_ai_response(self, question):
        """Generate AI response using GROQ"""
        if not self.groq_api_key:
            return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now. Maybe will ask Adarsh to answer that question."
        
        try:
            # Get recent context from learned Q&A pairs
            context_pairs = []
            if self.learned_qa:
                # Sort by created_at and get last 25
                sorted_qa = sorted(
                    self.learned_qa.values(), 
                    key=lambda x: x.get('created_at') or datetime.now(timezone.utc), 
                    reverse=True
                )[:25]
                
                for qa in sorted_qa:
                    context_pairs.append(f"Q: {qa['question']}\nA: {qa['answer']}")
            
            context_text = "\n\n".join(context_pairs) if context_pairs else "No previous conversations yet."
            
            # Build dynamic prompt
            dynamic_context = self.get_dynamic_prompt_context()
            
            prompt = f"""You are Adarsh's personal AI assistant. Answer as Adarsh in first person ("I", "my"). You should be knowledgeable, engaging, and redirect to Adarsh's career when relevant.

LIVE SOURCES (direct visitors here for more info if they ask):
- Portfolio: https://adarshgella.com
- GitHub: https://github.com/gadarsh043
- LinkedIn: https://linkedin.com/in/g-adarsh-sonu
- YouTube: https://www.youtube.com/@g_adarsh_sonu

{dynamic_context}

PREVIOUS CONVERSATIONS (last 25):
{context_text}

INSTRUCTIONS:
1. Answer ANY question asked with genuine knowledge and enthusiasm.
2. Provide interesting facts, insights, or personal touches when possible based on the PERSONAL FACTS.
3. ALWAYS smoothly transition to how this relates to Adarsh's skills or projects when appropriate.
4. Be conversational, smart, and personable. Feel free to use markdown formatting like tables, bold text, or lists if it makes the answer better.
5. If the question is about technology/programming, emphasize Adarsh's expertise.
6. When answering personal questions, use the PERSONAL FACTS provided.
7. Keep responses concise (under 80 words) but impactful. Do not mention word limits.
8. Check the previous conversations below to avoid repeating answers exactly.

CURRENT QUESTION: {question}"""

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.groq_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama-3.3-70b-versatile',
                    'messages': [{'role': 'system', 'content': prompt}],
                    'max_tokens': 500,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                ai_answer = response.json()['choices'][0]['message']['content'].strip()
                print(f"🤖 Generated AI response for: {question[:50]}...")
                return ai_answer
            else:
                print(f"⚠️ GROQ API error: {response.status_code}")
                try:
                    print(response.json())
                except:
                    pass
                return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now. Maybe will ask Adarsh to answer that question."
                
        except requests.exceptions.Timeout:
            print("⚠️ API request timed out")
            return f"That's a great question about '{question}'! It's taking me a little too long to think of the perfect answer right now. Could you ask me something else?"
            
        except Exception as e:
            print(f"⚠️ AI generation error: {e}")
            return f"That's a great question about '{question}'! While I'm here to share Adarsh's incredible journey in technology. I don't think I can answer that question right now as I am having trouble. Maybe will ask Adarsh to answer that question."

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
                    response += "\n\n*💡 This answer was AI-generated and may be updated as I learn more!*"
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
            ai_response += "\n\n*💡 This answer was AI-generated. I'm always learning and improving my responses!*"
        else:
            ai_response += "\n\n*💡 This answer was AI-generated. Note: Learning features are currently limited.*"
        
        return ai_response

# Create chatbot instance
chatbot = PersonalChatbot("AdarshBot")

# Compatibility function
def get_response(question):
    return chatbot.get_response(question)
