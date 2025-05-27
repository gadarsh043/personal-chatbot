# 🤖 Enhanced AI Chatbot Setup Guide

## Overview

This enhanced chatbot system features:
- **2-way learning**: Learns from new questions and improves over time
- **DeepSeek AI integration**: Generates intelligent responses for unknown questions
- **Firebase storage**: Persists learned Q&A pairs across sessions
- **Admin interface**: Review and edit AI-generated responses
- **Portfolio integration**: Embeddable widget for your website

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up DeepSeek AI

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account and get your API key
3. Check your credits at https://platform.deepseek.com/usage

### 3. Set Up Firebase (Optional but Recommended)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Firestore Database
4. Create a service account:
   - Go to Project Settings → Service Accounts
   - Generate new private key
   - Download the JSON file

### 4. Configure Environment Variables

Create a `.env` file in your project root:

```env
# DeepSeek AI Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Firebase Configuration (Method 1: Service Account File)
FIREBASE_KEY_PATH=firebase-key.json

# Firebase Configuration (Method 2: Environment Variables for Production)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nyour_private_key_here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your_service_account_email@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your_service_account_email%40project.iam.gserviceaccount.com
```

### 5. Run the Application

```bash
# Main chatbot application
python app.py

# Admin interface (separate terminal)
python admin.py
```

## 🔧 Configuration Options

### Running Without Firebase

The system will work without Firebase but won't persist learned Q&A pairs:

```bash
# Just set DeepSeek API key
DEEPSEEK_API_KEY=your_api_key
```

### Running Without DeepSeek AI

The system will use fallback responses for unknown questions:

```bash
# No API key needed, but responses will be generic
```

### Running with Both (Recommended)

Full functionality with AI responses and persistent learning:

```bash
DEEPSEEK_API_KEY=your_api_key
FIREBASE_KEY_PATH=firebase-key.json
```

## 🎯 How It Works

### 1. Question Processing Flow

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

### 2. AI Context Building

The system automatically builds context for AI responses using:
- Personal information from `resume.yaml`
- Skills, experience, and projects
- Personality traits and career goals
- Contact information

### 3. Learning System

- **AI-generated responses** are marked and can be reviewed
- **Manual Q&A pairs** can be added through admin interface
- **Similar questions** are matched using fuzzy string matching
- **Response quality** improves over time through admin review

## 🛠 Admin Interface

Access the admin interface at `http://localhost:5001/admin`

### Features:
- **Dashboard**: View all learned Q&A pairs
- **Edit**: Modify AI-generated responses
- **Add**: Create manual Q&A pairs
- **Delete**: Remove unwanted entries
- **Statistics**: Track learning progress

### Admin Routes:
- `/admin` - Main dashboard
- `/admin/add` - Add new Q&A pair
- `/admin/edit/<id>` - Edit specific Q&A
- `/admin/stats` - View statistics
- `/admin/delete/<id>` - Delete Q&A pair

## 🌐 Deployment

### Vercel Deployment

1. **Set Environment Variables** in Vercel dashboard:
   ```
   DEEPSEEK_API_KEY=your_api_key
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_PRIVATE_KEY=your_private_key
   FIREBASE_CLIENT_EMAIL=your_email
   # ... other Firebase variables
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

### Firebase Security Rules

Set up Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /learned_qa/{document} {
      allow read, write: if true; // Adjust based on your security needs
    }
  }
}
```

## 🔍 Monitoring & Analytics

### DeepSeek Usage Tracking

Monitor your API usage at: https://platform.deepseek.com/usage

### Firebase Usage

Monitor Firestore usage in Firebase Console:
- Document reads/writes
- Storage usage
- Active connections

### Application Logs

The system provides detailed logging:
- `✅ Firebase initialized successfully`
- `📚 Loaded X learned Q&A pairs from Firebase`
- `🤖 Generated AI response for: question...`
- `💾 Saved new Q&A to Firebase: question...`

## 🎨 Customization

### Personality Customization

Edit `chatbot.py` to modify AI personality:

```python
def build_ai_context(self):
    context_parts.extend([
        "Personality: Your custom personality traits",
        "Interests: Your specific interests",
        "Work Style: Your work preferences",
        "Career Goals: Your career objectives"
    ])
```

### Response Templates

Modify response templates in `setup_responses()` method:

```python
self.responses = {
    "custom_keyword": "Your custom response",
    # ... other responses
}
```

### UI Customization

Update CSS variables in templates:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-secondary-color;
    /* ... other colors */
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Firebase Connection Failed**
   - Check service account credentials
   - Verify project ID
   - Ensure Firestore is enabled

2. **DeepSeek API Errors**
   - Verify API key is correct
   - Check credit balance
   - Ensure proper request format

3. **Admin Interface Not Loading**
   - Check if admin.py is running on port 5001
   - Verify Firebase connection
   - Check browser console for errors

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Optimization

### Caching

The system caches learned Q&A pairs in memory for faster responses.

### Rate Limiting

Consider implementing rate limiting for production:

```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

### Database Optimization

- Index frequently queried fields in Firestore
- Implement pagination for large Q&A datasets
- Use Firebase offline persistence for better performance

## 🔐 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure key management
- Rotate keys regularly

### Firebase Security
- Implement proper security rules
- Use service accounts with minimal permissions
- Monitor access logs

### Input Validation
- Sanitize user inputs
- Implement rate limiting
- Validate question length and content

## 📈 Scaling

### High Traffic Scenarios
- Use Firebase Functions for serverless scaling
- Implement caching layers (Redis)
- Consider CDN for static assets

### Multiple Chatbots
- Use different Firebase collections
- Separate DeepSeek API keys
- Implement multi-tenant architecture

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review Firebase and DeepSeek documentation
- Create an issue in the repository

---

**Happy Chatting! 🚀** 