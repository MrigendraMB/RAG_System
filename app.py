"""
Nepal Labour Law Assistant - Modern SaaS Frontend
An AI-powered RAG system for Nepal Labour Laws, Employment Rights, and Workplace Regulations
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Nepal Labour Law Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

custom_css = """
<style>
    /* Root variables */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #0f172a;
        --accent-color: #dc2626;
        --success-color: #16a34a;
        --warning-color: #ea580c;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --bg-light: #f8fafc;
        --bg-white: #ffffff;
        --border-color: #e2e8f0;
    }

    /* Global styles */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        padding: 2rem 1rem;
    }

    /* Main container */
    .main {
        padding: 2rem 3rem;
    }

    /* Cards styling */
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        border-color: #cbd5e1;
    }

    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
        border-color: #1e3a8a;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    /* Statistics cards */
    .stat-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Chat messages */
    .chat-message {
        margin: 1rem 0;
        border-radius: 12px;
        padding: 1.5rem;
    }

    .user-message {
        background: #1e3a8a;
        color: white;
        margin-left: 2rem;
        border-radius: 18px 18px 4px 18px;
    }

    .assistant-message {
        background: #f1f5f9;
        color: #0f172a;
        margin-right: 2rem;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #e2e8f0;
    }

    .message-time {
        font-size: 0.75rem;
        opacity: 0.6;
        margin-top: 0.5rem;
    }

    /* Source citation */
    .source-citation {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .source-title {
        font-weight: 600;
        color: #92400e;
        margin-bottom: 0.5rem;
    }

    .source-details {
        font-size: 0.875rem;
        color: #b45309;
    }

    /* Buttons */
    .primary-btn {
        background: #1e3a8a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .primary-btn:hover {
        background: #1e40af;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
    }

    .secondary-btn {
        background: #f1f5f9;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .secondary-btn:hover {
        background: #e2e8f0;
        border-color: #cbd5e1;
    }

    /* Input styling */
    .streamlit-textinput input,
    .streamlit-textarea textarea {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* File uploader */
    .uploadedFile {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 8px;
    }

    /* Table styling */
    .dataframe {
        border-radius: 8px !important;
    }

    /* Alerts */
    .success-alert {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-left: 4px solid #16a34a;
    }

    .error-alert {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-left: 4px solid #dc2626;
    }

    .warning-alert {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
    }

    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #e2e8f0;
        border-top: 3px solid #1e3a8a;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Disclaimer */
    .disclaimer {
        background: linear-gradient(135deg, #ede9fe 0%, #f3e8ff 100%);
        border: 1px solid #ddd6fe;
        border-left: 4px solid #7c3aed;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 2rem 0;
    }

    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #64748b;
        margin-bottom: 2rem;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 8px !important;
    }

    /* Metric styling */
    .metric {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# API CONFIGURATION & HELPERS
# ============================================================================

BACKEND_URL = "http://localhost:8000"
ADMIN_PASSWORD = "admin123"

class LawAssistantAPI:
    """Wrapper for backend API calls"""
    
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url
        self.timeout = 10

    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle API errors gracefully"""
        error_msg = str(error)
        return {
            "error": True,
            "message": "Unable to connect to backend server",
            "details": error_msg
        }

    def ask(self, question: str) -> Dict[str, Any]:
        """Send ask to backend"""
        try:
            response = requests.post(
             f"{self.base_url}/ask",
             params={"question": question},
             timeout=30
             )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/stats",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def get_documents(self) -> List[Dict[str, Any]]:
        """Get list of indexed documents"""
        try:
            response = requests.get(
                f"{self.base_url}/documents",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return []

    def upload_document(self, file_name: str, file_content: bytes) -> Dict[str, Any]:
        """Upload a document"""
        try:
            files = {"file": (file_name, file_content, "application/pdf")}
            response = requests.post(
                f"{self.base_url}/upload",
                files=files,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document"""
        try:
            response = requests.delete(
                f"{self.base_url}/document/{doc_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

    def reindex(self) -> Dict[str, Any]:
        """Reindex documents"""
        try:
            response = requests.post(
                f"{self.base_url}/reindex",
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)

# Initialize API client
api = LawAssistantAPI()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "authenticated_admin" not in st.session_state:
    st.session_state.authenticated_admin = False

if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = None

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚖️</div>
            <h1 style="margin: 0; font-size: 1.5rem; color: #1e3a8a;">
                Labour Law<br>Assistant
            </h1>
            <p style="color: #64748b; margin-top: 0.5rem; font-size: 0.9rem;">
                Nepal
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
    with col2:
        if st.button("💬 Ask", use_container_width=True):
            st.session_state.page = "Ask"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Knowledge", use_container_width=True):
            st.session_state.page = "Knowledge"
    with col2:
        if st.button("🔐 Admin", use_container_width=True):
            st.session_state.page = "Admin"

    st.divider()

    # Version info
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; text-align: center; margin-top: 2rem;">
            <p>v1.0.0 | Nepal Labour Law Assistant</p>
            <p style="margin-top: 0.5rem;">Powered by RAG & AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# PAGE: HOME
# ============================================================================

def page_home():
    # Hero section
    st.markdown(
        """
        <div class="hero">
            <h1 class="hero-title">Nepal Labour Law Assistant</h1>
            <p class="hero-subtitle">
                AI-powered legal assistant for Nepal Labour and Employment Laws
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Features
    st.markdown("### ✨ Key Features")
    cols = st.columns(3)
    
    features = [
        ("🏢", "Labour Rights", "Understand your fundamental labour rights"),
        ("📋", "Employment Contracts", "Get clarity on contract terms and conditions"),
        ("🛡️", "Social Security", "Learn about social security benefits"),
        ("✈️", "Foreign Employment", "Guide for foreign workers in Nepal"),
        ("💰", "Wage & Benefits", "Information on minimum wage and benefits"),
        ("🔒", "Workplace Safety", "Workplace safety regulations and standards"),
    ]
    
    for idx, (icon, title, desc) in enumerate(features):
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3 style="margin: 0.5rem 0; color: #1e3a8a; font-size: 1.1rem;">{title}</h3>
                    <p style="margin: 0.5rem 0; color: #64748b; font-size: 0.9rem;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Statistics
    st.markdown("### 📊 System Statistics")
    
    with st.spinner("Loading statistics..."):
        stats = api.get_stats()
    
    if not stats.get("error", False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Documents Indexed</div>
                    <div class="stat-number">{stats.get('total_documents', 0)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Total Chunks</div>
                    <div class="stat-number">{stats.get('total_chunks', 0)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Questions Answered</div>
                    <div class="stat-number">{stats.get('questions_answered', 0)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Last Update</div>
                    <div style="font-size: 1rem; margin-top: 1rem; color: white;">
                        {stats.get('last_update', 'N/A')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Could not load statistics. Backend server may be unavailable.")

    st.markdown("---")

    # CTA
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
            ### 🚀 Get Started
            
            Have a question about Nepal Labour Law? 
            Ask our AI assistant for instant answers backed by official legal documents.
            """
        )
    with col2:
        if st.button("Ask a Question →", use_container_width=True, type="primary"):
            st.session_state.page = "Ask"
            st.rerun()

    # Disclaimer
    st.markdown("---")
    st.markdown(
        """
        <div class="disclaimer">
            <h4 style="color: #6b21a8; margin-top: 0;">⚖️ Legal Disclaimer</h4>
            <p style="margin: 0.5rem 0; color: #581c87; font-size: 0.9rem;">
                This assistant provides information based on Nepal Labour Laws and is designed for educational purposes. 
                It is not a substitute for professional legal advice. Always consult with a qualified legal professional 
                for specific legal matters. The information provided is accurate to the best of our knowledge but may not 
                reflect the most recent changes in legislation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# PAGE: ASK A QUESTION
# ============================================================================

def page_ask_question():
    st.markdown("### 💬 Ask About Nepal Labour Law")
    st.markdown("Get instant answers to your questions about labour rights, employment contracts, and workplace regulations.")
    
    st.divider()

    # Chat container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-message user-message">
                            <strong>You:</strong> {msg['content']}
                            <div class="message-time">{msg.get('time', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-message assistant-message">
                            <strong>Assistant:</strong><br>{msg['content']}
                            <div class="message-time">{msg.get('time', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Display sources if available
                    if msg.get("sources"):
                        unique_sources = list(set(s.get('source', 'Unknown') for s in msg["sources"]))
                        for source in unique_sources:
                            st.markdown(
                                f"""
                                <div class="source-citation">
                                   <div class="source-title">📖 Source: {source}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                       )

    st.divider()

    # Input section
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask a question about Nepal Labour Law...",
            placeholder="e.g., What is the minimum wage in Nepal?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True, type="primary")

    if send_button and user_input.strip():
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })

        # Get response from API
        with st.spinner("Thinking..."):
            response = api.ask(user_input)

        if not response.get("error"):
            # Add assistant response
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response.get("answer", "No answer available"),
                "sources": response.get("citations", []),
                "time": datetime.now().strftime("%H:%M")
            })
        else:
            st.error(f"Error: {response.get('message', 'Unknown error occurred')}")

        st.rerun()

    st.divider()

    # Example questions
    st.markdown("### 💡 Example Questions")
    
    examples = [
        "What is the minimum wage in Nepal?",
        "How many annual leave days are employees entitled to?",
        "What benefits are covered by Social Security?",
        "Can an employer terminate an employee without notice?",
    ]
    
    cols = st.columns(2)
    for idx, example in enumerate(examples):
        col = cols[idx % 2]
        with col:
            if st.button(
                f"📌 {example}",
                use_container_width=True,
                key=f"example_{idx}"
            ):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": example,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                with st.spinner("Finding answer..."):
                    response = api.ask(example)
                
                if not response.get("error"):
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response.get("answer", "No answer available"),
                        "sources": response.get("sources", []),
                        "time": datetime.now().strftime("%H:%M")
                    })
                
                st.rerun()

    st.divider()

    # Clear chat button
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================================
# PAGE: KNOWLEDGE BASE
# ============================================================================

