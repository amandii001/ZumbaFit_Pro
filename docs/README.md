# ZumbaFit Pro 🎵

An AI-powered Zumba dance analysis and feedback system that helps users improve their dance form through video analysis and personalized recommendations.

## Features

- **AI Video Analysis**: Upload Zumba videos and get instant posture feedback
- **User Authentication**: Secure registration and login system
- **Personalized Feedback**: Get specific improvement suggestions based on your form
- **Music Recommendations**: Receive dance-style-specific music suggestions
- **Admin Dashboard**: Manage users and view analytics
- **Real-time Processing**: Fast video analysis using trained ML models

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MySQL**: Database for user data and video metadata
- **TensorFlow**: ML model for pose analysis
- **OpenCV**: Video processing
- **bcrypt**: Password hashing

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript**: Interactive UI and API integration

### AI/ML
- **Custom CNN Model**: Trained on Zumba pose data
- **Pose Detection**: Real-time posture analysis
- **6 Class Classification**: Squat, Arm Raise, Knee Extension (Correct/Incorrect)

## Project Structure

```
ZumbaFit Pro/
├── app/                          # Backend application
│   ├── main.py                   # FastAPI entry point
│   ├── db.py                     # Database connection
│   ├── models/                   # ML models
│   │   └── zumba_model.h5        # Trained model
│   ├── routers/                  # API endpoints
│   │   ├── auth.py              # Authentication
│   │   ├── video.py             # Video upload & analysis
│   │   └── feedback.py          # Feedback & recommendations
│   ├── schemas/                  # Pydantic models
│   │   ├── auth_schema.py
│   │   ├── video_schema.py
│   │   └── feedback_schema.py
│   ├── utils/                    # Utilities
│   │   ├── hashing.py           # Password hashing
│   │   └── ml_pipeline.py       # ML inference
│   └── uploads/                  # Uploaded videos
├── UI/                          # Frontend files
│   ├── index.html               # Landing page
│   ├── user_registration.html   # User registration
│   ├── user_login.html          # User login
│   ├── upload.html              # Video upload
│   ├── admin-login.html         # Admin login
│   ├── admin-dashboard.html     # Admin dashboard
│   ├── about.html               # About page
│   └── styles.css               # Custom styles
├── ZumbaFitPro_Database.txt     # Database schema
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Setup Instructions

### Prerequisites

1. **Python 3.8+**
2. **XAMPP** (for MySQL database)
3. **Git**

### 1. Database Setup

1. Start XAMPP and ensure MySQL is running
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Create a new database named `zumbafitpro`
4. Import the database schema from `ZumbaFitPro_Database.txt`

### 2. Backend Setup

#### Option A: Automated Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ZumbaFit-Pro
   ```

2. **Run automated setup**:
   ```bash
   # Windows
   setup_environment.bat
   
   # macOS/Linux
   python setup_environment.py
   ```

   This will automatically:
   - Create virtual environment
   - Install protobuf 3.20.3 (compatible with TensorFlow + MediaPipe)
   - Install all dependencies
   - Verify installation

#### Option B: Manual Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ZumbaFit-Pro
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install protobuf first** (IMPORTANT for compatibility):
   ```bash
   pip install protobuf==3.20.3
   ```

4. **Install other dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify protobuf version**:
   ```bash
   pip show protobuf
   # Should show Version: 3.20.3
   ```

6. **Configure database** (if needed):
   - Edit `app/db.py` to match your MySQL credentials
   - Default: `localhost`, `root`, no password

7. **Start the backend server**:
   ```bash
   python start_backend.py
   # or
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: http://localhost:8000
   API Documentation: http://localhost:8000/docs

### 3. Frontend Setup

1. **Serve the UI files**:
   - Use any local server (Python, Node.js, etc.)
   - Or open files directly in browser (for development)

2. **Python simple server**:
   ```bash
   cd UI
   python -m http.server 8080
   ```

3. **Access the application**:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000

## Usage

### For Users

1. **Register**: Create a new account at `/user_registration.html`
2. **Login**: Sign in with your credentials at `/user_login.html`
3. **Upload Video**: Upload your Zumba video for analysis
4. **Get Feedback**: Receive instant AI-powered posture feedback
5. **View Recommendations**: Get personalized music and improvement suggestions

### For Admins

1. **Admin Login**: Access admin panel at `/admin-login.html`
2. **Dashboard**: View user analytics and video submissions
3. **Manage Content**: Add music recommendations and manage users

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/admin/login` - Admin login

### Video Analysis
- `POST /video/upload` - Upload and analyze video
- `GET /video/user/{user_id}` - Get user's videos
- `GET /video/{video_id}` - Get video details

### Feedback
- `GET /feedback/user/{user_id}` - Get user feedback
- `GET /feedback/music/recommendations` - Get music recommendations
- `GET /feedback/personalized/{user_id}` - Get personalized feedback

## ML Model

The system uses a custom CNN model trained on Zumba pose data to classify:
- **Squat_Correct/Incorrect**
- **Arm_Raise_Correct/Incorrect**
- **Knee_Extension_Correct/Incorrect**

The model analyzes video frames and provides confidence scores for each classification.

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `app/routers/`
2. **Frontend**: Create new HTML pages in `UI/`
3. **Database**: Update schema in `ZumbaFitPro_Database.txt`

### Testing

1. **API Testing**: Use the interactive docs at `/docs`
2. **Frontend Testing**: Test UI flows manually
3. **Integration Testing**: Test full user journey

## Troubleshooting

### Common Issues

1. **Protobuf Compatibility Error**:
   ```
   mediapipe 0.10.7 requires protobuf<4,>=3.11, but you have protobuf 4.21.12
   ```
   **Solution**:
   ```bash
   pip install protobuf==3.20.3 --force-reinstall
   pip show protobuf  # Should show Version: 3.20.3
   ```

2. **Database Connection Error**:
   - Ensure XAMPP MySQL is running
   - Check database credentials in `app/db.py`

3. **Model Loading Error**:
   - Ensure `zumba_model.h5` is in `app/models/`
   - Check TensorFlow installation

4. **CORS Errors**:
   - Backend CORS is configured for development
   - Update `allow_origins` for production

5. **File Upload Issues**:
   - Ensure `app/uploads/` directory exists
   - Check file size limits

6. **MediaPipe Import Error**:
   - Ensure protobuf is version 3.20.3
   - Reinstall MediaPipe: `pip install mediapipe==0.10.7 --force-reinstall`

### Dependency Conflicts

If you encounter dependency conflicts:

1. **Clean installation**:
   ```bash
   pip uninstall protobuf tensorflow mediapipe -y
   pip install protobuf==3.20.3
   pip install tensorflow==2.15.0
   pip install mediapipe==0.10.7
   ```

2. **Verify versions**:
   ```bash
   pip list | grep -E "(protobuf|tensorflow|mediapipe)"
   ```

3. **Use the automated setup script**:
   ```bash
   python setup_environment.py
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team

---

**Dance your way to fitness with AI-powered feedback! 🎵💃**
