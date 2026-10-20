# SnapClass - Complete AI Attendance System UI/UX & Technical Specification

> **Prompt Context for UI Generation Model:**
> This document is a complete architectural, functional, and UI/UX design specification for **SnapClass** (an AI-powered Classroom Attendance Application). Use this document to generate or build a modern, intuitive, responsive, and high-fidelity user interface (e.g., in React, Next.js, Vue, Tailwind CSS, or Figma).

---

## 1. Executive Summary & Brand Identity

- **Application Name**: SnapClass
- **Tagline**: *Making Attendance Faster & Smarter Using AI*
- **Target Audience**: University & School Professors/Teachers, Lecturers, and Students.
- **Core Value Proposition**: Eliminates manual roll calls by combining **Multi-Face Computer Vision** from classroom photos and **Voice Speaker Identification** from ambient audio recordings, paired with QR-code course self-enrollment.
- **Brand Personality**: Playful yet modern, academic, futuristic, accessible, and fast.

### Visual Foundations & Color Tokens
| Token | Value | Description / Usage |
| :--- | :--- | :--- |
| **Primary (Brand Blue)** | `#5865F2` | Main buttons, active tabs, header accents |
| **Secondary (Accent Pink)** | `#EB459E` | Secondary actions, badges, logout buttons, card highlights |
| **App Background (Home)** | `#5865F2` | Vibrant brand backdrop on landing page |
| **App Background (Dashboard)** | `#E0E3FF` / `#F1F5F9` | Clean, high-legibility canvas for data screens |
| **Surface / Card Background** | `#FFFFFF` | Crisp elevated white containers with rounded corners |
| **Border & Outlines** | `#000000` or `#E2E8F0` | Defined card borders (neo-brutalist or modern glass card) |
| **Typography (Display)** | `'Climate Crisis', 'Outfit', sans-serif` | Bold, impactful headline typography |
| **Typography (Body & UI)** | `'Outfit', 'Inter', -apple-system` | Legible, clean dashboard typography |
| **Border Radius** | Cards: `20px` / `1.5rem`, Buttons: `24px` / `1.5rem` | Friendly, pill-shaped and rounded aesthetics |

---

## 2. System Architecture & User Roles

```
                         ┌────────────────────────────────────────┐
                         │           SnapClass Home Page          │
                         │ (Role Selection & DB Status Indicator) │
                         └──────────────────┬─────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         ┌─────────────────────┐                         ┌─────────────────────┐
         │   Teacher Portal    │                         │   Student Portal    │
         └──────────┬──────────┘                         └──────────┬──────────┘
                    │                                               │
      ┌─────────────┼─────────────┐                   ┌─────────────┼─────────────┐
      ▼             ▼             ▼                   ▼             ▼             ▼
 [Take AI      [Manage       [Attendance         [FaceID Login  [Enroll in   [Attendance
 Attendance]   Subjects]      Records]           & Voice Reg]    Subject]      Stats]
```

### User Roles
1. **Teacher**:
   - Registers/Logs in with username and password.
   - Creates and manages subjects (courses) with code, name, and section.
   - Generates and shares join links and QR codes.
   - Uploads classroom photos or captures camera snapshots for AI facial recognition.
   - Captures classroom audio for AI voice-based recognition.
   - Reviews, edits, and confirms attendance logs.
   - Views attendance records and statistics.
2. **Student**:
   - Logs in via **FaceID** (camera snapshot or photo upload).
   - Enrolls in courses using a 5-6 character subject code or QR code scan.
   - Registers profile with facial embedding and optional voice audio enrollment.
   - Views enrolled subjects, total classes held, attended classes, and percentage.
   - Unenrolls from courses.

---

## 3. Detailed Screen-by-Screen Specifications

### Screen 1: Home / Role Selector Screen
- **Header**:
  - Logo (`SnapClass` icon + wordmark)
  - Database status pill:
    - `🟢 Local Database Ready` or `🟢 Supabase Cloud Connected`
    - Optional expander with cloud configuration instructions.
- **Main Hero**:
  - Two primary interactive role cards side-by-side (Split layout):
    1. **Student Card**:
       - Mascot: Student with backpack/books (`https://i.ibb.co/844D9Lrt/mascot-student.png`)
       - Title: *"I'm Student"*
       - Action Button: `"Student Portal"` (Primary button with arrow outward icon)
    2. **Teacher Card**:
       - Mascot: Professor with glasses (`https://i.ibb.co/CsmQQV6X/mascot-prof.png`)
       - Title: *"I'm Teacher"*
       - Action Button: `"Teacher Portal"` (Primary button with arrow outward icon)

