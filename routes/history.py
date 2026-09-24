"""History Router for EduGenie."""

import logging
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from models.schemas import APIResponse
from services.storage_service import storage

router = APIRouter(prefix="/api/history", tags=["History"])
logger = logging.getLogger("edugenie.routes.history")


@router.get("", response_model=APIResponse[List[dict]])
async def get_history(
    activity_type: Optional[str] = Query(None, description="all, qa, explain, quiz, summary, learning_path"),
    search: Optional[str] = Query(None, description="Search term for title or subtitle"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    try:
        activities = storage.get_activities(
            activity_type=activity_type,
            search_query=search,
            limit=limit,
            offset=offset,
        )
        return APIResponse[List[dict]](
            success=True,
            data=activities,
            message="History retrieved successfully",
        )
    except Exception as e:
        logger.error(f"Error fetching history: {e}", exc_info=True)
        return APIResponse[List[dict]](
            success=False,
            data=[],
            message="Failed to fetch history.",
        )


@router.get("/{activity_id}", response_model=APIResponse[dict])
async def get_history_item(activity_id: str):
    item = storage.get_activity_by_id(activity_id)
    if not item:
        raise HTTPException(status_code=404, detail="Activity item not found.")
    return APIResponse[dict](
        success=True,
        data=item,
        message="Activity retrieved successfully",
    )


@router.delete("/{activity_id}", response_model=APIResponse[bool])
async def delete_history_item(activity_id: str):
    deleted = storage.delete_activity(activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Activity item not found or already deleted.")
    return APIResponse[bool](
        success=True,
        data=True,
        message="Activity deleted successfully",
    )


@router.delete("", response_model=APIResponse[int])
async def clear_all_history():
    count = storage.clear_all_activities()
    return APIResponse[int](
        success=True,
        data=count,
        message=f"Cleared {count} history records successfully",
    )
