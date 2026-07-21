import streamlit as st
import uuid
import os
from datetime import datetime
from PIL import Image
import io
import time
from functools import lru_cache
import plotly.express as px
import pandas as pd

# Import modules
from backend import backend
from geolocation import geo_manager
from translations import get_translation, SUPPORTED_LANGUAGES
from utils import compress_image, validate_image, format_file_size
from styles import inject_custom_css, create_header, create_card, create_metric_card, create_success_message, create_error_message, create_loading_spinner, create_upload_zone
from visualization import create_stats_chart, create_category_distribution, create_language_usage_chart, create_activity_timeline, create_user_contribution_chart, create_location_map

# Configure page
st.set_page_config(
    page_title="LabelIt! 🇮🇳 - Professional Multilingual Platform",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply professional styling
inject_custom_css()

# Categories for image classification
CATEGORIES = ['Animals', 'Food', 'Objects', 'Nature', 'People', 'Transportation', 'Buildings', 'Technology']

# Ensure data directory exists
os.makedirs('data/images', exist_ok=True)

# Performance optimization constants
CACHE_TTL = 300  # 5 minutes cache
IMAGES_PER_PAGE = 8  # Optimized for better performance
MAX_IMAGE_SIZE = (800, 600)  # Max display size for images

@st.cache_data(ttl=CACHE_TTL)
def get_cached_stats():
    """Cache community statistics for better performance"""
    return backend.get_statistics()

@st.cache_data(ttl=CACHE_TTL)
def get_cached_user_stats(username):
    """Cache user statistics for better performance"""
    return backend.get_user_stats(username)

@st.cache_data(ttl=CACHE_TTL)
def get_cached_images(category=None, language=None, search=None, limit=50):
    """Cache image queries for better performance"""
    return backend.get_images(category=category, language=language, search=search, limit=limit)

def get_user_language():
    """Get user's preferred language"""
    return st.session_state.get('user_language', 'en')

def t(key, default=None):
    """Translation helper"""
    return get_translation(key, get_user_language(), default)

def render_auth_page():
    """Professional authentication page"""
    create_header("🏷️ LabelIt! 🇮🇳", "Professional Multilingual Image Labeling Platform")
    
    # Language selection with professional styling
    st.markdown('<div class="language-selector">', unsafe_allow_html=True)
    st.subheader("🌐 Select Your Language")
    
    language_options = list(SUPPORTED_LANGUAGES.items())
    selected_lang = st.selectbox(
        "Choose your preferred language:",
        options=language_options,
        format_func=lambda x: f"{x[1]} ({x[0]})",
        index=0,
        help="This will be your default language for the platform"
    )
    st.session_state.user_language = selected_lang[0]
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Professional tabs
    tab1, tab2 = st.tabs([f"🔑 {t('login', 'Login')}", f"📝 {t('register', 'Register')}"])
    
    with tab1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.subheader(f"🔑 {t('login', 'Login')}")
        st.write("Welcome back! Please sign in to your account.")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                t('username', 'Username'),
                placeholder="Enter your username",
                help="Use the username you registered with"
            )
            password = st.text_input(
                t('password', 'Password'),
                type="password",
                placeholder="Enter your password",
                help="Your secure password"
            )
            
            col1, col2 = st.columns([2, 1])
            with col1:
                login_submitted = st.form_submit_button(
                    f"🔑 {t('login', 'Login')}",
                    use_container_width=True,
                    type="primary"
                )
            
            if login_submitted:
                if username and password:
                    with st.spinner("Authenticating..."):
                        if backend.authenticate_user(username, password):
                            st.session_state.authenticated = True
                            st.session_state.user = username
                            create_success_message("Login successful! Welcome back!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            create_error_message(t('invalid_credentials', 'Invalid username or password'))
                else:
                    create_error_message(t('fill_all_fields', 'Please fill in all required fields'))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.subheader(f"📝 {t('register', 'Register')}")
        st.write("Create your account to start labeling images in your language!")
        
        with st.form("register_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input(
                    f"{t('username', 'Username')} *",
                    placeholder="Choose a unique username",
                    help="Minimum 3 characters, letters and numbers only"
                )
                new_password = st.text_input(
                    f"{t('password', 'Password')} *",
                    type="password",
                    placeholder="Create a secure password",
                    help="Minimum 3 characters"
                )
                confirm_password = st.text_input(
                    f"{t('confirm_password', 'Confirm Password')} *",
                    type="password",
                    placeholder="Confirm your password"
                )
            
            with col2:
                full_name = st.text_input(
                    "Full Name (Optional)",
                    placeholder="Your full name"
                )
                email = st.text_input(
                    "Email (Optional)",
                    placeholder="your.email@example.com"
                )
                age = st.number_input(
                    "Age (Optional)",
                    min_value=13,
                    max_value=120,
                    value=None,
                    help="Must be 13 or older"
                )
            
            register_submitted = st.form_submit_button(
                f"📝 {t('register', 'Register')}",
                use_container_width=True,
                type="primary"
            )
            
            if register_submitted:
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        with st.spinner("Creating your account..."):
                            success, message = backend.create_user(
                                new_username, 
                                new_password, 
                                preferred_language=selected_lang[0],
                                full_name=full_name,
                                email=email,
                                age=age
                            )
                            if success:
                                create_success_message("Registration successful! Please login with your credentials.")
                                st.balloons()
                            elif "already exists" in message:
                                create_error_message(t('username_exists', 'Username already exists. Please choose another.'))
                            else:
                                create_error_message(message)
                    else:
                        create_error_message(t('passwords_dont_match', 'Passwords do not match'))
                else:
                    create_error_message(t('fill_all_fields', 'Please fill in all required fields'))
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    """Professional sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🏷️ LabelIt! Navigation")
        
        # User info
        if st.session_state.get('authenticated'):
            st.success(f"👋 Welcome, **{st.session_state.user}**!")
            
            # Navigation buttons
            if st.button("🏠 Dashboard", use_container_width=True, type="primary"):
                st.session_state.page = "dashboard"
                st.rerun()
            
            if st.button("📱 Upload Image", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
            
            if st.button("📸 Image Feed", use_container_width=True):
                st.session_state.page = "feed"
                st.rerun()
            
            if st.button("📊 Analytics", use_container_width=True):
                st.session_state.page = "analytics"
                st.rerun()
            
            if st.button("💾 Export Data", use_container_width=True):
                st.session_state.page = "export"
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                # Clear all session state and cache
                st.cache_data.clear()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

def render_dashboard():
    """Professional dashboard with analytics"""
    create_header("📊 Dashboard", f"Welcome back, {st.session_state.user}!")
    
    try:
        # Get user and community stats
        user_stats = get_cached_user_stats(st.session_state.user)
        community_stats = get_cached_stats()
        
        # User Statistics Section
        st.subheader("👤 Your Contributions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_metric_card(
                user_stats.get('images_uploaded', 0),
                "Images Uploaded"
            )
        
        with col2:
            create_metric_card(
                user_stats.get('labels_added', 0),
                "Labels Added"
            )
        
        with col3:
            create_metric_card(
                user_stats.get('languages_contributed', 0),
                "Languages Used"
            )
        
        with col4:
            create_metric_card(
                user_stats.get('categories_contributed', 0),
                "Categories Covered"
            )
        
        st.markdown("---")
        
        # Community Statistics
        st.subheader("🌍 Community Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_metric_card(
                community_stats.get('total_images', 0),
                "Total Images"
            )
        
        with col2:
            create_metric_card(
                community_stats.get('total_labels', 0),
                "Total Labels"
            )
        
        with col3:
            create_metric_card(
                community_stats.get('total_users', 0),
                "Active Users"
            )
        
        with col4:
            create_metric_card(
                community_stats.get('languages_used', 0),
                "Languages Supported"
            )
        
        # Quick actions
        st.markdown("---")
        st.subheader("🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 Upload New Image", use_container_width=True, type="primary"):
                st.session_state.page = "upload"
                st.rerun()
        
        with col2:
            if st.button("🔍 Browse Images", use_container_width=True):
                st.session_state.page = "feed"
                st.rerun()
        
        with col3:
            if st.button("📈 View Analytics", use_container_width=True):
                st.session_state.page = "analytics"
                st.rerun()
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

def render_upload_page():
    """Professional image upload page"""
    create_header("📱 Upload Image", "Share your images with the community")
    
    uploaded_file = st.file_uploader(
        "Choose an image to upload",
        type=['png', 'jpg', 'jpeg', 'gif'],
        help="Supported formats: PNG, JPG, JPEG, GIF (max 10MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Validate image
        if not validate_image(uploaded_file):
            return
        
        # Professional layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.subheader("📷 Image Preview")
            st.image(uploaded_file, use_container_width=True, caption=f"File: {uploaded_file.name}")
            
            # File info
            file_size = format_file_size(uploaded_file.size)
            st.caption(f"📁 Size: {file_size}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.subheader("📝 Image Details")
            
            with st.form("upload_form"):
                title = st.text_input(
                    "Image Title *",
                    max_chars=100,
                    placeholder="Give your image a descriptive title",
                    help="A clear, descriptive title helps others find your image"
                )
                
                description = st.text_area(
                    "Description",
                    max_chars=500,
                    placeholder="Describe what's in the image...",
                    help="Optional description providing more context"
                )
                
                category = st.selectbox(
                    "Category *",
                    CATEGORIES,
                    help="Choose the most appropriate category"
                )
                
                # Enhanced geolocation section
                st.markdown("---")
                st.subheader("📍 Location Information")
                location_data = geo_manager.display_location_widget_in_form()
                
                # Submit button
                st.markdown("---")
                submitted = st.form_submit_button(
                    "📤 Upload Image",
                    use_container_width=True,
                    type="primary"
                )
                
                if submitted:
                    if not title or not category:
                        create_error_message("Please fill in all required fields (Title and Category)")
                        return
                    
                    # Professional progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Compress image
                        status_text.text("🗜️ Compressing image...")
                        progress_bar.progress(25)
                        time.sleep(0.5)
                        
                        compressed_image = compress_image(uploaded_file)
                        
                        # Generate unique filename
                        status_text.text("💾 Preparing for storage...")
                        progress_bar.progress(50)
                        time.sleep(0.5)
                        
                        file_extension = uploaded_file.name.split('.')[-1].lower()
                        unique_filename = f"{uuid.uuid4()}.{file_extension}"
                        file_path = os.path.join('data/images', unique_filename)
                        
                        # Save image
                        with open(file_path, 'wb') as f:
                            f.write(compressed_image.getvalue())
                        
                        # Get image metadata
                        image = Image.open(file_path)
                        width, height = image.size
                        file_size = os.path.getsize(file_path)
                        
                        # Save to database
                        status_text.text("💿 Saving to database...")
                        progress_bar.progress(75)
                        time.sleep(0.5)
                        
                        image_id = backend.add_image(
                            title=title,
                            description=description,
                            category=category,
                            image_path=file_path,
                            uploaded_by=st.session_state.user,
                            file_size=file_size,
                            image_width=width,
                            image_height=height,
                            latitude=location_data.get('latitude') if location_data else None,
                            longitude=location_data.get('longitude') if location_data else None
                        )
                        
                        # Complete
                        progress_bar.progress(100)
                        status_text.text("✅ Upload complete!")
                        time.sleep(1)
                        
                        create_success_message("Image uploaded successfully! Thank you for your contribution.")
                        st.balloons()
                        
                        # Clear cache
                        st.cache_data.clear()
                        
                        # Auto-redirect after success
                        time.sleep(1)
                        # Show success for a bit before redirect
                        st.success("✅ Redirecting to image feed...")
                        st.session_state.page = "feed"
                        st.rerun()
                        
                    except Exception as e:
                        create_error_message(f"Upload failed: {str(e)}")
                    finally:
                        progress_bar.empty()
                        status_text.empty()
            
            st.markdown('</div>', unsafe_allow_html=True)

def render_feed_page():
    """Professional image feed with enhanced filtering"""
    create_header("📸 Image Feed", "Explore and label community images")
    
    # Enhanced filters
    with st.container():
        st.subheader("🔍 Filters & Search")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            category_filter = st.selectbox(
                "Category",
                options=["All"] + CATEGORIES,
                key="feed_category_filter"
            )
        
        with col2:
            language_filter = st.selectbox(
                "Language",
                options=["All"] + list(SUPPORTED_LANGUAGES.values()),
                key="feed_language_filter"
            )
        
        with col3:
            search_query = st.text_input(
                "Search",
                placeholder="Search titles, descriptions...",
                key="feed_search"
            )
        
        with col4:
            sort_by = st.selectbox(
                "Sort by",
                options=["Newest", "Oldest", "Most Labels", "Alphabetical"],
                key="feed_sort"
            )
    
    st.markdown("---")
    
    try:
        # Process filters
        cat_filter = None if category_filter == "All" else category_filter
        
        lang_filter = None
        if language_filter != "All":
            for code, display in SUPPORTED_LANGUAGES.items():
                if display == language_filter:
                    lang_filter = code
                    break
        
        search_filter = search_query.strip() if search_query else None
        
        # Get filtered images
        images = get_cached_images(
            category=cat_filter,
            language=lang_filter,
            search=search_filter,
            limit=100
        )
        
        # Results header
        st.subheader(f"📊 Results ({len(images)} images found)")
        
        if not images:
            st.info("🔍 No images found matching your criteria. Try adjusting the filters or be the first to upload!")
            if st.button("📱 Upload First Image", type="primary"):
                st.session_state.page = "upload"
                st.rerun()
            return
        
        # Pagination
        total_pages = (len(images) + IMAGES_PER_PAGE - 1) // IMAGES_PER_PAGE
        
        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                page = st.select_slider(
                    "Page",
                    options=list(range(1, total_pages + 1)),
                    value=st.session_state.get('feed_page', 1),
                    key="feed_page_slider"
                )
                st.session_state.feed_page = page
        else:
            page = 1
        
        # Display images in professional grid
        start_idx = (page - 1) * IMAGES_PER_PAGE
        end_idx = start_idx + IMAGES_PER_PAGE
        page_images = images[start_idx:end_idx]
        
        # Professional image grid
        for i in range(0, len(page_images), 2):
            col1, col2 = st.columns(2)
            
            for j, col in enumerate([col1, col2]):
                if i + j < len(page_images):
                    image_data = page_images[i + j]
                    render_image_card(image_data, col)
    
    except Exception as e:
        st.error(f"Error loading images: {str(e)}")

def render_image_card(image_data, container):
    """Render professional image card"""
    with container:
        with st.container():
            # Image display
            if os.path.exists(image_data['image_path']):
                st.image(
                    image_data['image_path'],
                    use_container_width=True,
                    caption=image_data['title']
                )
            else:
                st.error("Image file not found")
            
            # Image metadata
            st.markdown(f"**📂 {image_data['category']}**")
            st.markdown(f"*By: {image_data['uploaded_by']}*")
            
            if image_data.get('description'):
                st.caption(f"📝 {image_data['description']}")
            
            # Display geocoordinates if available
            if image_data.get('latitude') and image_data.get('longitude'):
                lat = image_data['latitude']
                lon = image_data['longitude']
                st.caption(f"📍 {lat:.6f}, {lon:.6f}")
            else:
                st.caption("📍 Location not provided")
            
            # Labels section
            labels = backend.get_image_labels(image_data['id'])
            if labels:
                st.markdown("**🏷️ Labels:**")
                for label in labels[:3]:  # Show first 3 labels
                    lang_name = SUPPORTED_LANGUAGES.get(label['language'], label['language'])
                    st.markdown(f"• {label['text']} ({lang_name})")
                
                if len(labels) > 3:
                    st.caption(f"... and {len(labels) - 3} more")
            
            # Add label form
            with st.expander("➕ Add Label"):
                with st.form(f"label_form_{image_data['id']}"):
                    label_lang = st.selectbox(
                        "Language",
                        options=list(SUPPORTED_LANGUAGES.keys()),
                        format_func=lambda x: SUPPORTED_LANGUAGES[x],
                        key=f"lang_{image_data['id']}"
                    )
                    
                    label_text = st.text_input(
                        "Label",
                        placeholder="Enter your label...",
                        key=f"text_{image_data['id']}"
                    )
                    
                    if st.form_submit_button("Add Label", use_container_width=True):
                        if label_text.strip():
                            try:
                                backend.add_label(
                                    image_data['id'],
                                    label_text.strip(),
                                    label_lang,
                                    st.session_state.user
                                )
                                create_success_message("Label added successfully!")
                                st.cache_data.clear()
                                st.rerun()
                            except Exception as e:
                                create_error_message(f"Error adding label: {str(e)}")
                        else:
                            create_error_message("Please enter a label")
            
            st.markdown("---")

def render_analytics_page():
    """Professional analytics dashboard"""
    create_header("📈 Analytics", "Platform insights and statistics")
    
    try:
        stats = get_cached_stats()
        
        if not stats:
            st.info("No data available yet. Upload some images to see analytics!")
            return
        
        # Overview metrics
        st.subheader("📊 Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_metric_card(stats.get('total_images', 0), "Total Images")
        with col2:
            create_metric_card(stats.get('total_labels', 0), "Total Labels")
        with col3:
            create_metric_card(stats.get('total_users', 0), "Active Users")
        with col4:
            create_metric_card(stats.get('languages_used', 0), "Languages")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Category distribution
            category_stats = backend.get_category_statistics()
            if category_stats:
                fig = create_category_distribution(category_stats)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Language usage
            language_stats = backend.get_language_statistics()
            if language_stats:
                fig = create_language_usage_chart(language_stats)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        # Additional charts
        st.markdown("---")
        
        # Activity timeline
        activity_data = backend.get_activity_timeline()
        if activity_data:
            fig = create_activity_timeline(activity_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

def render_export_page():
    """Professional data export interface"""
    create_header("💾 Export Data", "Download your data and community contributions")
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Excel Export")
        st.write("Export complete database in Excel format with multiple sheets")
        
        if st.button("📥 Download Excel File", use_container_width=True, type="primary"):
            try:
                with st.spinner("Preparing Excel export..."):
                    excel_data = backend.export_to_excel()
                    if excel_data:
                        st.download_button(
                            label="💾 Download Excel",
                            data=excel_data,
                            file_name=f"labelit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                        create_success_message("Excel export ready for download!")
                    else:
                        create_error_message("No data available for export")
            except Exception as e:
                create_error_message(f"Export failed: {str(e)}")
    
    with col2:
        st.subheader("🗂️ Images Archive")
        st.write("Download all images as organized ZIP archive")
        
        if st.button("📦 Create ZIP Archive", use_container_width=True, type="secondary"):
            try:
                with st.spinner("Creating ZIP archive..."):
                    zip_data = backend.create_images_zip()
                    if zip_data:
                        st.download_button(
                            label="💾 Download ZIP",
                            data=zip_data,
                            file_name=f"labelit_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        create_success_message("ZIP archive ready for download!")
                    else:
                        create_error_message("No images available for export")
            except Exception as e:
                create_error_message(f"Archive creation failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application flow"""
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    
    # Authentication check
    if not st.session_state.authenticated:
        render_auth_page()
        return
    
    # Render sidebar navigation
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.get('page', 'dashboard')
    
    try:
        if page == 'dashboard':
            render_dashboard()
        elif page == 'upload':
            render_upload_page()
        elif page == 'feed':
            render_feed_page()
        elif page == 'analytics':
            render_analytics_page()
        elif page == 'export':
            render_export_page()
        else:
            render_dashboard()
    except Exception as e:
        st.error(f"Page error: {str(e)}")
        st.info("Redirecting to dashboard...")
        st.session_state.page = 'dashboard'
        st.rerun()

if __name__ == "__main__":
    main()
