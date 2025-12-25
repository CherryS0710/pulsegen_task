import streamlit as st
import requests
import json
from typing import List

# Page configuration
st.set_page_config(
    page_title="Module Extraction AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .module-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: white;
    }
    .submodule-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: #f9f9f9;
        border-left: 3px solid #667eea;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_URL = st.sidebar.text_input(
    "Backend API URL",
    value="http://localhost:8000",
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

def display_modules(modules: List[dict]):
    """Display extracted modules in a nice format."""
    if not modules or len(modules) == 0:
        st.info("No modules found in the documentation.")
        return
    
    st.success(f"✅ Found {len(modules)} module{'s' if len(modules) != 1 else ''}")
    
    for idx, module in enumerate(modules, 1):
        with st.container():
            st.markdown(f"""
            <div class="module-card">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">{module.get('module', 'Unknown Module')}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if module.get('description'):
                st.markdown(f"**Description:** {module['description']}")
            
            if module.get('submodules'):
                st.markdown("**Submodules:**")
                for sub_name, sub_desc in module['submodules'].items():
                    st.markdown(f"""
                    <div class="submodule-item">
                        <strong>{sub_name}</strong> — {sub_desc}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.divider()

# Main UI
st.markdown("""
<div class="main-header">
    <h1>🔍 Module Extraction AI</h1>
    <p>Extract product modules from documentation</p>
</div>
""", unsafe_allow_html=True)

# URL Input Section
st.markdown("### 📝 Documentation URLs")
st.markdown("Enter one or more documentation URLs to analyze:")

# URL input
urls_input = st.text_area(
    "URLs (one per line)",
    height=150,
    placeholder="https://docs.example.com\nhttps://docs.example.com/api\nhttps://docs.example.com/guides",
    help="Enter documentation URLs, one per line"
)

# Extract button
if st.button("🚀 Extract Modules", type="primary", use_container_width=True):
    if not urls_input.strip():
        st.warning("Please enter at least one URL")
    else:
        # Parse URLs
        urls = [url.strip() for url in urls_input.strip().split('\n') if url.strip()]
        
        # Validate URLs
        valid_urls = []
        for url in urls:
            if url.startswith('http://') or url.startswith('https://'):
                valid_urls.append(url)
            else:
                st.warning(f"Invalid URL (missing http/https): {url}")
        
        if not valid_urls:
            st.error("No valid URLs provided")
        else:
            with st.spinner(f"Extracting modules from {len(valid_urls)} URL(s)... This may take a moment."):
                result = extract_modules(valid_urls)
                
                if result:
                    modules = result.get('modules', [])
                    if modules:
                        st.markdown("---")
                        st.markdown("### 📊 Extracted Modules")
                        st.info(f"Modules extracted and merged from {len(valid_urls)} documentation source(s)")
                        display_modules(modules)
                        
                        # Download JSON button
                        json_str = json.dumps(modules, indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name="extracted_modules.json",
                            mime="application/json"
                        )
                    else:
                        st.warning("No modules found in the documentation. The URLs may not contain extractable module information.")

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool extracts product modules and submodules from documentation using AI.
    
    **How it works:**
    1. Enter documentation URLs
    2. The system crawls and analyzes the content
    3. AI extracts modules and submodules
    4. Results are displayed and can be downloaded
    
    **Requirements:**
    - Backend API must be running
    - Valid API key configured in backend
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Configuration")
    
    if st.button("Test Backend Connection"):
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend is running!")
            else:
                st.error(f"❌ Backend returned status {response.status_code}")
        except Exception as e:
            st.error(f"❌ Cannot connect to backend: {str(e)}")
            st.info("Make sure the backend is running on the specified URL")

