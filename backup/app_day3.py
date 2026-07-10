import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path

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
# Streamlit Page Settings
# -------------------------------
st.set_page_config(
    page_title="AI Project Architect",
    page_icon="🚀",
    layout="wide"
)

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

# Initialize session state
if "project" not in st.session_state:
    st.session_state.project = ""

# Sidebar buttons
for example in examples:
    if st.sidebar.button(example):
        st.session_state.project = f"Build a {example}"
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.info(
    """
### About

This application uses **Google Gemini AI** to generate professional software architecture blueprints.

**Built with:**

- Python
- Streamlit
- Google Gemini API
"""
)

# -------------------------------
# Main Page
# -------------------------------
st.title("🚀 AI Project Architect")

st.write(
    "Generate complete software architecture, technology stack, database design, APIs, folder structure, and development roadmap using AI."
)

project = st.text_area(
    "Describe your project idea",
    value=st.session_state.project,
    placeholder="Example: Build a Hospital Management System",
    height=180
)

# -------------------------------
# Generate Button
# -------------------------------
if st.button("🚀 Generate Software Blueprint"):

    if not project.strip():
        st.warning("⚠ Please enter a project idea.")

    else:

        prompt = f"""
You are a Senior Software Architect with over 20 years of experience in designing enterprise software systems.

Generate a professional software blueprint for the following project.

Project:
{project}

The response MUST be in Markdown format.

Use these headings exactly and in this order:

# Project Overview
- Purpose
- Target Users
- Objectives

# Problem Statement

# Functional Requirements

# Non-Functional Requirements

# Core Features

# Recommended Tech Stack
Provide a table with:
- Frontend
- Backend
- Database
- Authentication
- Cloud
- DevOps

# Database Design
List the main tables and briefly describe each one.

# REST API Endpoints
Provide sample REST APIs with HTTP methods.

# Folder Structure
Display a clean folder structure using a code block.

# Security Considerations

# Deployment Strategy

# Future Enhancements

# Development Roadmap
Divide into Phase 1, Phase 2, Phase 3, and Phase 4.

Keep the explanation professional, concise, and easy to understand.
"""

        with st.spinner("🤖 AI is designing your software architecture..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.success("✅ Blueprint Generated Successfully!")

        st.divider()

        st.markdown(response.text)

        # Create filename for download
        filename = (
            project.strip()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        st.download_button(
            label="📥 Download Blueprint",
            data=response.text,
            file_name=f"{filename}_Blueprint.md",
            mime="text/markdown"
        )

# -------------------------------
# Footer
# -------------------------------
st.divider()

st.caption("Built with ❤️ using Streamlit and Google Gemini")