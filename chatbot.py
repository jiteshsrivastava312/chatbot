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
        <title>ChatGPT Interface</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial, sans-serif; background-color: #f7f7f7; text-align: center; padding: 50px; }
            .input-container { display: flex; justify-content: center; margin-top: 20px; }
            input, button { padding: 10px; margin: 5px; }
            #chat-box { width: 60%; margin: 20px auto; padding: 10px; background: white; border-radius: 5px; max-height: 400px; overflow-y: auto; }
        </style>
    </head>
    <body>
        <h1>AI Chatbot</h1>
        <div id="chat-box"></div>
        <div class="input-container">
            <input id="user-input" type="text" placeholder="Ask anything..." />
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
            async function sendMessage() {
                let inputField = document.getElementById("user-input");
                let chatBox = document.getElementById("chat-box");
                let userText = inputField.value.trim();
                
                if (userText === "") return;
                
                chatBox.innerHTML += "<p><b>You:</b> " + userText + "</p>";
                inputField.value = "";

                let response = await fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_input: userText })
                });

                let data = await response.json();
                chatBox.innerHTML += "<p><b>Bot:</b> " + data.response + "</p>";
            }
        </script>
    </body>
    </html>
    ''')
# Route to handle chatbot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    # Run the app on 0.0.0.0 (accessible from any device on the network)
    app.run(host="0.0.0.0", port=5000, debug=True)
