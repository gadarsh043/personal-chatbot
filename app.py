from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import get_response

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow embedding

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/widget")
def widget():
    """Serve the embeddable chat widget"""
    return render_template("widget.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    response = get_response(question)
    return jsonify({"response": response})

@app.route("/embed.js")
def embed_script():
    """Serve the JavaScript embed script for external websites"""
    script = f"""
(function() {{
    // Create and inject the widget iframe
    const widget = document.createElement('iframe');
    widget.src = '{request.url_root}widget';
    widget.style.cssText = `
        position: fixed !important;
        bottom: 0 !important;
        right: 0 !important;
        width: 100% !important;
        height: 100% !important;
        border: none !important;
        z-index: 999999 !important;
        pointer-events: none !important;
        background: transparent !important;
    `;
    widget.id = 'adarsh-chat-widget';
    
    // Make only the widget interactive
    widget.onload = function() {{
        widget.style.pointerEvents = 'auto';
    }};
    
    document.body.appendChild(widget);
}})();
"""
    return script, 200, {'Content-Type': 'application/javascript'}

if __name__ == "__main__":
    app.run(debug=True)