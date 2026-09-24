"""Settings and System Health Router for EduGenie."""

import logging
import os
from pathlib import Path
from fastapi import APIRouter
from config import settings, ENV_PATH
from models.schemas import APIResponse, SettingsStatusResponse, SettingsUpdateRequest
from services.ai_service import ai_service

router = APIRouter(prefix="/api/settings", tags=["Settings"])
logger = logging.getLogger("edugenie.routes.settings")


@router.get("", response_model=APIResponse[SettingsStatusResponse])
async def get_settings_status():
    status = SettingsStatusResponse(
        app_name=settings.APP_NAME,
        is_gemini_configured=settings.is_gemini_configured(),
        current_model=settings.GEMINI_MODEL,
        environment=settings.APP_ENV,
        database_status="Connected (SQLite WAL Mode)",
    )
    return APIResponse[SettingsStatusResponse](
        success=True,
        data=status,
        message="System status retrieved successfully",
    )


@router.post("", response_model=APIResponse[SettingsStatusResponse])
async def update_settings(update: SettingsUpdateRequest):
    env_path = ENV_PATH
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    updated_key = False
    updated_model = False
    new_lines = []

    for line in lines:
        if line.startswith("GEMINI_API_KEY=") and update.gemini_api_key is not None:
            new_lines.append(f"GEMINI_API_KEY={update.gemini_api_key.strip()}\n")
            updated_key = True
        elif line.startswith("GEMINI_MODEL=") and update.gemini_model is not None:
            new_lines.append(f"GEMINI_MODEL={update.gemini_model.strip()}\n")
            updated_model = True
        else:
            new_lines.append(line)

    if not updated_key and update.gemini_api_key is not None:
        new_lines.append(f"GEMINI_API_KEY={update.gemini_api_key.strip()}\n")
    if not updated_model and update.gemini_model is not None:
        new_lines.append(f"GEMINI_MODEL={update.gemini_model.strip()}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    # Immediately update runtime environment
    if update.gemini_api_key is not None and update.gemini_api_key.strip():
        os.environ["GEMINI_API_KEY"] = update.gemini_api_key.strip()
    if update.gemini_model is not None and update.gemini_model.strip():
        os.environ["GEMINI_MODEL"] = update.gemini_model.strip()

    # Refresh runtime settings and client
    ai_service.refresh_client()

    status = SettingsStatusResponse(
        app_name=settings.APP_NAME,
        is_gemini_configured=settings.is_gemini_configured(),
        current_model=settings.GEMINI_MODEL,
        environment=settings.APP_ENV,
        database_status="Connected (SQLite WAL Mode)",
    )

    return APIResponse[SettingsStatusResponse](
        success=True,
        data=status,
        message="Settings updated and AI client reloaded successfully",
    )
