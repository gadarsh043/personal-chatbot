import yaml
import re
from difflib import SequenceMatcher

class SimpleBot:
    def __init__(self, name="AdarshBot"):
        self.name = name
        self.resume = None
        self.responses = {}
        self.load_resume_data()
        self.setup_responses()
    
    def load_resume_data(self):
        """Load resume data from YAML file"""
        try:
            with open("resume.yaml", "r") as file:
                self.resume = yaml.safe_load(file)
        except FileNotFoundError:
            print("Warning: resume.yaml not found")
            self.resume = {}
    
    def setup_responses(self):
        """Setup predefined responses based on resume data"""
        if not self.resume:
            return
            
        self.responses = {
            # Personal information
            "name": f"My name is {self.resume.get('personal', {}).get('name', 'Adarsh')}",
            "location": f"I'm located in {self.resume.get('personal', {}).get('location', 'Unknown')}",
            "color": f"My favorite color is {self.resume.get('personal', {}).get('favorite_color', 'red')}",
            
            # Education
            "education": self._format_education(),
            "degree": self._format_education(),
            "university": self._format_education(),
            "college": self._format_education(),
            
            # Skills
            "skills": f"My skills include: {', '.join(self.resume.get('skills', []))}",
            "technologies": f"I work with: {', '.join(self.resume.get('skills', []))}",
            
            # Projects
            "projects": self._format_projects(),
            "photoshare": self._get_project_description("PhotoShare"),
            "mushroom": self._get_project_description("Mushroom Classification"),
            "quinbay": self._get_project_description("Quinbay"),
            
            # Experience
            "experience": self._format_experience(),
            "work": self._format_experience(),
            "job": self._format_experience(),
            
            # Greetings and general
            "hello": f"Hello! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')}. Ask me about my skills, projects, or experience!",
            "hi": f"Hi there! I'm {self.resume.get('personal', {}).get('name', 'Adarsh')}. What would you like to know about me?",
            "help": "You can ask me about my name, location, education, skills, projects, or work experience!",
        }
    
    def _format_education(self):
        """Format education information"""
        education = self.resume.get('education', [])
        if education:
            edu = education[0]
            return f"I have a {edu.get('degree', 'degree')} from {edu.get('university', 'university')} ({edu.get('year', 'year')})"
        return "I have educational background in technology"
    
    def _format_projects(self):
        """Format projects information"""
        projects = self.resume.get('projects', [])
        if projects:
            project_names = [p.get('name', 'Project') for p in projects]
            return f"I've worked on several projects including: {', '.join(project_names)}"
        return "I have experience with various projects"
    
    def _get_project_description(self, project_name):
        """Get specific project description"""
        projects = self.resume.get('projects', [])
        for project in projects:
            if project_name.lower() in project.get('name', '').lower():
                return project.get('description', f"I worked on {project_name}")
        return f"I have experience with {project_name}"
    
    def _format_experience(self):
        """Format work experience"""
        experience = self.resume.get('experience', [])
        if experience:
            exp = experience[0]
            responsibilities = ', '.join(exp.get('responsibilities', []))
            return f"I worked as a {exp.get('role', 'role')} at {exp.get('company', 'company')} ({exp.get('duration', 'duration')}). Responsibilities: {responsibilities}"
        return "I have professional experience in technology"
    
    def similarity(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def get_response(self, question):
        """Get response for a given question"""
        if not question:
            return "Please ask me something!"
        
        question_lower = question.lower().strip()
        
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
        
        # Return best match or fallback
        if best_match and best_score > 0.2:
            return best_match
        else:
            return "I'm not sure about that, but I can tell you more about my skills, projects, or experience! For now, here's a fun fact: I like the color red."

# Create chatbot instance
chatbot = SimpleBot("AdarshBot")

# Function to get chatbot response (maintaining compatibility with existing code)
def get_response(question):
    return chatbot.get_response(question)