---

### Screen 2: Teacher Authentication (Login & Register)
- **Header**: Logo on left, *"Go back to Home"* button on right.
- **View A: Teacher Login**:
  - Title: *"Login using password"*
  - Form Fields:
    - `Username` (text input, placeholder: `ananyaroy`)
    - `Password` (password input, placeholder: `••••••••`)
  - Actions:
    - Button 1: `"Login"` (Primary, keyboard shortcut: `Ctrl+Enter`)
    - Button 2: `"Register Instead"` (Secondary switch)
  - Toast notifications: Error on invalid credentials, success toast on valid login.
- **View B: Teacher Register**:
  - Title: *"Register your teacher profile"*
  - Form Fields:
    - `Username`
    - `Full Name` (placeholder: `Dr. Sarah Mitchell`)
    - `Password`
    - `Confirm Password`
  - Actions:
    - Button 1: `"Register now"` (Submits form)
    - Button 2: `"Login Instead"` (Switches to Login view)

---

### Screen 3: Teacher Dashboard
- **Header**:
  - Left: SnapClass Logo.
  - Right: Greeting: `"Welcome, {teacher_name}"` + `"Logout"` button (`#EB459E` secondary styling).
- **Navigation Tabs (3 Pill Buttons)**:
  1. `Take Attendance` (Icon: `ar_on_you`)
  2. `Manage Subjects` (Icon: `book_ribbon`)
  3. `Attendance Records` (Icon: `cards_stack`)

#### Tab 1: "Take AI Attendance"
1. **Course Selection Row**:
   - Dropdown: `"Select Subject"` (lists: `{Subject Name} - {Subject Code}`)
   - Action Button: `"Add Photos"` (opens modal)
2. **Added Photos Gallery**:
   - Grid layout (up to 4 columns) displaying all added classroom photos.
   - Caption per card: `"Photo 1"`, `"Photo 2"`, etc.
3. **Action Bar**:
   - Button 1: `"Clear all photos"` (Black tertiary button, trash icon)
   - Button 2: `"Run Face Analysis"` (Pink secondary button, analytics icon, disabled if no photos)
   - Button 3: `"Use Voice Attendance"` (Brand blue primary button, microphone icon)
4. **Attendance Review Modal / Dialog**:
   - Pops up after running analysis.
   - Table showing:
     - `Name` (Student name)
     - `ID` (Student ID)
     - `Source` (e.g., `"Photo 1, Photo 2"` or Voice Confidence score)
     - `Status` (`✅ Present` or `❌ Absent`)
   - Actions:
     - `"Discard"` (clears session images and results)
     - `"Confirm & Save"` (writes logs to database and shows success toast)

#### Tab 2: "Manage Subjects"
1. **Header Row**:
   - Title: *"Manage Subjects"*
   - Action Button: `"+ Create New Subject"` (opens modal)
2. **Subject Cards Grid**:
   - Each course card includes:
     - Left accent border (`#EB459E`, 8px width).
     - Subject Name (h3, dark slate).
     - Subtitle: `Code: [CS101]` badge + `Section: A`.
     - Stat Badges:
       - `🫂 {count} Students`
       - `🕰️ {count} Classes Held`
     - Footer Action: `"Share Code: {name}"` button with share icon (opens QR modal).
3. **Empty State**:
   - `"No subjects found. Create one above to get started."`

#### Tab 3: "Attendance Records"
1. **Header**: *"Attendance Records"*
2. **Historical Data Table**:
   - Grouped and sorted by latest timestamp descending.
   - Columns:
     - `Time` (Formatted: `YYYY-MM-DD hh:mm AM/PM`)
     - `Subject` (e.g., `AI & Machine Learning`)
     - `Subject Code` (e.g., `CS101`)
     - `Attendance Stats` (e.g., `✅ 3 / 4 Students`)
3. **Empty State**:
   - `"No attendance records found yet. Take attendance using Face Analysis or Voice Attendance to generate logs."`

---

### Screen 4: Student Portal
- **Header**:
  - Left: SnapClass Logo.
  - Right: Greeting / `"Logout"` or `"Go back to Home"`.

