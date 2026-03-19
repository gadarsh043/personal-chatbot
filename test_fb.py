from chatbot import chatbot
if chatbot.firebase_db:
    docs = chatbot.firebase_db.collection('learned_qa').stream()
    for doc in docs:
        print(doc.id, doc.to_dict().get('answer')[:30])
