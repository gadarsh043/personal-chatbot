#!/usr/bin/env python3
"""
Script to extract information from resume.pdf and enhance resume.yaml
"""

import PyPDF2
import yaml
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def parse_resume_text(text):
    """Parse resume text and extract structured information"""
    if not text:
        return {}
    
    # Clean up text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Extract phone numbers
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    
    # Extract LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
    
    # Extract GitHub
    github_pattern = r'github\.com/[\w-]+'
    github = re.findall(github_pattern, text, re.IGNORECASE)
    
    # Extract education (look for degree keywords)
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'institute']
    education_sections = []
    
    # Extract experience (look for job titles and companies)
    experience_keywords = ['developer', 'engineer', 'analyst', 'manager', 'intern', 'consultant']
    
    # Extract skills (look for technical keywords)
    skill_keywords = [
        'javascript', 'python', 'java', 'react', 'node', 'angular', 'vue',
        'html', 'css', 'sql', 'mongodb', 'postgresql', 'aws', 'azure',
        'docker', 'kubernetes', 'git', 'agile', 'scrum'
    ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return {
        'emails': emails,
        'phones': [phone[0] + phone[1] if len(phone) > 1 else phone for phone in phones],
        'linkedin': linkedin,
        'github': github,
        'found_skills': found_skills,
        'raw_text': text
    }

def enhance_resume_yaml(extracted_data, current_yaml_path='resume.yaml'):
    """Enhance the existing resume.yaml with extracted data"""
    
    # Load current resume.yaml
    try:
        with open(current_yaml_path, 'r') as file:
            current_resume = yaml.safe_load(file)
    except FileNotFoundError:
        current_resume = {}
    
    # Enhance personal section
    if 'personal' not in current_resume:
        current_resume['personal'] = {}
    
    if extracted_data.get('emails'):
        current_resume['personal']['email'] = extracted_data['emails'][0]
    
    if extracted_data.get('phones'):
        current_resume['personal']['phone'] = extracted_data['phones'][0]
    
    if extracted_data.get('linkedin'):
        current_resume['personal']['linkedin'] = f"https://{extracted_data['linkedin'][0]}"
    
    if extracted_data.get('github'):
        current_resume['personal']['github'] = f"https://{extracted_data['github'][0]}"
    
    # Add extracted skills to existing skills
    if extracted_data.get('found_skills'):
        if 'skills' not in current_resume:
            current_resume['skills'] = {'languages': [], 'frameworks': [], 'tools': [], 'practices': []}
        
        # Categorize found skills
        programming_langs = ['Python', 'Javascript', 'Java', 'Html', 'Css', 'Sql']
        frameworks = ['React', 'Node', 'Angular', 'Vue', 'Mongodb', 'Postgresql']
        tools = ['Git', 'Docker', 'Kubernetes', 'Aws', 'Azure']
        practices = ['Agile', 'Scrum']
        
        for skill in extracted_data['found_skills']:
            if skill in programming_langs and skill not in current_resume['skills']['languages']:
                current_resume['skills']['languages'].append(skill)
            elif skill in frameworks and skill not in current_resume['skills']['frameworks']:
                current_resume['skills']['frameworks'].append(skill)
            elif skill in tools and skill not in current_resume['skills']['tools']:
                current_resume['skills']['tools'].append(skill)
            elif skill in practices and skill not in current_resume['skills']['practices']:
                current_resume['skills']['practices'].append(skill)
    
    return current_resume

def save_enhanced_resume(enhanced_resume, output_path='resume_enhanced.yaml'):
    """Save the enhanced resume to a new YAML file"""
    with open(output_path, 'w') as file:
        yaml.dump(enhanced_resume, file, default_flow_style=False, sort_keys=False, indent=2)

def main():
    print("🔍 Extracting information from resume.pdf...")
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf('resume.pdf')
    
    if not pdf_text:
        print("❌ Could not extract text from PDF")
        return
    
    print("✅ Successfully extracted text from PDF")
    print(f"📄 Extracted {len(pdf_text)} characters")
    
    # Parse the extracted text
    print("\n🔍 Parsing resume information...")
    extracted_data = parse_resume_text(pdf_text)
    
    # Display found information
    print("\n📋 Found Information:")
    if extracted_data.get('emails'):
        print(f"📧 Email(s): {', '.join(extracted_data['emails'])}")
    if extracted_data.get('phones'):
        print(f"📞 Phone(s): {', '.join(extracted_data['phones'])}")
    if extracted_data.get('linkedin'):
        print(f"💼 LinkedIn: {', '.join(extracted_data['linkedin'])}")
    if extracted_data.get('github'):
        print(f"🐙 GitHub: {', '.join(extracted_data['github'])}")
    if extracted_data.get('found_skills'):
        print(f"🛠️  Skills found: {', '.join(extracted_data['found_skills'])}")
    
    # Enhance existing resume.yaml
    print("\n🔧 Enhancing resume.yaml...")
    enhanced_resume = enhance_resume_yaml(extracted_data)
    
    # Save enhanced version
    save_enhanced_resume(enhanced_resume, 'resume_enhanced.yaml')
    print("✅ Enhanced resume saved as 'resume_enhanced.yaml'")
    
    # Show raw text for manual review
    print(f"\n📄 Raw extracted text (first 500 chars):")
    print("=" * 50)
    print(pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text)
    print("=" * 50)
    
    print("\n💡 Next steps:")
    print("1. Review 'resume_enhanced.yaml' for accuracy")
    print("2. Manually add any missing information")
    print("3. Replace 'resume.yaml' with enhanced version if satisfied")

if __name__ == "__main__":
    main() 