def page_knowledge_base():
    st.markdown("### 📚 Knowledge Base")
    st.markdown("Browse indexed Nepal Labour Law documents")
    
    st.divider()

    # Search functionality
    search_query = st.text_input(
        "🔍 Search documents...",
        placeholder="Search by document name or type...",
        label_visibility="collapsed"
    )

    st.divider()

    # Document cards
    with st.spinner("Loading documents..."):
        documents = api.get_documents()

    if documents:
        # Sample documents (in real implementation, these come from API)
        sample_docs = [
            {
                "id": "1",
                "name": "Labour Act, 2074",
                "chunks": 256,
                "status": "Active",
                "upload_date": "2024-01-15",
                "description": "Comprehensive labour law covering employment rights and regulations"
            },
            {
                "id": "2",
                "name": "Social Security Act, 2074",
                "chunks": 184,
                "status": "Active",
                "upload_date": "2024-01-20",
                "description": "Social security benefits and coverage for workers"
            },
            {
                "id": "3",
                "name": "Foreign Employment Act, 2064",
                "chunks": 142,
                "status": "Active",
                "upload_date": "2024-02-01",
                "description": "Guidelines for foreign employment and worker protection"
            },
            {
                "id": "4",
                "name": "Right to Employment Act, 2064",
                "chunks": 98,
                "status": "Active",
                "upload_date": "2024-02-10",
                "description": "Employment rights and protections for workers"
            },
        ]

        cols = st.columns(2)
        for idx, doc in enumerate(sample_docs):
            col = cols[idx % 2]
            with col:
                st.markdown(
                    f"""
                    <div class="card">
                        <h4 style="margin-top: 0; color: #1e3a8a;">{doc['name']}</h4>
                        <p style="color: #64748b; margin: 0.5rem 0; font-size: 0.9rem;">
                            {doc['description']}
                        </p>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; font-size: 0.9rem;">
                            <div>
                                <span style="color: #64748b;">Chunks:</span><br>
                                <strong style="color: #1e3a8a;">{doc['chunks']}</strong>
                            </div>
                            <div>
                                <span style="color: #64748b;">Status:</span><br>
                                <strong style="color: #16a34a;">● {doc['status']}</strong>
                            </div>
                        </div>
                        <div style="font-size: 0.85rem; color: #94a3b8;">
                            📅 {doc['upload_date']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No documents indexed yet. Upload documents from the Admin Panel.")

# ============================================================================
# PAGE: ADMIN PANEL
# ============================================================================

def page_admin():
    st.markdown("### 🔐 Admin Panel")
    
    if not st.session_state.authenticated_admin:
        st.warning("This section is password protected.")
        
        password_input = st.text_input(
            "Enter admin password:",
            type="password",
            label_visibility="collapsed"
        )
        
        if st.button("Login", use_container_width=True, type="primary"):
            if password_input == ADMIN_PASSWORD:
                st.session_state.authenticated_admin = True
                st.success("✅ Authenticated!")
                st.rerun()
            else:
                st.error("❌ Invalid password")
        
        return

    # Admin authenticated
    st.success("✅ Admin Panel Unlocked")
    st.divider()

    # Statistics
    st.markdown("### 📊 System Statistics")
    
    with st.spinner("Loading statistics..."):
        stats = api.get_stats()
    
    if not stats.get("error", False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", stats.get('total_documents', 0))
        with col2:
            st.metric("Total Chunks", stats.get('total_chunks', 0))
        with col3:
            st.metric("Total Uploads", stats.get('total_uploads', 0))
        with col4:
            status = "🟢 Online" if not stats.get("error") else "🔴 Offline"
            st.metric("System Status", status)

    st.divider()

    # Document Management
    st.markdown("### 📄 Document Management")
    
    tab1, tab2, tab3 = st.tabs(["Upload", "Manage", "Reindex"])

    with tab1:
        st.markdown("#### Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Drop PDF files here or click to upload",
            type="pdf",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        if uploaded_files:
            if st.button("Upload Documents", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, file in enumerate(uploaded_files):
                    status_text.text(f"Uploading {idx + 1}/{len(uploaded_files)}: {file.name}")
                    
                    response = api.upload_document(file.name, file.getbuffer())
                    
                    if not response.get("error"):
                        st.success(f"✅ {file.name} uploaded successfully")
                    else:
                        st.error(f"❌ Failed to upload {file.name}")
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                status_text.empty()
                progress_bar.empty()

    with tab2:
        st.markdown("#### Manage Documents")
        
        with st.spinner("Loading documents..."):
            documents = api.get_documents()

        if documents:
            # Create table
            doc_list = []
            for doc in documents:
                doc_list.append({
                    "ID": doc.get("id", "N/A"),
                    "Name": doc.get("name", "N/A"),
                    "Chunks": doc.get("chunks", 0),
                    "Status": "✅ Active"
                })
            
            st.dataframe(doc_list, use_container_width=True, hide_index=True)
            
            # Delete document
            st.markdown("**Delete Document**")
            doc_id = st.text_input("Enter Document ID to delete:")
            
            if st.button("Delete", type="secondary"):
                if doc_id:
                    response = api.delete_document(doc_id)
                    if not response.get("error"):
                        st.success("✅ Document deleted successfully")
                    else:
                        st.error("❌ Failed to delete document")
                else:
                    st.warning("Please enter a document ID")
        else:
            st.info("No documents to manage")

    with tab3:
        st.markdown("#### Reindex Documents")
        st.info("Reindex all documents to update the knowledge base. This may take a few minutes.")
        
        if st.button("Start Reindexing", type="primary", use_container_width=True):
            with st.spinner("Reindexing documents..."):
                response = api.reindex()
            
            if not response.get("error"):
                st.success("✅ Reindexing completed successfully")
                st.balloons()
            else:
                st.error(f"❌ Reindexing failed: {response.get('message')}")

    st.divider()

    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated_admin = False
        st.rerun()

# ============================================================================
# MAIN APP ROUTING
# ============================================================================

def main():
    if st.session_state.page == "Home":
        page_home()
    elif st.session_state.page == "Ask":
        page_ask_question()
    elif st.session_state.page == "Knowledge":
        page_knowledge_base()
    elif st.session_state.page == "Admin":
        page_admin()
    else:
        page_home()

if __name__ == "__main__":
    main()
