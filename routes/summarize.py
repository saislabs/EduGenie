"""Summarization Router for EduGenie."""

import logging
from fastapi import APIRouter, HTTPException
from models.schemas import APIResponse, SummaryRequest, SummaryResponseData
from services.summary_service import summary_service

router = APIRouter(tags=["Summarize"])
logger = logging.getLogger("edugenie.routes.summarize")


@router.post("/api/summarize", response_model=APIResponse[SummaryResponseData])
@router.post("/summarize", response_model=APIResponse[SummaryResponseData])
async def summarize_content(request: SummaryRequest):
    try:
        data = summary_service.summarize(request)
        return APIResponse[SummaryResponseData](
            success=True,
            data=data,
            message="Content summarized successfully",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error summarizing content: {e}", exc_info=True)
        return APIResponse[SummaryResponseData](
            success=False,
            data=None,
            message="The AI service was unable to summarize the provided content. Please check input and try again.",
        )
