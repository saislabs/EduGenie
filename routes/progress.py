"""Progress & Analytics Router for EduGenie."""

import logging
from fastapi import APIRouter
from models.schemas import APIResponse, ProgressMetricsResponse
from services.storage_service import storage

router = APIRouter(prefix="/api/progress", tags=["Progress & Analytics"])
logger = logging.getLogger("edugenie.routes.progress")


@router.get("", response_model=APIResponse[ProgressMetricsResponse])
async def get_progress():
    try:
        metrics_dict = storage.get_progress_metrics()
        progress_data = ProgressMetricsResponse(**metrics_dict)
        return APIResponse[ProgressMetricsResponse](
            success=True,
            data=progress_data,
            message="Progress metrics retrieved successfully",
        )
    except Exception as e:
        logger.error(f"Error computing progress metrics: {e}", exc_info=True)
        return APIResponse[ProgressMetricsResponse](
            success=False,
            data=None,
            message="Failed to compute learning progress metrics.",
        )
