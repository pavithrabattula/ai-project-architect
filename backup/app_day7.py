import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------
# Load Environment Variables
# -------------------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

# -------------------------------
# Gemini Client
# -------------------------------
client = genai.Client(api_key=api_key)
# -------------------------------
# PDF Generator
# -------------------------------
def create_pdf(text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        # Empty line
        if line.strip() == "":
            story.append(Paragraph("<br/>", styles["BodyText"]))
            continue

        # Escape HTML characters
        line = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        # Preserve spaces
        line = line.replace("  ", "&nbsp;&nbsp;")

        story.append(
            Paragraph(line, styles["BodyText"])
        )

    doc.build(story)

    buffer.seek(0)

    return buffer
# -------------------------------
# Streamlit Page Settings
# -------------------------------
st.set_page_config(
    page_title="AI Project Architect",
    page_icon="🚀",
    layout="wide"
)
# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0E1117;
}

/* Main Title */
h1 {
    color: #4CAF50;
    text-align: center;
    font-weight: bold;
}

/* Sub Headers */
h2, h3 {
    color: #00BFFF;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background-color: #4CAF50;
    color: white;
}

.stButton > button:hover {
    background-color: #45a049;
}

/* Text Area */
textarea {
    border-radius: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "project" not in st.session_state:
    st.session_state.project = ""

if "blueprint" not in st.session_state:
    st.session_state.blueprint = ""

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🚀 AI Project Architect")

st.sidebar.markdown("### 📌 Sample Projects")

examples = [
    "Hospital Management System",
    "E-Commerce Website",
    "Food Delivery App",
    "Bank Management System",
    "Library Management System",
    "Student Management System",
    "AI Resume Builder",
    "Inventory Management System",
    "Hotel Management System",
    "AI Chatbot"
]

for example in examples:
    if st.sidebar.button(example):
        st.session_state.project = f"Build a {example}"
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.info("""
### About

This application uses **Google Gemini AI**
to generate professional software architecture blueprints.

**Built with**

- Python
- Streamlit
- Google Gemini API
""")

# -------------------------------
# Main Page
# -------------------------------
st.markdown("""
<div style="
background: linear-gradient(90deg,#4CAF50,#2196F3);
padding:25px;
border-radius:15px;
text-align:center;
margin-bottom:25px;
">

<h1 style="color:white;">
🚀 AI Project Architect
</h1>

<p style="font-size:20px;color:white;">
Generate professional software architecture, REST APIs,
database design, deployment strategy and development roadmap using Google Gemini AI.
</p>

</div>
""", unsafe_allow_html=True)
# -------------------------------
# Feature Cards
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
### ⚡ AI Blueprint

Generate a complete software architecture using Google Gemini AI.
""")

with col2:
    st.info("""
### 🗄 Database Design

Automatically create database schema and REST API endpoints.
""")

with col3:
    st.info("""
### 📄 Export

Download your blueprint as Markdown or PDF.
""")

project = st.text_area(
    "Describe your project idea",
    value=st.session_state.project,
    placeholder="Example: Build a Hospital Management System",
    height=180
)

complexity = st.selectbox(
    "🎯 Select Project Complexity",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# -------------------------------
# Generate Button
# -------------------------------
if st.button("🚀 Generate Software Blueprint"):

    if not project.strip():
        st.warning("⚠ Please enter a project idea.")

    else:

        prompt = f"""
You are a Senior Software Architect with over 20 years of experience.

Generate a professional software blueprint.

Project:
{project}

Complexity:
{complexity}

If Beginner:
- Flask
- SQLite
- Simple Folder Structure
- Basic Authentication

If Intermediate:
- FastAPI
- PostgreSQL
- JWT
- Docker
- Modular Architecture

If Advanced:
- Microservices
- Kubernetes
- Kafka
- Redis
- Docker
- CI/CD
- AWS

Return Markdown.

Use these headings exactly:

# Project Overview

# Problem Statement

# Functional Requirements

# Non Functional Requirements

# Core Features

# Recommended Tech Stack

# Database Design

# REST API Endpoints

# Folder Structure

# Security Considerations

# Deployment Strategy

# Future Enhancements

# Development Roadmap
"""

        try:

            with st.spinner("🤖 AI is designing your software architecture..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.session_state.blueprint = response.text

            st.success("✅ Blueprint Generated Successfully!")

            st.divider()

            st.markdown(st.session_state.blueprint)

            # -------------------------------
            # AI Project Analytics
            # -------------------------------
            st.divider()

            st.subheader("📊 AI Project Analytics")

            if complexity == "Beginner":
                duration = "1-2 Months"
                team = "2 Developers"
                budget = "$2K - $5K"

            elif complexity == "Intermediate":
                duration = "3-5 Months"
                team = "4-6 Developers"
                budget = "$10K - $25K"

            else:
                duration = "6-12 Months"
                team = "8-12 Developers"
                budget = "$50K+"

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "⏱ Development Time",
                duration
            )

            col2.metric(
                "👨‍💻 Team Size",
                team
            )

            col3.metric(
                "💰 Estimated Budget",
                budget
            )

            col4.metric(
                "⭐ Complexity",
                complexity
            )


            filename = (
                project.strip()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            pdf_file = create_pdf(st.session_state.blueprint)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📥 Download Markdown",
                    data=st.session_state.blueprint,
                    file_name=f"{filename}_Blueprint.md",
                    mime="text/markdown"
                )

            with col2:
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_file,
                    file_name=f"{filename}_Blueprint.pdf",
                    mime="application/pdf"
                )

        except Exception as e:

            st.error("❌ Something went wrong while generating the blueprint.")

            st.info("Please check your internet connection or Gemini API key and try again.")

            with st.expander("🔍 Technical Details"):
                st.code(str(e))
# -------------------------------
# Footer
# -------------------------------
st.divider()

st.caption("Built with ❤️ using Streamlit and Google Gemini")