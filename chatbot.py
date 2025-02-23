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
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 50px;
        }
        header {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 800px;
            margin-bottom: 20px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }
        .input-container {
            display: flex;
            align-items: center;
            width: 100%;
            max-width: 800px;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            background: white;
        }
        .input-container input {
            flex: 1;
            border: none;
            outline: none;
            padding: 10px;
            border-radius: 5px 0 0 5px;
        }
        .button {
            border: none;
            background: transparent;
            cursor: pointer;
            padding: 10px;
        }
        .button:hover {
            background-color: #f0f0f0;
        }
        .options {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
            width: 100%;
            max-width: 800px;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <header>
        <div>ChatGPT</div>
        <div>
            <button class="button">Log in</button>
            <button class="button">Sign up</button>
        </div>
    </header>
    
    <h1>What can I help with?</h1>
    
    <div class="input-container">
        <input type="text" placeholder="Ask anything" />
        <button class="button"><i class="fas fa-paperclip"></i></button>
        <button class="button"><i class="fas fa-search"></i></button>
        <button class="button"><i class="fas fa-question-circle"></i></button>
        <button class="button">Voice</button>
    </div>
    
    <div class="options">
        <button class="button">Analyze images</button>
        <button class="button">Brainstorm</button>
        <button class="button">Surprise me</button>
        <button class="button">Make a plan</button>
        <button class="button">Code</button>
        <button class="button">More</button>
    </div>
    
    <div class="footer">
        By messaging ChatGPT, you agree to our <a href="#">Terms</a> and have read our <a href="#">Privacy Policy</a>.
    </div>
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
