# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

import streamlit as st
import importlib.util
import sys
import os

# ── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="ChAI", layout="wide")

# ── Global ChRIS CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Dark theme */
  body, .stApp { background-color: #111 !important; color: #f0f0f0 !important; }
  .block-container { padding: 1.5rem 2.5rem; }

  /* Headers */
  h1, h2, h3, h4 { color: ##ffffff !important; }

  /* Rounded cards/panels */
  .st-emotion-cache-1v0mbdj, .st-emotion-cache-1c7y2kd {
    background-color: #1a1a1a !important;
    border-radius: 10px;
  }

  /* Ensure the logo is at the top */
  [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    margin-top: 0;
    padding-top: 0;
  }
  
  /* Add space after logo */
  .logo-container {
    margin-bottom: 1rem;
  }
  
  /* Custom navigation buttons styling */
  .nav-button {
    background-color: transparent;
    border: none;
    color: #f0f0f0;
    padding: 8px 16px;
    text-align: left;
    width: 100%;
    cursor: pointer;
    border-radius: 4px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
  }
  
  .nav-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .nav-button.active {
    background-color: rgba(255, 107, 129, 0.2);
  }
  
  /* Icon in navigation */
  .nav-icon {
    margin-right: 8px;
  }

  /* Sidebar subtitle */
  .sidebar-subtitle {
    font-size: 16px;
    font-weight: 700;
    margin: 0.5rem 0;
  }

  /* Sidebar footer */
  .sidebar-footer {
    font-size: 12px; color: #999;
    margin-top: 2rem; line-height: 1.4;
  }
  
  /* Hide Streamlit's default navbar if present */
  section[data-testid="stSidebarUserContent"] > div:first-child {
    display: none !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Define Pages ──────────────────────────────────────────────────────────────
pages = {
    "Chat": ("page/playground/chat.py", "💬"),
    "Upload Documents": ("page/upload/upload.py", "📄"),
    "Inspect": ("page/distribution/inspect.py", "🔍"),
}

# Create session state to store the current page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"

# ── Sidebar: Logo → Subtitle → Separator → Navigation → Separator → Footer ──
with st.sidebar:
    # First place the logo at the very top, before any Streamlit components
    st.markdown("""
      <div class="logo-container">
        <a href="https://chrisproject.org" target="_blank">
          <img src="https://chrisproject.org/img/logo/ChRISlogo-color.svg" width="160"/>
        </a>
      </div>
    """, unsafe_allow_html=True)


    
    st.markdown("---")
    
    # Playground header
    st.markdown("### Select One")
    
    # Create custom navigation buttons
    for page_name, (path, icon) in pages.items():
        is_active = st.session_state.current_page == page_name
        active_class = "active" if is_active else ""
        
        if st.button(
            f"{icon} {page_name}", 
            key=f"nav_{page_name}", 
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = page_name
            st.rerun()

    st.markdown("---")

    # Footer with version and GitHub link
    st.markdown("""
      <div class="sidebar-footer">
        Version: 1.0.0<br/>
        <a href="https://github.com/FNNDSC/ChAI" target="_blank">View on GitHub</a>
      </div>
    """, unsafe_allow_html=True)

# ── Main Panel: Centered Title ────────────────────────────────────────────────
st.markdown(
  '<h1 style="text-align:center; margin-bottom:1rem;">'
  'ChAI</h1>',
  unsafe_allow_html=True
)

# ── Run the selected page ────────────────────────────────────────────────────
selected_path = pages[st.session_state.current_page][0]

# Load and run the selected page module
try:
    # Get the absolute path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    page_path = os.path.join(current_dir, selected_path)
    
    # Load the module
    spec = importlib.util.spec_from_file_location("page_module", page_path)
    if spec and spec.loader:
        page_module = importlib.util.module_from_spec(spec)
        sys.modules["page_module"] = page_module
        spec.loader.exec_module(page_module)
        
        # If the module has a main function, call it
        if hasattr(page_module, "main"):
            page_module.main()
except Exception as e:
    st.error(f"Error loading page: {e}")