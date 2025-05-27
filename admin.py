from flask import Flask, render_template, request, jsonify, redirect, url_for
from chatbot import chatbot
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to manage learned Q&A pairs"""
    if not chatbot.firebase_db:
        return render_template('admin/error.html', 
                             error="Firebase not configured. Cannot access learned Q&A data.")
    
    # Get all learned Q&A pairs
    learned_qa = []
    try:
        docs = chatbot.firebase_db.collection('learned_qa').order_by('created_at', direction='DESCENDING').stream()
        for doc in docs:
            data = doc.to_dict()
            learned_qa.append({
                'id': doc.id,
                'question': data.get('question', ''),
                'answer': data.get('answer', ''),
                'ai_generated': data.get('ai_generated', False),
                'reviewed': data.get('reviewed', False),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            })
    except Exception as e:
        return render_template('admin/error.html', 
                             error=f"Error loading Q&A data: {str(e)}")
    
    return render_template('admin/dashboard.html', learned_qa=learned_qa)

@app.route('/admin/edit/<qa_id>')
def edit_qa(qa_id):
    """Edit a specific Q&A pair"""
    if not chatbot.firebase_db:
        return redirect(url_for('admin_dashboard'))
    
    try:
        doc = chatbot.firebase_db.collection('learned_qa').document(qa_id).get()
        if not doc.exists:
            return redirect(url_for('admin_dashboard'))
        
        qa_data = doc.to_dict()
        qa_data['id'] = qa_id
        
        return render_template('admin/edit.html', qa=qa_data)
    except Exception as e:
        return render_template('admin/error.html', 
                             error=f"Error loading Q&A: {str(e)}")

@app.route('/admin/update/<qa_id>', methods=['POST'])
def update_qa(qa_id):
    """Update a Q&A pair"""
    if not chatbot.firebase_db:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()
        
        if not question or not answer:
            return jsonify({'error': 'Question and answer are required'}), 400
        
        # Update in Firebase
        update_data = {
            'question': question,
            'answer': answer,
            'reviewed': True,
            'updated_at': datetime.now()
        }
        
        chatbot.firebase_db.collection('learned_qa').document(qa_id).update(update_data)
        
        # Update local cache
        if qa_id in chatbot.learned_qa:
            chatbot.learned_qa[qa_id].update(update_data)
        
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        return jsonify({'error': f'Error updating Q&A: {str(e)}'}), 500

@app.route('/admin/delete/<qa_id>', methods=['POST'])
def delete_qa(qa_id):
    """Delete a Q&A pair"""
    if not chatbot.firebase_db:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        # Delete from Firebase
        chatbot.firebase_db.collection('learned_qa').document(qa_id).delete()
        
        # Remove from local cache
        if qa_id in chatbot.learned_qa:
            del chatbot.learned_qa[qa_id]
        
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        return jsonify({'error': f'Error deleting Q&A: {str(e)}'}), 500

@app.route('/admin/add', methods=['GET', 'POST'])
def add_qa():
    """Add a new Q&A pair manually"""
    if request.method == 'GET':
        return render_template('admin/add.html')
    
    if not chatbot.firebase_db:
        return jsonify({'error': 'Firebase not configured'}), 500
    
    try:
        question = request.form.get('question', '').strip()
        answer = request.form.get('answer', '').strip()
        
        if not question or not answer:
            return render_template('admin/add.html', 
                                 error='Question and answer are required')
        
        # Save to Firebase
        qa_id = chatbot.save_learned_qa(question, answer, ai_generated=False)
        
        if qa_id:
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/add.html', 
                                 error='Error saving Q&A pair')
    except Exception as e:
        return render_template('admin/add.html', 
                             error=f'Error adding Q&A: {str(e)}')

@app.route('/admin/stats')
def admin_stats():
    """Show statistics about learned Q&A"""
    if not chatbot.firebase_db:
        return render_template('admin/error.html', 
                             error="Firebase not configured.")
    
    try:
        # Get statistics
        total_qa = len(chatbot.learned_qa)
        ai_generated = sum(1 for qa in chatbot.learned_qa.values() if qa.get('ai_generated', False))
        reviewed = sum(1 for qa in chatbot.learned_qa.values() if qa.get('reviewed', False))
        manual = total_qa - ai_generated
        
        stats = {
            'total_qa': total_qa,
            'ai_generated': ai_generated,
            'manual': manual,
            'reviewed': reviewed,
            'unreviewed': total_qa - reviewed
        }
        
        return render_template('admin/stats.html', stats=stats)
    except Exception as e:
        return render_template('admin/error.html', 
                             error=f"Error loading statistics: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5001) 