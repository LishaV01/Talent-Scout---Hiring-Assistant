import streamlit as st
try:
    import streamlit.components.v1 as components
    USE_COMPONENTS = True
except:
    USE_COMPONENTS = False

def apply_minimal_color_changing_theme():
    """Apply Pinterest color theme with live background - ultra simple, no animations that hide content"""
    # Just basic color changes and animated background
    st.markdown("""
    <style>
    /* Animated gradient background with Pinterest colors */
    .stApp {
        background: linear-gradient(-45deg, #ffffff, #fff0f3, #ffe0e6, #ffd1d9, #ffffff);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    /* Alternative subtle particle background */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(230, 0, 35, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(230, 0, 35, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(230, 0, 35, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 90% 10%, rgba(230, 0, 35, 0.02) 0%, transparent 50%);
        animation: floatingOrbs 20s ease-in-out infinite;
    }
    
    @keyframes floatingOrbs {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg);
        }
        33% {
            transform: translate(30px, -30px) rotate(120deg);
        }
        66% {
            transform: translate(-20px, 20px) rotate(240deg);
        }
    }
    
    /* Pinterest colors only - no positioning or animations that hide content */
    
    /* Buttons */
    div.stButton > button {
        background-color: #9B7EBD;
        color: white;
        position: relative;
        z-index: 1;
    }
    
    div.stButton > button:hover {
        background-color: #7363B7;
    }
    
    /* Progress bar color */
    div.stProgress > div > div {
        background-color: #D3D3FF;
    }
    
    /* Ensure content is above background */
    .element-container {
        position: relative;
        z-index: 1;
    }
    
    /* Glass effect for containers */
    .stContainer {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Hide Streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def create_minimal_header(title, subtitle=None):
    """Create centered header"""
    # Using columns for centering - always works
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Use Streamlit's native markdown
        st.markdown(f"# {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")

def create_glass_card(content, title=None):
    """Create card - using native Streamlit"""
    # Use container with native Streamlit styling
    with st.container():
        if title:
            st.subheader(title)
        # Use native info box with content
        st.info(content)

def create_minimal_progress(progress, segments=10, candidate_info=None):
    """Create an enhanced progress bar with field indicators"""
    
    # Define the fields being tracked with icons
    fields = [
        {"name": "Name", "icon": "👤", "field": "full_name"},
        {"name": "Email", "icon": "📧", "field": "email"},
        {"name": "Phone", "icon": "📱", "field": "phone"},
        {"name": "Experience", "icon": "💼", "field": "years_experience"},
        {"name": "Position", "icon": "🎯", "field": "desired_positions"},
        {"name": "Location", "icon": "📍", "field": "current_location"},
        {"name": "Tech Stack", "icon": "🛠️", "field": "tech_stack"}
    ]
    
    # Enhanced progress bar with custom styling - Fixed version
    css_style = """
    <style>
    .enhanced-progress-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .progress-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }
    
    .progress-percentage {
        font-size: 24px;
        font-weight: bold;
        color: #7469B6;
    }
    
    .segmented-progress {
        display: flex;
        gap: 8px;
        margin-bottom: 20px;
    }
    
    .progress-segment {
        flex: 1;
        height: 8px;
        background: #E5D9F2;
        border-radius: 4px;
    }
    
    .progress-segment.filled {
        background: linear-gradient(90deg, #A594F9 0%, #CDC1FF 100%);
    }
    
    .progress-segment.filling {
        background: linear-gradient(90deg, #CDC1FF 0%, #A594F9 100%);
        opacity: 0.8;
    }
    
    .field-indicators {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    
    .field-item {
        flex: 1;
        text-align: center;
        padding: 10px 5px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .field-item.completed {
        background: rgba(230, 0, 35, 0.1);
        transform: translateY(-2px);
    }
    
    .field-icon {
        font-size: 24px;
        margin-bottom: 5px;
        display: block;
    }
    
    .field-name {
        font-size: 11px;
        color: #666;
        font-weight: 500;
    }
    
    .field-item.completed .field-name {
        color: #A594F9;
        font-weight: 600;
    }
    
    .checkmark {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #A594F9;
        color: white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    </style>
    """
    
    st.markdown(css_style, unsafe_allow_html=True)
    
    # Calculate filled segments
    filled_segments = int((progress / 100) * segments)
    
    # Build the progress HTML with proper escaping
    progress_html_parts = []
    progress_html_parts.append('<div class="enhanced-progress-container">')
    progress_html_parts.append('<div class="progress-header">')
    progress_html_parts.append('<span class="progress-title">Profile Completion</span>')
    progress_html_parts.append(f'<span class="progress-percentage">{int(progress)}%</span>')
    progress_html_parts.append('</div>')
    
    # Add segmented progress bar
    progress_html_parts.append('<div class="segmented-progress">')
    for i in range(segments):
        if i < filled_segments:
            progress_html_parts.append('<div class="progress-segment filled"></div>')
        elif i == filled_segments:
            progress_html_parts.append('<div class="progress-segment filling"></div>')
        else:
            progress_html_parts.append('<div class="progress-segment"></div>')
    progress_html_parts.append('</div>')
    
    # Add field indicators
    progress_html_parts.append('<div class="field-indicators">')
    
    if candidate_info:
        for field in fields:
            is_completed = False
            
            # Check if field is completed based on field type
            if field["field"] == "full_name":
                is_completed = bool(candidate_info.full_name)
            elif field["field"] == "email":
                is_completed = bool(candidate_info.email)
            elif field["field"] == "phone":
                is_completed = bool(candidate_info.phone)
            elif field["field"] == "years_experience":
                is_completed = candidate_info.years_experience is not None
            elif field["field"] == "desired_positions":
                is_completed = len(candidate_info.desired_positions) > 0
            elif field["field"] == "current_location":
                is_completed = bool(candidate_info.current_location)
            elif field["field"] == "tech_stack":
                is_completed = len(candidate_info.tech_stack) > 0
            
            completed_class = "completed" if is_completed else ""
            
            progress_html_parts.append(f'<div class="field-item {completed_class}">')
            progress_html_parts.append(f'<span class="field-icon">{field["icon"]}</span>')
            progress_html_parts.append(f'<span class="field-name">{field["name"]}</span>')
            if is_completed:
                progress_html_parts.append('<div class="checkmark">✓</div>')
            progress_html_parts.append('</div>')
    else:
        # Fallback to simple display if no candidate info
        for field in fields:
            progress_html_parts.append('<div class="field-item">')
            progress_html_parts.append(f'<span class="field-icon">{field["icon"]}</span>')
            progress_html_parts.append(f'<span class="field-name">{field["name"]}</span>')
            progress_html_parts.append('</div>')
    
    progress_html_parts.append('</div>')  # Close field-indicators
    progress_html_parts.append('</div>')  # Close container
    
    # Join all parts and render
    progress_html = ''.join(progress_html_parts)
    st.markdown(progress_html, unsafe_allow_html=True)

# Alternative minimal version that's more reliable
def create_minimal_progress_simple(progress, candidate_info=None):
    """Create a simple but enhanced progress bar"""
    
    # Create columns for a clean layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Use native progress bar with custom color
        st.progress(progress / 100)
    
    with col2:
        # Show percentage
        st.markdown(f"<h2 style='color: #A594F9; text-align: right; margin: 0;'>{int(progress)}%</h2>", 
                   unsafe_allow_html=True)
    
    # Show field completion status
    if candidate_info:
        # Create columns for field indicators
        cols = st.columns(7)
        
        fields = [
            ("👤", "Name", bool(candidate_info.full_name)),
            ("📧", "Email", bool(candidate_info.email)),
            ("📱", "Phone", bool(candidate_info.phone)),
            ("💼", "Experience", candidate_info.years_experience is not None),
            ("🎯", "Position", len(candidate_info.desired_positions) > 0),
            ("📍", "Location", bool(candidate_info.current_location)),
            ("🛠️", "Tech", len(candidate_info.tech_stack) > 0)
        ]
        
        for col, (icon, name, completed) in zip(cols, fields):
            with col:
                if completed:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: rgba(230, 0, 35, 0.1); 
                               border-radius: 10px; border: 2px solid #D3D3FF;'>
                        <div style='font-size: 24px;'>{icon}</div>
                        <div style='font-size: 10px; color: #D3D3FF; font-weight: bold;'>{name} ✓</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background: rgba(0, 0, 0, 0.05); 
                               border-radius: 10px; border: 2px solid #f0f0f0;'>
                        <div style='font-size: 24px; opacity: 0.5;'>{icon}</div>
                        <div style='font-size: 10px; color: #999;'>{name}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)

def create_pulse_button(text, key=None):
    """Create button"""
    # Just use native Streamlit button
    return st.button(text, key=key, use_container_width=True)

# Fallback functions if nothing works
def apply_minimal_color_changing_theme_fallback():
    """Fallback theme without HTML"""
    pass

def create_minimal_header_fallback(title, subtitle=None):
    """Fallback header"""
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def create_glass_card_fallback(content, title=None):
    """Fallback card"""
    if title:
        st.subheader(title)
    st.info(content)

def create_minimal_progress_fallback(progress):
    """Fallback progress"""
    st.progress(progress / 100)

def create_pulse_button_fallback(text, key=None):
    """Fallback button"""
    return st.button(text, key=key, type="primary", use_container_width=True)