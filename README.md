# 🚀 AI Project Architect

Generate professional software architecture blueprints — including tech stack recommendations, database design, REST API endpoints, folder structure, security considerations, deployment strategy, and a development roadmap — powered by Google Gemini AI.

Built with **Python**, **Streamlit**, and the **Google Gemini API**.

---

## ✨ Features

- 🤖 AI-generated software blueprints tailored to project complexity (Beginner / Intermediate / Advanced)
- 🗄 Auto-generated database schema and REST API endpoint suggestions
- 📌 One-click sample project ideas (e.g. Hospital Management System, E-Commerce Website, AI Chatbot)
- 📊 Quick estimate snapshot (development time, team size, budget) based on complexity tier
- 📥 Export blueprints as **Markdown** or **PDF**
- 🕒 Session history of previously generated blueprints

---

## 🛠 Setup

### 1. Clone the repository
```bash
git clone https://github.com/pavithrabattula/ai-project-architect.git
cd ai-project-architect
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```
Get a free API key from [Google AI Studio](https://aistudio.google.com/).

> ⚠️ Never commit your `.env` file — it's already listed in `.gitignore` to keep your key private.

### 5. Run the app
```bash
streamlit run app.py
```
Then open the local URL shown in your terminal (usually `http://localhost:8501`).

---

## 📁 Project Structure
```
ai-project-architect/
├── app.py              # Main Streamlit application
├── .env                # Your API key (not committed)
├── .gitignore
├── backup/             # Previous versions of app.py
├── requirements.txt
└── README.md
```

---

## 📄 Export Options

Once a blueprint is generated, you can download it as:
- **Markdown (.md)** — full formatting preserved
- **PDF** — rendered with headings, bullet points, and code blocks

---

## 🙌 Built With

- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [ReportLab](https://www.reportlab.com/) (PDF generation)

---

Built with ❤️ using Streamlit and Google Gemini.
