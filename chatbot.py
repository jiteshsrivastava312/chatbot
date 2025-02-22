import nltk
from nltk.chat.util import Chat, reflections

# Define pairs of patterns and responses
pairs = [
    [
        r"hi|hello|hey",
        ["Hello! How can I help you today?", "Hi there! How can I assist you?"]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you! How about you?", "I'm just a bot, but I'm great! How are you?"]
    ],
    [
        r"what is your name ?",
        ["I'm a simple chatbot. You can call me ChatBot!", "I don't have a name, but you can call me ChatBot!"]
    ],
    [
        r"bye|goodbye",
        ["Goodbye! Have a great day!", "Bye! Take care!"]
    ],
    [
        r"help",
        ["I can help you with basic questions. Just ask me anything!", "Sure, how can I assist you?"]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that. Can you please rephrase?"]
    ]
]

# Create a Chat object
chatbot = Chat(pairs, reflections)

# Start the conversation
def chat():
    print("ChatBot: Hello! I'm your friendly chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "goodbye"]:
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = chatbot.respond(user_input)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    chat()
