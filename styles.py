"""
Professional styling and UI components for LabelIt! platform
"""

import streamlit as st

def inject_custom_css():
    """Inject professional custom CSS styles"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styles */
    .app-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(46, 134, 171, 0.2);
        text-align: center;
    }
    
    .app-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card Styles */
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Button Styles */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(46, 134, 171, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(46, 134, 171, 0.3);
    }
    
    /* Primary Button */
    .primary-btn {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Secondary Button */
    .secondary-btn {
        background: white !important;
        color: #2E86AB !important;
        border: 2px solid #2E86AB !important;
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        font-family: 'Inter', sans-serif;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2E86AB;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1);
    }
    
    /* Navigation Styles */
    .nav-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #CBD5E1;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-card:hover {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 134, 171, 0.25);
    }
    
    /* Stats Cards */
    .stats-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 3px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E86AB;
        margin: 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        color: #64748B;
        font-weight: 500;
        margin: 0.5rem 0 0 0;
    }
    
    /* Upload Zone */
    .upload-zone {
        border: 3px dashed #CBD5E1;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: #F8FAFC;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #2E86AB;
        background: rgba(46, 134, 171, 0.05);
    }
    
    /* Success/Error Messages */
    .success-msg {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-msg {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        border-radius: 10px;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #F8FAFC 0%, #E2E8F0 100%);
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        border: 2px solid #E2E8F0;
        color: #64748B;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        border-color: transparent;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .app-subtitle {
            font-size: 1rem;
        }
        
        .custom-card {
            padding: 1.5rem;
        }
        
        .stats-number {
            font-size: 2rem;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid #E2E8F0;
        border-top: 4px solid #2E86AB;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Image Gallery */
    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        padding: 1rem 0;
    }
    
    .image-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .image-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    /* Language Selector */
    .language-selector {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 2px solid #E2E8F0;
        margin-bottom: 2rem;
    }
    
    /* Form Enhancements */
    .form-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E2E8F0;
    }
    
    .form-section {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .form-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    /* Enhanced Metrics */
    .metric-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 3px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E86AB;
        margin: 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748B;
        font-weight: 500;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #10B981;
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

def create_header(title, subtitle):
    """Create professional header with gradient background"""
    st.markdown(f"""
    <div class="app-header">
        <h1 class="app-title">{title}</h1>
        <p class="app-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def create_card(content, key=None):
    """Create a professional card container"""
    st.markdown(f"""
    <div class="custom-card">
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(value, label, delta=None):
    """Create enhanced metric display card"""
    delta_html = f'<p class="metric-delta">+{delta}</p>' if delta else ''
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_success_message(message):
    """Create professional success message"""
    st.markdown(f"""
    <div class="success-msg">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)

def create_error_message(message):
    """Create professional error message"""
    st.markdown(f"""
    <div class="error-msg">
        ❌ {message}
    </div>
    """, unsafe_allow_html=True)

def create_loading_spinner():
    """Create loading animation"""
    st.markdown("""
    <div class="loading-spinner"></div>
    """, unsafe_allow_html=True)

def create_upload_zone():
    """Create professional file upload zone"""
    st.markdown("""
    <div class="upload-zone">
        <h3>📁 Drag & Drop Your Images Here</h3>
        <p>or click to browse files</p>
        <small>Supported: PNG, JPG, JPEG, GIF (max 10MB)</small>
    </div>
    """, unsafe_allow_html=True)
