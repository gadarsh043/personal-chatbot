#!/usr/bin/env python3
"""
Test script for the personal chatbot
"""

from chatbot import get_response

def test_chatbot():
    """Test various chatbot responses"""
    test_questions = [
        "What is your name?",
        "Where are you located?",
        "What is your favorite color?",
        "What are your skills?",
        "Tell me about your education",
        "What projects have you worked on?",
        "Tell me about PhotoShare",
        "What is your work experience?",
        "Hello",
        "Help",
        "Random question that shouldn't match anything"
    ]
    
    print("🤖 Testing Personal Chatbot")
    print("=" * 50)
    
    for question in test_questions:
        response = get_response(question)
        print(f"Q: {question}")
        print(f"A: {response}")
        print("-" * 30)

if __name__ == "__main__":
    test_chatbot() 