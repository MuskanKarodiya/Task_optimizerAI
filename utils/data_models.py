import streamlit as st
from datetime import datetime, timedelta
import random
from typing import List, Dict

def initialize_session_state():
    """Initialize all session state variables"""
    
    if 'team_members' not in st.session_state:
        st.session_state.team_members = [
            {
                'id': 1,
                'name': 'Sarah Chen',
                'role': 'Frontend Developer',
                'email': 'sarah.chen@company.com',
                'emotion': 'happy',
                'stress_level': 3,
                'mood_score': 85,
                'last_update': datetime.now() - timedelta(hours=2),
                'mood_history': generate_mood_history('happy'),
                'tasks_assigned': 3,
                'tasks_completed': 8,
                'avatar_color': '#4A90E2'
            },
            {
                'id': 2,
                'name': 'Marcus Williams',
                'role': 'Backend Developer',
                'email': 'marcus.w@company.com',
                'emotion': 'stressed',
                'stress_level': 7,
                'mood_score': 45,
                'last_update': datetime.now() - timedelta(hours=1),
                'mood_history': generate_mood_history('stressed'),
                'tasks_assigned': 5,
                'tasks_completed': 6,
                'avatar_color': '#E94B3C'
            },
            {
                'id': 3,
                'name': 'Aisha Patel',
                'role': 'UX Designer',
                'email': 'aisha.patel@company.com',
                'emotion': 'motivated',
                'stress_level': 4,
                'mood_score': 78,
                'last_update': datetime.now() - timedelta(minutes=30),
                'mood_history': generate_mood_history('motivated'),
                'tasks_assigned': 2,
                'tasks_completed': 12,
                'avatar_color': '#50C878'
            },
            {
                'id': 4,
                'name': 'James Kim',
                'role': 'Project Manager',
                'email': 'james.kim@company.com',
                'emotion': 'neutral',
                'stress_level': 5,
                'mood_score': 65,
                'last_update': datetime.now() - timedelta(hours=4),
                'mood_history': generate_mood_history('neutral'),
                'tasks_assigned': 4,
                'tasks_completed': 15,
                'avatar_color': '#9B59B6'
            },
            {
                'id': 5,
                'name': 'Emma Rodriguez',
                'role': 'QA Engineer',
                'email': 'emma.r@company.com',
                'emotion': 'happy',
                'stress_level': 2,
                'mood_score': 92,
                'last_update': datetime.now() - timedelta(minutes=15),
                'mood_history': generate_mood_history('happy'),
                'tasks_assigned': 3,
                'tasks_completed': 10,
                'avatar_color': '#F39C12'
            }
        ]
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {
                'id': 1,
                'title': 'Implement user authentication',
                'description': 'Add OAuth 2.0 login functionality',
                'priority': 'High',
                'complexity': 'high',
                'status': 'In Progress',
                'assigned_to': 2,
                'created_date': datetime.now() - timedelta(days=3),
                'due_date': datetime.now() + timedelta(days=4),
                'progress': 60
            },
            {
                'id': 2,
                'title': 'Design landing page mockup',
                'description': 'Create high-fidelity designs for homepage',
                'priority': 'Medium',
                'complexity': 'medium',
                'status': 'In Progress',
                'assigned_to': 3,
                'created_date': datetime.now() - timedelta(days=2),
                'due_date': datetime.now() + timedelta(days=3),
                'progress': 75
            },
            {
                'id': 3,
                'title': 'Fix navigation bugs',
                'description': 'Resolve mobile menu issues',
                'priority': 'High',
                'complexity': 'low',
                'status': 'To Do',
                'assigned_to': 1,
                'created_date': datetime.now() - timedelta(days=1),
                'due_date': datetime.now() + timedelta(days=2),
                'progress': 0
            },
            {
                'id': 4,
                'title': 'Write API documentation',
                'description': 'Document all REST endpoints',
                'priority': 'Medium',
                'complexity': 'medium',
                'status': 'To Do',
                'assigned_to': None,
                'created_date': datetime.now() - timedelta(days=1),
                'due_date': datetime.now() + timedelta(days=5),
                'progress': 0
            },
            {
                'id': 5,
                'title': 'Setup automated testing',
                'description': 'Configure CI/CD pipeline with Jest',
                'priority': 'High',
                'complexity': 'high',
                'status': 'To Do',
                'assigned_to': None,
                'created_date': datetime.now(),
                'due_date': datetime.now() + timedelta(days=7),
                'progress': 0
            },
            {
                'id': 6,
                'title': 'Optimize database queries',
                'description': 'Improve performance of user data fetching',
                'priority': 'Low',
                'complexity': 'medium',
                'status': 'In Progress',
                'assigned_to': 2,
                'created_date': datetime.now() - timedelta(days=4),
                'due_date': datetime.now() + timedelta(days=6),
                'progress': 30
            },
            {
                'id': 7,
                'title': 'Conduct usability testing',
                'description': 'Test new features with 5 users',
                'priority': 'Medium',
                'complexity': 'low',
                'status': 'To Do',
                'assigned_to': 5,
                'created_date': datetime.now(),
                'due_date': datetime.now() + timedelta(days=8),
                'progress': 0
            }
        ]
    
    if 'mood_logs' not in st.session_state:
        st.session_state.mood_logs = []


