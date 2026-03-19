import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'llama-3.3-70b-versatile',
    'messages': [{'role': 'system', 'content': 'You are a helpful assistant. Answer the following: hello'}],
    'max_tokens': 100
}

r = requests.post(url, headers=headers, json=data)
print(r.status_code)
print(r.text)
