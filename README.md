# 🌐 Group Chat - Real-time Forum Web Application

A modern, feature-rich group discussion platform built with Flask, enabling users to create communities, share posts, and engage through likes and comments.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 User Management
- **Secure Authentication**: User registration and login with password hashing
- **User Profiles**: Personalized profiles with user information
- **Session Management**: Secure session handling with Flask

### 👥 Group Operations
- **Create Groups**: Users can create new discussion groups
- **Join Groups**: Join existing groups to participate in discussions
- **Group Discovery**: Browse and find groups to join

### 💬 Discussion Features
- **Post Creation**: Share thoughts and content within groups
- **Interactive Likes**: Like/unlike posts with real-time count updates
- **Comments System**: Add comments to posts with threaded discussions
- **Real-time Updates**: AJAX-powered interactions without page reloads

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Gradient Themes**: Beautiful purple gradient design throughout
- **Smooth Animations**: Fade-in, scale, and hover effects
- **Card-based Layout**: Clean, organized content presentation
- **User Avatars**: Automatic avatar generation with user initials

## 🛠️ Tech Stack

### Backend
- **[Flask](https://flask.palletsprojects.com/)** (v2.0+) - Python web framework
- **[SQLite3](https://www.sqlite.org/)** - Lightweight database
- **[Flask-WTF](https://flask-wtf.readthedocs.io/)** - Form handling and validation
- **[Werkzeug](https://werkzeug.palletsprojects.com/)** - WSGI utilities and security

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (ES6+)** - AJAX interactions and dynamic updates
- **[Ionicons](https://ionic.io/ionicons)** (v7.1.0) - Modern icon library

### Development Tools
- **Python Logging** - Application logging and debugging
- **Git** - Version control

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/realsanjeev/Group-Chat.git
cd Group-Chat
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python3 init_db.py
```

This will create the SQLite database with all necessary tables.

### 5. Run the Application
```bash
flask run
# or
python3 app.py
```

The application will be available at `http://localhost:5000`

> sample username: realfake
> sample password: realfake1

## 📖 Usage

### First Time Setup

1. **Register an Account**
   - Navigate to `http://localhost:5000/signup`
   - Fill in your details (username, email, password, etc.)
   - Submit the form

2. **Login**
   - Go to `http://localhost:5000/login`
   - Enter your credentials
   - You'll be redirected to the home page

3. **Create or Join a Group**
   - Navigate to "Groups" from the navbar
   - Create a new group or join an existing one
   - Start posting and engaging!

### Using the Discussion Forum

- **Create Posts**: Click on a group and use the "Create Post" form
- **Like Posts**: Click the heart icon to like/unlike posts
- **Add Comments**: Click the comment icon to expand the comment section, then add your comment
- **View Profiles**: Click on usernames to view user profiles

## 🗄️ Database Schema

The application uses SQLite with the following tables:

### Core Tables
- **`user`** - User accounts (id, username, password)
- **`userinfo`** - User profiles (user_id, firstname, middlename, lastname, email, dob, gender)
- **`user_group`** - Groups (id, name)
- **`group_member`** - User-group relationships (user_id, group_id)

### Content Tables
- **`posts`** - Posts in groups (id, content, user_id, group_id, doc)
- **`comment`** - Comments on posts (id, comment, post_id, user_id, commented_on)
- **`like`** - Likes on posts (post_id, user_id)

For detailed schema documentation, see [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

## 🔌 API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Groups
- `GET /group_ops` - Group operations page
- `POST /group_ops` - Create or join group
- `GET /group/<group_name>` - View group discussion

### Posts & Interactions
- `POST /group/<group_name>` - Create new post
- `POST /api/like/<post_id>` - Toggle like on post (AJAX)
- `POST /api/comment/<post_id>` - Add comment to post (AJAX)

### User
- `GET /profile` - View user profile
- `GET /home` - User home page

## 📁 Project Structure

```
Group-Chat/
├── app.py                      # Main Flask application
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── DATABASE_SCHEMA.md          # Database documentation
├── README.md                   # This file
│
├── src/
│   ├── database_handler.py    # Database operations
│   ├── logger.py              # Logging configuration
│   └── sanitize.py            # Input sanitization
│
├── templates/                  # HTML templates
│   ├── account/               # Auth pages (login, signup)
│   ├── public/                # Public pages (terms, privacy)
│   ├── base.html              # Base template
│   ├── discussion.html        # Group discussion page
│   ├── home.html              # User home page
│   ├── success.html           # Success page
│   └── sorry.html             # Error page
│
├── static/                     # Static files
│   ├── css/                   # Stylesheets
│   │   ├── main.css
│   │   ├── discussion.css
│   │   ├── auth.css
│   │   └── ...
│   └── images/                # Images and icons
│
└── database/                   # Legacy database files
    ├── create_database.py
    ├── sql_create_table.py
    └── SQL_INTRO.md
```

## 🎨 Design Features

### Color Scheme
- **Primary Gradient**: `#667eea` to `#764ba2` (Purple to Violet)
- **Error Gradient**: `#f093fb` to `#f5576c` (Pink to Red)
- **Text Colors**: `#333` (headings), `#555` (content), `#999` (meta)

### Animations
- **Fade In**: Smooth entrance animations for cards
- **Scale In**: Icon animations on load
- **Hover Effects**: Interactive feedback on buttons and cards
- **Transitions**: 0.3s ease for all interactive elements

### Responsive Breakpoints
- **Desktop**: Full features and spacing
- **Tablet/Mobile** (< 768px): Optimized layout and touch-friendly

## 🔒 Security Features

- **Password Hashing**: Secure password storage
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Input Sanitization**: XSS prevention
- **SQL Injection Prevention**: Parameterized queries
- **Session Security**: Secure session management

## 🐛 Known Issues & Future Enhancements

### Planned Features
- [ ] Real-time notifications
- [ ] File/image upload support
- [ ] User mentions (@username)
- [ ] Search functionality
- [ ] Email verification
- [ ] Password reset
- [ ] Admin dashboard
- [ ] Group moderation tools

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**RealSanjeev**
- GitHub: [@realsanjeev](https://github.com/realsanjeev)
- Twitter: [@realsanjeev2](https://twitter.com/realsanjeev2)

## 🙏 Acknowledgments

- **Flask** - The Python web framework that powers this application
- **Ionicons** - Beautiful open-source icons
- **SQLite** - Reliable embedded database
- **Flask-WTF** - Form handling and validation
- **Google Fonts** - Typography (Montserrat, Franklin Gothic)

---

**Note**: This is a learning project and may not be suitable for production use without additional security hardening and testing.
