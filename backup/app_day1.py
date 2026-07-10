import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="AI Project Architect", page_icon="🚀")

st.title("🚀 AI Project Architect")

project = st.text_area(
    "Describe your project idea",
    placeholder="Example: Hospital Management System"
)

if st.button("Generate Blueprint"):

    if not project.strip():
        st.warning("Please enter a project idea.")
    else:
        with st.spinner("Generating..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
You are an expert Software Architect.

Generate a detailed software blueprint for:

{project}

Include:
1. Project Overview
2. Features
3. Tech Stack
4. Database Design
5. APIs
6. Folder Structure
7. Development Roadmap
"""
            )

            st.markdown(response.text)