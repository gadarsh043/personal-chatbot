# 🤖 Enhanced AI Chatbot - 2-Way Learning System

A sophisticated conversational AI chatbot that **learns and improves over time** using DeepSeek AI and Firebase. Perfect for portfolio websites to engage recruiters 24/7 with intelligent, personality-driven responses.

## 🌟 Key Features

### 🧠 **2-Way Learning System**
- **Learns from new questions** automatically
- **AI-powered responses** for unknown questions using DeepSeek
- **Persistent storage** with Firebase Firestore
- **Admin interface** to review and edit AI responses
- **Continuous improvement** through human feedback

### 🤖 **AI Integration**
- **DeepSeek AI** for intelligent response generation
- **Context-aware** responses based on resume data
- **Personality-driven** conversations
- **Professional tone** suitable for recruiters

### 🎨 **Chat Interface**
- **Beautiful, modern design** with emerald green & teal theme
- **Responsive layout** for all devices
- **Professional interface** optimized for recruiters
- **Smooth animations** and intuitive user experience

### 🔥 **Firebase Backend**
- **Real-time learning** with Firestore database
- **Scalable architecture** for high traffic
- **Secure data storage** with proper authentication
- **Analytics tracking** for conversation insights

## 🚀 Quick Start

### 1. **Clone & Install**
```bash
git clone <repository>
cd personal-chatbot
pip install -r requirements.txt
```

### 2. **Set Up DeepSeek AI**
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create account and get API key
3. Check your credits at https://platform.deepseek.com/usage

### 3. **Configure Environment**
Create `.env` file:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
FIREBASE_KEY_PATH=firebase-key.json  # Optional
```

### 4. **Run the System**
```bash
# Main chatbot application
python app.py

# Admin interface (separate terminal)
python admin.py
```

### 5. **Access Interfaces**
- **Chat Interface**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5001/admin

## 🎯 How It Works

### **Question Processing Flow**
```
User Question
     ↓
1. Check Firebase learned Q&A
     ↓ (if not found)
2. Check resume.yaml responses  
     ↓ (if not found)
3. Generate AI response with DeepSeek
     ↓
4. Save to Firebase for future learning
     ↓
5. Return response to user
```

### **Learning Process**
1. **Unknown question** triggers AI response generation
2. **AI response** is saved to Firebase with metadata
3. **Admin review** allows editing and approval
4. **Future similar questions** use learned responses
5. **System improves** over time through feedback

## 🛠 Admin Interface

Access at `http://localhost:5001/admin`

### **Features:**
- 📊 **Dashboard**: View all learned Q&A pairs
- ✏️ **Edit**: Modify AI-generated responses
- ➕ **Add**: Create manual Q&A pairs
- 🗑️ **Delete**: Remove unwanted entries
- 📈 **Statistics**: Track learning progress

### **Q&A Management:**
- **AI-generated** responses marked for review
- **Manual responses** created by admin
- **Review status** tracking (reviewed/unreviewed)
- **Timestamp tracking** for all changes

## 🌐 Deployment

### **Vercel Deployment**
1. Set environment variables in Vercel dashboard
2. Deploy with `vercel --prod`
3. Configure Firebase security rules
4. Monitor usage and performance

### **Environment Variables for Production:**
```env
DEEPSEEK_API_KEY=your_api_key
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_email
# ... other Firebase variables
```

## 📱 Portfolio Integration

### **Direct Integration**
The chatbot runs at the main route (`/`) and provides a beautiful, responsive chat interface that you can:

1. **Embed directly** in your portfolio using an iframe
2. **Link to directly** from your portfolio 
3. **Integrate as a popup/modal** in your existing website

### **Simple Integration Example**
```html
<!-- Link to your chatbot -->
<a href="https://your-chatbot-url.com" target="_blank" class="chat-button">
    💬 Chat with Adarsh
</a>

<!-- Or embed as iframe -->
<iframe 
    src="https://your-chatbot-url.com" 
    width="450" 
    height="600"
    frameborder="0"
    title="Chat with Adarsh - AI Assistant">
</iframe>
```

### **Features:**
- **Professional appearance** optimized for recruiters
- **Suggestion chips** for common questions
- **Typing indicators** for better UX
- **Smooth animations** and modern design
- **Mobile responsive** with automatic adjustments

## 🎨 Customization

### **Color Scheme**
The system uses a professional portfolio color palette:
```css
:root {
    --primary-color: #2ecc71;    /* Emerald Green */
    --secondary-color: #008080;   /* Deep Teal */
    --dark-neutral: #2c3e50;     /* Charcoal Grey */
    --light-neutral: #f7f9f9;    /* Soft Ivory */
    --highlight-color: #f1c40f;  /* Amber Yellow */
    --error-color: #e74c3c;      /* Burnt Orange */
}
```

### **Personality Customization**
Edit `chatbot.py` to modify AI personality and responses.

## 📊 Analytics & Monitoring

### **DeepSeek Usage**
- Monitor API usage at https://platform.deepseek.com/usage
- Track credit consumption
- Optimize response generation

### **Firebase Analytics**
- Document reads/writes
- Storage usage
- User engagement metrics

### **Application Logs**
- Firebase connection status
- AI response generation
- Learning progress tracking

## 🔐 Security

### **API Key Management**
- Environment variables for sensitive data
- No hardcoded credentials
- Regular key rotation

### **Firebase Security**
- Proper security rules
- Service account permissions
- Access logging

## 📈 Performance

### **Optimization Features**
- **In-memory caching** of learned Q&A
- **Fuzzy string matching** for similar questions
- **Efficient Firebase queries**
- **Response time optimization**

### **Scaling Considerations**
- Firebase auto-scaling
- CDN for static assets
- Rate limiting for production

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests if applicable
5. Submit pull request

## 📞 Support

- 📖 See `SETUP_GUIDE.md` for detailed setup
- 🐛 Create issues for bugs
- 💡 Suggest features via discussions

## 🎉 Demo

Run the demo to see the system in action:
```bash
python demo.py
```

## 📋 File Structure

```
personal-chatbot/
├── chatbot.py              # Enhanced AI chatbot with learning
├── app.py                  # Main Flask application
├── admin.py                # Admin interface for Q&A management
├── demo.py                 # Demo script
├── resume.yaml             # Resume data source
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html         # Main chat interface
│   └── admin_*.html       # Admin interface templates
├── SETUP_GUIDE.md         # Detailed setup instructions
└── env.example            # Environment variables template
```

---

## 🚀 **Ready to Deploy Your AI Assistant?**

1. **Get your DeepSeek API key** from https://platform.deepseek.com/
2. **Set up Firebase** for persistent learning
3. **Deploy to Vercel** for production
4. **Integrate with your portfolio** to engage recruiters 24/7

**Transform your portfolio with an AI assistant that learns and improves over time!** 🌟 