import yaml
import re
from difflib import SequenceMatcher
import random

class PersonalChatbot:
    def __init__(self, name="AdarshBot"):
        self.name = name
        self.resume = None
        self.responses = {}
        self.personality_responses = {}
        self.conversation_starters = []
        self.load_resume_data()
        self.setup_personality()
        self.setup_responses()
    
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
    
    def get_response(self, question):
        """Get response for a given question with personality"""
        if not question:
            return "I'm here and ready to chat! What would you like to know about me?"
        
        question_lower = question.lower().strip()
        
        # Handle common conversational patterns
        if any(greeting in question_lower for greeting in ['how are you', 'how\'s it going', 'what\'s up']):
            return "I'm doing great, thanks for asking! I'm always excited to talk about technology and my projects. What brings you here today?"
        
        if any(word in question_lower for word in ['tell me about yourself', 'who are you', 'introduce yourself']):
            return f"I'm {self.resume.get('personal', {}).get('name', 'Adarsh')}, a passionate full-stack developer who loves building scalable web applications. I recently worked at Quinbay where I built UI solutions used by thousands of sellers. I'm always excited about new technologies and love solving complex problems. What would you like to know more about?"
        
        # Direct keyword matching
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
        
        # Return best match or engaging fallback
        if best_match and best_score > 0.2:
            return best_match
        else:
            fallback_responses = [
                "That's an interesting question! While I might not have a specific answer for that, I'd love to tell you about my experience in full-stack development or my recent projects. What aspect of my background interests you most?",
                "I'm not sure about that specific topic, but I'm passionate about technology and always learning! Feel free to ask me about my skills, projects, or what drives me as a developer.",
                "Great question! Though I might not have that particular information, I'm excited to share about my journey in tech. Ask me about my projects, experience, or even what I'm currently learning!",
                f"Hmm, that's not something I have details on, but here's a fun fact: my favorite color is {self.resume.get('personal', {}).get('favorite_color', 'red')}! 😊 What would you like to know about my technical background?"
            ]
            return random.choice(fallback_responses)

# Create chatbot instance
chatbot = PersonalChatbot("AdarshBot")

# Function to get chatbot response (maintaining compatibility with existing code)
def get_response(question):
    return chatbot.get_response(question)