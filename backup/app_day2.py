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

for example in examples:
    st.sidebar.write("• " + example)

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
    height=180,
    placeholder="Example: Build a Hospital Management System"
)

# -------------------------------
# Generate Button
# -------------------------------
if st.button("🚀 Generate Software Blueprint"):

    if not project.strip():
        st.warning("⚠ Please enter a project idea.")
    else:

        prompt = f"""
You are a Senior Software Architect with more than 20 years of experience.

Generate a professional software architecture document.

Project Idea:
{project}

Generate the response in Markdown.

Use the following headings exactly:

# Project Overview

# Problem Statement

# Objectives

# Core Features

# Functional Requirements

# Non Functional Requirements

# Recommended Tech Stack

# Database Design

# REST APIs

# Folder Structure

# Security Considerations

# Deployment Strategy

# Development Roadmap

# Future Enhancements
"""

        with st.spinner("🤖 AI is designing your software architecture..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.success("✅ Blueprint Generated Successfully!")

        st.divider()

        st.markdown(response.text)

        st.download_button(
            label="📥 Download Blueprint",
            data=response.text,
            file_name="software_blueprint.md",
            mime="text/markdown"
        )

# -------------------------------
# Footer
# -------------------------------
st.divider()

st.caption("Built with ❤️ using Streamlit and Google Gemini")