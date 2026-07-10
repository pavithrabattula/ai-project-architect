import re
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

# -------------------------------
# Load Environment Variables
# -------------------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY is missing. Add it in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# -------------------------------
# Markdown -> PDF helpers
# -------------------------------
def _inline_markdown_to_html(text: str) -> str:
    """Convert a subset of inline Markdown (bold/italic) to ReportLab-safe HTML,
    after escaping raw HTML special characters."""
    text = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )
    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
    # Italic: *text* or _text_
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<i>\1</i>", text)
    # Inline code: `text`
    text = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)
    return text


def create_pdf(text: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    h1_style = ParagraphStyle(
        "H1Custom", parent=styles["Heading1"],
        fontSize=18, spaceBefore=18, spaceAfter=10, textColor="#1a1a1a",
    )
    h2_style = ParagraphStyle(
        "H2Custom", parent=styles["Heading2"],
        fontSize=14, spaceBefore=14, spaceAfter=8, textColor="#1a1a1a",
    )
    h3_style = ParagraphStyle(
        "H3Custom", parent=styles["Heading3"],
        fontSize=12, spaceBefore=10, spaceAfter=6, textColor="#1a1a1a",
    )
    body_style = ParagraphStyle(
        "BodyCustom", parent=styles["BodyText"],
        fontSize=10.5, leading=15, spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "BulletCustom", parent=body_style,
        leftIndent=18, bulletIndent=6,
    )
    code_style = ParagraphStyle(
        "CodeCustom", parent=styles["Code"],
        fontSize=9, leading=12, backColor="#f0f0f0",
        leftIndent=10, spaceAfter=6,
    )

    story = []
    in_code_block = False
    code_buffer = []

    lines = text.split("\n")

    for raw_line in lines:
        line = raw_line.rstrip()

        # Fenced code blocks ```...```
        if line.strip().startswith("```"):
            if in_code_block:
                # closing fence - flush buffered code
                code_text = "\n".join(code_buffer)
                code_text = (
                    code_text.replace("&", "&amp;")
                             .replace("<", "&lt;")
                             .replace(">", "&gt;")
                             .replace("\n", "<br/>")
                )
                story.append(Paragraph(code_text or "&nbsp;", code_style))
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        stripped = line.strip()

        # Empty line -> small spacer
        if stripped == "":
            story.append(Spacer(1, 6))
            continue

        # Headings
        if stripped.startswith("### "):
            story.append(Paragraph(_inline_markdown_to_html(stripped[4:]), h3_style))
        elif stripped.startswith("## "):
            story.append(Paragraph(_inline_markdown_to_html(stripped[3:]), h2_style))
        elif stripped.startswith("# "):
            story.append(Paragraph(_inline_markdown_to_html(stripped[2:]), h1_style))
        # Bullet points
        elif stripped.startswith("- ") or stripped.startswith("* "):
            content = _inline_markdown_to_html(stripped[2:])
            story.append(Paragraph(f"• {content}", bullet_style))
        # Numbered list items (e.g. "1. Something")
        elif re.match(r"^\d+\.\s", stripped):
            content = _inline_markdown_to_html(re.sub(r"^\d+\.\s", "", stripped))
            num = re.match(r"^(\d+)\.", stripped).group(1)
            story.append(Paragraph(f"{num}. {content}", bullet_style))
        # Regular paragraph
        else:
            story.append(Paragraph(_inline_markdown_to_html(stripped), body_style))

    # Flush any unclosed code block just in case
    if code_buffer:
        code_text = "\n".join(code_buffer)
        code_text = (
            code_text.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace("\n", "<br/>")
        )
        story.append(Paragraph(code_text, code_style))

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

if "history" not in st.session_state:
    st.session_state.history = []

MAX_HISTORY = 15  # cap to avoid unbounded session growth

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

for idx, example in enumerate(examples):
    if st.sidebar.button(example, key=f"sample_{idx}"):
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
st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Recent Projects")

if st.session_state.history:

    # Use enumerate on the reversed list so every key is guaranteed unique,
    # even if two entries share the same project title.
    for pos, item in enumerate(reversed(st.session_state.history)):

        with st.sidebar.expander(item["project"]):

            st.write(f"🎯 Complexity: {item['complexity']}")
            st.write(item["blueprint"][:150] + "...")

            if st.button("📂 Open", key=f"open_{pos}"):
                st.session_state.blueprint = item["blueprint"]
                st.rerun()

else:
    st.sidebar.write("No projects generated yet.")

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

            blueprint_text = getattr(response, "text", None)

            if not blueprint_text or not blueprint_text.strip():
                st.error(
                    "❌ The AI returned an empty response. This can happen if the "
                    "content was filtered or the request failed silently. Please try again "
                    "or rephrase your project idea."
                )
                st.stop()

            st.session_state.blueprint = blueprint_text

            st.session_state.history.append({
                "project": project,
                "complexity": complexity,
                "blueprint": blueprint_text
            })

            # Cap history size to avoid unbounded growth in long sessions
            if len(st.session_state.history) > MAX_HISTORY:
                st.session_state.history = st.session_state.history[-MAX_HISTORY:]

            st.success("✅ Blueprint Generated Successfully!")

            st.divider()

            # -------------------------------
            # Estimate Snapshot (based on complexity tier, not AI-generated)
            # -------------------------------
            st.subheader("📊 Estimate Snapshot")
            st.caption("Typical ranges for this complexity tier — not project-specific AI output.")

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

            col1.metric("⏱ Development Time", duration)
            col2.metric("👨‍💻 Team Size", team)
            col3.metric("💰 Estimated Budget", budget)
            col4.metric("⭐ Complexity", complexity)

            # Sanitize filename for common invalid characters across OSes
            filename = project.strip()
            filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
            filename = re.sub(r"\s+", "_", filename)

            pdf_file = create_pdf(st.session_state.blueprint)

            dl_col1, dl_col2 = st.columns(2)

            with dl_col1:
                st.download_button(
                    label="📥 Download Markdown",
                    data=st.session_state.blueprint,
                    file_name=f"{filename}_Blueprint.md",
                    mime="text/markdown"
                )

            with dl_col2:
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_file,
                    file_name=f"{filename}_Blueprint.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("❌ Something went wrong while generating the blueprint.")
            st.write(e)

if st.session_state.blueprint:
    st.divider()
    st.subheader("📄 Current Blueprint")
    st.markdown(st.session_state.blueprint)

# -------------------------------
# Footer
# -------------------------------
st.divider()

st.caption("Built with ❤️ using Streamlit and Google Gemini")