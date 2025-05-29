# ProfessorSTEM 🎓

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An innovative AI-powered STEM education platform that revolutionizes how students learn science and mathematics through personalized, adaptive learning experiences.

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

### 🧠 Intelligent Assessment System
- **AI-Driven Initial Evaluation**: Uses Gemini AI to accurately assess student's starting knowledge level
- **Real-Time Proficiency Tracking**: Continuously monitors student progress and adapts content difficulty
- **Performance Analytics**: Detailed insights into learning progress with comparative analysis

### 📚 Personalized Learning Experience
- **Custom Study Plans**: Automatically generated learning paths based on individual student needs
- **Age-Appropriate Content**: Tailored content delivery for different school levels (Elementary, Middle, High School)
- **Adaptive Difficulty**: Content automatically adjusts based on student performance and learning speed

### 🎯 Comprehensive Learning Journey
- Initial Proficiency Assessment
- Customized Study Material
- Interactive Learning Guides
- Progress Validation
- Final Assessment
- Performance Comparison

### 🛠️ Smart Features
- **Intelligent Task Management**: Built-in todo list to help students organize their learning goals
- **Progress Tracking**: Visual representations of improvement and learning milestones
- **Multi-Subject Support**: Comprehensive coverage of both Mathematics and Science topics

## 🎬 Cover

![ProfessorSTEM Cover](Cover%20Image.png)

*Experience personalized STEM education powered by AI*

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- PostgreSQL database

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ProfessorSTEM.git
   cd ProfessorSTEM
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API credentials
   ```

5. **Initialize the database**
   ```bash
   python create_db.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

\```

## 💻 Usage

### For Students
1. **Sign Up**: Create an account with your grade level
2. **Take Assessment**: Complete the initial proficiency quiz
3. **Follow Study Plan**: Work through your personalized learning path
4. **Track Progress**: Monitor your improvement over time
5. **Final Assessment**: Validate your learning with comprehensive tests

### For Administrators
1. **Admin Dashboard**: Monitor student progress and platform analytics
2. **User Management**: Manage student accounts and access levels
3. **Performance Reports**: Generate detailed learning analytics

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with Supabase
- **Authentication**: JWT with bcrypt password hashing
- **AI Integration**: Google Gemini AI

### Frontend
- **Templates**: Jinja2
- **Styling**: CSS3 with responsive design
- **JavaScript**: Vanilla JS for interactive features

### Deployment
- **Platform**: Vercel (configuration included)
- **WSGI**: Gunicorn compatible
- **Database**: PostgreSQL (production)

## 📁 Project Structure

```
ProfessorSTEM/
├── 📄 app.py                 # Main Flask application
├── 📄 config.py              # Configuration settings
├── 📄 auth.py                # Authentication logic
├── 📄 routes.py              # URL routes and views
├── 📄 agents.py              # AI agents and logic
├── 📄 db.py                  # Database operations
├── 📄 proficiency.py         # Proficiency assessment logic
├── 📁 static/                # Static assets
│   ├── 📁 css/              # Stylesheets
│   ├── 📁 js/               # JavaScript files
│   └── 📁 images/           # Images and icons
├── 📁 templates/            # HTML templates
├── 📄 requirements.txt      # Python dependencies
├── 📄 vercel.json          # Vercel deployment config
└── 📄 README.md            # Project documentation
```

## 📖 API Documentation

### Authentication Endpoints

- `POST /signup` - User registration
- `POST /signin` - User login
- `GET /logout` - User logout

### Learning Endpoints

- `GET /quiz` - Get quiz questions
- `POST /quiz` - Submit quiz answers
- `GET /study_plan` - Get personalized study plan
- `GET /results` - View learning progress

### Admin Endpoints

- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management

## 🎯 Target Audience

- **Primary**: K-12 Students (Ages 5-18)
- **Secondary**: Teachers and Educational Institutions
- **Tertiary**: Parents and Education Administrators

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- 💼 LinkedIn: [Elewashy](https://linkedin.com/in/elewashy)

---

<div align="center">
  <p>Made with ❤️ for STEM Education</p>
  <p>© 2025 ProfessorSTEM. All rights reserved.</p>
</div>