#### View A: FaceID Login & Registration
1. **Title**: *"Login using FaceID"*
2. **Photo Input Tabs**:
   - Tab 1: `📷 Camera` (Active video viewfinder with capture trigger)
   - Tab 2: `📁 Upload Photo` (Drag & drop image upload)
3. **Recognition Flow**:
   - When photo is submitted:
     - **Match Found**: Matches enrolled student embedding -> logs student in -> redirects to dashboard with toast `"Welcome Back {name}!"`.
     - **Face Not Recognized**: Displays info badge: *"Face not recognized! You might be a new student!"* and reveals the **Registration Form Container**.
     - **Error States**: *"Face not found!"* or *"Multiple faces found"*.
4. **Student Registration Form**:
   - Appears inside a bordered container:
     - `Full Name` (input)
     - Optional: `Voice Enrollment` (Audio recorder for voice phrase: *"I am present, my name is..."*)
     - Button: `"Create Account"` (extracts 128-d face vector + voice vector, registers student, and logs them in).
5. **Quick Access / Testing Drawer**:
   - Expander: `🎓 Direct Student Login (Quick Access)`
   - Dropdown of all enrolled students with a `"Login as Selected Student"` button for instant testing without a camera.

#### View B: Student Dashboard
1. **Header Row**:
   - Title: *"Your Enrolled Subjects"*
   - Action Button: `"+ Enroll in Subject"` (opens modal)
2. **Subject Cards Grid**:
   - Enrolled course cards displaying:
     - Course title, Code, Section.
     - Stat Badges:
       - `📅 Total Classes: {X}`
       - `✅ Attended: {Y}`
       - Attendance percentage indicator.
     - Footer Action: `"Unenroll from this course"` (tertiary red/black button with delete icon).

---

## 4. Modals & Dialog Specifications

### Modal 1: Create New Subject
- **Trigger**: Click `"+ Create New Subject"` in Teacher Dashboard.
- **Fields**:
  - `Subject Code` (e.g., `CS101`)
  - `Subject Name` (e.g., `AI & Machine Learning`)
  - `Section` (e.g., `Section A`)
- **Actions**:
  - `"Create Subject Now"` (Primary button, validates non-empty fields, commits to database).

### Modal 2: Share Class Link & QR Code
- **Trigger**: Click `"Share Code"` on any Subject Card.
- **Content (2 Columns)**:
  - **Left Column ("Copy Link")**:
    - Full Join URL (e.g., `http://localhost:8501/?join-code=CS101`)
    - Raw Subject Code (e.g., `CS101`)
    - Helper note: *"Copy this link to share on WhatsApp or Email"*
  - **Right Column ("Scan to Join")**:
    - High-resolution generated QR Code image encoding the join URL.

### Modal 3: Add Classroom Photos
- **Trigger**: Click `"Add Photos"` in Take Attendance tab.
- **Tabs**:
  - Tab 1: `Camera` (Webcam snapshot capture with `"Take Snapshot"` button).
  - Tab 2: `Upload photos` (Multi-file uploader accepting `.jpg`, `.jpeg`, `.png`).
- **Actions**:
  - `"Done"` (Closes dialog and renders photos in the gallery).

### Modal 4: Voice Attendance
- **Trigger**: Click `"Use Voice Attendance"`.
- **Content**:
  - Instruction: *"Record classroom audio where students say 'I am present'. AI will recognize speaker voices."*
  - Audio Input Widget: Audio recorder / file upload.
  - Button: `"Analyze Audio"` (runs speaker identification model, scores against enrolled student voice profiles).
  - Review table with detected confidence and `"Confirm & Save"` action.

### Modal 5: Quick URL Enrollment (Auto-Enroll)
- **Trigger**: Student accesses link with query parameter `/?join-code={code}`.
- **Content**:
  - `"Would you like to enroll in {Subject Name}?"`
  - Actions: `"No thanks"` (clears query parameter) vs `"Yes enroll now!"` (enrolls student and refreshes).

---

## 5. Database Schema & Data Models

### 1. `teachers`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `teacher_id` | BIGINT / INTEGER | PRIMARY KEY AUTOINCREMENT | Unique teacher identifier |
| `username` | TEXT | UNIQUE, NOT NULL | Login handle |
| `password` | TEXT | NOT NULL | Bcrypt hashed password |
| `name` | TEXT | NOT NULL | Teacher full display name |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() | Account creation time |

