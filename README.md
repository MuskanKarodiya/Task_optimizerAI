# AI Task Optimizer

🚀 **AI Task Optimizer** is a Streamlit-based application for team task management with integrated emotional intelligence. It leverages OpenAI GPT technology to help teams stay productive while monitoring and supporting emotional wellbeing.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
  - [Frontend](#frontend-architecture)
  - [AI Integration](#ai-integration-layer)
  - [Data Management](#data-management)
  - [Visualization & Analytics](#visualization--analytics)
- [Installation](#installation)
- [Usage](#usage)
- [Application Structure](#application-structure)
- [Configuration](#configuration)
- [Sample Data Models](#sample-data-models)
- [Credits](#credits)
- [License](#license)

---

## Overview

**AI Task Optimizer** combines a multi-user task manager with real-time mood tracking and analytics, fostering productivity and wellbeing in team environments. The application provides:

- Task assignment, progress tracking, and team statistics
- Mood/emotion detection using OpenAI's GPT-5 API
- Analytics/visualizations to monitor emotional and productivity trends

---

## Features

- **User Authentication**: Secure login/logout system for team members.
- **Multi-Page Navigation**:
  - **Dashboard**: Overview of team status and metrics.
  - **Mood Tracker**: Log and analyze emotional wellbeing.
  - **Task Manager**: Create, assign, and monitor tasks.
  - **Team Members**: Manage and view member profiles and mood history.
  - **Analytics**: Interactive charts for mood and productivity trends.
- **AI-Powered Emotion Analysis**: Interprets textual mood updates with GPT-5 (or fallback logic if OpenAI unavailable), outputting:
  - Emotion category (happy, stressed, neutral, anxious, motivated)
  - Mood score (1–100)
  - Stress level (1–10)
  - Actionable insights
- **Personalized Task Suggestions**: AI recommends suitable tasks depending on a member’s emotional state and load.
- **Team Analytics**: Real-time charts for mood trends, completion rates, and additional metrics using Plotly.
- **Minimalist Professional UI**: Custom CSS for clean look; responsive, mobile-friendly design.

---

## System Architecture

### Frontend Architecture

- **Framework**: Streamlit
- **Pages**: Modular design (dashboard, mood tracker, task manager, team members, analytics)
  - Must reside in `/pages/` directory
  - Each exposes a `show()` function
- **Sidebar Navigation**: Built with `streamlit-option-menu`, includes page icons and a clean navigation flow
- **Custom Styles**: Defined in `utils/styles.py`, applied via injected HTML/CSS

### AI Integration Layer

- **Emotion Detection & Task Suggestions**: Via OpenAI GPT-5 API (or fallback heuristic)
  - Core logic in `utils/ai_helper.py`:
    - `analyze_emotion()`: Parses text into emotion, mood score, and insight
    - `suggest_tasks()`: AI and rule-based task assignment
    - `generate_mood_insight()`: Summarizes/team analysis
- **Mock Mode**: If no OpenAI API key, uses keyword heuristics and randomization
- **Direct SDK Usage**: OpenAI’s official SDK called directly (no intermediate frameworks, for simplicity and lower overhead)

### Data Management

- **Session State**: All live data stored in Streamlit’s session state (RAM)
  - No persistent DB (demo/prototype mode)
  - Data includes lists of members, tasks, and mood history (see `/utils/data_models.py`)
- **Data Models**:
  - **Team Member**: id, name, role, email, emotion, stress_level, mood_score, task stats, color/avatar, mood_history
  - **Task**: id, title, desc, priority, complexity, status, assignee, created_date, due_date, progress
  - **Mood History**: Per-member, 7-day time-series for graphing

### Visualization & Analytics

- **Charting**: Interactive graphs via Plotly and pandas
- **Available Visuals**: Mood timelines, gauge metrics, completion rates, etc.
- **Theme**: Consistent minimalist white/blue/gray palette, matching professional apps

---

## Installation

### Python Requirements

- Python 3.11 or higher

### Dependencies

All required libraries are listed in `pyproject.toml`:
- streamlit
- streamlit-option-menu
- streamlit-extras
- openai (optional for AI features)
- pandas
- plotly

Install via:

```bash
pip install -r requirements.txt
# or
pip install streamlit pandas plotly openai streamlit-option-menu streamlit-extras
```

### Environment Variables

If using OpenAI features, set:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

---

## Usage

1. **Run the App**:

   ```bash
   streamlit run app.py
   # or if using Replit, deploy from interface
   ```

2. **Login**:
   - Use the default account(s) listed in `users.json` for demo purposes
3. **Navigate**:
   - Use sidebar to switch pages: Dashboard, Mood Tracker, Task Manager, Team Members, Analytics

4. **Interact**:
   - Add/update tasks or log mood status to see real-time changes
   - Page content adapts based on authentication state

---

## Application Structure

```
/Task_optimizerAI
├── app.py                # Main entry point, handles navigation/layout
├── main.py               # (Demo/testing utility)
├── utils/
│   ├── ai_helper.py      # AI logic (emotion analysis, tasks, AI fallback)
│   ├── data_models.py    # Data modeling and session state logic
│   └── styles.py         # Custom CSS for professional UI
├── pages/                # Modular app pages (dashboard, mood_tracker, etc.)
├── users.json            # Demo user database
├── pyproject.toml        # Dependency management
├── replit.md             # (Extended architecture and design explanation)
└── README.md             # (You’re reading it!)
```

---

## Configuration

- **OpenAI Integration**: Optional (recommended for full experience)
  - Set `OPENAI_API_KEY` as an environment variable
- **Session Storage**: Data is stored in-memory (RAM) and resets on app restart (no persistence!)
- **Browser**: Must support modern JS, WebSockets (Chrome, Firefox, Edge, Safari recent)

---

## Sample Data Models

**User (`users.json`)**

```json
{
  "XYZ": {
    "password": "<hashed>",
    "email": "xyz@gmail.com",
    "role": "Developer",
    "team_size": 6,
    "created_at": "...",
    "team_members": []
  }
}
```

**Task (`utils/data_models.py`)**

```python
{
  'id': 1,
  'title': 'Implement user authentication',
  'description': 'Add OAuth 2.0 login functionality',
  'priority': 'High',
  'complexity': 'high',
  'status': 'In Progress',
  'assigned_to': 2,
  'created_date': ...,
  'due_date': ...,
  'progress': 60
}
```

**Team Member (`utils/data_models.py`)**

```python
{
  'id': 1,
  'name': 'Sarah Chen',
  'role': 'Frontend Developer',
  'email': 'sarah.chen@company.com',
  'emotion': 'happy',
  'stress_level': 3,
  'mood_score': 85,
  'last_update': ...,
  'mood_history': [...],
  'tasks_assigned': 3,
  'tasks_completed': 8,
  'avatar_color': '#4A90E2'
}
```

## License

This project is provided for educational/demonstration use. See repository for details or add your own license file.

---

**For further details, see `replit.md` in this repository for in-depth tech/design explanations.**
