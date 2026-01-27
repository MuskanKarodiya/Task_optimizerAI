import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from utils.data_models import (
    get_team_member_by_id, add_new_task, update_task_status, 
    assign_task_to_member, get_priority_color
)
from utils.ai_helper import suggest_tasks

def show():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>📋 Task Management</h1>", unsafe_allow_html=True)
    
    # Task Overview Metrics
    total_tasks = len(st.session_state.tasks)
    todo_tasks = sum(1 for t in st.session_state.tasks if t['status'] == 'To Do')
    in_progress_tasks = sum(1 for t in st.session_state.tasks if t['status'] == 'In Progress')
    completed_tasks = sum(1 for t in st.session_state.tasks if t['status'] == 'Completed')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; opacity: 0.9;'>Total Tasks</p>
            <p style='font-size: 2.5rem; font-weight: 700; margin: 10px 0;'>{total_tasks}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; opacity: 0.9;'>To Do</p>
            <p style='font-size: 2.5rem; font-weight: 700; margin: 10px 0; color: #FF9800;'>{todo_tasks}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; opacity: 0.9;'>In Progress</p>
            <p style='font-size: 2.5rem; font-weight: 700; margin: 10px 0; color: #2196F3;'>{in_progress_tasks}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; opacity: 0.9;'>Completed</p>
            <p style='font-size: 2.5rem; font-weight: 700; margin: 10px 0; color: #4CAF50;'>{completed_tasks}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 All Tasks", "➕ Create Task", "🤖 AI Suggestions"])
    
    with tab1:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_status = st.selectbox("Filter by Status", ["All", "To Do", "In Progress", "Completed"])
        with col2:
            filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        with col3:
            filter_assignee = st.selectbox("Filter by Assignee", ["All"] + [m['name'] for m in st.session_state.team_members])
        
        # Filter tasks
        filtered_tasks = st.session_state.tasks
        
        if filter_status != "All":
            filtered_tasks = [t for t in filtered_tasks if t['status'] == filter_status]
        if filter_priority != "All":
            filtered_tasks = [t for t in filtered_tasks if t['priority'] == filter_priority]
        if filter_assignee != "All":
            member_id = None
            for m in st.session_state.team_members:
                if m['name'] == filter_assignee:
                    member_id = m['id']
                    break
            if member_id:
                filtered_tasks = [t for t in filtered_tasks if t['assigned_to'] == member_id]
        
        st.markdown(f"<p style='font-size: 0.9rem; opacity: 0.8;'>Showing {len(filtered_tasks)} tasks</p>", unsafe_allow_html=True)
        
        # Display tasks
        for task in filtered_tasks:
            assignee_name = "Unassigned"
            if task['assigned_to']:
                member = get_team_member_by_id(task['assigned_to'])
                if member:
                    assignee_name = member['name']
            
            priority_color = get_priority_color(task['priority'])
            status_color = {"To Do": "#FF9800", "In Progress": "#2196F3", "Completed": "#4CAF50"}.get(task['status'], "#9E9E9E")
            
            # Days until due
            days_until = (task['due_date'] - datetime.now()).days
            due_text = f"{days_until} days" if days_until > 0 else f"Overdue by {abs(days_until)} days"
            due_color = "#4CAF50" if days_until > 3 else "#FF9800" if days_until > 0 else "#F44336"
            
            with st.expander(f"**{task['title']}** - {task['priority']} Priority"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;'>
                        <p style='margin: 0 0 10px 0;'><strong>Description:</strong></p>
                        <p style='margin: 0 0 15px 0; font-size: 0.95rem; opacity: 0.9;'>{task['description']}</p>
                        
                        <div style='display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px;'>
                            <div>
                                <span style='opacity: 0.7;'>Status:</span>
                                <span style='background: {status_color}; padding: 4px 12px; border-radius: 12px; 
                                           margin-left: 8px; font-size: 0.85rem; font-weight: 600;'>{task['status']}</span>
                            </div>
                            <div>
                                <span style='opacity: 0.7;'>Priority:</span>
                                <span style='background: {priority_color}; padding: 4px 12px; border-radius: 12px; 
                                           margin-left: 8px; font-size: 0.85rem; font-weight: 600;'>{task['priority']}</span>
                            </div>
                            <div>
                                <span style='opacity: 0.7;'>Assigned to:</span>
                                <span style='font-weight: 600; margin-left: 8px;'>{assignee_name}</span>
                            </div>
                            <div>
                                <span style='opacity: 0.7;'>Due:</span>
                                <span style='color: {due_color}; font-weight: 600; margin-left: 8px;'>{due_text}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**Progress: {task['progress']}%**")
                    st.progress(task['progress'] / 100)
                    
                    new_status = st.selectbox(
                        "Update Status",
                        ["To Do", "In Progress", "Completed"],
                        index=["To Do", "In Progress", "Completed"].index(task['status']),
                        key=f"status_{task['id']}"
                    )
                    
                    new_progress = st.slider(
                        "Update Progress",
                        0, 100, task['progress'],
                        key=f"progress_{task['id']}"
                    )
                    
                    if st.button("💾 Save Changes", key=f"save_{task['id']}"):
                        update_task_status(task['id'], new_status, new_progress)
                        st.success("Task updated!")
                        st.rerun()
    
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Create New Task</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title")
            task_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            task_complexity = st.selectbox("Complexity", ["high", "medium", "low"])
        
        with col2:
            task_status = st.selectbox("Initial Status", ["To Do", "In Progress"])
            due_days = st.number_input("Due in (days)", min_value=1, max_value=30, value=7)
            assign_to = st.selectbox("Assign To", ["Unassigned"] + [m['name'] for m in st.session_state.team_members])
        
        task_description = st.text_area("Task Description", height=100)
        
        if st.button("➕ Create Task", type="primary"):
            if task_title and task_description:
                assignee_id = None
                if assign_to != "Unassigned":
                    for m in st.session_state.team_members:
                        if m['name'] == assign_to:
                            assignee_id = m['id']
                            break
                
                new_task = {
                    'title': task_title,
                    'description': task_description,
                    'priority': task_priority,
                    'complexity': task_complexity,
                    'status': task_status,
                    'assigned_to': assignee_id,
                    'due_date': datetime.now() + timedelta(days=due_days)
                }
                
                add_new_task(new_task)
                st.success(f"✅ Task '{task_title}' created successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>🤖 AI-Powered Task Suggestions</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style='opacity: 0.9; margin-bottom: 20px;'>
        Get intelligent task recommendations based on team member's current emotional state and stress levels.
        </p>
        """, unsafe_allow_html=True)
        
        selected_member = st.selectbox(
            "Select Team Member",
            [m['name'] for m in st.session_state.team_members],
            key="ai_suggest_member"
        )
        
        if st.button("🎯 Get Task Suggestions", type="primary"):
            # Find selected member
            member = None
            for m in st.session_state.team_members:
                if m['name'] == selected_member:
                    member = m
                    break
            
            if member:
                # Get unassigned or available tasks
                available_tasks = [t for t in st.session_state.tasks if t['status'] != 'Completed']
                
                if available_tasks:
                    with st.spinner("🤖 Analyzing best task matches..."):
                        suggestions = suggest_tasks(
                            member['name'],
                            member['emotion'],
                            member['stress_level'],
                            available_tasks
                        )
                        
                        st.markdown(f"""
                        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;'>
                            <p style='margin: 0;'><strong>Analysis for {member['name']}</strong></p>
                            <p style='margin: 5px 0; opacity: 0.9;'>Current Mood: {member['emotion'].title()} | Stress: {member['stress_level']}/10</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for idx, suggestion in enumerate(suggestions[:5], 1):
                            score_color = "#4CAF50" if suggestion['suitability_score'] > 70 else "#FF9800" if suggestion['suitability_score'] > 50 else "#F44336"
                            
                            st.markdown(f"""
                            <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                                    <p style='margin: 0; font-weight: 600; font-size: 1.1rem;'>#{idx}. {suggestion['task_title']}</p>
                                    <span style='background: {score_color}; padding: 6px 14px; border-radius: 15px; 
                                               font-weight: 600; font-size: 0.9rem;'>{suggestion['suitability_score']}% Match</span>
                                </div>
                                <p style='margin: 0; font-size: 0.95rem; opacity: 0.9;'>💡 {suggestion['reason']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No available tasks for assignment.")
        
        st.markdown("</div>", unsafe_allow_html=True)
