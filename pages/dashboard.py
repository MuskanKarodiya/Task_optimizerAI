import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from utils.data_models import (
    get_team_statistics, get_emotion_emoji, get_emotion_color
)
from utils.ai_helper import generate_mood_insight

def show():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>📊 Team Dashboard</h1>", unsafe_allow_html=True)
    
    # Get team statistics
    stats = get_team_statistics()
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; margin-bottom: 10px; opacity: 0.9;'>Team Mood</p>
            <div class='metric-value'>{stats['avg_mood']:.0f}</div>
            <p style='font-size: 0.8rem; opacity: 0.7;'>Average Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        stress_emoji = "🟢" if stats['avg_stress'] < 5 else "🟡" if stats['avg_stress'] < 7 else "🔴"
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; margin-bottom: 10px; opacity: 0.9;'>Stress Level</p>
            <div class='metric-value'>{stress_emoji} {stats['avg_stress']:.1f}</div>
            <p style='font-size: 0.8rem; opacity: 0.7;'>Out of 10</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; margin-bottom: 10px; opacity: 0.9;'>Task Completion</p>
            <div class='metric-value'>{stats['completion_rate']:.0f}%</div>
            <p style='font-size: 0.8rem; opacity: 0.7;'>{stats['completed_tasks']}/{stats['total_tasks']} Tasks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='glass-card' style='text-align: center;'>
            <p style='font-size: 0.9rem; margin-bottom: 10px; opacity: 0.9;'>Active Tasks</p>
            <div class='metric-value'>{stats['in_progress_tasks']}</div>
            <p style='font-size: 0.8rem; opacity: 0.7;'>In Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # AI Insights Section
    st.markdown("<h2>🤖 AI Team Insights</h2>", unsafe_allow_html=True)
    insight = generate_mood_insight(st.session_state.team_members)
    st.markdown(f"""
    <div class='glass-card'>
        <p style='font-size: 1.1rem; line-height: 1.6;'>{insight}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>Team Mood Distribution</h3>", unsafe_allow_html=True)
        
        # Mood distribution pie chart
        mood_data = {
            'Status': ['Positive', 'Neutral', 'Stressed'],
            'Count': [stats['happy_count'], stats['neutral_count'], stats['stressed_count']],
            'Color': ['#4CAF50', '#9E9E9E', '#F44336']
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=mood_data['Status'],
            values=mood_data['Count'],
            marker=dict(colors=mood_data['Color']),
            hole=0.4,
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<h3>Team Stress Heatmap</h3>", unsafe_allow_html=True)
        
        # Stress level bar chart
        members_data = []
        for member in st.session_state.team_members:
            members_data.append({
                'name': member['name'],
                'stress': member['stress_level'],
                'color': '#4CAF50' if member['stress_level'] < 5 else '#FF9800' if member['stress_level'] < 7 else '#F44336'
            })
        
        fig = go.Figure(data=[go.Bar(
            x=[m['name'] for m in members_data],
            y=[m['stress'] for m in members_data],
            marker=dict(
                color=[m['stress'] for m in members_data],
                colorscale=[[0, '#4CAF50'], [0.5, '#FF9800'], [1, '#F44336']],
                showscale=False
            ),
            text=[f"{m['stress']}/10" for m in members_data],
            textposition='outside',
            textfont=dict(color='white'),
            hovertemplate='<b>%{x}</b><br>Stress Level: %{y}/10<extra></extra>'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            yaxis=dict(range=[0, 10], title='Stress Level', gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(title='', gridcolor='rgba(255,255,255,0.1)'),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Team Member Cards
    st.markdown("<h2>👥 Team Overview</h2>", unsafe_allow_html=True)
    
    cols = st.columns(min(3, len(st.session_state.team_members)))
    
    for idx, member in enumerate(st.session_state.team_members[:6]):
        with cols[idx % 3]:
            emoji = get_emotion_emoji(member['emotion'])
            color = get_emotion_color(member['emotion'])
            
            st.markdown(f"""
            <div class='glass-card'>
                <div style='display: flex; align-items: center; margin-bottom: 15px;'>
                    <div class='avatar' style='background: {member["avatar_color"]};'>
                        {member['name'][0]}
                    </div>
                    <div style='margin-left: 15px;'>
                        <p style='margin: 0; font-weight: 600; font-size: 1.1rem;'>{member['name']}</p>
                        <p style='margin: 0; font-size: 0.85rem; opacity: 0.8;'>{member['role']}</p>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin: 10px 0;'>
                    <p style='margin: 0; font-size: 0.9rem;'>Mood: {emoji} {member['emotion'].title()}</p>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem;'>Stress: {member['stress_level']}/10</p>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 10px;'>
                    <div style='text-align: center;'>
                        <p style='margin: 0; font-size: 1.3rem; font-weight: 700; color: #4CAF50;'>{member['tasks_completed']}</p>
                        <p style='margin: 0; font-size: 0.75rem; opacity: 0.7;'>Completed</p>
                    </div>
                    <div style='text-align: center;'>
                        <p style='margin: 0; font-size: 1.3rem; font-weight: 700; color: #FF9800;'>{member['tasks_assigned']}</p>
                        <p style='margin: 0; font-size: 0.75rem; opacity: 0.7;'>Active</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent Activity Timeline
    st.markdown("<h2>📝 Recent Mood Updates</h2>", unsafe_allow_html=True)
    
    if st.session_state.mood_logs:
        for log in st.session_state.mood_logs[:5]:
            time_diff = datetime.now() - log['timestamp']
            if time_diff.seconds < 3600:
                time_str = f"{time_diff.seconds // 60} minutes ago"
            else:
                time_str = f"{time_diff.seconds // 3600} hours ago"
            
            emoji = get_emotion_emoji(log['emotion'])
            
            st.markdown(f"""
            <div class='glass-card' style='padding: 15px; margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='margin: 0; font-weight: 600;'>{emoji} {log['member_name']}</p>
                        <p style='margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;'>{log['insight']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <p style='margin: 0; font-size: 0.85rem; opacity: 0.7;'>{time_str}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No mood updates yet. Visit the Mood Tracker to log team emotions!")
