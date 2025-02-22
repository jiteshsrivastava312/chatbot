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
        <title>ChatBot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .chat-container {
                width: 400px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
            .chat-header {
                background-color: #007bff;
                color: #fff;
                padding: 15px;
                text-align: center;
                font-size: 18px;
            }
            .chat-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                border-bottom: 1px solid #ddd;
            }
            .chat-input {
                display: flex;
                border-top: 1px solid #ddd;
            }
            .chat-input input {
                flex: 1;
                padding: 10px;
                border: none;
                outline: none;
            }
            .chat-input button {
                padding: 10px 15px;
                background-color: #007bff;
                color: #fff;
                border: none;
                cursor: pointer;
            }
            .message {
                margin-bottom: 10px;
            }
            .user-message {
                text-align: right;
                color: #007bff;
            }
            .bot-message {
                text-align: left;
                color: #333;
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
