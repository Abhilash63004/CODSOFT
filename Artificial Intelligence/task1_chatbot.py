"""
CODSOFT AI Internship - Task 1: Rule-Based Chatbot
A simple chatbot using pattern matching and if-else rules.
"""

import re

# Knowledge base with patterns and responses
RESPONSES = {
    "greetings": {
        "patterns": [r"\b(hi|hello|hey|howdy|greetings|good morning|good evening|good afternoon)\b"],
        "responses": [
            "Hello! How can I assist you today? 😊",
            "Hey there! What can I help you with?",
            "Hi! Nice to meet you. How can I help?"
        ]
    },
    "farewell": {
        "patterns": [r"\b(bye|goodbye|see you|take care|exit|quit|cya|farewell)\b"],
        "responses": [
            "Goodbye! Have a great day! 👋",
            "See you later! Take care!",
            "Bye! It was nice chatting with you!"
        ]
    },
    "name": {
        "patterns": [r"\b(what.*(your name)|who are you|introduce yourself)\b"],
        "responses": [
            "I'm ChatBot, your AI assistant built for CodSoft! 🤖",
            "My name is ChatBot! I'm here to help you."
        ]
    },
    "how_are_you": {
        "patterns": [r"\b(how are you|how do you do|how.*(going|doing)|are you (okay|fine|good))\b"],
        "responses": [
            "I'm doing great, thanks for asking! How about you? 😊",
            "I'm just a bot, but I'm functioning perfectly! How can I help?"
        ]
    },
    "age": {
        "patterns": [r"\b(how old are you|what.*(your age)|when were you (born|created|made))\b"],
        "responses": [
            "I was created recently for the CodSoft AI internship! Age is just a number for bots 😄",
            "I'm a brand new chatbot! Fresh out of the code editor."
        ]
    },
    "weather": {
        "patterns": [r"\b(weather|temperature|forecast|rain|sunny|cloudy|hot|cold)\b"],
        "responses": [
            "I don't have access to live weather data, but you can check weather.com for the latest forecast! ⛅",
            "I wish I could tell you the weather, but I don't have internet access. Try a weather app!"
        ]
    },
    "help": {
        "patterns": [r"\b(help|assist|support|what can you do|capabilities|features)\b"],
        "responses": [
            "I can chat with you, answer general questions, tell jokes, and more! Just ask me anything 😊",
            "I'm here to help! You can ask me about: greetings, jokes, time, facts, or just have a conversation!"
        ]
    },
    "joke": {
        "patterns": [r"\b(joke|funny|make me laugh|tell me something funny|humor)\b"],
        "responses": [
            "Why don't scientists trust atoms? Because they make up everything! 😂",
            "Why did the computer go to the doctor? Because it had a virus! 💻😄",
            "What do you call a fake noodle? An Impasta! 🍝😂",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads! 😄"
        ]
    },
    "thanks": {
        "patterns": [r"\b(thank(s| you)|appreciate|grateful|cheers)\b"],
        "responses": [
            "You're welcome! Happy to help 😊",
            "No problem at all! Let me know if you need anything else.",
            "Glad I could help! 🙌"
        ]
    },
    "time": {
        "patterns": [r"\b(what.*(time|date)|current time|today.*(date|day))\b"],
        "responses": ["__TIME__"]  # Special marker for dynamic response
    },
    "ai": {
        "patterns": [r"\b(artificial intelligence|machine learning|deep learning|neural network|what is ai)\b"],
        "responses": [
            "AI (Artificial Intelligence) is the simulation of human intelligence in machines! It includes ML, deep learning, NLP, and more. 🤖",
            "Artificial Intelligence is a fascinating field! It enables machines to learn, reason, and solve problems like humans."
        ]
    },
    "python": {
        "patterns": [r"\b(python|programming|code|coding|developer)\b"],
        "responses": [
            "Python is one of the most popular programming languages for AI! It's clean, readable, and has amazing libraries like TensorFlow, PyTorch, and scikit-learn. 🐍",
            "Great choice for coding! Python is fantastic for AI and data science."
        ]
    },
    "codsoft": {
        "patterns": [r"\b(codsoft|internship|company)\b"],
        "responses": [
            "CodSoft is a great platform for internships! It helps individuals develop leadership skills through mentorship programs, workshops, and collaborative projects. 🚀",
            "CodSoft offers amazing internship opportunities in AI, web development, and more!"
        ]
    }
}

import random
from datetime import datetime

def get_response(user_input: str) -> str:
    """Match user input against patterns and return appropriate response."""
    user_input_lower = user_input.lower().strip()

    # Check for empty input
    if not user_input_lower:
        return "Please say something! I'm here to chat. 😊"

    # Match patterns
    for category, data in RESPONSES.items():
        for pattern in data["patterns"]:
            if re.search(pattern, user_input_lower):
                response = random.choice(data["responses"])
                # Handle dynamic responses
                if response == "__TIME__":
                    now = datetime.now()
                    return f"The current date and time is: {now.strftime('%A, %B %d, %Y at %I:%M %p')} ⏰"
                return response

    # Default fallback response
    fallbacks = [
        "I'm not sure I understand that. Could you rephrase? 🤔",
        "Hmm, that's a tricky one! Try asking me something else.",
        "I don't have an answer for that yet, but I'm always learning! 🤖",
        f"Interesting! I heard: '{user_input}'. But I'm not sure how to respond. Try asking about jokes, weather, or AI!"
    ]
    return random.choice(fallbacks)


def run_chatbot():
    """Main chatbot loop."""
    print("=" * 55)
    print("   🤖  CodSoft AI Internship - Rule-Based ChatBot  🤖")
    print("=" * 55)
    print("  Type 'bye' or 'quit' to exit the chatbot.")
    print("  Type 'help' to see what I can do.")
    print("=" * 55)
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            response = get_response(user_input)
            print(f"Bot: {response}")
            print()

            # Exit conditions
            if re.search(r"\b(bye|goodbye|exit|quit|farewell)\b", user_input.lower()):
                break

        except KeyboardInterrupt:
            print("\nBot: Goodbye! See you next time! 👋")
            break


if __name__ == "__main__":
    run_chatbot()
