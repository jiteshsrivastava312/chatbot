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
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: #fff;
            }

            .chat-container {
                width: 400px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                overflow: hidden;
                display: flex;
                flex-direction: column;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .chat-header {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: #fff;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }

            .chat-messages {
                flex: 1;
                padding: 15px;
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
                background: #007bff;
                align-self: flex-end;
                color: #fff;
            }

            .bot-message {
                background: rgba(255, 255, 255, 0.2);
                align-self: flex-start;
                color: #fff;
            }

            .chat-input {
                display: flex;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
            }

            .chat-input input {
                flex: 1;
                padding: 10px;
                border: none;
                border-radius: 10px;
                outline: none;
                background: rgba(255, 255, 255, 0.2);
                color: #fff;
                font-size: 16px;
            }

            .chat-input input::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }

            .chat-input button {
                padding: 10px 15px;
                background: #007bff;
                border: none;
                border-radius: 10px;
                color: #fff;
                cursor: pointer;
                margin-left: 10px;
                transition: background 0.3s ease;
            }

            .chat-input button:hover {
                background: #0056b3;
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
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }

            .chat-messages::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 10px;
            }

            .chat-messages::-webkit-scrollbar-thumb:hover {
                background: rgba(255, 255, 255, 0.5);
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
