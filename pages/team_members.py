import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from utils.data_models import get_emotion_emoji, get_emotion_color

def show():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>👥 Team Members</h1>", unsafe_allow_html=True)
    
    # Team overview
    st.markdown(f"""
    <div class='glass-card'>
        <h3>Team Overview</h3>
        <p style='font-size: 1rem; opacity: 0.9;'>
        Manage your team members, view individual performance metrics, and track mood trends over time.
        </p>
        <p style='font-size: 0.95rem; opacity: 0.8; margin-top: 10px;'>
        Total Team Members: <strong>{len(st.session_state.team_members)}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each team member
    for member in st.session_state.team_members:
        emoji = get_emotion_emoji(member['emotion'])
        color = get_emotion_color(member['emotion'])
        
        with st.expander(f"**{member['name']}** - {member['role']}", expanded=False):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style='text-align: center; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px;'>
                    <div class='avatar' style='background: {member["avatar_color"]}; width: 80px; height: 80px; 
                                               font-size: 2rem; margin: 0 auto 15px;'>
                        {member['name'][0]}
                    </div>
                    <p style='font-size: 1.3rem; font-weight: 600; margin: 0;'>{member['name']}</p>
                    <p style='font-size: 1rem; opacity: 0.8; margin: 5px 0;'>{member['role']}</p>
                    <p style='font-size: 0.85rem; opacity: 0.7; margin: 5px 0;'>{member['email']}</p>
                    
                    <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);'>
                        <p style='font-size: 2.5rem; margin: 5px 0;'>{emoji}</p>
                        <p style='font-size: 1.1rem; font-weight: 600; color: {color}; margin: 5px 0;'>{member['emotion'].title()}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Performance metrics
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;'>
                    <p style='font-size: 0.9rem; font-weight: 600; margin-bottom: 10px;'>Performance Metrics</p>
                    <div style='display: flex; justify-content: space-around; margin-top: 10px;'>
                        <div style='text-align: center;'>
                            <p style='font-size: 1.8rem; font-weight: 700; margin: 0; color: #4CAF50;'>{member['tasks_completed']}</p>
                            <p style='font-size: 0.75rem; opacity: 0.8; margin: 0;'>Completed</p>
                        </div>
                        <div style='text-align: center;'>
                            <p style='font-size: 1.8rem; font-weight: 700; margin: 0; color: #FF9800;'>{member['tasks_assigned']}</p>
                            <p style='font-size: 0.75rem; opacity: 0.8; margin: 0;'>Active</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Current Status
                st.markdown("#### Current Status")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;'>
                        <p style='font-size: 0.85rem; opacity: 0.8; margin: 0 0 5px 0;'>Stress Level</p>
                        <p style='font-size: 2rem; font-weight: 700; margin: 0;'>{member['stress_level']}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;'>
                        <p style='font-size: 0.85rem; opacity: 0.8; margin: 0 0 5px 0;'>Mood Score</p>
                        <p style='font-size: 2rem; font-weight: 700; margin: 0;'>{member['mood_score']}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mood History Chart
                st.markdown("#### Mood Trend (Last 7 Days)")
                
                if member.get('mood_history'):
                    dates = [h['date'] for h in member['mood_history']]
                    mood_scores = [h['mood_score'] for h in member['mood_history']]
                    stress_levels = [h['stress_level'] * 10 for h in member['mood_history']]  # Scale to 100
                    
                    fig = go.Figure()
                    
                    # Mood score line
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=mood_scores,
                        mode='lines+markers',
                        name='Mood Score',
                        line=dict(color='#4CAF50', width=3),
                        marker=dict(size=8),
                        hovertemplate='<b>%{x}</b><br>Mood: %{y}/100<extra></extra>'
                    ))
                    
                    # Stress level line
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=stress_levels,
                        mode='lines+markers',
                        name='Stress Level',
                        line=dict(color='#F44336', width=3, dash='dash'),
                        marker=dict(size=8),
                        hovertemplate='<b>%{x}</b><br>Stress: %{y}/100<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis=dict(
                            title='Date',
                            gridcolor='rgba(255,255,255,0.1)',
                            showgrid=True
                        ),
                        yaxis=dict(
                            title='Score',
                            range=[0, 100],
                            gridcolor='rgba(255,255,255,0.1)',
                            showgrid=True
                        ),
                        hovermode='x unified',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        height=300,
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No mood history available yet.")
                
                # Last Update
                time_diff = datetime.now() - member['last_update']
                if time_diff.seconds < 3600:
                    time_str = f"{time_diff.seconds // 60} minutes ago"
                elif time_diff.seconds < 86400:
                    time_str = f"{time_diff.seconds // 3600} hours ago"
                else:
                    time_str = f"{time_diff.days} days ago"
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; margin-top: 15px;'>
                    <p style='font-size: 0.85rem; margin: 0;'>
                        <strong>Last Update:</strong> {time_str}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Add New Member Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2>➕ Add New Team Member</h2>", unsafe_allow_html=True)
    
    with st.expander("Create New Member Profile"):
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name")
            new_role = st.text_input("Role / Position")
        
        with col2:
            new_email = st.text_input("Email Address")
            new_color = st.color_picker("Avatar Color", "#4A90E2")
        
        if st.button("➕ Add Team Member", type="primary"):
            if new_name and new_role and new_email:
                new_id = max([m['id'] for m in st.session_state.team_members]) + 1
                
                new_member = {
                    'id': new_id,
                    'name': new_name,
                    'role': new_role,
                    'email': new_email,
                    'emotion': 'neutral',
                    'stress_level': 5,
                    'mood_score': 60,
                    'last_update': datetime.now(),
                    'mood_history': [],
                    'tasks_assigned': 0,
                    'tasks_completed': 0,
                    'avatar_color': new_color
                }
                
                st.session_state.team_members.append(new_member)
                st.success(f"✅ {new_name} has been added to the team!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
