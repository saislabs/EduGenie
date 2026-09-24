"""Domain service for Content Summarization."""

from typing import Any, Dict
from models.schemas import ImportantTerm, SummaryRequest, SummaryResponseData
from prompts.summary_prompts import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT_TEMPLATE
from services.ai_service import ai_service
from services.storage_service import storage
from services.validation_service import validation_service


class SummaryService:
    def summarize(self, req: SummaryRequest) -> SummaryResponseData:
        sanitized_content = validation_service.sanitize_text(req.content, max_length=25000)
        
        user_prompt = SUMMARY_USER_PROMPT_TEMPLATE.format(
            length=req.length,
            content=sanitized_content,
        )

        raw_result = ai_service.generate_json_response(
            system_prompt=SUMMARY_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
        )

        summary_text = str(raw_result.get("summary") or "").strip()
        if not summary_text:
            summary_text = "Summary could not be generated from the given text."

        key_points = [str(kp).strip() for kp in raw_result.get("key_points", []) if str(kp).strip()]
        
        terms_raw = raw_result.get("important_terms", [])
        important_terms = []
        if isinstance(terms_raw, list):
            for item in terms_raw:
                if isinstance(item, dict):
                    t = str(item.get("term") or "").strip()
                    d = str(item.get("definition") or "").strip()
                    if t and d:
                        important_terms.append(ImportantTerm(term=t, definition=d))

        quick_revision = [str(qr).strip() for qr in raw_result.get("quick_revision", []) if str(qr).strip()]
        model_used = raw_result.get("_model_used", "gemini")

        response_data = SummaryResponseData(
            original_length_chars=len(sanitized_content),
            summary_length_type=req.length,
            summary=summary_text,
            key_points=key_points,
            important_terms=important_terms,
            quick_revision=quick_revision,
            model_used=model_used,
        )

        # Record activity into database for history and progress
        preview_title = sanitized_content[:80].replace("\n", " ").strip() + "..."
        storage.record_activity(
            activity_type="summary",
            title=f"Summary: {preview_title}",
            subtitle=f"{req.length.capitalize()} length • {len(key_points)} key points",
            payload=response_data.model_dump(),
        )

        return response_data


summary_service = SummaryService()
