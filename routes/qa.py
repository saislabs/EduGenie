"""Q&A Router for EduGenie."""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import APIResponse, QARequest, QAResponseData
from prompts.qa_prompts import QA_SYSTEM_PROMPT, QA_USER_PROMPT_TEMPLATE
from services.ai_service import ai_service
from services.storage_service import storage
from services.validation_service import validation_service

router = APIRouter(tags=["Q&A"])
logger = logging.getLogger("edugenie.routes.qa")


@router.post("/api/qa", response_model=APIResponse[QAResponseData])
@router.post("/qa", response_model=APIResponse[QAResponseData])
async def ask_question(request: QARequest):
    try:
        sanitized_q = validation_service.sanitize_text(request.question, max_length=3000)
        if not sanitized_q:
            raise HTTPException(status_code=400, detail="Please enter a question before continuing.")

        context_clause = f"Subject / Context: {request.context.strip()}" if request.context and request.context.strip() else ""
        follow_up_clause = f"Previous context: {request.follow_up_to.strip()}" if request.follow_up_to and request.follow_up_to.strip() else ""

        user_prompt = QA_USER_PROMPT_TEMPLATE.format(
            question=sanitized_q,
            context_clause=context_clause,
            follow_up_clause=follow_up_clause,
        )

        result = ai_service.generate_json_response(
            system_prompt=QA_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.35,
        )

        answer = str(result.get("answer") or result.get("response") or "I could not formulate an answer for this question.").strip()
        simple_explanation = str(result.get("simple_explanation") or result.get("simpleExplanation") or answer).strip()
        
        raw_kp = (
            result.get("key_points")
            or result.get("keyPoints")
            or result.get("key_takeaways")
            or result.get("takeaways")
            or []
        )
        if isinstance(raw_kp, list):
            key_points = [str(p).strip() for p in raw_kp if str(p).strip()]
        elif isinstance(raw_kp, str):
            key_points = [p.strip() for p in raw_kp.split("\n") if p.strip()]
        else:
            key_points = []

        if not key_points:
            key_points = [
                f"Fundamental concepts and key terminology related to {sanitized_q[:80]}.",
                "Core operational principles and analytical framework.",
                "Practical applications, trade-offs, and best practices.",
            ]

        example = str(result.get("example") or "").strip() or None
        model_used = result.get("_model_used", "gemini")

        qa_data = QAResponseData(
            question=sanitized_q,
            answer=answer,
            simple_explanation=simple_explanation,
            key_points=key_points,
            example=example,
            model_used=model_used,
        )

        # Store in activities
        storage.record_activity(
            activity_type="qa",
            title=sanitized_q[:120],
            subtitle=f"{len(key_points)} key points • {simple_explanation[:60]}...",
            payload=qa_data.model_dump(),
        )

        return APIResponse[QAResponseData](
            success=True,
            data=qa_data,
            message="Question answered successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error answering question: {e}", exc_info=True)
        return APIResponse[QAResponseData](
            success=False,
            data=None,
            message="The AI service encountered an issue processing your question. Please try again.",
        )
