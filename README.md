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

### 🎨 **Portfolio Integration**
- **Embeddable widget** for any website
- **Matches portfolio colors** (emerald green & teal theme)
- **Responsive design** for all devices
- **Professional interface** optimized for recruiters

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
- **Embeddable Widget**: http://localhost:5000/widget

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

### **Embed Widget**

#### **Method 1: Basic Iframe Embed**
```html
<iframe 
  src="https://personal-chatbot-q2wp.onrender.com/widget" 
  width="56" 
  height="56" 
  frameborder="0"
  title="Chat with Adarsh - AI Assistant">
</iframe>
```

#### **Method 2: Dynamic Corner Positioning**
The widget supports four corner positions through URL parameters:

**Bottom-Right Corner (Default)**
```html
<iframe 
  src="https://personal-chatbot-q2wp.onrender.com/widget?position=right-bottom" 
  style="position: fixed; bottom: 20px; right: 20px; width: 56px; height: 56px;"
  frameborder="0">
</iframe>
```

**Top-Right Corner**
```html
<iframe 
  src="https://personal-chatbot-q2wp.onrender.com/widget?position=right-top" 
  style="position: fixed; top: 20px; right: 20px; width: 56px; height: 56px;"
  frameborder="0">
</iframe>
```

**Bottom-Left Corner**
```html
<iframe 
  src="https://personal-chatbot-q2wp.onrender.com/widget?position=left-bottom" 
  style="position: fixed; bottom: 20px; left: 20px; width: 56px; height: 56px;"
  frameborder="0">
</iframe>
```

**Top-Left Corner**
```html
<iframe 
  src="https://personal-chatbot-q2wp.onrender.com/widget?position=left-top" 
  style="position: fixed; top: 20px; left: 20px; width: 56px; height: 56px;"
  frameborder="0">
</iframe>
```

#### **Method 3: Flexible Inline Embedding**
Place anywhere in your content:
```html
<div style="margin: 20px;">
  <iframe 
    src="https://personal-chatbot-q2wp.onrender.com/widget" 
    width="56" 
    height="56" 
    frameborder="0">
  </iframe>
</div>
```

### **Position Parameters:**
- `right-bottom` (default) - Modal opens upward and leftward
- `right-top` - Modal opens downward and leftward  
- `left-bottom` - Modal opens upward and rightward
- `left-top` - Modal opens downward and rightward

### **Features:**
- **Smart modal positioning** based on corner placement
- **Mobile responsive design** with automatic adjustments
- **Notification badge** appears after 3 seconds of inactivity
- **Floating chat button** with smooth animations
- **Professional appearance** optimized for recruiters

## 🎨 Customization

### **Color Scheme**
The system uses my portfolio colors:
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
│   ├── widget.html        # Embeddable widget
│   └── admin_*.html       # Admin interface templates
├── SETUP_GUIDE.md         # Detailed setup instructions
├── EMBEDDING_GUIDE.md     # Widget embedding guide
└── env.example            # Environment variables template
```

---

## 🚀 **Ready to Deploy Your AI Assistant?**

1. **Get your DeepSeek API key** from https://platform.deepseek.com/
2. **Set up Firebase** for persistent learning
3. **Deploy to Vercel** for production
4. **Embed on your portfolio** to engage recruiters 24/7

**Transform your portfolio with an AI assistant that learns and improves over time!** 🌟 