import streamlit as st
from datetime import datetime
from utils.data_models import update_member_mood, get_emotion_emoji, get_emotion_color
from utils.ai_helper import analyze_emotion

def show():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>😊 Team Mood Tracker</h1>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class='glass-card'>
        <h3>🎯 Track Your Team's Emotional Well-being</h3>
        <p style='font-size: 1rem; line-height: 1.6;'>
        Use AI-powered emotion detection to analyze team member status updates. 
        The system will detect mood, stress levels, and provide personalized insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mood Check-in Form
    st.markdown("<h2>📝 Mood Check-in</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # Select team member
        member_names = [m['name'] for m in st.session_state.team_members]
        selected_member = st.selectbox(
            "Select Team Member",
            member_names,
            key="mood_member_select"
        )
        
        # Text input for status update
        status_text = st.text_area(
            "How are you feeling today? Share your current status:",
            placeholder="e.g., I'm feeling great! Completed three tasks and excited about the new project...",
            height=150,
            key="mood_status_input"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze_btn = st.button("🤖 Analyze Emotion", type="primary", use_container_width=True)
        with col_btn2:
            quick_log_btn = st.button("⚡ Quick Log", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4>💡 Quick Tips</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;'>
            <p style='font-size: 0.9rem; margin: 5px 0;'>✓ Be honest about feelings</p>
            <p style='font-size: 0.9rem; margin: 5px 0;'>✓ Mention workload stress</p>
            <p style='font-size: 0.9rem; margin: 5px 0;'>✓ Share accomplishments</p>
            <p style='font-size: 0.9rem; margin: 5px 0;'>✓ Note energy levels</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Process emotion analysis
    if analyze_btn and status_text and selected_member:
        with st.spinner("🔍 Analyzing emotional state..."):
            # Get emotion analysis
            result = analyze_emotion(status_text)
            
            # Find selected member
            member_id = None
            for member in st.session_state.team_members:
                if member['name'] == selected_member:
                    member_id = member['id']
                    break
            
            if member_id:
                # Update member mood
                update_member_mood(
                    member_id,
                    result['emotion'],
                    result['stress_level'],
                    result['mood_score'],
                    result['insight']
                )
                
                st.success(f"✅ Mood updated for {selected_member}!")
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    emoji = get_emotion_emoji(result['emotion'])
                    st.markdown(f"""
                    <div class='glass-card' style='text-align: center;'>
                        <p style='font-size: 3rem; margin: 10px 0;'>{emoji}</p>
                        <p style='font-size: 1.2rem; font-weight: 600;'>{result['emotion'].title()}</p>
                        <p style='font-size: 0.85rem; opacity: 0.8;'>Detected Emotion</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    stress_color = "#4CAF50" if result['stress_level'] < 5 else "#FF9800" if result['stress_level'] < 7 else "#F44336"
                    st.markdown(f"""
                    <div class='glass-card' style='text-align: center;'>
                        <p style='font-size: 2.5rem; margin: 10px 0; font-weight: 700; color: {stress_color};'>{result['stress_level']}</p>
                        <p style='font-size: 1.2rem; font-weight: 600;'>Stress Level</p>
                        <p style='font-size: 0.85rem; opacity: 0.8;'>Out of 10</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    mood_color = "#4CAF50" if result['mood_score'] >= 70 else "#FF9800" if result['mood_score'] >= 40 else "#F44336"
                    st.markdown(f"""
                    <div class='glass-card' style='text-align: center;'>
                        <p style='font-size: 2.5rem; margin: 10px 0; font-weight: 700; color: {mood_color};'>{result['mood_score']}</p>
                        <p style='font-size: 1.2rem; font-weight: 600;'>Mood Score</p>
                        <p style='font-size: 0.85rem; opacity: 0.8;'>Out of 100</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # AI Insight
                st.markdown(f"""
                <div class='glass-card'>
                    <h4>🤖 AI Insight</h4>
                    <p style='font-size: 1rem; line-height: 1.6;'>{result['insight']}</p>
                    <p style='font-size: 0.8rem; opacity: 0.7; margin-top: 10px;'>
                    {'🟢 Powered by OpenAI GPT-5' if result['ai_powered'] else '🟡 Basic analysis (Add API key for AI insights)'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    elif quick_log_btn and selected_member:
        # Quick manual mood log
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4>⚡ Quick Mood Entry</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            emotion = st.selectbox("Emotion", ["happy", "neutral", "stressed", "anxious", "motivated", "tired"])
        with col2:
            stress = st.slider("Stress Level", 1, 10, 5)
        with col3:
            mood_score = st.slider("Mood Score", 1, 100, 50)
        
        if st.button("Save Quick Entry"):
            member_id = None
            for member in st.session_state.team_members:
                if member['name'] == selected_member:
                    member_id = member['id']
                    break
            
            if member_id:
                update_member_mood(member_id, emotion, stress, mood_score, "Manual quick entry")
                st.success(f"✅ Quick mood logged for {selected_member}!")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Current Team Mood Status
    st.markdown("<h2>📊 Current Team Status</h2>", unsafe_allow_html=True)
    
    cols = st.columns(min(3, len(st.session_state.team_members)))
    
    for idx, member in enumerate(st.session_state.team_members):
        with cols[idx % 3]:
            emoji = get_emotion_emoji(member['emotion'])
            color = get_emotion_color(member['emotion'])
            
            # Time since last update
            time_diff = datetime.now() - member['last_update']
            if time_diff.seconds < 3600:
                time_str = f"{time_diff.seconds // 60}m ago"
            elif time_diff.seconds < 86400:
                time_str = f"{time_diff.seconds // 3600}h ago"
            else:
                time_str = f"{time_diff.days}d ago"
            
            st.markdown(f"""
            <div class='glass-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                    <div style='display: flex; align-items: center;'>
                        <div class='avatar' style='background: {member["avatar_color"]}; width: 45px; height: 45px; font-size: 1rem;'>
                            {member['name'][0]}
                        </div>
                        <div style='margin-left: 12px;'>
                            <p style='margin: 0; font-weight: 600; font-size: 1rem;'>{member['name']}</p>
                            <p style='margin: 0; font-size: 0.75rem; opacity: 0.7;'>{member['role']}</p>
                        </div>
                    </div>
                    <div style='text-align: right;'>
                        <p style='margin: 0; font-size: 0.75rem; opacity: 0.6;'>{time_str}</p>
                    </div>
                </div>
                
                <div style='background: rgba(255,255,255,0.1); padding: 12px; border-radius: 10px; text-align: center;'>
                    <p style='font-size: 2rem; margin: 5px 0;'>{emoji}</p>
                    <p style='font-size: 1.1rem; font-weight: 600; margin: 5px 0;'>{member['emotion'].title()}</p>
                </div>
                
                <div style='margin-top: 12px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='font-size: 0.9rem;'>Stress</span>
                        <span style='font-weight: 600; font-size: 0.9rem;'>{member['stress_level']}/10</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; overflow: hidden;'>
                        <div style='background: {"#4CAF50" if member["stress_level"] < 5 else "#FF9800" if member["stress_level"] < 7 else "#F44336"}; 
                                    height: 100%; width: {member["stress_level"] * 10}%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
                
                <div style='margin-top: 12px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='font-size: 0.9rem;'>Mood</span>
                        <span style='font-weight: 600; font-size: 0.9rem;'>{member['mood_score']}/100</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #667eea, #764ba2); 
                                    height: 100%; width: {member["mood_score"]}%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Mood history legend
    st.markdown("""
    <div class='glass-card' style='margin-top: 30px;'>
        <h4>📖 Mood Indicators Guide</h4>
        <div style='display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.5rem; margin-right: 8px;'>😊</span>
                <span>Happy / Positive</span>
            </div>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.5rem; margin-right: 8px;'>🚀</span>
                <span>Motivated / Energized</span>
            </div>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.5rem; margin-right: 8px;'>😐</span>
                <span>Neutral / Balanced</span>
            </div>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.5rem; margin-right: 8px;'>😰</span>
                <span>Stressed / Overwhelmed</span>
            </div>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.5rem; margin-right: 8px;'>😟</span>
                <span>Anxious / Worried</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
