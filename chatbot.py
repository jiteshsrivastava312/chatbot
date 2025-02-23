from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Configure DeepSeek API
DeepSeek_API_KEY = "sk-0065948518d44372a46c45abb72b9166"  # Replace with your DeepSeek API key
client = OpenAI(api_key=DeepSeek_API_KEY, base_url="https://api.deepseek.com")

# Chatbot logic using DeepSeek API
def chatbot_response(user_input):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )
        return response.choices[0].message.content
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
    <title>DeepSeek ChatBot</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: url('https://source.unsplash.com/1600x900/?technology,ai') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .chat-container {
            width: 90%;
            max-width: 900px;
            height: 80vh;
            display: flex;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }

        .chat-main {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding-left: 10px;
        }

        .chat-header {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            padding: 10px 0;
            color: white;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            padding-bottom: 10px;
        }

        .message {
            max-width: 80%;
            padding: 12px;
            border-radius: 15px;
            margin: 5px 0;
            font-size: 14px;
            animation: fadeIn 0.3s ease-in-out;
        }

        .user-message {
            background: #0078ff;
            color: white;
            align-self: flex-end;
        }

        .bot-message {
            background: rgba(255, 255, 255, 0.8);
            color: black;
            align-self: flex-start;
        }

        .chat-input {
            display: flex;
            border-top: 1px solid rgba(255, 255, 255, 0.3);
            padding: 10px;
        }

        .chat-input input {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 10px;
            outline: none;
            font-size: 14px;
            background: rgba(255, 255, 255, 0.6);
        }

        .chat-input button {
            margin-left: 10px;
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: #0078ff;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }

        .chat-input button:hover {
            background: #0056b3;
        }

        .new-chat-button {
            margin-top: 10px;
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: #ff4757;
            color: white;
            cursor: pointer;
            text-align: center;
            transition: 0.3s;
        }

        .new-chat-button:hover {
            background: #d63031;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-main">
            <div class="chat-header">ChatBot</div>
            <div class="chat-messages" id="chat-messages"></div>
            <div class="chat-input">
                <input type="text" id="user-input" placeholder="Ask something...">
                <button onclick="sendMessage()">Send</button>
            </div>
            <button class="new-chat-button" onclick="startNewChat()">New Chat</button>
        </div>
    </div>
    <script>
        function sendMessage() {
            const userInput = document.getElementById("user-input").value;
            if (userInput.trim() === "") return;
            const chatMessages = document.getElementById("chat-messages");
            const userMessage = document.createElement("div");
            userMessage.className = "message user-message";
            userMessage.textContent = userInput;
            chatMessages.appendChild(userMessage);
            document.getElementById("user-input").value = "";
            fetch("/get_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_input: userInput }),
            })
            .then(response => response.json())
            .then(data => {
                const botMessage = document.createElement("div");
                botMessage.className = "message bot-message";
                botMessage.textContent = data.response;
                chatMessages.appendChild(botMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
        }
        function startNewChat() {
            document.getElementById("chat-messages").innerHTML = "";
        }
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
    app.run(host="0.0.0.0", port=5000, debug=True)
