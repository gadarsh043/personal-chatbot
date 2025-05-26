from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import yaml

# Create a new chatbot
chatbot = ChatBot("AdarshBot")

# Load resume data
with open("resume.yaml", "r") as file:
    resume = yaml.safe_load(file)

# Create training data from resume
training_data = [
    "What is your name?", resume["personal"]["name"],
    "Where are you located?", resume["personal"]["location"],
    "What is your favorite color?", resume["personal"]["favorite_color"],
    "What is your education?", f"I have a {resume['education'][0]['degree']} from {resume['education'][0]['university']} ({resume['education'][0]['year']}).",
    "What are your skills?", ", ".join(resume["skills"]),
    "Tell me about PhotoShare", resume["projects"][0]["description"],
    "Tell me about Mushroom Classification", resume["projects"][1]["description"],
    "Tell me about Quinbay", resume["projects"][2]["description"],
    "What is your experience?", f"I worked as a {resume['experience'][0]['role']} at {resume['experience'][0]['company']} ({resume['experience'][0]['duration']}). Responsibilities: {', '.join(resume['experience'][0]['responsibilities'])}"
]

# Train the chatbot
trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Function to get chatbot response
def get_response(question):
    response = chatbot.get_response(question)
    # Fallback for unknown questions
    if response.confidence < 0.5:
        return "I'm not sure about that, but I can tell you more about my skills or projects! For now, here's a fun fact: I like the color red."
    return str(response)