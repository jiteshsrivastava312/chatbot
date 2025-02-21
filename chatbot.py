import wikipediaapi
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Initialize Wikipedia API with proper User-Agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="MyChatbot/1.0 (Contact: your-email@example.com)"
)

def chatbot_response(message):
    if message.lower().startswith("wiki"):
        query = message[5:].strip()  # Extract query after "wiki "
        return wikipedia_search(query)

    responses = {
        "hello": "Hi there! How can I help you?",
        "how are you": "I'm just a bot, but I'm doing great!",
        "bye": "Goodbye! Have a great day!"
    }
    return responses.get(message.lower(), "I'm not sure how to respond to that.")

def wikipedia_search(query):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:500] + "..."  # Return first 500 characters
    return "No Wikipedia article found for that topic."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Please provide a message."}), 400
    
    response = chatbot_response(data["message"])
    return jsonify({"response": response})

@app.route("/", methods=["GET"])
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot</title>
        <script>
            async function sendMessage() {
                let message = document.getElementById("userMessage").value;
                let response = await fetch("/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({"message": message})
                });
                let data = await response.json();
                document.getElementById("chatbox").innerHTML += "<p><b>You:</b> " + message + "</p>";
                document.getElementById("chatbox").innerHTML += "<p><b>Bot:</b> " + data.response + "</p>";
                document.getElementById("userMessage").value = "";
            }
        </script>
    </head>
    <body>
        <h1>Simple Chatbot</h1>
        <div id="chatbox" style="border:1px solid #000; padding:10px; width:300px; height:300px; overflow:auto;"></div>
        <input type="text" id="userMessage" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
    </body>
    </html>
    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
