from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ✅ Secure API Key Handling
GEMINI_API_KEY = "AIzaSyAy52P5asQzo0AqHrb0zJSQUbFdAcJO6OM"  # ❌ Publicly Leak Mat Karo! Environment Variable Use Karo
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Chatbot logic with structured response
def chatbot_response(user_input):
    try:
        response = model.generate_content(user_input)

        # ✅ Ensure the response is formatted properly
        formatted_response = response.text.replace("\n", "<br>")  # Line Breaks Ke Liye HTML Format
        return f"<b>🤖 Bot:</b><br>{formatted_response}"
    
    except Exception as e:
        return f"<b>🚨 Error:</b> {str(e)}"

# ✅ Route for the home page
@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Chatbot</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial, sans-serif; background-color: #f7f7f7; text-align: center; padding: 30px; }
            .input-container { display: flex; justify-content: center; margin-top: 20px; }
            input, button { padding: 10px; margin: 5px; }
            #chat-box { width: 60%; margin: 20px auto; padding: 10px; background: white; border-radius: 5px; max-height: 400px; overflow-y: auto; text-align: left; }
            .bot-response { color: #0056b3; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>💬 AI Chatbot</h1>
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
                
                chatBox.innerHTML += "<p><b>👤 You:</b> " + userText + "</p>";
                inputField.value = "";

                let response = await fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_input: userText })
                });

                let data = await response.json();
                chatBox.innerHTML += `<p class='bot-response'>${data.response}</p>`;
            }
        </script>
    </body>
    </html>
    '''

# ✅ Route to handle chatbot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
