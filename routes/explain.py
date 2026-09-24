"""Concept Explanation Router for EduGenie."""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import APIResponse, ExplainRequest, ExplainResponseData
from prompts.explain_prompts import EXPLAIN_SYSTEM_PROMPT, EXPLAIN_USER_PROMPT_TEMPLATE
from services.ai_service import ai_service
from services.storage_service import storage
from services.validation_service import validation_service

router = APIRouter(tags=["Concept Explanation"])
logger = logging.getLogger("edugenie.routes.explain")


@router.post("/api/explain", response_model=APIResponse[ExplainResponseData])
@router.post("/explain", response_model=APIResponse[ExplainResponseData])
async def explain_concept(request: ExplainRequest):
    try:
        sanitized_c = validation_service.sanitize_text(request.concept, max_length=300)
        if not sanitized_c:
            raise HTTPException(status_code=400, detail="Please enter a concept to explain.")

        user_prompt = EXPLAIN_USER_PROMPT_TEMPLATE.format(
            concept=sanitized_c,
            difficulty=request.difficulty,
            style=request.style,
        )

        result = ai_service.generate_json_response(
            system_prompt=EXPLAIN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.35,
        )

        concept_title = str(result.get("concept") or sanitized_c).strip()
        simple_explanation = str(result.get("simple_explanation") or f"{sanitized_c} explained simply.").strip()
        how_it_works = str(result.get("how_it_works") or "Explanation details are being formatted.").strip()
        example = str(result.get("example") or "Example illustration.").strip()
        key_points = [str(p).strip() for p in result.get("key_points", []) if str(p).strip()]
        exam_tips = str(result.get("exam_tips") or "").strip() or None
        model_used = result.get("_model_used", "gemini")

        explain_data = ExplainResponseData(
            concept=concept_title,
            difficulty=request.difficulty,
            style=request.style,
            simple_explanation=simple_explanation,
            how_it_works=how_it_works,
            example=example,
            key_points=key_points,
            exam_tips=exam_tips,
            model_used=model_used,
        )

        # Store in activities
        storage.record_activity(
            activity_type="explain",
            title=f"Concept: {concept_title}",
            subtitle=f"{request.difficulty.capitalize()} level • {request.style.replace('_', ' ').capitalize()} style",
            payload=explain_data.model_dump(),
        )

        return APIResponse[ExplainResponseData](
            success=True,
            data=explain_data,
            message="Concept explained successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error explaining concept: {e}", exc_info=True)
        return APIResponse[ExplainResponseData](
            success=False,
            data=None,
            message="The AI service was unable to explain this concept at the moment. Please try again.",
        )
