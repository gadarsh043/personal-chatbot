import yaml
import re
from difflib import SequenceMatcher
import random
import requests
import json
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnhancedPersonalChatbot:
    def __init__(self, name="AdarshBot"):
        self.name = name
        self.resume = None
        self.responses = {}
        self.personality_responses = {}
        self.conversation_starters = []
        self.firebase_db = None
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"
        
        # Initialize Firebase
        self.init_firebase()
        
        # Load data
        self.load_resume_data()
        self.setup_personality()
        self.setup_responses()
        
        # Load learned Q&A from Firebase
        self.learned_qa = self.load_learned_qa()
    
    def init_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # For local development, use service account key
                firebase_key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
                if os.path.exists(firebase_key_path):
                    cred = credentials.Certificate(firebase_key_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # For production, use environment variables
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
            
            self.firebase_db = firestore.client()
            print("✅ Firebase initialized successfully")
        except Exception as e:
            print(f"⚠️ Firebase initialization failed: {e}")
            print("📝 Continuing without Firebase - learned Q&A will not persist")
            self.firebase_db = None
    
    def load_learned_qa(self):
        """Load previously learned Q&A pairs from Firebase"""
        learned_qa = {}
        if not self.firebase_db:
            return learned_qa
        
        try:
            docs = self.firebase_db.collection('learned_qa').stream()
            for doc in docs:
                data = doc.to_dict()
                learned_qa[doc.id] = {
                    'question': data.get('question', ''),
                    'answer': data.get('answer', ''),
                    'ai_generated': data.get('ai_generated', False),
                    'reviewed': data.get('reviewed', False),
                    'created_at': data.get('created_at'),
                    'updated_at': data.get('updated_at')
                }
            print(f"📚 Loaded {len(learned_qa)} learned Q&A pairs from Firebase")
        except Exception as e:
            print(f"⚠️ Error loading learned Q&A: {e}")
        
        return learned_qa
    
    def save_learned_qa(self, question, answer, ai_generated=True):
        """Save new Q&A pair to Firebase"""
        if not self.firebase_db:
            print("⚠️ Firebase not available - cannot save learned Q&A")
            return None
        
        try:
            # Create a unique ID based on question
            question_id = re.sub(r'[^a-zA-Z0-9]', '_', question.lower())[:50]
            
            qa_data = {
                'question': question,
                'answer': answer,
                'ai_generated': ai_generated,
                'reviewed': False,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Save to Firebase
            doc_ref = self.firebase_db.collection('learned_qa').document(question_id)
            doc_ref.set(qa_data)
            
            # Update local cache
            self.learned_qa[question_id] = qa_data
            
            print(f"💾 Saved new Q&A to Firebase: {question[:50]}...")
            return question_id
        except Exception as e:
            print(f"⚠️ Error saving learned Q&A: {e}")
            return None
    
    def generate_ai_response(self, question):
        """Generate response using DeepSeek AI with Firebase context"""
        if not self.deepseek_api_key:
            return self.generate_fallback_response(question)
        
        try:
            # Create context about Adarsh for the AI
            context = self.build_ai_context()
            
            # Add Firebase learned Q&A context
            firebase_context = self.build_firebase_context()
            
            prompt = f"""You are Adarsh's AI assistant. Based on the context below, answer the question as if you are representing Adarsh professionally.

CONTEXT ABOUT ADARSH:
{context}

PREVIOUS CONVERSATIONS (for reference only):
{firebase_context}

QUESTION: {question}

INSTRUCTIONS:
- Answer in first person as Adarsh
- Be professional but conversational
- If the question is similar to previous conversations, you can reference that knowledge
- If the question is not directly related to Adarsh's background, politely redirect to his professional expertise
- Keep responses concise but informative (max 150 words)
- Show enthusiasm for technology and development
- If you don't have specific information, be honest but offer related information you do have

ANSWER:"""

            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 300,
                'temperature': 0.7
            }
            
            response = requests.post(self.deepseek_api_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                ai_answer = result['choices'][0]['message']['content'].strip()
                print(f"🤖 Generated AI response for: {question[:50]}...")
                return ai_answer
            else:
                print(f"⚠️ DeepSeek API error: {response.status_code}")
                return self.generate_fallback_response(question)
                
        except Exception as e:
            print(f"⚠️ Error generating AI response: {e}")
            return self.generate_fallback_response(question)
    
    def build_ai_context(self):
        """Build context about Adarsh for AI responses"""
        context_parts = []
        
        if self.resume:
            # Personal info
            personal = self.resume.get('personal', {})
            if personal:
                context_parts.append(f"Name: {personal.get('name', 'Adarsh')}")
                context_parts.append(f"Location: {personal.get('location', '')}")
                context_parts.append(f"Email: {personal.get('email', '')}")
                context_parts.append(f"Phone: {personal.get('phone', '')}")
                context_parts.append(f"Favorite color: {personal.get('favorite_color', 'red')}")
            
            # Skills
            skills = self.resume.get('skills', {})
            if skills:
                context_parts.append(f"Programming Languages: {', '.join(skills.get('languages', []))}")
                context_parts.append(f"Frameworks: {', '.join(skills.get('frameworks', []))}")
                context_parts.append(f"Tools: {', '.join(skills.get('tools', []))}")
            
            # Experience
            experience = self.resume.get('experience', [])
            if experience:
                exp = experience[0]
                context_parts.append(f"Current/Recent Role: {exp.get('role', '')} at {exp.get('company', '')} ({exp.get('duration', '')})")
                context_parts.append(f"Responsibilities: {'. '.join(exp.get('responsibilities', []))}")
            
            # Education
            education = self.resume.get('education', [])
            if education:
                edu = education[0]
                context_parts.append(f"Education: {edu.get('degree', '')} from {edu.get('university', '')} ({edu.get('year', '')})")
            
            # Projects
            projects = self.resume.get('projects', [])
            if projects:
                project_names = [p.get('name', '') for p in projects[:3]]  # Top 3 projects
                context_parts.append(f"Key Projects: {', '.join(project_names)}")
        
        # Add personality traits
        context_parts.extend([
            "Personality: Passionate about full-stack development, loves solving complex problems",
            "Interests: Cloud technologies, AI/ML integration, scalable architectures",
            "Work Style: Collaborative, agile methodologies, continuous learning",
            "Career Goals: Building products that scale globally and impact millions of users"
        ])
        
        return '\n'.join(context_parts)
    
    def build_firebase_context(self):
        """Build context from Firebase learned Q&A for AI reference"""
        if not self.learned_qa:
            return "No previous conversations available."
        
        context_parts = []
        # Limit to most recent or relevant Q&A pairs
        for qa_id, qa_data in list(self.learned_qa.items())[:25]:  # Last 25 Q&A pairs
            question = qa_data.get('question', '')
            answer = qa_data.get('answer', '')
            if question and answer:
                context_parts.append(f"Q: {question}\nA: {answer}")
        
        if context_parts:
            return "\n\n".join(context_parts)
        else:
            return "No previous conversations available."
    
    def generate_fallback_response(self, question):
        """Generate a fallback response when AI is not available"""
        fallback_responses = [
            f"That's an interesting question about '{question}'! While I don't have specific information on that topic, I'd love to tell you about my experience in full-stack development, my projects at Quinbay, or my technical skills. What aspect of my background would you like to explore?",
            f"Great question! Though I might not have details on '{question}' specifically, I'm passionate about technology and always learning. Feel free to ask me about my programming skills, recent projects, or what drives me as a developer.",
            f"I appreciate your question about '{question}'! While that's not something I have specific information on, I'm excited to share about my journey in tech, my experience building scalable applications, or my work with modern frameworks. What interests you most?",
            f"Interesting question! While I might not have specific details about '{question}', I can tell you about my technical expertise, my experience at Quinbay where I built solutions for 10,000+ users, or my passion for cloud technologies. What would you like to know?"
        ]
        return random.choice(fallback_responses)
    
    def load_resume_data(self):
        """Load resume data from YAML file"""
        try:
            with open("resume.yaml", "r") as file:
                self.resume = yaml.safe_load(file)
        except FileNotFoundError:
            print("Warning: resume.yaml not found")
            self.resume = {}
    
    def _format_skills(self):
        """Format skills from the nested structure in resume.yaml"""
        skills = self.resume.get('skills', {})
        if not skills:
            return "I have various technical skills that I'm passionate about!"
        
        skill_parts = []
        if 'languages' in skills:
            skill_parts.append(f"Programming Languages: {', '.join(skills['languages'])}")
        if 'frameworks' in skills:
            skill_parts.append(f"Frameworks & Technologies: {', '.join(skills['frameworks'])}")
        if 'tools' in skills:
            skill_parts.append(f"Tools: {', '.join(skills['tools'])}")
        if 'practices' in skills:
            skill_parts.append(f"Practices: {', '.join(skills['practices'])}")
        
        return ". ".join(skill_parts)
    
    def setup_personality(self):
        """Setup personality-driven responses to make the chatbot more conversational"""
        self.personality_responses = {
            # Professional personality
            "motivation": "I'm driven by the challenge of solving complex problems and creating solutions that make a real impact. There's nothing quite like the feeling of seeing your code come to life and help thousands of users!",
            "passion": "I'm passionate about full-stack development and cloud technologies. I love how technology can transform ideas into reality and connect people across the globe.",
            "learning": "I'm always learning! Currently exploring advanced cloud architectures and AI/ML integration. The tech world moves fast, and I enjoy staying on the cutting edge.",
            "teamwork": "I believe great software is built by great teams. I enjoy collaborating, sharing knowledge, and learning from others. My experience at Quinbay taught me the value of clear communication and agile methodologies.",
            
            # Personal touches
            "coffee": "I'm definitely a coffee person! ☕ It fuels my coding sessions, especially during those late-night debugging marathons.",
            "music": "I often code with music - it helps me get into the flow state. Usually something instrumental or lo-fi beats.",
            "weekend": "On weekends, you'll find me either working on side projects, reading tech blogs, or exploring new frameworks. I also enjoy hiking when I need to disconnect and recharge.",
            "advice": "My advice to fellow developers: never stop building. Side projects are where you truly learn and experiment with new technologies without constraints.",
            
            # Career insights
            "goals": "My goal is to work on products that scale globally and impact millions of users. I'm particularly interested in roles where I can architect solutions and mentor other developers.",
            "challenge": "One of my biggest challenges was optimizing the Quinbay platform for 10,000+ concurrent users. It taught me the importance of scalable architecture and performance optimization.",
            "proud": "I'm most proud of the Seller Shipping Voucher UI I built at Quinbay - seeing 10,000+ sellers adopt it within a month was incredibly rewarding!",
        }
        
        self.conversation_starters = [
            "Feel free to ask me about my projects, experience, or even what drives me as a developer!",
            "I'd love to tell you about my journey from building personal projects to working with enterprise-scale applications.",
            "Ask me anything - from technical skills to what I'm passionate about in the tech world!",
            "I'm here to chat about my experience, projects, or what it's like working in full-stack development.",
        ]
    
    def setup_responses(self):
        """Setup predefined responses based on resume data"""
        if not self.resume:
            return
            
        self.responses = {
            # Personal information with personality
            "name": f"Hi! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')} - nice to meet you! 👋",
            "location": f"I'm based in {self.resume.get('personal', {}).get('location', 'the United States')}, but I'm open to remote opportunities worldwide!",
            "color": f"My favorite color is {self.resume.get('personal', {}).get('favorite_color', 'red')} - it represents energy and passion, which I bring to everything I do! 🔴",
            
            # Contact with professional tone
            "email": f"You can reach me at {self.resume.get('personal', {}).get('email', 'my email')} - I typically respond within 24 hours!",
            "phone": f"Feel free to call me at {self.resume.get('personal', {}).get('phone', 'my number')} for a quick chat!",
            "contact": f"I'd love to connect! Reach me at {self.resume.get('personal', {}).get('email', 'my email')} or {self.resume.get('personal', {}).get('phone', 'my phone')}. I'm always open to discussing new opportunities!",
            "portfolio": f"Check out my work at {self.resume.get('personal', {}).get('portfolio', 'my website')} - I've showcased my best projects there!",
            "github": f"You can see my code and contributions at {self.resume.get('personal', {}).get('github', 'my GitHub')} - I believe in open source and sharing knowledge!",
            "linkedin": f"Let's connect professionally on LinkedIn: {self.resume.get('personal', {}).get('linkedin', 'my LinkedIn profile')}",
            
            # Education with context
            "education": self._format_education_with_personality(),
            "degree": self._format_education_with_personality(),
            "university": self._format_education_with_personality(),
            "college": self._format_education_with_personality(),
            
            # Skills with enthusiasm
            "skills": f"I'm excited to share my technical expertise! {self._format_skills()}",
            "technologies": f"I work with a diverse tech stack: {self._format_skills()}",
            "programming": f"Programming is my passion! {self._format_skills()}",
            "languages": f"I'm proficient in several programming languages: {', '.join(self.resume.get('skills', {}).get('languages', []))}. Each one has its strengths for different use cases!",
            "frameworks": f"I love working with modern frameworks: {', '.join(self.resume.get('skills', {}).get('frameworks', []))}. They help me build robust, scalable applications quickly!",
            "tools": f"My development toolkit includes: {', '.join(self.resume.get('skills', {}).get('tools', []))}. The right tools make all the difference in productivity!",
            
            # Projects with storytelling
            "projects": self._format_projects_with_stories(),
            "photoshare": self._get_project_story("PhotoShare"),
            "mushroom": self._get_project_story("Mushroom Classification"),
            "quinbay": self._get_project_story("Quinbay"),
            
            # Experience with insights
            "experience": self._format_experience_with_insights(),
            "work": self._format_experience_with_insights(),
            "job": self._format_experience_with_insights(),
            
            # Conversational greetings
            "hello": f"Hello there! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')}, a passionate full-stack developer. {random.choice(self.conversation_starters)}",
            "hi": f"Hi! Great to meet you! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')}. {random.choice(self.conversation_starters)}",
            "hey": f"Hey! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')} - thanks for stopping by! What would you like to know about my journey in tech?",
            "help": "I'm here to chat about anything - my technical skills, project experiences, career journey, or even what drives me as a developer. What interests you most?",
            
            # Add personality responses to main responses
            **self.personality_responses
        }
    
    def _format_education_with_personality(self):
        """Format education with personal touch"""
        education = self.resume.get('education', [])
        if education:
            edu = education[0]
            return f"I earned my {edu.get('degree', 'degree')} from {edu.get('university', 'university')} ({edu.get('year', 'year')}). It gave me a solid foundation in computer science, but I've learned the most through hands-on projects and real-world experience!"
        return "My educational background in technology has been complemented by continuous learning through projects and industry experience!"
    
    def _format_projects_with_stories(self):
        """Format projects with engaging descriptions"""
        projects = self.resume.get('projects', [])
        if projects:
            project_names = [p.get('name', 'Project') for p in projects]
            return f"I've built some exciting projects that I'm really proud of: {', '.join(project_names)}. Each one taught me something new and pushed my skills further. Which one would you like to hear about?"
        return "I love building projects that solve real problems - it's where I learn the most!"
    
    def _get_project_story(self, project_name):
        """Get project description with personal story"""
        projects = self.resume.get('projects', [])
        for project in projects:
            if project_name.lower() in project.get('name', '').lower():
                description = project.get('description', f"I worked on {project_name}")
                technologies = project.get('technologies', [])
                impact = project.get('impact', '')
                
                story = f"{description}"
                if technologies:
                    story += f" I built this using {', '.join(technologies)}"
                if impact:
                    story += f" The result? {impact}"
                story += f" It was a great learning experience that challenged me to think about scalability and user experience!"
                return story
        return f"I have experience with {project_name} - it was an interesting project that taught me a lot about problem-solving!"
    
    def _format_experience_with_insights(self):
        """Format work experience with personal insights"""
        experience = self.resume.get('experience', [])
        if experience:
            exp = experience[0]
            responsibilities = '. '.join(exp.get('responsibilities', []))
            return f"I had an amazing experience as a {exp.get('role', 'role')} at {exp.get('company', 'company')} ({exp.get('duration', 'duration')}). {responsibilities} What I loved most was seeing the direct impact of my work - having 10,000+ sellers adopt the UI I built was incredibly fulfilling!"
        return "I have professional experience in technology where I've learned the importance of building user-centric solutions!"
    
    def similarity(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def search_learned_qa(self, question):
        """Search for similar questions in learned Q&A with strict matching"""
        question_lower = question.lower().strip()
        best_match = None
        best_score = 0
        
        print(f"🔍 Searching learned Q&A for: '{question}'")
        print(f"📚 Available Q&A pairs: {len(self.learned_qa)}")
        
        for qa_id, qa_data in self.learned_qa.items():
            stored_question = qa_data['question'].lower()
            
            # Calculate base similarity
            similarity_score = self.similarity(question_lower, stored_question)
            
            # Only proceed if there's reasonable base similarity
            if similarity_score < 0.3:
                continue
            
            # Check for exact phrase matches (high confidence)
            if question_lower == stored_question:
                similarity_score = 1.0
            elif question_lower in stored_question or stored_question in question_lower:
                similarity_score += 0.3
            
            # Keyword matching with stricter criteria
            question_words = set(word for word in question_lower.split() if len(word) > 3)
            stored_words = set(word for word in stored_question.split() if len(word) > 3)
            common_words = question_words.intersection(stored_words)
            
            # Only boost if significant word overlap
            if common_words and len(common_words) >= 2:
                keyword_boost = len(common_words) / max(len(question_words), len(stored_words))
                similarity_score += keyword_boost * 0.2
            
            print(f"  📝 '{stored_question[:50]}...' -> Score: {similarity_score:.3f}")
            
            # Much higher threshold for strict matching
            if similarity_score > best_score and similarity_score > 0.7:
                best_score = similarity_score
                best_match = qa_data
                print(f"  ✅ New best match! Score: {best_score:.3f}")
        
        if best_match:
            print(f"🎯 Found match with score {best_score:.3f}")
        else:
            print("❌ No suitable match found")
        
        return best_match, best_score
    
    def get_response(self, question):
        """Enhanced get response with AI learning capability"""
        if not question:
            return "I'm here and ready to chat! What would you like to know about me?"
        
        question_lower = question.lower().strip()
        
        # Handle common conversational patterns
        if any(greeting in question_lower for greeting in ['how are you', 'how\'s it going', 'what\'s up']):
            return "I'm doing great, thanks for asking! I'm always excited to talk about technology and my projects. What brings you here today?"
        
        if any(word in question_lower for word in ['tell me about yourself', 'who are you', 'introduce yourself']):
            return f"I'm {self.resume.get('personal', {}).get('name', 'Adarsh')}, a passionate full-stack developer who loves building scalable web applications. I recently worked at Quinbay where I built UI solutions used by thousands of sellers. I'm always excited about new technologies and love solving complex problems. What would you like to know more about?"
        
        # 1. First check learned Q&A from Firebase (strict matching)
        learned_match, learned_score = self.search_learned_qa(question)
        if learned_match and learned_score > 0.7:  # Higher threshold for strict matching
            print(f"📚 Found learned answer for: {question[:50]}...")
            response = learned_match['answer']
            if learned_match['ai_generated'] and not learned_match['reviewed']:
                response += "<br><p style='font-size: 0.8em; color: #666; font-style: italic; margin-top: 10px;'>💡 This answer was AI-generated and may be updated as I learn more!</p>"
            return response
        
        # 2. Check predefined responses from resume.yaml
        best_match = None
        best_score = 0
        
        for keyword, response in self.responses.items():
            # Check if keyword is in the question
            if keyword in question_lower:
                score = self.similarity(question_lower, keyword)
                if score > best_score:
                    best_score = score
                    best_match = response
        
        # If no direct match, try fuzzy matching
        if best_score < 0.3:
            for keyword, response in self.responses.items():
                score = self.similarity(question_lower, keyword)
                if score > best_score:
                    best_score = score
                    best_match = response
        
        # 3. If good match found in predefined responses, return it
        if best_match and best_score > 0.4:
            print(f"📋 Using resume-based response for: {question[:50]}...")
            return best_match
        
        # 4. If no good match, use AI to generate response and save it
        print(f"🤖 Generating AI response for new question: {question[:50]}...")
        ai_response = self.generate_ai_response(question)
        
        # Save the new Q&A pair to Firebase for future learning
        self.save_learned_qa(question, ai_response, ai_generated=True)
        
        # Add indicator that this is AI-generated
        ai_response += "<br><p style='font-size: 0.8em; color: #666; font-style: italic; margin-top: 10px;'>💡 This answer was AI-generated. I'm always learning and improving my responses!</p>"
        
        return ai_response

# Create enhanced chatbot instance
chatbot = EnhancedPersonalChatbot("AdarshBot")

# Function to get chatbot response (maintaining compatibility with existing code)
def get_response(question):
    return chatbot.get_response(question)