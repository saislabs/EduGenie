"""Domain service for Personalized Learning Path generation."""

from typing import Any, Dict, List
from models.schemas import LearningPathRequest, LearningPathResponseData, LearningStage
from prompts.learning_prompts import LEARNING_SYSTEM_PROMPT, LEARNING_USER_PROMPT_TEMPLATE
from services.ai_service import ai_service
from services.storage_service import storage
from services.validation_service import validation_service


class LearningService:
    def generate_learning_path(self, req: LearningPathRequest) -> LearningPathResponseData:
        sanitized_topic = validation_service.sanitize_text(req.topic, max_length=200)
        sanitized_goal = validation_service.sanitize_text(req.goal, max_length=300)

        user_prompt = LEARNING_USER_PROMPT_TEMPLATE.format(
            topic=sanitized_topic,
            current_level=req.current_level,
            available_time=req.available_time,
            goal=sanitized_goal,
        )

        raw_result = ai_service.generate_json_response(
            system_prompt=LEARNING_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.35,
        )

        overview = str(raw_result.get("overview") or f"A personalized curriculum to master {sanitized_topic}.").strip()
        stages_raw = raw_result.get("stages") or []
        stages: List[LearningStage] = []

        if isinstance(stages_raw, list):
            for idx, stg in enumerate(stages_raw, start=1):
                if not isinstance(stg, dict):
                    continue
                level_num = int(stg.get("level_number", idx))
                level_title = str(stg.get("level_title") or f"Level {level_num}: Concepts").strip()
                estimated_time = str(stg.get("estimated_time") or "2 weeks").strip()
                topics = [str(t).strip() for t in stg.get("topics", []) if str(t).strip()]
                sequence_guide = str(stg.get("sequence_guide") or "Follow in sequential order.").strip()
                practice_suggestions = [str(p).strip() for p in stg.get("practice_suggestions", []) if str(p).strip()]
                recommended_resources = [str(r).strip() for r in stg.get("recommended_resources", []) if str(r).strip()]

                stages.append(
                    LearningStage(
                        level_number=level_num,
                        level_title=level_title,
                        estimated_time=estimated_time,
                        topics=topics,
                        sequence_guide=sequence_guide,
                        practice_suggestions=practice_suggestions,
                        recommended_resources=recommended_resources,
                    )
                )

        model_used = raw_result.get("_model_used", "gemini")

        response_data = LearningPathResponseData(
            topic=sanitized_topic,
            current_level=req.current_level,
            available_time=req.available_time,
            goal=sanitized_goal,
            stages=stages,
            overview=overview,
            model_used=model_used,
        )

        # Record activity into database for history & progress
        storage.record_activity(
            activity_type="learning_path",
            title=f"Roadmap: {sanitized_topic}",
            subtitle=f"{req.current_level.capitalize()} • {len(stages)} Stages • {req.available_time}",
            payload=response_data.model_dump(),
        )

        return response_data


learning_service = LearningService()
