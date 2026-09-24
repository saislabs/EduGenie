"""Quiz Router for EduGenie."""

import logging
from fastapi import APIRouter, HTTPException
from models.quiz_models import (
    QuizEvaluationRequest,
    QuizEvaluationResult,
    QuizGenerateRequest,
    QuizSessionData,
)
from models.schemas import APIResponse
from services.quiz_service import quiz_service

router = APIRouter(tags=["Quiz"])
logger = logging.getLogger("edugenie.routes.quiz")


@router.post("/api/quiz", response_model=APIResponse[QuizSessionData])
@router.post("/quiz", response_model=APIResponse[QuizSessionData])
async def generate_quiz(request: QuizGenerateRequest):
    try:
        session_data = quiz_service.generate_quiz(request)
        return APIResponse[QuizSessionData](
            success=True,
            data=session_data,
            message="Quiz generated successfully",
        )
    except Exception as e:
        logger.error(f"Error generating quiz: {e}", exc_info=True)
        return APIResponse[QuizSessionData](
            success=False,
            data=None,
            message="The AI service was unable to generate a quiz for this topic. Please try again.",
        )


@router.post("/api/quiz/evaluate", response_model=APIResponse[QuizEvaluationResult])
@router.post("/quiz/evaluate", response_model=APIResponse[QuizEvaluationResult])
async def evaluate_quiz(request: QuizEvaluationRequest):
    try:
        result = quiz_service.evaluate_quiz(
            quiz_id=request.quiz_id,
            user_answers=request.user_answers,
        )
        return APIResponse[QuizEvaluationResult](
            success=True,
            data=result,
            message="Quiz evaluated successfully",
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error evaluating quiz: {e}", exc_info=True)
        return APIResponse[QuizEvaluationResult](
            success=False,
            data=None,
            message="Unable to evaluate quiz session. Please generate a new quiz.",
        )
