# SnapClass - AI-Based Classroom Attendance System

An intelligent, modern classroom attendance platform powered by **Multi-Face Computer Vision** and **Voice Speaker Identification** using Streamlit, Dlib, and Resemblyzer.

---

## 🌟 Key Features

- **Dual AI Recognition Engines**:
  - **Facial Recognition**: Multi-face detection and 128-dimensional embedding comparison using Dlib models and Euclidean distance matching.
  - **Voice Speaker Identification**: Ambient classroom audio processing using Resemblyzer neural voice embeddings and cosine similarity.
- **Dual-Mode Database**:
  - **Local SQLite Mode** (Default): Works completely offline out-of-the-box without requiring cloud configurations.
  - **Cloud Supabase Mode**: Seamlessly switches to Supabase cloud when credentials are provided in `.streamlit/secrets.toml`.
- **Teacher Portal**:
  - Course creation & management (Subject Code, Name, Section).
  - Dynamic QR Code and Join Link sharing for instant student enrollment.
  - Single/Bulk classroom photo upload or webcam capture for AI facial roll call.
  - Ambient classroom audio recording for AI voice roll call.
  - Attendance log review, confirmation, and historical records.
- **Student Portal**:
  - Biometric FaceID login and registration (via webcam or photo upload).
  - Optional voice enrollment for audio-based roll calls.
  - Instant enrollment via course code (e.g. `CS101`) or QR code scan.
  - Dashboard tracking total classes held vs. attended classes and attendance percentage.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+ (Python 3.10 - 3.14 supported)
- Git

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/gaurav9021-d/AI-Based-Attendance-System-with-Face-And-Voice-Recognization.git
cd AI-Based-Attendance-System-with-Face-And-Voice-Recognization
pip install -r requirements.txt
```

### 3. Run the Application
On Windows, you can simply double-click:
```bat
run.bat
```
Or run directly using Streamlit:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🔑 Default Credentials (Ready-to-Test)

- **Teacher Account**:
  - **Username**: `teacher`
  - **Password**: `password123`
  *(You can also register your own teacher profile anytime).*
- **Pre-Configured Courses**:
  - `CS101` — AI & Machine Learning (Section A)
  - `CS202` — Computer Vision & Robotics (Section B)
- **Pre-Configured Students**: Alex Johnson, Priya Sharma, David Lee, Emma Watson.

---

## 🛠️ Tech Stack

- **Frontend & Web Framework**: [Streamlit](https://streamlit.io/)
- **Computer Vision & Face Embeddings**: [Dlib](http://dlib.net/), `face_recognition_models`, OpenCV, NumPy
- **Voice Recognition**: [Resemblyzer](https://github.com/resemble-ai/Resemblyzer), [Librosa](https://librosa.org/)
- **Database**: SQLite3 (Local) / [Supabase](https://supabase.com/) (Cloud PostgreSQL)
- **Security**: Bcrypt password hashing
- **QR Code Generation**: Segno

---

## 📁 Project Structure

```
├── .streamlit/
│   └── secrets.toml.example        # Cloud Supabase template
├── src/
│   ├── components/                 # Modals, dialogs, cards & headers
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_attendance_results.py
│   │   ├── dialog_auto_enroll.py
│   │   ├── dialog_create_subject.py
│   │   ├── dialog_enroll.py
│   │   ├── dialog_share_subject.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── header.py
│   │   └── subject_card.py
│   ├── database/                   # Database drivers & config
│   │   ├── config.py               # Dual-mode switcher
│   │   ├── db.py                   # Business logic operations
│   │   └── sqlite_db.py            # Local SQLite driver
│   ├── pipelines/                  # AI Models
│   │   ├── face_pipeline.py        # Facial recognition & matching
│   │   └── voice_pipeline.py       # Voice speaker identification
│   ├── screens/                    # Application Views
│   │   ├── home_screen.py          # Role selection & status
│   │   ├── teacher_screen.py       # Teacher dashboard & tabs
│   │   └── student_screen.py       # Student FaceID & dashboard
│   └── ui/                         # Custom CSS styles
│       └── base_layout.py
├── app.py                          # Streamlit application entry point
├── run.bat                         # Windows one-click launcher
├── requirements.txt                # Python dependencies
├── supabase_schema.sql             # SQL schema for cloud database
├── PROJECT_UI_SPECIFICATION.md     # Full architectural & UI specification
└── figma_helper.js                 # Figma API design inspection utility
```

---

## 📄 License
MIT License