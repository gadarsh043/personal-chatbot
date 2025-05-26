# Personal Resume Chatbot

A Flask-based web application featuring an intelligent chatbot that answers questions about Adarsh's professional background, skills, and experience.

## 🚀 Features

- **Interactive Chat Interface**: Clean, responsive web interface for chatting
- **Resume-based Responses**: Answers questions about education, skills, projects, and experience
- **Fuzzy Matching**: Intelligent keyword matching for natural conversation
- **Vercel Deployment Ready**: Optimized for serverless deployment

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data**: YAML for resume information
- **Deployment**: Vercel
- **Chatbot**: Custom rule-based system with fuzzy string matching

## 📁 Project Structure

```
personal-chatbot/
├── app.py              # Flask application
├── chatbot.py          # Custom chatbot implementation
├── resume.yaml         # Resume data
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel deployment configuration
├── test_chatbot.py    # Test script
├── templates/
│   └── index.html     # Frontend interface
└── README.md          # This file
```

## 🔧 Recent Updates

### Migration from ChatterBot to Custom Solution

**Problem**: The original implementation used ChatterBot, which is incompatible with Python 3.12 and hasn't been maintained since 2020.

**Solution**: Replaced ChatterBot with a custom, lightweight chatbot that:
- Uses fuzzy string matching for intelligent responses
- Loads data directly from `resume.yaml`
- Provides better error handling and fallback responses
- Is compatible with modern Python versions
- Reduces deployment size and complexity

### Key Improvements

1. **Python 3.12 Compatibility**: Fully compatible with modern Python versions
2. **Reduced Dependencies**: Removed heavy, outdated packages
3. **Better Performance**: Faster response times and smaller memory footprint
4. **Improved Responses**: More natural and contextual answers
5. **Easier Maintenance**: Simple, readable codebase

## 🚀 Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd personal-chatbot
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

### Testing

Run the test script to verify chatbot functionality:
```bash
python test_chatbot.py
```

## 🌐 Deployment

### Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Follow the prompts** to configure your deployment

### Environment Variables

No environment variables are required for basic functionality.

## 💬 Chatbot Capabilities

The chatbot can answer questions about:

- **Personal Information**: Name, location, favorite color
- **Education**: Degree, university, graduation year
- **Skills**: Programming languages, frameworks, tools
- **Projects**: Detailed descriptions of work projects
- **Experience**: Work history, roles, responsibilities
- **General**: Greetings, help, and fallback responses

### Example Interactions

```
User: What is your name?
Bot: My name is Adarsh Gella

User: What are your skills?
Bot: My skills include: languages, frameworks, tools, practices

User: Tell me about PhotoShare
Bot: A photo-sharing application built with a responsive frontend and scalable backend.
```

## 📝 Customization

### Adding New Responses

Edit `chatbot.py` and modify the `setup_responses()` method to add new keywords and responses.

### Updating Resume Data

Edit `resume.yaml` to update personal information, skills, projects, or experience.

### Modifying the Interface

Edit `templates/index.html` to customize the chat interface appearance and behavior.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **YAML Errors**: Verify `resume.yaml` syntax is correct
3. **Port Issues**: Change the port in `app.py` if 5000 is already in use

### Vercel Deployment Issues

1. **Build Failures**: Check that `requirements.txt` contains only compatible packages
2. **Function Size**: The current configuration supports up to 15MB lambda functions
3. **Python Version**: Vercel uses Python 3.9 by default, which is compatible with this project

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Contact

For questions or support, please contact Adarsh Gella through the chatbot interface or via the contact information in the resume data.

---

**Note**: This project has been updated to resolve Python 3.12 compatibility issues and improve overall performance and maintainability. 