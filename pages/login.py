import streamlit as st
import hashlib
import json
from datetime import datetime
import os

# File to store user data (in production, use a proper database)
USER_DATA_FILE = "users.json"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def verify_login(username, password):
    """Verify login credentials"""
    users = load_users()
    if username in users:
        if users[username]['password'] == hash_password(password):
            return True, users[username]
    return False, None

def register_user(username, password, email, role, team_size):
    """Register a new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'role': role,
        'team_size': team_size,
        'created_at': datetime.now().isoformat(),
        'team_members': []
    }
    
    save_users(users)
    return True, "Registration successful"

def initialize_auth_state():
    """Initialize authentication session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False

def show_login():
    """Display login form"""
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='font-size: 3rem; margin-bottom: 10px;'>🚀</h1>
        <h2 style='margin: 0;'>AI Task Optimizer</h2>
        <p style='opacity: 0.8; margin-top: 10px;'>Optimize your team's productivity with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='glass-card' style='padding: 40px;'>", unsafe_allow_html=True)
        
        # Tab selection
        tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])
        
        with tab1:
            st.markdown("<h3 style='text-align: center; margin-bottom: 25px;'>Welcome Back!</h3>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit:
                    if username and password:
                        success, user_data = verify_login(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.user_data = user_data
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                    else:
                        st.warning("⚠️ Please fill in all fields")
            
            st.markdown("<p style='text-align: center; margin-top: 20px; opacity: 0.7;'>Don't have an account? Switch to Sign Up tab</p>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<h3 style='text-align: center; margin-bottom: 25px;'>Create Your Account</h3>", unsafe_allow_html=True)
            
            with st.form("signup_form"):
                new_username = st.text_input("👤 Username", placeholder="Choose a username", key="signup_username")
                new_email = st.text_input("📧 Email", placeholder="your.email@company.com", key="signup_email")
                new_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password", key="signup_password")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 👥 Team Information")
                
                col_x, col_y = st.columns(2)
                with col_x:
                    role = st.selectbox("Your Role", [
                        "Team Lead",
                        "Project Manager",
                        "Developer",
                        "Designer",
                        "Data Analyst",
                        "HR Manager",
                        "Other"
                    ])
                
                with col_y:
                    team_size = st.number_input("Team Size", min_value=1, max_value=100, value=5, step=1)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    signup_submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if signup_submit:
                    # Validation
                    if not all([new_username, new_email, new_password, confirm_password]):
                        st.warning("⚠️ Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords don't match")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters long")
                    elif "@" not in new_email:
                        st.error("❌ Please enter a valid email address")
                    else:
                        success, message = register_user(new_username, new_password, new_email, role, team_size)
                        if success:
                            st.success("✅ " + message + " - Please sign in!")
                        else:
                            st.error("❌ " + message)
            
            st.markdown("<p style='text-align: center; margin-top: 20px; opacity: 0.7;'>Already have an account? Switch to Sign In tab</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Features section
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Why Choose AI Task Optimizer?</h3>", unsafe_allow_html=True)
        
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>😊</div>
                <h4 style='margin: 10px 0;'>Mood Tracking</h4>
                <p style='font-size: 0.9rem; opacity: 0.8;'>Monitor team wellness and emotional health</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col2:
            st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>📊</div>
                <h4 style='margin: 10px 0;'>Smart Analytics</h4>
                <p style='font-size: 0.9rem; opacity: 0.8;'>AI-powered insights for better decisions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col3:
            st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>✅</div>
                <h4 style='margin: 10px 0;'>Task Management</h4>
                <p style='font-size: 0.9rem; opacity: 0.8;'>Organize and prioritize work efficiently</p>
            </div>
            """, unsafe_allow_html=True)

def show_logout_button():
    """Display logout button in sidebar"""
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; margin-bottom: 10px;'>
                <p style='margin: 0; font-size: 0.9rem; opacity: 0.8;'>Logged in as</p>
                <p style='margin: 5px 0 0 0; font-weight: 600; font-size: 1.1rem;'>{st.session_state.username}</p>
                <p style='margin: 5px 0 0 0; font-size: 0.85rem; opacity: 0.7;'>{st.session_state.user_data.get('role', 'User')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.user_data = None
                st.rerun()

def show():
    """Main function to display login page"""
    initialize_auth_state()
    
    if not st.session_state.authenticated:
        show_login()
    else:
        # User is logged in - redirect to dashboard
        st.success(f"Welcome back, {st.session_state.username}! 🎉")
        st.info("You are already logged in. Use the sidebar to navigate to different pages.")
        show_logout_button()