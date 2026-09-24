from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuizOption(BaseModel):
    key: str = Field(..., description="Option key: A, B, C, or D")
    text: str = Field(..., description="Option description")


class QuizQuestionClient(BaseModel):
    """Question sent to client (without revealing correct answer prematurely)."""
    id: int
    question: str
    options: List[QuizOption]


class QuizQuestionFull(BaseModel):
    """Full question with correct answer and explanation for backend evaluation."""
    id: int
    question: str
    options: List[QuizOption]
    correct_answer: str = Field(..., description="A, B, C, or D")
    explanation: str = Field(..., description="Why this answer is correct")


class QuizGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, description="Quiz subject or topic")
    passage: Optional[str] = Field(None, max_length=15000, description="Optional reading passage to base quiz on")
    num_questions: int = Field(5, ge=1, le=15, description="Number of questions (1-15)")
    difficulty: str = Field("intermediate", description="beginner, intermediate, or advanced")

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Please provide a topic for the quiz.")
        return v

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        allowed = {"beginner", "intermediate", "advanced"}
        v = v.strip().lower()
        if v not in allowed:
            return "intermediate"
        return v


class QuizSessionData(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    quiz_id: str
    topic: str
    difficulty: str
    total_questions: int
    questions: List[QuizQuestionClient]
    model_used: str = "gemini"
    created_at: Optional[str] = None


class QuizAnswerSubmission(BaseModel):
    question_id: int
    selected_option: str  # "A", "B", "C", "D"


class QuizEvaluationRequest(BaseModel):
    quiz_id: str
    user_answers: Dict[int, str] = Field(..., description="Map of question_id -> selected_option")


class QuestionResultDetail(BaseModel):
    question_id: int
    question: str
    options: List[QuizOption]
    user_answer: Optional[str]
    correct_answer: str
    is_correct: bool
    explanation: str


class QuizEvaluationResult(BaseModel):
    quiz_id: str
    topic: str
    difficulty: str
    total_questions: int
    correct_count: int
    incorrect_count: int
    score_percentage: float
    passed: bool
    results: List[QuestionResultDetail]
    feedback: str
