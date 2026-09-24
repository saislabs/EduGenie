# EduGenie — AI-Powered Personalized Learning Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5%20Flash-4285F4.svg?style=flat&logo=google)](https://aistudio.google.com/)
[![SQLite](https://img.shields.io/badge/SQLite3-WAL%20Mode-003B57.svg?style=flat&logo=sqlite)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EduGenie is a production-grade, AI-driven educational web application engineered to serve as an intelligent, personal study companion for students and self-learners. Built with **FastAPI**, **Google Gemini**, and a vanilla **HTML5/CSS3/ES6** design system, EduGenie delivers structured conceptual explanations, rigorous interactive quizzes, notes summarization, personalized curriculum roadmaps, and authentic progress tracking.

---

## 1. Project Overview

EduGenie bridges the gap between raw generative AI outputs and structured pedagogy. Rather than presenting unstructured chat walls, EduGenie formats knowledge into actionable learning blocks: core answers, simple analogies, key takeaways, practical examples, exam preparation hints, and validated multiple-choice assessments.

### Key Highlights
- **Real Backend Flow**: Frontend &rarr; REST API &rarr; Domain Service &rarr; AI/Prompt Layer &rarr; Schema Validation & JSON Repair &rarr; SQLite Persistence &rarr; Frontend.
- **Zero Fake Data**: Every statistic, history item, and quiz score is computed dynamically from real user activity in SQLite (WAL mode).
- **Dual Engine Architecture**: Directly integrates Google's modern `google-genai` SDK with an intelligent offline academic fallback engine, ensuring the application remains functional even in network-constrained or offline demo environments.
- **Enterprise-Grade UI/UX**: Lightweight design system featuring seamless Dark/Light/System theme toggles, mobile drawer navigation, responsive cards, accessible ARIA attributes, and zero external frontend framework overhead.

---

## 2. Core Features

### 1. Question & Answer (`/api/qa`)
- **Direct & Concise Answer**: Immediate resolution to the student's query.
- **Simple Explanation**: Everyday analogies and jargon-free clarification.
- **Key Points**: 3 to 5 high-yield bullet takeaways.
- **Concrete Example**: Practical scenarios, illustrations, or code snippets.
- **Interactive Tools**: 1-click clipboard copy, response regeneration, and follow-up question chaining.

### 2. Concept Explanation (`/api/explain`)
- **Custom Difficulty**: Beginner (everyday analogies), Intermediate (balanced), and Advanced (architectural depth and rigor).
- **Pedagogical Styles**: Simple overview, Step-by-Step sequential flow, Real Example deep dive, or Exam Preparation (definitions, scoring keys, and common pitfalls).
- **Sequential Visual Chain**: 5-step numbered flow mapping from foundation to mechanics and exam tips.

### 3. Quiz Generator & Interactive Assessment (`/api/quiz`)
- **Customizable MCQs**: Topic-based or passage-based question synthesis (3, 5, or 10 questions).
- **Secure Server-Side Evaluation**: Correct answers and pedagogical explanations are kept on the server and revealed only upon submission, preventing client-side inspection.
- **Real-Time Assessment**: Instant scoring, accuracy percentages, pass/fail status, and question-by-question review with explanations.
- **Session Continuity**: Allows instant re-take of the current quiz or generation of a fresh assessment.

### 4. Content Summarization (`/api/summarize`)
- **Document-Style Summarizer**: Tailored for textbook chapters, research articles, and lecture notes.
- **Length Control**: Short (executive overview), Medium (balanced context), and Detailed (nuanced synthesis).
- **Structured Outputs**: Summary prose, Key Points, Important Terms & Definitions glossary, and a Quick Revision checklist.
- **Exporting**: 1-click clipboard copy and TXT file export.

### 5. Personalized Learning Path (`/api/learn/recommendations`)
- **Adaptive Curriculum Blueprint**: Generates a 5-stage learning roadmap based on user's current level, daily study hours, and specific end goal.
- **Visual Roadmap Timeline**: Connected vertical stage cards detailing sequential topics, estimated durations, sequence strategies, hands-on practice projects, and recommended study resources.

### 6. Activity History (`/api/history`)
- **Persistent Tracking**: Real-time SQLite storage for all Q&A sessions, concept breakdowns, quizzes, summaries, and roadmaps.
- **Search & Filter**: Filter by category (Questions, Explanations, Quizzes, Summaries, Roadmaps) or search by keyword.
- **Deep Inspection**: View past outputs in detail modals or clear individual/all records.

### 7. Progress & Analytics Dashboard (`/api/progress`)
- **Authentic Metrics**: Displays questions asked, concepts explored, quizzes taken, and average quiz accuracy computed strictly from database records.
- **Weekly Learning Activity Chart**: Native CSS bar chart showing daily activity over the rolling 7-day window.
- **Empty States**: Friendly empty states when starting out ("No learning activity yet. Start your first learning session.").

---

## 3. Architecture & Tech Stack

```text
┌────────────────────────────────────────────────────────┐
│                   Frontend (SPA)                       │
│    HTML5 • CSS3 (Design System) • Vanilla ES6+ JS      │
└───────────────────────────▲────────────────────────────┘
                            │ REST / JSON (HTTP)
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
│         CORS • Exception Handlers • Pydantic v2        │
├───────────┬───────────┬───────────┬──────────┬─────────┤
│    Q&A    │  Explain  │   Quiz    │ Summary  │ Learn   │
│  Router   │  Router   │  Router   │  Router  │ Router  │
└─────┬─────┴─────┬─────┴─────┬─────┴────┬─────┴────┬────┘
      │           │           │          │          │
┌─────▼───────────▼───────────▼──────────▼──────────▼────┐
│                    Domain Services                     │
│    quiz_service • summary_service • learning_service   │
├────────────────────────────────────────────────────────┤
│                   AI Service Layer                     │
│   • Google GenAI Client (google-genai / Gemini Flash)  │
│   • Prompt Templates (prompts/*.py)                   │
│   • JSON Extraction, Sanitization & Auto-Repair        │
│   • Retry Logic & Exponential Backoff                  │
│   • Offline Academic Engine Fallback                   │
├────────────────────────────────────────────────────────┤
│                 Storage Service Layer                  │
│            SQLite (WAL Mode, Real Tracking)            │
└────────────────────────────────────────────────────────┘
```

### Technology Stack Details
- **Backend Framework**: Python 3.10+ with [FastAPI](https://fastapi.tiangolo.com)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Data Validation & Serialization**: [Pydantic v2](https://docs.pydantic.dev/)
- **AI / LLM Integration**: Official `google-genai` SDK (`gemini-2.5-flash` / `gemini-1.5-flash`)
- **Database Engine**: SQLite 3 with Write-Ahead Logging (WAL) for thread-safe concurrency
- **Frontend Layer**: Semantic HTML5, Custom CSS3 Custom Properties (Design System), Vanilla JavaScript (Modular ES6)
- **Testing**: `pytest` and `httpx` (TestClient)

---

## 4. Folder Structure

```text
EduGenie/
│
├── main.py                     # FastAPI application setup, middleware, routes
├── config.py                   # Centralized configuration & environment loader
├── requirements.txt            # Python package dependencies
├── .env                        # Local environment variables (git-ignored)
├── .env.example                # Example environment template
├── README.md                   # Complete production documentation
├── edugenie.db                 # SQLite database (auto-created on startup)
│
├── routes/                     # REST API Routers
│   ├── __init__.py
│   ├── qa.py                   # POST /api/qa
│   ├── explain.py              # POST /api/explain
│   ├── quiz.py                 # POST /api/quiz, POST /api/quiz/evaluate
│   ├── summarize.py           # POST /api/summarize
│   ├── learning.py             # POST /api/learn/recommendations
│   ├── history.py              # GET/DELETE /api/history
│   ├── progress.py             # GET /api/progress
│   └── settings.py             # GET/POST /api/settings
│
├── services/                   # Business Logic & Infrastructure Layer
│   ├── __init__.py
│   ├── ai_service.py           # Gemini SDK interface, retry handling & fallbacks
│   ├── quiz_service.py         # Quiz generation, answer masking & evaluation
│   ├── summary_service.py      # Note synthesis & glossary extraction
│   ├── learning_service.py     # 5-stage curriculum generation
│   ├── storage_service.py      # SQLite operations, history & analytics
│   └── validation_service.py   # Input sanitation, JSON extraction & repair
│
├── models/                     # Pydantic Schemas & DTOs
│   ├── __init__.py
│   ├── schemas.py              # General API models & response wrappers
│   └── quiz_models.py          # Quiz options, questions, sessions, submissions
│
├── prompts/                    # Specialized System & User AI Prompts
│   ├── __init__.py
│   ├── qa_prompts.py
│   ├── explain_prompts.py
│   ├── quiz_prompts.py
│   ├── summary_prompts.py
│   └── learning_prompts.py
│
├── templates/                  # Server-Rendered Templates
│   └── index.html              # Main application single-page interface
│
├── static/                     # Frontend Assets
│   ├── css/
│   │   └── style.css           # Premium EdTech design system & dark mode
│   └── js/
│       └── app.js              # Client state, event orchestration, API client
│
└── tests/                      # Automated Test Suite
    ├── __init__.py
    ├── test_qa.py
    ├── test_explain.py
    ├── test_quiz.py
    ├── test_summary.py
    ├── test_learning.py
    ├── test_history.py
    └── test_frontend.py
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your machine.
- `pip` package manager.

### Step 1: Clone or Navigate to Project
```bash
cd EduGenie
```

### Step 2: Create and Activate Virtual Environment (Recommended)
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

---

## 6. Environment Variables

Create your `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your preferred configuration:
```ini
# Google Gemini API Key (Get free key from https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# Model Selection
GEMINI_MODEL=gemini-2.5-flash

# Application Configuration
APP_NAME=EduGenie
APP_ENV=development
DEBUG=True
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///./edugenie.db
```

> **Note**: If `GEMINI_API_KEY` is not provided initially, EduGenie will seamlessly run in **Demonstration Mode** using its built-in academic engine. You can also input or change your API key directly inside the running application via the **Settings** menu at any time!

---

## 7. Running the Application

Start the local server using `uvicorn`:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open your web browser and navigate to:
```text
http://127.0.0.1:8000
```

---

## 8. API Endpoints

All responses conform to a unified envelope:
```json
{
  "success": true,
  "data": {},
  "message": "Request completed successfully",
  "error_code": null
}
```

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the single-page application dashboard |
| `GET` | `/api/health` | Health check endpoint and Gemini connectivity state |
| `POST` | `/api/qa` | Submits student question; returns answer, simple explanation, key points, example |
| `POST` | `/api/explain` | Concept explanation by difficulty and pedagogical style |
| `POST` | `/api/quiz` | Generates verified MCQs with server-masked answers |
| `POST` | `/api/quiz/evaluate` | Evaluates submitted answers and returns score, accuracy %, and explanations |
| `POST` | `/api/summarize` | Summarizes notes; returns summary, terms, and revision checklist |
| `POST` | `/api/learn/recommendations` | Builds 5-stage personalized learning roadmap |
| `GET` | `/api/history` | Retrieves stored activity history (filterable by type and search) |
| `GET` | `/api/history/{id}` | Retrieves full payload for a single historical activity |
| `DELETE` | `/api/history/{id}` | Deletes a single historical activity |
| `DELETE` | `/api/history` | Clears all activity records |
| `GET` | `/api/progress` | Computes live analytics, question counts, quiz accuracy, and weekly chart |
| `GET` | `/api/settings` | Returns system status and current AI model configuration |
| `POST` | `/api/settings` | Updates Gemini API key or model and reloads runtime client |

---

## 9. Automated Testing

EduGenie includes 18 automated tests covering valid/invalid inputs, edge cases, session evaluation, database metrics, and asset delivery.

Run tests using `pytest`:
```bash
pytest -v
```

Output:
```text
============================= test session starts =============================
collected 18 items

tests/test_explain.py::test_explain_concept_success PASSED               [  5%]
tests/test_explain.py::test_explain_concept_empty_fails PASSED           [ 11%]
tests/test_explain.py::test_explain_concept_fallback_difficulty PASSED   [ 16%]
tests/test_frontend.py::test_index_page_delivery PASSED                  [ 22%]
tests/test_frontend.py::test_static_css_delivery PASSED                  [ 27%]
tests/test_frontend.py::test_static_js_delivery PASSED                   [ 33%]
tests/test_frontend.py::test_api_health PASSED                           [ 38%]
tests/test_history.py::test_history_and_progress_integration PASSED      [ 44%]
tests/test_learning.py::test_generate_learning_path_success PASSED       [ 50%]
tests/test_learning.py::test_generate_learning_path_empty_topic PASSED   [ 55%]
tests/test_qa.py::test_ask_question_success PASSED                       [ 61%]
tests/test_qa.py::test_ask_question_empty_fails PASSED                   [ 66%]
tests/test_qa.py::test_ask_question_too_short PASSED                     [ 72%]
tests/test_quiz.py::test_generate_and_evaluate_quiz PASSED               [ 77%]
tests/test_quiz.py::test_generate_quiz_empty_topic PASSED                [ 83%]
tests/test_quiz.py::test_evaluate_nonexistent_quiz PASSED                [ 88%]
tests/test_summary.py::test_summarize_content_success PASSED             [ 94%]
tests/test_summary.py::test_summarize_too_short PASSED                   [100%]

============================= 18 passed in 1.25s ==============================
```

---

## 10. Project Demonstration Guide

EduGenie is tailored for academic evaluation and live project reviews. Follow this demonstration flow:

1. **Dashboard Overview**: Show the clean hero section, quick action cards, zero-state metrics, and real-time connection status pill.
2. **Q&A Demo**: Click **Ask Question**, click the demo chip `"What is Artificial Intelligence?"`, and submit. Highlight the structured sections: Answer, Simple Explanation, Key Points, Example, and copy to clipboard.
3. **Concept Explanation Demo**: Click **Explain Concept**, type `"Neural Networks"`, select **Intermediate** and **Step-by-Step**. Review the 5-stage conceptual breakdown.
4. **Interactive Quiz Demo**:
   - Go to **Quiz Generator**, enter `"Machine Learning"`, select 5 questions.
   - Answer the interactive MCQs using the selectable buttons.
   - Observe the progress bar and dot indicators.
   - Click **Submit Quiz**.
   - Review the Score Circle, Accuracy %, and pedagogical explanations.
5. **Summarization Demo**: Go to **Summarize Notes**, click `"Load OS Notes Sample"`, choose **Medium**, and click **Summarize Material**. Show the generated summary, glossary terms, and export to TXT.
6. **Learning Roadmap Demo**: Go to **Learning Path**, select `"Python for AI/ML"`, and click **Generate Roadmap**. Walk through the 5 sequential stages.
7. **Real Analytics & History Verification**:
   - Click **Activity History** to show all actions recorded in real-time.
   - Click **Progress & Analytics** to show live KPI counts and the real 7-day weekly activity bar chart reflecting your actions!
8. **Theme Toggle**: Switch between **Light**, **Dark**, and **System** themes from the sidebar or header.

---

## 11. Security & Reliability Principles

- **No Hardcoded Fake Output**: Every UI feature connects to real backend routes.
- **Key Safety**: The API key is stored securely in `.env` on the server and is never sent to the browser DOM or JavaScript bundle.
- **Graceful Error Recovery**: Unhandled exceptions are intercepted by FastAPI exception handlers, providing user-friendly notifications rather than raw stack traces.
- **Defensive Anti-Cheating**: Quizzes store answer keys on the server side; answers are validated via `/api/quiz/evaluate`.
- **Concurrency & Concurrency Control**: SQLite uses Write-Ahead Logging (WAL) to prevent lock contention during concurrent student reads and writes.

---

## 12. Future Enhancements

While EduGenie is production-ready for its core requirements, its modular architecture makes it easy to add:
- Multimodal doubt solving (uploading textbook diagrams and handwritten math).
- Speech synthesis for audio lectures and voice doubt asking.
- Flashcard decks with Spaced Repetition (SM-2 algorithm).
- Collaborative study groups and peer quiz challenges.
- LMS Integration (Canvas / Google Classroom / Blackboard LTI).

---

## 13. Team / Academic Information

- **Project**: EduGenie — AI-Powered Personalized Learning Assistant
- **Framework**: FastAPI (Python 3.10+) & Vanilla Web Standards
- **AI Core**: Google Gemini (`google-genai`)
- **Evaluation Status**: Fully verified with 18 unit and integration tests passing.
