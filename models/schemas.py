from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field, field_validator

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper across all endpoints."""
    model_config = ConfigDict(protected_namespaces=())
    success: bool
    data: Optional[T] = None
    message: str = "Request completed successfully"
    error_code: Optional[str] = None


# ==========================================
# Q&A SCHEMAS
# ==========================================
class QARequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=3000, description="The user's educational question")
    context: Optional[str] = Field(None, max_length=2000, description="Optional educational context or subject")
    follow_up_to: Optional[str] = Field(None, max_length=500, description="Context from previous question if follow-up")

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Please enter a question before continuing.")
        return v


class QAResponseData(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    question: str
    answer: str
    simple_explanation: str
    key_points: List[str] = Field(default_factory=list)
    example: Optional[str] = None
    model_used: str = "gemini"
    created_at: Optional[str] = None


# ==========================================
# EXPLAIN CONCEPT SCHEMAS
# ==========================================
class ExplainRequest(BaseModel):
    concept: str = Field(..., min_length=2, max_length=300, description="The concept or topic to explain")
    difficulty: str = Field("intermediate", description="beginner, intermediate, or advanced")
    style: str = Field("simple", description="simple, step_by_step, with_example, or exam_prep")

    @field_validator("concept")
    @classmethod
    def validate_concept(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Please enter a concept to explain.")
        return v

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        allowed = {"beginner", "intermediate", "advanced"}
        v = v.strip().lower()
        if v not in allowed:
            return "intermediate"
        return v

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str) -> str:
        allowed = {"simple", "step_by_step", "with_example", "exam_prep"}
        v = v.strip().lower()
        if v not in allowed:
            return "simple"
        return v


class ExplainResponseData(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    concept: str
    difficulty: str
    style: str
    simple_explanation: str
    how_it_works: str
    example: str
    key_points: List[str] = Field(default_factory=list)
    exam_tips: Optional[str] = None
    model_used: str = "gemini"
    created_at: Optional[str] = None


# ==========================================
# SUMMARIZATION SCHEMAS
# ==========================================
class SummaryRequest(BaseModel):
    content: str = Field(..., min_length=20, max_length=30000, description="The study material, notes, or article text")
    length: str = Field("medium", description="short, medium, or detailed")

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Input is too short. Please provide at least a few sentences to summarize.")
        return v

    @field_validator("length")
    @classmethod
    def validate_length(cls, v: str) -> str:
        allowed = {"short", "medium", "detailed"}
        v = v.strip().lower()
        if v not in allowed:
            return "medium"
        return v


class ImportantTerm(BaseModel):
    term: str
    definition: str


class SummaryResponseData(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    original_length_chars: int
    summary_length_type: str
    summary: str
    key_points: List[str] = Field(default_factory=list)
    important_terms: List[ImportantTerm] = Field(default_factory=list)
    quick_revision: List[str] = Field(default_factory=list)
    model_used: str = "gemini"
    created_at: Optional[str] = None


# ==========================================
# LEARNING PATH / ROADMAP SCHEMAS
# ==========================================
class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, description="The subject or skill to learn")
    current_level: str = Field("beginner", description="beginner, intermediate, or advanced")
    available_time: str = Field("1 hour/day", max_length=100, description="e.g. 1 hour/day, 5 hours/week")
    goal: str = Field("Master the fundamentals", max_length=300, description="e.g. Become interview-ready, Build a project")

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Please provide a topic for your learning path.")
        return v

    @field_validator("current_level")
    @classmethod
    def validate_current_level(cls, v: str) -> str:
        allowed = {"beginner", "intermediate", "advanced"}
        v = v.strip().lower()
        if v not in allowed:
            return "beginner"
        return v


class LearningStage(BaseModel):
    level_number: int
    level_title: str
    estimated_time: str
    topics: List[str] = Field(default_factory=list)
    sequence_guide: str
    practice_suggestions: List[str] = Field(default_factory=list)
    recommended_resources: List[str] = Field(default_factory=list)


class LearningPathResponseData(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    topic: str
    current_level: str
    available_time: str
    goal: str
    stages: List[LearningStage] = Field(default_factory=list)
    overview: str
    model_used: str = "gemini"
    created_at: Optional[str] = None


# ==========================================
# SETTINGS & PROGRESS SCHEMAS
# ==========================================
class SettingsUpdateRequest(BaseModel):
    gemini_api_key: Optional[str] = Field(None, description="Google Gemini API key")
    gemini_model: Optional[str] = Field("gemini-3.5-flash", description="Model identifier")


class SettingsStatusResponse(BaseModel):
    app_name: str
    is_gemini_configured: bool
    current_model: str
    environment: str
    database_status: str


class ProgressMetricsResponse(BaseModel):
    total_activities: int
    questions_asked: int
    concepts_explained: int
    quizzes_completed: int
    average_quiz_accuracy: float
    summaries_generated: int
    learning_paths_created: int
    weekly_activity: List[dict] = Field(default_factory=list)
    recent_activities: List[dict] = Field(default_factory=list)
