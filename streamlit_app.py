import streamlit as st
import requests
import json
import pandas as pd
from typing import List

# Page configuration
st.set_page_config(
    page_title="Module Extraction AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with modern design
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
    }
    
    /* Module card styling */
    .module-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .module-card:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .module-name {
        color: #667eea;
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Submodule styling */
    .submodule-item {
        padding: 1rem;
        margin: 0.5rem 0;
        background: linear-gradient(90deg, #f8f9ff 0%, #ffffff 100%);
        border-left: 4px solid #667eea;
        border-radius: 6px;
        transition: background 0.2s;
    }
    
    .submodule-item:hover {
        background: linear-gradient(90deg, #f0f2ff 0%, #f8f9ff 100%);
    }
    
    .submodule-name {
        font-weight: 600;
        color: #333;
        font-size: 1.05rem;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Info boxes */
    .stSuccess {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Stats display */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-box {
        flex: 1;
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_URL = st.sidebar.text_input(
    "Backend API URL",
    value="https://pulsegen-task.onrender.com",
    help="URL of the FastAPI backend server"
)

def extract_modules(urls: List[str]) -> dict:
    """Call the backend API to extract modules."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/extract",
            json={"urls": urls},
            timeout=300  # 5 minutes timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend API: {str(e)}")
        return None

def display_modules(modules: List[dict], source_urls: List[str] = None):
    """Display extracted modules in tabular and card format."""
    if not modules or len(modules) == 0:
        st.info(" No modules found in the documentation.")
        return
    
    # Statistics
    total_submodules = sum(len(m.get('submodules', {})) for m in modules)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(modules)}</div>
            <div class="stat-label">Modules</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{total_submodules}</div>
            <div class="stat-label">Submodules</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{sum(1 for m in modules if m.get('submodules'))}</div>
            <div class="stat-label">With Submodules</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabular View
    st.markdown("### 📊 Modules Table")
    
    # Prepare table data
    table_data = []
    for idx, module in enumerate(modules, 1):
        module_name = module.get('module', 'Unknown Module')
        description = module.get('description', '')
        submodules = module.get('submodules', {})
        submodule_count = len(submodules)
        submodule_list = ", ".join(list(submodules.keys())[:3])  # First 3 submodules
        if len(submodules) > 3:
            submodule_list += f" (+{len(submodules) - 3} more)"
        
        table_data.append({
            "Module": module_name,
            "Description": description[:100] + "..." if len(description) > 100 else description,
            "Submodules": submodule_count,
            "Submodule List": submodule_list if submodule_list else "None"
        })
    
    # Display table
    import pandas as pd
    df = pd.DataFrame(table_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Module": st.column_config.TextColumn("Module", width="medium"),
            "Description": st.column_config.TextColumn("Description", width="large"),
            "Submodules": st.column_config.NumberColumn("Submodules", width="small"),
            "Submodule List": st.column_config.TextColumn("Submodule List", width="large")
        }
    )
    
    st.markdown("---")
    st.markdown("### 📋 Detailed View")
    
    # Detailed card view with expanders
    for idx, module in enumerate(modules, 1):
        module_name = module.get('module', 'Unknown Module')
        description = module.get('description', '')
        submodules = module.get('submodules', {})
        
        with st.expander(f"🔷 {module_name} ({len(submodules)} submodules)", expanded=False):
            if description:
                st.markdown(f"**Description:** {description}")
                st.markdown("")
            
            if submodules:
                st.markdown("**Submodules:**")
                for sub_name, sub_desc in submodules.items():
                    st.markdown(f"""
                    <div class="submodule-item">
                        <span class="submodule-name">• {sub_name}</span>
                        <br>
                        <span style="color: #666; font-size: 0.95rem;">{sub_desc}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        if idx < len(modules):
            st.markdown("")

# Main UI
st.markdown("""
<div class="main-header">
    <h1>🔍 Module Extraction AI</h1>
    <p>Extract product modules from documentation using AI</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">Powered by Pulsegen.io</p>
</div>
""", unsafe_allow_html=True)

# URL Input Section
st.markdown("###  Documentation URLs")
st.markdown("Enter one or more documentation URLs to analyze. The AI will extract modules and submodules from all provided sources.")

# URL input with better styling
urls_input = st.text_area(
    "Documentation URLs",
    height=120,
    placeholder="https://docs.example.com\nhttps://docs.example.com/api\nhttps://docs.example.com/guides",
    help="Enter documentation URLs, one per line. The system will crawl and analyze all URLs.",
    label_visibility="visible"
)

# Extract button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    extract_button = st.button(" Extract Modules", type="primary", use_container_width=True)

if extract_button:
    if not urls_input.strip():
        st.warning("⚠️ Please enter at least one URL")
    else:
        # Parse URLs
        urls = [url.strip() for url in urls_input.strip().split('\n') if url.strip()]
        
        # Validate URLs
        valid_urls = []
        invalid_urls = []
        for url in urls:
            if url.startswith('http://') or url.startswith('https://'):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            for url in invalid_urls:
                st.warning(f"⚠️ Invalid URL (missing http/https): `{url}`")
        
        if not valid_urls:
            st.error("❌ No valid URLs provided. Please enter at least one valid URL starting with http:// or https://")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info(f"🔄 Processing {len(valid_urls)} URL(s)... This may take 30-90 seconds.")
            progress_bar.progress(20)
            
            result = extract_modules(valid_urls)
            progress_bar.progress(80)
            
                if result:
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    modules = result.get('modules', [])
                    if modules:
                        st.markdown("---")
                        st.markdown("### 📊 Extracted Modules")
                        st.success(f"✅ Successfully extracted {len(modules)} module(s) from {len(valid_urls)} documentation source(s)")
                        
                        # Show which URLs were processed
                        if len(valid_urls) > 1:
                            with st.expander(f"📎 Processed URLs ({len(valid_urls)})", expanded=False):
                                for url in valid_urls:
                                    st.markdown(f"• {url}")
                        
                        st.markdown("")
                        display_modules(modules, valid_urls)
                    
                    st.markdown("---")
                    
                    # Download JSON button
                    json_str = json.dumps(modules, indent=2)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name="extracted_modules.json",
                            mime="application/json",
                            use_container_width=True
                        )
                else:
                    st.warning("⚠️ No modules found in the documentation. The URLs may not contain extractable module information.")
            else:
                progress_bar.empty()
                status_text.empty()

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Module Extraction AI** extracts product modules and submodules from documentation using advanced AI.
    
    **How it works:**
    1. 📝 Enter documentation URLs
    2. 🕷️ System crawls and analyzes content
    3. 🤖 AI extracts modules and submodules
    4. 📊 Results displayed with statistics
    5. 📥 Download as JSON
    
    **Features:**
    - ✅ Multiple URL support
    - ✅ Automatic module merging
    - ✅ Smart content extraction
    - ✅ PM-friendly output
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Configuration")
    
    st.markdown(f"**Backend URL:**")
    st.code(BACKEND_URL, language=None)
    
    if st.button("🔌 Test Connection", use_container_width=True):
        with st.spinner("Testing connection..."):
            try:
                response = requests.get(f"{BACKEND_URL}/", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Backend is running!")
                else:
                    st.error(f"❌ Backend returned status {response.status_code}")
            except Exception as e:
                st.error(f"❌ Cannot connect to backend")
                st.exception(e)
                st.info("💡 Make sure the backend is running on the specified URL")
    
    st.markdown("---")
    st.markdown("### 📚 Quick Tips")
    st.markdown("""
    - Enter multiple URLs for comprehensive analysis
    - URLs should be publicly accessible
    - Processing takes 30-90 seconds
    - Results are merged from all sources
    """)

