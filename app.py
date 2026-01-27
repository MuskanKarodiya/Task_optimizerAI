import streamlit as st
from streamlit_option_menu import option_menu
from utils.styles import get_custom_css
from utils.data_models import initialize_session_state
from pages import login

st.set_page_config(
    page_title="AI Task Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_session_state()
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Check authentication
login.initialize_auth_state()

if not st.session_state.authenticated:
    # Show login page if not authenticated
    login.show()
else:
    # Show main app if authenticated
    login.show_logout_button()
    

# Sidebar navigation
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; margin-bottom: 30px; color: #111827;'>🚀 AI Task Optimizer</h1>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Mood Tracker", "Task Manager", "Team Members", "Analytics"],
            icons=["speedometer2", "emoji-smile", "list-task", "people", "graph-up"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "transparent"},
                "icon": {"color": "#DA2727", "font-size": "18px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "12px 16px",
                    "border-radius": "8px",
                    "color": "#0565FF",
                    "background-color": "transparent",
                },
                "nav-link-selected": {
                    "background-color": "#EFF6FF",
                    "color": "#2563EB",
                    "font-weight": "500",
                },
            },
        )
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #F9FAFB; border-radius: 8px; margin-top: 20px; border: 1px solid #E5E7EB;'>
            <p style='font-size: 0.9rem; margin: 0; color: #111827;'><strong>Team Wellness</strong></p>
            <p style='font-size: 0.8rem; color: #6B7280; margin: 5px 0;'>Monitor & Optimize</p>
        </div>
        """, unsafe_allow_html=True)

    # Main content area - load selected page
    if selected == "Dashboard":
        from pages import dashboard
        dashboard.show()   
    elif selected == "Mood Tracker":
        from pages import mood_tracker
        mood_tracker.show()
    elif selected == "Task Manager":
        from pages import task_manager
        task_manager.show()
    elif selected == "Team Members":
        from pages import team_members
        team_members.show()
    elif selected == "Analytics":
        from pages import analytics
        analytics.show()
