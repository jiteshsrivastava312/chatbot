from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyALzptugTlxe8CNQr2WR5xrmxQr3Kjy7m8"  # Replace with your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Chatbot logic using Gemini API
def chatbot_response(user_input):
    try:
        # Send user input to Gemini API
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Route for the home page
@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatBot with Gemini</title>
        <style>
            /* General Styles */
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #f0f4f8, #d9e2ec); /* Light gradient background */
                margin: 0;
                color: #333; /* Dark text for contrast */
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .chat-container {
                width: 100%; /* Full width */
                height: 100vh; /* Full height */
                background: rgba(255, 255, 255, 0.9); /* Semi-transparent white background */
                display: flex;
                flex-direction: column;
            }

            .chat-header {
                background: rgba(255, 255, 255, 0.9); /* Semi-transparent white */
                padding: 15px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: #333; /* Dark text */
                border-bottom: 1px solid rgba(0, 0, 0, 0.1); /* Light border */
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
            }

            .chat-messages {
                flex: 1;
                padding: 80px 15px 70px; /* Adjust padding for header and input */
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .message {
                max-width: 80%;
                padding: 10px 15px;
                border-radius: 15px;
                animation: fadeIn 0.5s ease-in-out;
            }

            .user-message {
                background: #007bff; /* Blue for user messages */
                align-self: flex-end;
                color: #fff;
            }

            .bot-message {
                background: rgba(0, 0, 0, 0.05); /* Light gray for bot messages */
                align-self: flex-start;
                color: #333; /* Dark text */
            }

            .chat-input {
                display: flex;
                border-top: 1px solid rgba(0, 0, 0, 0.1); /* Light border */
                padding: 10px;
                background: rgba(255, 255, 255, 0.9); /* Semi-transparent white */
                position: fixed;
                bottom: 0;
                width: 100%;
                z-index: 1000;
            }

            .chat-input input {
                flex: 1;
                padding: 10px;
                border: none;
                border-radius: 10px;
                outline: none;
                background: rgba(255, 255, 255, 0.9); /* Semi-transparent white */
                color: #333; /* Dark text */
                font-size: 16px;
            }

            .chat-input input::placeholder {
                color: rgba(0, 0, 0, 0.5); /* Light placeholder text */
            }

            .chat-input button {
                padding: 10px 15px;
                background: #007bff; /* Blue button */
                border: none;
                border-radius: 10px;
                color: #fff;
                cursor: pointer;
                margin-left: 10px;
                transition: background 0.3s ease;
            }

            .chat-input button:hover {
                background: #0056b3; /* Darker blue on hover */
            }

            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Scrollbar Styles */
            .chat-messages::-webkit-scrollbar {
                width: 8px;
            }

            .chat-messages::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.1); /* Light track */
                border-radius: 10px;
            }

            .chat-messages::-webkit-scrollbar-thumb {
                background: rgba(0, 0, 0, 0.3); /* Light thumb */
                border-radius: 10px;
            }

            .chat-messages::-webkit-scrollbar-thumb:hover {
                background: rgba(0, 0, 0, 0.5); /* Darker thumb on hover */
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">ChatBot with Gemini</div>
            <div class="chat-messages" id="chat-messages"></div>
            <div class="chat-input">
                <input type="text" id="user-input" placeholder="Type a message...">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            function sendMessage() {
                const userInput = document.getElementById("user-input").value;
                if (userInput.trim() === "") return;

                // Display user message
                const chatMessages = document.getElementById("chat-messages");
                const userMessage = document.createElement("div");
                userMessage.className = "message user-message";
                userMessage.textContent = userInput;
                chatMessages.appendChild(userMessage);

                // Clear input
                document.getElementById("user-input").value = "";

                // Fetch bot response
                fetch("/get_response", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ user_input: userInput }),
                })
                .then(response => response.json())
                .then(data => {
                    const botMessage = document.createElement("div");
                    botMessage.className = "message bot-message";
                    botMessage.textContent = data.response;
                    chatMessages.appendChild(botMessage);

                    // Scroll to bottom
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                });
            }

            // Allow pressing Enter to send message
            document.getElementById("user-input").addEventListener("keyup", function(event) {
                if (event.key === "Enter") {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    '''

# Route to handle chatbot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    # Run the app on 0.0.0.0 (accessible from any device on the network)
    app.run(host="0.0.0.0", port=5000, debug=True)