### 2. `students`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `student_id` | BIGINT / INTEGER | PRIMARY KEY AUTOINCREMENT | Unique student identifier |
| `name` | TEXT | NOT NULL | Student full name |
| `face_embedding` | JSONB / TEXT | NULLABLE | 128-dimensional float array from dlib |
| `voice_embedding` | JSONB / TEXT | NULLABLE | 256-dimensional float array from Resemblyzer |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() | Enrollment date |

### 3. `subjects`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `subject_id` | BIGINT / INTEGER | PRIMARY KEY AUTOINCREMENT | Unique subject ID |
| `subject_code` | TEXT | NOT NULL | Unique course code (e.g., `CS101`) |
| `name` | TEXT | NOT NULL | Full course name |
| `section` | TEXT | NOT NULL | Class section (e.g., `A`, `Morning`) |
| `teacher_id` | BIGINT / INTEGER | FOREIGN KEY -> teachers | Course instructor |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |

### 4. `subject_students` (Enrollments)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT / INTEGER | PRIMARY KEY AUTOINCREMENT | Enrollment ID |
| `subject_id` | BIGINT / INTEGER | FOREIGN KEY -> subjects | Enrolled course |
| `student_id` | BIGINT / INTEGER | FOREIGN KEY -> students | Enrolled student |
| `enrolled_at` | TIMESTAMPTZ | DEFAULT NOW() | Date enrolled |
| *Constraint* | UNIQUE(subject_id, student_id) | Prevents duplicate enrollments |

### 5. `attendance_logs`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT / INTEGER | PRIMARY KEY AUTOINCREMENT | Log entry ID |
| `subject_id` | BIGINT / INTEGER | FOREIGN KEY -> subjects | Course session |
| `student_id` | BIGINT / INTEGER | FOREIGN KEY -> students | Student checked |
| `timestamp` | TEXT / TIMESTAMPTZ| NOT NULL | ISO date-time string of session |
| `is_present` | BOOLEAN / INTEGER | DEFAULT FALSE (0 or 1) | Attendance status |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() | Log creation time |

---

## 6. AI Pipelines & Algorithms

### 1. Computer Vision Face Recognition Pipeline
1. **Model Source**: `dlib` frontal face detector + 68-point pose predictor + ResNet 128-d descriptor model (`face_recognition_models`).
2. **Extraction**:
   - Multi-face detection extracts bounding boxes for all faces in image.
   - Computes normalized 128-dimensional feature embedding vectors.
3. **Classification & Matching**:
   - Compares query face descriptors against enrolled student face vectors.
   - Calculates Euclidean distance: $d = || \vec{v}_{query} - \vec{v}_{student} ||$.
   - **Threshold**: $d \le 0.6$ signifies a positive match.

### 2. Voice Identification Pipeline
1. **Model Source**: `Resemblyzer` (Deep learning voice encoder) with `librosa`.
2. **Preprocessing**: Ambient audio resampled to 16kHz, silence split with `top_db=30`.
3. **Matching**:
   - Generates 256-d voice embedding.
   - Computes Cosine Similarity with enrolled student voice embeddings: $\text{sim} = \vec{e}_{new} \cdot \vec{e}_{enrolled}$.
   - **Threshold**: $\text{sim} \ge 0.65$ marks student present.

---

## 7. UI Implementation Guidelines for Target Model

When generating code or mockups based on this document:
1. **Component Hierarchy**: Keep components modular (`SubjectCard`, `AttendanceTable`, `PhotoGallery`, `QRModal`, `MascotHeader`).
2. **Responsive Layout**:
   - Desktop: Multi-column side-by-side cards, 4-column photo grid.
   - Mobile: Collapses into a single stacked column with sticky bottom confirmation bars.
3. **Micro-Interactions**:
   - Button hover scale effect: `transform: scale(1.05); transition: 0.2s ease-in-out`.
   - Cards should have gentle hover lifts and distinct border-left colored accents.
4. **Feedback & States**:
   - Prominent loading states during facial/voice scanning (*"Deep scanning classroom photos..."*).
   - Non-blocking toast messages for actions like *"Photo Captured"*, *"Welcome Back"*, and *"Attendance Confirmed"*.
5. **Accessibility**:
   - Ensure high contrast between `#5865F2`, `#EB459E`, and background surfaces.
   - Provide clear textual alternatives for camera-only workflows.
