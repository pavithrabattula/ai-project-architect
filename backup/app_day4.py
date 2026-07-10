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
st.title("🚀 AI Project Architect")

st.write(
    "Generate complete software architecture, technology stack, database design, REST APIs, folder structure, deployment strategy and roadmap using AI."
)

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