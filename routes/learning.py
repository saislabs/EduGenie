"""Personalized Learning Path Router for EduGenie."""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import APIResponse, LearningPathRequest, LearningPathResponseData
from services.learning_service import learning_service

router = APIRouter(tags=["Learning Path"])
logger = logging.getLogger("edugenie.routes.learning")


@router.post("/api/learn/recommendations", response_model=APIResponse[LearningPathResponseData])
@router.post("/learn/recommendations", response_model=APIResponse[LearningPathResponseData])
async def generate_learning_recommendations(request: LearningPathRequest):
    try:
        data = learning_service.generate_learning_path(request)
        return APIResponse[LearningPathResponseData](
            success=True,
            data=data,
            message="Personalized learning roadmap generated successfully",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating learning path: {e}", exc_info=True)
        return APIResponse[LearningPathResponseData](
            success=False,
            data=None,
            message="The AI service was unable to build a learning roadmap for this topic. Please try again.",
        )