def generate_mood_history(emotion: str) -> List[Dict]:
    """Generate sample mood history for visualization"""
    history = []
    base_score = {'happy': 80, 'stressed': 45, 'motivated': 75, 'neutral': 60, 'anxious': 40}
    base = base_score.get(emotion, 60)
    
    for i in range(7):
        date = datetime.now() - timedelta(days=6-i)
        score = base + random.randint(-15, 15)
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'mood_score': max(10, min(100, score)),
            'stress_level': random.randint(1, 10)
        })
    
    return history


def get_emotion_emoji(emotion: str) -> str:
    """Return emoji for emotion"""
    emoji_map = {
        'happy': '😊',
        'stressed': '😰',
        'anxious': '😟',
        'motivated': '🚀',
        'neutral': '😐',
        'tired': '😴',
        'excited': '🎉'
    }
    return emoji_map.get(emotion.lower(), '😐')


def get_emotion_color(emotion: str) -> str:
    """Return color for emotion"""
    color_map = {
        'happy': '#4CAF50',
        'stressed': '#F44336',
        'anxious': '#FF9800',
        'motivated': '#2196F3',
        'neutral': '#9E9E9E',
        'tired': '#795548',
        'excited': '#E91E63'
    }
    return color_map.get(emotion.lower(), '#9E9E9E')


def get_priority_color(priority: str) -> str:
    """Return color for task priority"""
    color_map = {
        'High': '#F44336',
        'Medium': '#FF9800',
        'Low': '#4CAF50'
    }
    return color_map.get(priority, '#9E9E9E')


def get_team_member_by_id(member_id: int) -> Dict:
    """Get team member data by ID"""
    for member in st.session_state.team_members:
        if member['id'] == member_id:
            return member
    return None


def update_member_mood(member_id: int, emotion: str, stress_level: int, mood_score: int, insight: str):
    """Update team member's mood data"""
    for member in st.session_state.team_members:
        if member['id'] == member_id:
            member['emotion'] = emotion
            member['stress_level'] = stress_level
            member['mood_score'] = mood_score
            member['last_update'] = datetime.now()
            
            # Add to mood history
            member['mood_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'mood_score': mood_score,
                'stress_level': stress_level
            })
            
            # Keep only last 7 days
            if len(member['mood_history']) > 7:
                member['mood_history'] = member['mood_history'][-7:]
            
            # Log mood update
            st.session_state.mood_logs.insert(0, {
                'timestamp': datetime.now(),
                'member_name': member['name'],
                'emotion': emotion,
                'stress_level': stress_level,
                'mood_score': mood_score,
                'insight': insight
            })
            break


def add_new_task(task_data: Dict):
    """Add a new task to the task list"""
    new_id = max([t['id'] for t in st.session_state.tasks]) + 1 if st.session_state.tasks else 1
    task_data['id'] = new_id
    task_data['created_date'] = datetime.now()
    task_data['progress'] = 0
    st.session_state.tasks.append(task_data)


def update_task_status(task_id: int, status: str, progress: int = None):
    """Update task status and progress"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['status'] = status
            if progress is not None:
                task['progress'] = progress
            
            # Update member task counts
            if task['assigned_to']:
                member = get_team_member_by_id(task['assigned_to'])
                if member and status == 'Completed':
                    member['tasks_completed'] += 1
                    member['tasks_assigned'] = max(0, member['tasks_assigned'] - 1)
            break


def assign_task_to_member(task_id: int, member_id: int):
    """Assign a task to a team member"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            old_assignee = task['assigned_to']
            task['assigned_to'] = member_id
            
            # Update old assignee count
            if old_assignee:
                old_member = get_team_member_by_id(old_assignee)
                if old_member:
                    old_member['tasks_assigned'] = max(0, old_member['tasks_assigned'] - 1)
            
            # Update new assignee count
            if member_id:
                new_member = get_team_member_by_id(member_id)
                if new_member:
                    new_member['tasks_assigned'] += 1
            break


def get_team_statistics() -> Dict:
    """Calculate team-wide statistics"""
    if not st.session_state.team_members:
        return {}
    
    total_members = len(st.session_state.team_members)
    avg_mood = sum(m['mood_score'] for m in st.session_state.team_members) / total_members
    avg_stress = sum(m['stress_level'] for m in st.session_state.team_members) / total_members
    
    happy_count = sum(1 for m in st.session_state.team_members if m['mood_score'] >= 70)
    neutral_count = sum(1 for m in st.session_state.team_members if 40 <= m['mood_score'] < 70)
    stressed_count = sum(1 for m in st.session_state.team_members if m['mood_score'] < 40)
    
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for t in st.session_state.tasks if t['status'] == 'Completed')
    in_progress_tasks = sum(1 for t in st.session_state.tasks if t['status'] == 'In Progress')
    
    return {
        'total_members': total_members,
        'avg_mood': avg_mood,
        'avg_stress': avg_stress,
        'happy_count': happy_count,
        'neutral_count': neutral_count,
        'stressed_count': stressed_count,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }
