# 🚀 Embedding Adarsh's AI Chatbot Widget

This guide explains how to embed Adarsh's AI-powered resume chatbot on any website, including your portfolio at `adarshgella.com`.

## 🎯 **What You Get**

- **Floating Chat Button**: Unobtrusive chat icon in the bottom-right corner
- **Professional Interface**: Modern, responsive chat modal
- **Smart Responses**: AI-powered answers about skills, projects, and experience
- **Mobile Optimized**: Works perfectly on all devices
- **Zero Dependencies**: No external libraries required

## 📋 **Quick Integration**

### Method 1: Simple Script Tag (Recommended)

Add this single line to your website's HTML, just before the closing `</body>` tag:

```html
<script src="https://your-chatbot-domain.vercel.app/embed.js"></script>
```

### Method 2: Manual Integration

If you prefer more control, copy the widget code directly:

```html
<!-- Add this CSS to your <head> section -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Add this HTML before closing </body> tag -->
<div class="adarsh-chat-widget">
    <button class="chat-toggle" onclick="toggleAdarshChat()">
        <span id="adarsh-toggle-icon">💬</span>
        <div class="notification-badge" id="adarsh-notification-badge" style="display: none;">1</div>
    </button>
    
    <div class="chat-modal" id="adarsh-chat-modal">
        <!-- Widget content here -->
    </div>
</div>

<!-- Add the widget JavaScript -->
<script>
    // Widget JavaScript code here
</script>
```

## 🌐 **For adarshgella.com Integration**

### Step 1: Add to Your Portfolio

1. **Open your portfolio's main HTML file** (usually `index.html`)
2. **Add the embed script** just before `</body>`:

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Your existing head content -->
</head>
<body>
    <!-- Your existing portfolio content -->
    
    <!-- Add this line for the chatbot -->
    <script src="https://your-deployed-chatbot.vercel.app/embed.js"></script>
</body>
</html>
```

### Step 2: Customize for Your Brand

You can customize the widget colors to match your portfolio:

```html
<style>
.adarsh-chat-widget .chat-toggle {
    background: linear-gradient(135deg, #your-primary-color 0%, #your-secondary-color 100%) !important;
}

.adarsh-chat-widget .chat-header {
    background: linear-gradient(135deg, #your-primary-color 0%, #your-secondary-color 100%) !important;
}
</style>
```

## 🛠️ **Advanced Configuration**

### Custom API Endpoint

If you're hosting the chatbot on a different domain:

```javascript
// Override the API endpoint
window.ADARSH_CHAT_API = 'https://your-custom-domain.com/chat';
```

### Custom Positioning

```css
.adarsh-chat-widget {
    bottom: 30px !important;
    right: 30px !important;
}
```

### Hide on Specific Pages

```javascript
// Hide widget on specific pages
if (window.location.pathname === '/contact') {
    document.querySelector('.adarsh-chat-widget').style.display = 'none';
}
```

## 📱 **Mobile Optimization**

The widget automatically adapts to mobile devices:

- **Desktop**: Floating modal (380px width)
- **Mobile**: Full-width modal (responsive)
- **Touch-friendly**: Optimized button sizes

## 🎨 **Customization Options**

### Colors
```css
:root {
    --adarsh-primary: #667eea;
    --adarsh-secondary: #764ba2;
    --adarsh-success: #10b981;
    --adarsh-background: #f8fafc;
}
```

### Messages
```javascript
// Customize welcome message
window.ADARSH_WELCOME_MESSAGE = "Hi! I'm Adarsh's AI assistant. How can I help you today?";
```

### Quick Actions
```javascript
// Customize quick action buttons
window.ADARSH_QUICK_ACTIONS = [
    'What are your skills?',
    'Tell me about your projects',
    'How can I contact you?',
    'What motivates you?'
];
```

## 🚀 **Deployment Checklist**

### For Your Portfolio (adarshgella.com):

- [ ] Add embed script to main HTML file
- [ ] Test on desktop and mobile
- [ ] Verify chat responses work correctly
- [ ] Customize colors to match your brand
- [ ] Test contact information responses
- [ ] Ensure widget doesn't interfere with existing content

### Performance Optimization:

- [ ] Widget loads asynchronously (doesn't block page load)
- [ ] Minimal CSS/JS footprint
- [ ] Cached resources for faster loading
- [ ] Mobile-optimized for all screen sizes

## 🔧 **Troubleshooting**

### Widget Not Appearing
1. Check browser console for errors
2. Verify the embed script URL is correct
3. Ensure no CSS conflicts with existing styles

### Chat Not Responding
1. Check network tab for API call failures
2. Verify CORS settings on the chatbot server
3. Test the `/chat` endpoint directly

### Mobile Issues
1. Check viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
2. Verify touch events are working
3. Test on actual mobile devices

## 📊 **Analytics Integration**

Track chatbot interactions:

```javascript
// Google Analytics example
function trackChatInteraction(question) {
    gtag('event', 'chat_interaction', {
        'event_category': 'chatbot',
        'event_label': question
    });
}
```

## 🔒 **Security Considerations**

- Widget runs in isolated context
- No access to parent page data
- HTTPS required for production
- Rate limiting on API endpoints

## 📞 **Support**

If you need help integrating the widget:

- **Email**: g.adarsh043@gmail.com
- **GitHub**: https://github.com/gadarsh043/personal-chatbot
- **Portfolio**: https://adarshgella.com

## 🎉 **Go Live!**

Once integrated, recruiters visiting your portfolio will be able to:

1. **Click the chat button** to start a conversation
2. **Ask about your skills** and get detailed responses
3. **Learn about your projects** with technical details
4. **Get your contact information** instantly
5. **Understand your personality** and work style

The chatbot represents you 24/7, ensuring no opportunity is missed!

---

**Ready to enhance your portfolio with AI?** Add the embed script and watch your engagement soar! 🚀 