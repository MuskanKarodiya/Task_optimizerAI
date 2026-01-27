import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from utils.data_models import get_team_statistics, get_emotion_color

def show():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>📈 Advanced Analytics</h1>", unsafe_allow_html=True)
    
    stats = get_team_statistics()
    
    # Time period selector
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3>Performance & Wellness Analytics</h3>
            <p style='opacity: 0.9;'>Comprehensive insights into team productivity and emotional well-being.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        time_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "All Time"])
    
    # Main Analytics Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>Task Completion Timeline</h3>", unsafe_allow_html=True)
        
        # Simulated task completion over time
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        completed = [3, 5, 4, 7, 6, 8, stats['completed_tasks'] if stats['completed_tasks'] > 0 else 5]
        in_progress = [4, 3, 5, 4, 6, 5, stats['in_progress_tasks'] if stats['in_progress_tasks'] > 0 else 4]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=dates,
            y=completed,
            name='Completed',
            marker_color='#4CAF50',
            hovertemplate='<b>%{x}</b><br>Completed: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=dates,
            y=in_progress,
            name='In Progress',
            marker_color='#2196F3',
            hovertemplate='<b>%{x}</b><br>In Progress: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title='Date', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Tasks', gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<h3>Team Productivity Score</h3>", unsafe_allow_html=True)
        
        # Calculate productivity score
        productivity_score = min(100, int(
            (stats['completion_rate'] * 0.4) +
            ((100 - stats['avg_stress'] * 10) * 0.3) +
            (stats['avg_mood'] * 0.3)
        ))
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=productivity_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Productivity Score", 'font': {'size': 24, 'color': 'white'}},
            delta={'reference': 75, 'increasing': {'color': "#4CAF50"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#667eea"},
                'bgcolor': "rgba(255,255,255,0.1)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(244, 67, 54, 0.3)'},
                    {'range': [50, 75], 'color': 'rgba(255, 152, 0, 0.3)'},
                    {'range': [75, 100], 'color': 'rgba(76, 175, 80, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Inter"},
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Individual Performance Matrix
    st.markdown("<h3>Individual Performance Matrix</h3>", unsafe_allow_html=True)
    
    # Create performance dataframe
    perf_data = []
    for member in st.session_state.team_members:
        completion_rate = (member['tasks_completed'] / (member['tasks_completed'] + member['tasks_assigned']) * 100) if (member['tasks_completed'] + member['tasks_assigned']) > 0 else 0
        perf_data.append({
            'Name': member['name'],
            'Role': member['role'],
            'Mood Score': member['mood_score'],
            'Stress Level': member['stress_level'],
            'Tasks Completed': member['tasks_completed'],
            'Active Tasks': member['tasks_assigned'],
            'Completion Rate': f"{completion_rate:.1f}%"
        })
    
    df = pd.DataFrame(perf_data)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mood vs Productivity Correlation
    st.markdown("<h3>Mood vs Task Completion Analysis</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot: Mood Score vs Tasks Completed
        fig = go.Figure()
        
        for member in st.session_state.team_members:
            fig.add_trace(go.Scatter(
                x=[member['mood_score']],
                y=[member['tasks_completed']],
                mode='markers+text',
                name=member['name'],
                marker=dict(
                    size=15,
                    color=member['avatar_color'],
                    line=dict(width=2, color='white')
                ),
                text=[member['name'].split()[0]],
                textposition="top center",
                textfont=dict(color='white', size=10),
                hovertemplate=f"<b>{member['name']}</b><br>Mood: {member['mood_score']}<br>Completed: {member['tasks_completed']}<extra></extra>"
            ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title='Mood Score', range=[0, 100], gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Tasks Completed', gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False,
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Emotion distribution radar chart
        emotions = {}
        for member in st.session_state.team_members:
            emotion = member['emotion']
            emotions[emotion] = emotions.get(emotion, 0) + 1
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(emotions.values()),
            theta=list(emotions.keys()),
            fill='toself',
            line=dict(color='#667eea', width=2),
            marker=dict(size=8, color='#764ba2'),
            hovertemplate='<b>%{theta}</b><br>Count: %{r}<extra></extra>'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(emotions.values()) + 1],
                    gridcolor='rgba(255,255,255,0.2)',
                    color='white'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.2)',
                    color='white'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            height=350,
            title=dict(text='Emotion Distribution', font=dict(color='white', size=16))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights and Recommendations
    st.markdown("<h3>📊 Key Insights & Recommendations</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # High performers
        top_performer = max(st.session_state.team_members, key=lambda x: x['tasks_completed'])
        st.markdown(f"""
        <div class='glass-card'>
            <h4>🏆 Top Performer</h4>
            <p style='font-size: 1.2rem; font-weight: 600; margin: 10px 0;'>{top_performer['name']}</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>{top_performer['tasks_completed']} tasks completed</p>
            <p style='font-size: 0.85rem; opacity: 0.8; margin-top: 10px;'>
            Mood: {top_performer['mood_score']}/100<br>
            Stress: {top_performer['stress_level']}/10
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Members needing support
        stressed_members = [m for m in st.session_state.team_members if m['stress_level'] > 7]
        st.markdown(f"""
        <div class='glass-card'>
            <h4>⚠️ Needs Support</h4>
            <p style='font-size: 2rem; font-weight: 700; margin: 10px 0; color: #F44336;'>{len(stressed_members)}</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>members with high stress</p>
            <p style='font-size: 0.85rem; opacity: 0.8; margin-top: 10px;'>
            Consider workload adjustment or additional support
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Team health score
        health_score = int((stats['avg_mood'] + (100 - stats['avg_stress'] * 10)) / 2)
        health_color = "#4CAF50" if health_score >= 70 else "#FF9800" if health_score >= 50 else "#F44336"
        st.markdown(f"""
        <div class='glass-card'>
            <h4>💚 Team Health</h4>
            <p style='font-size: 2rem; font-weight: 700; margin: 10px 0; color: {health_color};'>{health_score}%</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>Overall wellness score</p>
            <p style='font-size: 0.85rem; opacity: 0.8; margin-top: 10px;'>
            Based on mood and stress metrics
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Export Data Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3>📥 Export Analytics Data</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Team Data (CSV)", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"team_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Generate Report", use_container_width=True):
            st.info("Report generation feature coming soon!")
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
