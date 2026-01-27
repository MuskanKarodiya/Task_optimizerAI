# AI Task Optimizer

## Overview

AI Task Optimizer is a Streamlit-based team management application that combines task tracking with emotional well-being monitoring. The application leverages OpenAI's GPT-5 API to analyze team member moods from text input, providing insights into stress levels and emotional states. It features a multi-page dashboard for tracking tasks, team member performance, mood trends, and analytics.

The application is designed to help teams balance productivity with mental health by providing real-time emotional intelligence alongside traditional task management capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack**: Streamlit with minimalist professional UI
- Multi-page application structure using Streamlit's native page routing
- Pages organized in dedicated `pages/` module: dashboard, mood tracker, task manager, team members, and analytics
- Navigation handled via `streamlit-option-menu` in sidebar
- Custom CSS with clean, minimalist design using professional color palette
- Visualizations powered by Plotly for interactive charts and graphs

**Design Pattern**: Component-based architecture
- Each page is a standalone module with a `show()` function
- Shared utilities abstracted into `utils/` directory
- Session state management centralized in `utils/data_models.py`
- Styling separated into `utils/styles.py` for maintainability

**Rationale**: Streamlit provides rapid development for data-focused applications. The minimalist professional design creates a clean, corporate-friendly user experience with light gray backgrounds, white cards, and subtle shadows. Separating concerns (pages, styles, data, AI logic) enables easier maintenance and feature additions.

### AI Integration Layer

**OpenAI GPT-5 Integration**: Emotion detection and task suggestions
- Emotion analysis from free-text status updates using structured JSON output
- Model: `gpt-5` (latest as of August 2025)
- Structured prompts for consistent emotion categorization (happy/neutral/stressed/anxious/motivated)
- Returns emotion type, stress level (1-10), mood score (1-100), and contextual insights
- Graceful fallback to mock data when API key unavailable

**Design Decision**: Direct OpenAI SDK usage rather than LangChain or similar frameworks
- Pros: Simpler dependency tree, direct control over prompts, faster response times
- Cons: Manual prompt engineering, no built-in chain-of-thought features
- Rationale: Application needs are straightforward (single-shot emotion detection), avoiding framework overhead

**Integration Points**:
- `utils/ai_helper.py`: Central AI logic module
- Functions: `analyze_emotion()`, `suggest_tasks()`, `generate_mood_insight()`
- Error handling with fallback to deterministic analysis when API unavailable

### Data Management

**Session State Storage**: In-memory storage using Streamlit's session state
- No persistent database - data resets on application restart
- Team members, tasks, mood history stored as Python dictionaries/lists
- Initialization in `utils/data_models.py::initialize_session_state()`

**Data Models**:
- **Team Members**: id, name, role, email, emotion, stress_level, mood_score, mood_history, task metrics, avatar_color
- **Tasks**: id, title, description, status (To Do/In Progress/Completed), priority, assignee, dates, tags
- **Mood History**: Time-series data for charting emotional trends

**Design Rationale**: Session state chosen for simplicity in prototype/demo scenario
- Pros: Zero setup, no database configuration, fast development
- Cons: No data persistence, not suitable for production, doesn't scale
- Future consideration: Migration to SQLite, PostgreSQL, or cloud database for production deployment

### Visualization & Analytics

**Charting Library**: Plotly
- Interactive graphs for mood trends, task timelines, team performance
- Supports bar charts, line graphs, gauge charts, and custom layouts
- Theming matches minimalist professional design with clean white backgrounds

**Analytics Features**:
- Real-time calculation of team statistics (avg mood, stress, completion rates)
- Simulated historical data for demonstration purposes
- Time-period filtering (last 7 days, 30 days, all time)

## External Dependencies

### Third-Party Services

**OpenAI API** (gpt-5)
- Purpose: Emotion analysis from text, task suggestions, mood insights
- Authentication: API key via `OPENAI_API_KEY` environment variable
- Fallback: Mock responses when API unavailable
- Cost consideration: Pay-per-token usage model

### Python Packages

**Core Framework**:
- `streamlit`: Web application framework
- `streamlit-option-menu`: Enhanced sidebar navigation

**Data & Visualization**:
- `plotly`: Interactive charting library
- `pandas`: Data manipulation (used for analytics)

**AI/ML**:
- `openai`: Official OpenAI Python SDK (optional, graceful degradation)

**Standard Library**:
- `datetime`: Timestamp handling and date calculations
- `json`: API response parsing
- `random`: Mock data generation
- `typing`: Type hints for code clarity

### Configuration Requirements

**Environment Variables**:
- `OPENAI_API_KEY`: Required for AI-powered emotion analysis (optional for demo mode)

**No Database**: Application currently uses in-memory storage only

### Browser Requirements

- Modern browser with JavaScript enabled
- WebSocket support for Streamlit real-time updates
- Recommended: Chrome, Firefox, Safari, Edge (latest versions)