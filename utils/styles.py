def get_custom_css():
    """Return custom CSS for minimalist professional styling"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app background - clean light gray */
    .stApp {
        background: #F5F7FA;
    }
    
    /* Sidebar styling - white with subtle shadow */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #FFFFFF;
    }
    
    /* Clean professional cards */
    .glass-card {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.2s ease;
    }
    
    .glass-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    /* Metric values - clean dark text */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1F2937;
    }
    
    /* Custom buttons - single professional blue */
    .stButton > button {
        background: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 0.95rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #1D4ED8;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Input fields - clean white with border */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        color: #1F2937;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2563EB;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9CA3AF;
    }
    
    /* Progress bars - professional blue */
    .stProgress > div > div > div {
        background: #2563EB;
        border-radius: 4px;
    }
    
    /* Data tables */
    .dataframe {
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #F9FAFB;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        color: #1F2937;
        font-weight: 500;
    }
    
    /* Tabs - clean design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px 8px 0 0;
        color: #6B7280;
        font-weight: 500;
        padding: 10px 20px;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #2563EB;
        border-bottom: 2px solid #2563EB;
    }
    
    /* Mood indicator badges - subtle colors */
    .mood-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        margin: 4px;
    }
    
    .mood-happy {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .mood-stressed {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    .mood-neutral {
        background: #E5E7EB;
        color: #374151;
    }
    
    /* Task priority badges - clean colors */
    .priority-high {
        background: #FEE2E2;
        color: #991B1B;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        display: inline-block;
    }
    
    .priority-medium {
        background: #FEF3C7;
        color: #92400E;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        display: inline-block;
    }
    
    .priority-low {
        background: #D1FAE5;
        color: #065F46;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        display: inline-block;
    }
    
    /* Avatar circles - clean design */
    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 2px solid #FFFFFF;
    }
    
    /* Scrollbar styling - minimal */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F3F4F6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D1D5DB;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    
    /* Heading styles - dark professional text */
    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 600 !important;
        text-shadow: none;
    }
    
    h1 {
        font-size: 2rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.25rem !important;
    }
    
    /* Paragraph text - dark gray */
    p, div, span, label {
        color: #374151 !important;
    }
    
    /* Chart containers - clean white */
    .js-plotly-plot {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #E5E7EB;
    }
    
    /* Notification/Alert styling */
    .stAlert {
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        color: #374151;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #2563EB !important;
    }
    
    /* Success/Info/Warning/Error messages */
    .element-container .stSuccess {
        background: #ECFDF5;
        border-radius: 8px;
        border-left: 4px solid #10B981;
    }
    
    .element-container .stInfo {
        background: #EFF6FF;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
    }
    
    .element-container .stWarning {
        background: #FFFBEB;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
    }
    
    .element-container .stError {
        background: #FEF2F2;
        border-radius: 8px;
        border-left: 4px solid #EF4444;
    }
    
    /* Column gap */
    [data-testid="column"] {
        padding: 0 8px;
    }
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    /* Remove any remaining gradients or animations */
    * {
        animation: none !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .glass-card {
            padding: 16px;
            margin: 12px 0;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        h1 {
            font-size: 1.75rem !important;
        }
    }
    </style>
    """
