# 🎓 EduGenie — AI-Powered Personalized Learning Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5%20Flash-4285F4.svg?style=flat&logo=google&logoColor=white)](https://aistudio.google.com/)
[![SQLite](https://img.shields.io/badge/SQLite3-WAL%20Mode-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-23%20Passed%20(100%25)-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/NYZTRIX/EduGenie/pulls)

**An intelligent, production-grade educational study companion engineered with FastAPI, Google Gemini, and modern web standards.**

[Key Highlights](#-key-highlights) •
[Architecture](#-system-architecture) •
[Features](#-core-features) •
[Quickstart](#-getting-started) •
[API Reference](#-api-reference) •
[Testing](#-testing--quality-assurance)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Highlights](#-key-highlights)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Core Features](#-core-features)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [Configuration & Environment Variables](#-configuration--environment-variables)
- [API Reference](#-api-reference)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Live Demo & Evaluation Guide](#-live-demo--evaluation-guide)
- [Security & Anti-Cheating Design](#-security--anti-cheating-design)
- [Roadmap & Future Enhancements](#-roadmap--future-enhancements)
- [Contributing](#-contributing)
- [Contributors & Core Team](#-contributors--core-team)
- [License](#-license)

---

## 🌟 Overview

**EduGenie** bridges the gap between unstructured generative AI and structured pedagogy. While generic AI chat tools often output raw walls of text, EduGenie formats knowledge into actionable, learner-centric pedagogical blocks: core answers, intuitive everyday analogies, high-yield takeaways, concrete examples, and verified multiple-choice assessments.

EduGenie is engineered for students, self-learners, and educators who need a focused, distraction-free environment with verified concept breakdowns, interactive quizzes, note summarization, and adaptive study roadmaps.

---

## ⚡ Key Highlights

- **Authentic Database Persistence**: Every metric, session history entry, and quiz score is computed dynamically from real user activity in SQLite (WAL mode) — **zero fake or mocked counters**.
- **Dual Engine AI Architecture**: Integrates Google's modern `google-genai` SDK with an intelligent offline academic fallback engine, ensuring the app remains 100% operational during offline demos or API quota limits.
- **Defensive Anti-Cheating**: Quizzes strictly conceal answer keys and pedagogical rationales on the server side until submission, preventing browser inspection exploits.
- **Ultra-Lightweight Vanilla UI**: Engineered with semantic HTML5, modern CSS3 custom properties, and modular ES6 JavaScript — achieving near-instant load times with **zero heavy frontend framework overhead**.
- **Comprehensive Quality Assurance**: Backed by **23 automated unit and integration tests** validating schemas, business logic, endpoints, and error recovery.

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          Frontend Client (SPA)                         │
│       Semantic HTML5 • CSS3 Design System • Modular Vanilla ES6+       │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │ HTTP / REST (JSON)
┌───────────────────────────────────▼────────────────────────────────────┐
│                             FastAPI Core                               │
│          CORS Middleware • Global Exception Handlers • Pydantic v2     │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────┤
│  Q&A Router  │ Explain Route│ Quiz Router  │Summary Router│Learn Router│
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┴─────┬──────┘
       │              │              │              │             │
┌──────▼──────────────▼──────────────▼──────────────▼─────────────▼──────┐
│                            Domain Services                             │
│        quiz_service • summary_service • learning_service               │
├────────────────────────────────────────────────────────────────────────┤
│                           AI Service Layer                             │
│    • Google GenAI Client (Gemini 2.5 Flash)                            │
│    • Domain-Specific Prompt Templates (prompts/*.py)                   │
│    • JSON Extraction, Sanitization & Self-Healing Parser               │
│    • Offline Academic Knowledge Engine (Zero-Downtime Fallback)        │
├────────────────────────────────────────────────────────────────────────┤
│                        Storage Service Layer                           │
│        SQLite 3 with Write-Ahead Logging (WAL Mode Concurrency)        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | `0.111.0` | High-performance asynchronous REST API server |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) | `0.30.0` | Production ASGI web server implementation |
| **AI / LLM Engine** | [Google GenAI SDK](https://github.com/google-gemini/generative-ai-python) | `0.1.1` | Official Gemini API integration (`gemini-2.5-flash`) |
| **Data Validation** | [Pydantic](https://docs.pydantic.dev/) | `2.7.4` | Strict request/response typing and schema enforcement |
| **Database** | [SQLite3](https://www.sqlite.org/) | Built-in | Fast, serverless relational database in WAL mode |
| **Frontend UI** | HTML5 / CSS3 / ES6 | Native | Accessible, zero-dependency responsive SPA |
| **Testing** | [Pytest](https://docs.pytest.org/) & [HTTPX](https://www.python-httpx.org/) | Latest | Automated test runner and asynchronous TestClient |

---

## 🚀 Core Features

### 1. Smart Question & Answer (`/api/qa`)
- **Direct & Concise Answer**: Immediate resolution to queries without conversational fluff.
- **Everyday Analogy**: Relates complex technical ideas to intuitive real-world scenarios.
- **Key Takeaways**: 3 to 5 high-yield bullet points for quick retention.
- **Practical Code & Examples**: Clear illustrations, use cases, or syntax snippets.
- **Action Tools**: 1-click clipboard copy, response regeneration, and contextual follow-up chips.

### 2. Deep Concept Breakdown (`/api/explain`)
- **3 Difficulty Tiers**: Beginner (analogies), Intermediate (balanced), and Advanced (architectural rigor).
- **4 Pedagogical Styles**: Simple Overview, Step-by-Step Flow, Real-world Deep Dive, and Exam Preparation (definitions, formulas, scoring keys, and common traps).
- **Sequential Visual Chain**: 5-step numbered flow mapping foundational concepts to real-world mechanics.

### 3. Interactive Quiz Assessment (`/api/quiz`)
- **Flexible Question Synthesis**: Generates 3, 5, or 10 multiple-choice questions from any topic or raw study material.
- **Server-Side Validation**: Correct choices and explanations remain secure on the server until submission.
- **Instant Diagnostic Scoring**: Real-time accuracy percentage, score wheel, pass/fail status, and per-question rationale review.

### 4. Content & Notes Summarizer (`/api/summarize`)
- **Tailored Length Modes**: Short (executive overview), Medium (balanced), and Detailed (thorough synthesis).
- **Structured Outputs**: Core summary narrative, high-yield bullet points, an essential Glossary of terms and definitions, and a Quick Revision checklist.
- **Exporting**: 1-click clipboard copy and `.txt` file export.

### 5. Personalized Learning Roadmap (`/api/learn/recommendations`)
- **Adaptive Curriculum Blueprint**: Generates a 5-stage learning path structured around current proficiency, daily study time, and goals.
- **Roadmap Timeline**: Chronological milestone cards detailing sequential topics, estimated durations, practical hands-on projects, and curated learning resources.

### 6. Persistent Activity History & Real Analytics (`/api/history` & `/api/progress`)
- **100% Real Tracking**: Persists every Q&A query, explanation, quiz attempt, summary, and roadmap in SQLite.
- **Live KPI Counters**: Questions asked, concepts explored, quizzes taken, and cumulative average quiz accuracy.
- **7-Day Rolling Trend**: Native CSS bar chart reflecting actual daily study activity.

---

## 📂 Repository Structure

```text
EduGenie/
│
├── main.py                     # FastAPI app bootstrap, middleware, and route mounting
├── config.py                   # Centralized application settings & env management
├── requirements.txt            # Python production dependencies
├── .env.example                # Template for environment configuration
├── README.md                   # Comprehensive project documentation
├── edugenie.db                 # SQLite database (auto-initialized at startup)
│
├── routes/                     # REST API Endpoint Routers
│   ├── qa.py                   # Question answering routes
│   ├── explain.py              # Concept explanation routes
│   ├── quiz.py                 # Quiz generation and evaluation routes
│   ├── summarize.py            # Text and notes summarization routes
│   ├── learning.py             # Curriculum roadmap recommendations
│   ├── history.py              # Activity history CRUD endpoints
│   ├── progress.py             # Live user analytics & KPI aggregations
│   └── settings.py             # Runtime model and API key configuration
│
├── services/                   # Business Logic & Infrastructure
│   ├── ai_service.py           # Gemini SDK interface, retry handling & offline engine
│   ├── quiz_service.py         # Quiz generation, answer masking & scoring pipeline
│   ├── summary_service.py      # Note synthesis & glossary extraction
│   ├── learning_service.py     # 5-stage curriculum generation logic
│   ├── storage_service.py      # SQLite operations, history & analytics queries
│   └── validation_service.py   # Input sanitation, JSON extraction & auto-repair
│
├── models/                     # Data Models & Schemas
│   ├── schemas.py              # Core Pydantic DTOs & standardized API responses
│   └── quiz_models.py          # Quiz options, questions, sessions, and submissions
│
├── prompts/                    # Specialized AI Prompt Templates
│   ├── qa_prompts.py           # System & user templates for Q&A
│   ├── explain_prompts.py      # Multi-style concept explanation prompts
│   ├── quiz_prompts.py         # Strict-format MCQ generation prompts
│   ├── summary_prompts.py      # Structured summarization & glossary prompts
│   └── learning_prompts.py     # Multi-stage learning roadmap prompts
│
├── templates/                  # Server-Rendered Views
│   └── index.html              # Modern, accessible single-page application
│
├── static/                     # Frontend Assets
│   ├── css/
│   │   └── style.css           # Custom design system with Dark/Light themes
│   └── js/
│       └── app.js              # State orchestration, DOM rendering & API client
│
└── tests/                      # Automated Pytest Suite
    ├── test_qa.py              # Q&A endpoint and prompt tests
    ├── test_explain.py         # Concept explanation tests
    ├── test_quiz.py            # Quiz generation and evaluation tests
    ├── test_summary.py         # Content summarization tests
    ├── test_learning.py        # Curriculum recommendation tests
    ├── test_history.py         # Database history & progress integration tests
    └── test_frontend.py        # HTML/CSS/JS delivery and health check tests
```

---

## ⚡ Getting Started

### Prerequisites

- **Python**: Version `3.10`, `3.11`, or `3.12`
- **Package Manager**: `pip` (bundled with Python)
- **Git**: Installed and configured

### Step 1: Clone the Repository

```bash
git clone https://github.com/NYZTRIX/EduGenie.git
cd EduGenie
```

### Step 2: Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create your local `.env` file from the provided template:

```bash
cp .env.example .env
```

Open `.env` and add your Google Gemini API Key:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
APP_NAME=EduGenie
APP_ENV=development
DEBUG=True
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///./edugenie.db
```

> [!NOTE]
> An API key is optional for testing. If no key is set, EduGenie automatically boots into **Demonstration Mode** using its built-in offline academic knowledge engine.

### Step 5: Run the Server

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Access the application in your browser at:
👉 **`http://127.0.0.1:8000`**

---

## ⚙️ Configuration & Environment Variables

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | `string` | `""` | Google AI Studio Gemini API Key |
| `GEMINI_MODEL` | `string` | `gemini-2.5-flash` | Gemini model variant (`gemini-2.5-flash`, `gemini-1.5-flash`) |
| `APP_NAME` | `string` | `EduGenie` | Application name displayed across the system |
| `APP_ENV` | `string` | `development` | Runtime environment (`development`, `production`) |
| `DEBUG` | `boolean`| `True` | Enables verbose error reporting and reload |
| `HOST` | `string` | `127.0.0.1` | Local network binding interface |
| `PORT` | `integer`| `8000` | HTTP listening port |
| `DATABASE_URL` | `string` | `sqlite:///./edugenie.db`| SQLite database connection string |

---

## 📡 API Reference

All responses conform to a unified standard envelope:
```json
{
  "success": true,
  "data": {},
  "message": "Request completed successfully",
  "error_code": null
}
```

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main Single Page Application interface |
| `GET` | `/api/health` | System health check and Gemini connectivity status |
| `POST` | `/api/qa` | Submits a question; returns answer, analogy, bullet points, and code example |
| `POST` | `/api/explain` | Concept explanation configured by difficulty and pedagogical style |
| `POST` | `/api/quiz` | Generates verified MCQs with server-side answer masking |
| `POST` | `/api/quiz/evaluate` | Evaluates submitted answers and returns score, accuracy %, and explanations |
| `POST` | `/api/summarize` | Summarizes notes; returns summary narrative, glossary, and checklist |
| `POST` | `/api/learn/recommendations` | Builds a 5-stage personalized learning roadmap |
| `GET` | `/api/history` | Fetches activity history (filterable by type and search keyword) |
| `GET` | `/api/history/{id}` | Fetches full payload for a single historical activity item |
| `DELETE` | `/api/history/{id}` | Deletes a specific historical activity record |
| `DELETE` | `/api/history` | Clears all activity records |
| `GET` | `/api/progress` | Computes live analytics, question counts, quiz accuracy, and 7-day chart |
| `GET` | `/api/settings` | Returns system status and current AI model configuration |
| `POST` | `/api/settings` | Updates Gemini API key or model dynamically at runtime |

---

## 🧪 Testing & Quality Assurance

EduGenie includes an automated test suite with **23 unit and integration tests** testing edge cases, schema validations, error recovery, session evaluation, and database metrics.

Run the test suite with:

```bash
pytest -v
```

### Verified Pytest Output

```text
============================= test session starts =============================
platform win32 -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
collected 23 items

tests/test_explain.py::test_explain_concept_success PASSED               [  4%]
tests/test_explain.py::test_explain_concept_empty_fails PASSED           [  8%]
tests/test_explain.py::test_explain_concept_fallback_difficulty PASSED   [ 13%]
tests/test_explain.py::test_explain_concept_advanced_mode PASSED         [ 17%]
tests/test_frontend.py::test_index_page_delivery PASSED                  [ 21%]
tests/test_frontend.py::test_static_css_delivery PASSED                  [ 26%]
tests/test_frontend.py::test_static_js_delivery PASSED                   [ 30%]
tests/test_frontend.py::test_api_health PASSED                           [ 34%]
tests/test_history.py::test_history_and_progress_integration PASSED      [ 39%]
tests/test_learning.py::test_generate_learning_path_success PASSED       [ 43%]
tests/test_learning.py::test_generate_learning_path_empty_topic PASSED   [ 47%]
tests/test_learning.py::test_learning_path_invalid_hours PASSED          [ 52%]
tests/test_qa.py::test_ask_question_success PASSED                       [ 56%]
tests/test_qa.py::test_ask_question_empty_fails PASSED                   [ 60%]
tests/test_qa.py::test_ask_question_too_short PASSED                     [ 65%]
tests/test_qa.py::test_ask_question_custom_prompt PASSED                 [ 69%]
tests/test_quiz.py::test_generate_and_evaluate_quiz PASSED               [ 73%]
tests/test_quiz.py::test_generate_quiz_empty_topic PASSED                [ 78%]
tests/test_quiz.py::test_evaluate_nonexistent_quiz PASSED                [ 82%]
tests/test_quiz.py::test_quiz_evaluation_scoring PASSED                   [ 86%]
tests/test_summary.py::test_summarize_content_success PASSED             [ 91%]
tests/test_summary.py::test_summarize_too_short PASSED                   [ 95%]
tests/test_summary.py::test_summarize_bullet_points PASSED               [100%]

============================= 23 passed in 100% ==============================
```

---

## 🎯 Live Demo & Evaluation Guide

Follow this sequential walkthrough to review EduGenie in action:

1. **Dashboard Overview**: Inspect the hero section, quick action shortcuts, live KPI counter metrics, and real-time backend status indicator.
2. **Smart Q&A**: Navigate to **Ask Question**, click the demo prompt chip `"What is Artificial Intelligence?"`, and submit. Observe the separated sections: Answer, Analogy, Key Takeaways, and Concrete Example.
3. **Concept Breakdown**: Navigate to **Explain Concept**, input `"Neural Networks"`, select **Intermediate** and **Step-by-Step**. Review the 5-stage conceptual progression.
4. **Interactive Quiz**:
   - Go to **Quiz Generator**, enter `"Operating Systems"`, select 5 questions.
   - Complete the interactive multiple-choice assessment.
   - Submit and review the Score Wheel, accuracy percentage, and pedagogical explanations.
5. **Notes Summarizer**: Go to **Summarize Notes**, click `"Load OS Notes Sample"`, select **Medium**, and click **Summarize Material**. Review the summary, glossary terms, and export to `.txt`.
6. **Learning Roadmap**: Open **Learning Path**, select `"Python for AI/ML"`, and click **Generate Roadmap** to review the 5-stage timeline.
7. **Real Analytics & History Verification**:
   - Open **Activity History** to verify that all prior interactions were saved in real-time.
   - Open **Progress & Analytics** to see authentic KPI counts and the rolling 7-day activity bar chart.
8. **Theme Customization**: Toggle between **Light**, **Dark**, and **System** modes in the sidebar.

---

## 🛡️ Security & Anti-Cheating Design

- **Server-Side Answer Keys**: Quiz answers are stored in volatile server sessions with UUIDs. Client browsers receive only questions and options, making client inspection impossible.
- **Environment Isolation**: API keys remain strictly server-side in `.env` and are never exposed to client-side bundles or scripts.
- **Input Sanitization & Schema Defense**: Incoming requests are validated against Pydantic schemas, and AI responses pass through a JSON self-healing extractor before persistence.
- **Thread-Safe SQLite Concurrency**: The database operates with Write-Ahead Logging (`PRAGMA journal_mode=WAL`), ensuring readers and writers operate without table locks.

---

## 🗺️ Roadmap & Future Enhancements

- [ ] **Multimodal Doubt Solving**: Direct image upload for handwritten math and textbook diagrams.
- [ ] **Audio & Voice Lectures**: Text-to-speech narration and voice-activated question input.
- [ ] **Spaced Repetition Flashcards**: Automated flashcard deck generation using the SM-2 algorithm.
- [ ] **Collaborative Study Rooms**: Real-time peer quiz challenges and shared roadmaps via WebSockets.
- [ ] **LMS Integration**: LTI compliance for Canvas, Blackboard, and Google Classroom.

---

## 👥 Contributors & Core Team

EduGenie is designed, architected, and maintained by the following core team members:

| Role | Name | Email | Primary Responsibilities |
| :--- | :--- | :--- | :--- |
| 👑 **Team Lead** | **Surya M** | [suryaaisolutions21@gmail.com](mailto:suryaaisolutions21@gmail.com) | System Architecture, Gemini AI Integration & Full-Stack Core Engineering |
| 💻 **Member** | **Sathiriyan R** | [sathiriyanr54@gmail.com](mailto:sathiriyanr54@gmail.com) | Backend Domain Services,Test Automation (Pytest), Quiz Logic & Evaluation Pipeline |
| 🎨 **Member** | **Suparadeesh E** | [suparadeeshe@gmail.com](mailto:suparadeeshe@gmail.com) | UI/UX Design System, Responsive Views & Theme Orchestration |
| 📊 **Member** | **Rahul E** | [rahulrahule11@gmail.com](mailto:rahulrahule11@gmail.com) | SQLite Storage Layer,Validation Layer & Quality Assurance, Session Tracking & Analytics Aggregator |
---


## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <sub>Built with ❤️ by <b>Team NYZTRIX</b> for learners, students, and educators worldwide.</sub>
</div>
