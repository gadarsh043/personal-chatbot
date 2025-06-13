from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from chatbot import chatbot, get_response
from datetime import datetime
from functools import wraps

app = Flask(__name__)
# Configure CORS to allow all origins and methods
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
app.secret_key = 'chatbot-admin-secret-key-2024'

# Admin password
ADMIN_PASSWORD = 'Adarsh232774'

# ==================== AUTHENTICATION ====================

def login_required(f):
    """Decorator to require login for admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login page"""
    if request.method == "POST":
        password = request.form.get("password", "")
        
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Successfully logged in!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid password!", "error")
    
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash("Successfully logged out!", "success")
    return redirect(url_for("admin_login"))

# ==================== CHATBOT ROUTES ====================

@app.route("/")
def index():
    """Main chat interface"""
    return render_template("index.html")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    """Handle chat messages"""
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json()
    question = data.get("question", "")
    response = get_response(question)
    return jsonify({"response": response})

# ==================== ADMIN ROUTES ====================

def handle_firebase_error():
    """Handle Firebase connection errors"""
    if not chatbot.firebase_db:
        return render_template("admin/error.html", error="Firebase not connected")
    return None

@app.route("/admin")
@login_required
def admin_dashboard():
    """Admin dashboard - view all Q&A pairs"""
    error = handle_firebase_error()
    if error:
        return error
    
    try:
        docs = chatbot.firebase_db.collection('learned_qa').stream()
        qa_pairs = []
        
        for doc in docs:
            data = doc.to_dict()
            qa_pairs.append({
                'id': doc.id,
                'question': data.get('question', ''),
                'answer': data.get('answer', ''),
                'ai_generated': data.get('ai_generated', False),
                'reviewed': data.get('reviewed', False),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            })
        
        qa_pairs.sort(key=lambda x: x.get('created_at') or datetime.min, reverse=True)
        return render_template("admin/dashboard.html", qa_pairs=qa_pairs)
    
    except Exception as e:
        return render_template("admin/error.html", error=f"Error: {str(e)}")

@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def admin_add():
    """Add new Q&A pair"""
    if request.method == "GET":
        return render_template("admin/add.html")
    
    # POST request
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()
    
    if not question or not answer:
        flash("Both question and answer are required!", "error")
        return redirect(url_for("admin_add"))
    
    error = handle_firebase_error()
    if error:
        flash("Firebase not connected!", "error")
        return redirect(url_for("admin_add"))
    
    try:
        doc_id = question.lower().replace(" ", "_").replace("?", "").replace("!", "")[:50]
        qa_data = {
            'question': question,
            'answer': answer,
            'ai_generated': False,
            'reviewed': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        chatbot.firebase_db.collection('learned_qa').document(doc_id).set(qa_data)
        flash("Q&A pair added successfully!", "success")
        return redirect(url_for("admin_dashboard"))
        
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("admin_add"))

@app.route("/admin/edit/<qa_id>", methods=["GET", "POST"])
@login_required
def admin_edit(qa_id):
    """Edit existing Q&A pair"""
    error = handle_firebase_error()
    if error:
        return error
    
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()
        reviewed = request.form.get("reviewed") == "on"
        
        if not question or not answer:
            flash("Both question and answer are required!", "error")
            return redirect(url_for("admin_edit", qa_id=qa_id))
        
        try:
            chatbot.firebase_db.collection('learned_qa').document(qa_id).update({
                'question': question,
                'answer': answer,
                'reviewed': reviewed,
                'updated_at': datetime.now()
            })
            
            flash("Q&A pair updated successfully!", "success")
            return redirect(url_for("admin_dashboard"))
            
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("admin_edit", qa_id=qa_id))
    
    # GET request
    try:
        doc = chatbot.firebase_db.collection('learned_qa').document(qa_id).get()
        if not doc.exists:
            return render_template("admin/error.html", error="Q&A pair not found")
        
        qa_data = doc.to_dict()
        qa_data['id'] = doc.id
        return render_template("admin/edit.html", qa=qa_data)
        
    except Exception as e:
        return render_template("admin/error.html", error=f"Error: {str(e)}")

@app.route("/admin/delete/<qa_id>", methods=["POST"])
@login_required
def admin_delete(qa_id):
    """Delete Q&A pair"""
    error = handle_firebase_error()
    if error:
        flash("Firebase not connected!", "error")
        return redirect(url_for("admin_dashboard"))
    
    try:
        chatbot.firebase_db.collection('learned_qa').document(qa_id).delete()
        flash("Q&A pair deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/stats")
@login_required
def admin_stats():
    """Statistics dashboard"""
    error = handle_firebase_error()
    if error:
        return error
    
    try:
        docs = chatbot.firebase_db.collection('learned_qa').stream()
        
        total_qa = 0
        ai_generated = 0
        reviewed = 0
        
        for doc in docs:
            data = doc.to_dict()
            total_qa += 1
            if data.get('ai_generated', False):
                ai_generated += 1
            if data.get('reviewed', False):
                reviewed += 1
        
        stats = {
            'total_qa': total_qa,
            'ai_generated': ai_generated,
            'manual': total_qa - ai_generated,
            'reviewed': reviewed,
            'unreviewed': total_qa - reviewed
        }
        
        return render_template("admin/stats.html", stats=stats)
        
    except Exception as e:
        return render_template("admin/error.html", error=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, port=5002)