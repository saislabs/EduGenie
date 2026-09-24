"""Validation, sanitization, and JSON recovery service for EduGenie."""

import json
import re
from typing import Any, Dict, List, Optional


class ValidationService:
    @staticmethod
    def sanitize_text(text: str, max_length: int = 25000) -> str:
        """Sanitizes user input text by trimming, stripping control chars, and enforcing max length."""
        if not text:
            return ""
        # Remove zero-width spaces and control characters except common whitespace
        sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
        sanitized = sanitized.strip()
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        return sanitized

    @staticmethod
    def extract_and_repair_json(raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Extracts, cleans, repairs, and parses JSON from AI responses.
        Handles markdown blocks (```json ... ```), trailing commas, and boundary issues.
        """
        if not raw_text or not raw_text.strip():
            return None

        cleaned = raw_text.strip()

        # Step 1: Remove markdown code block fences if present
        if "```" in cleaned:
            # Match ```json ... ``` or just ``` ... ```
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
            if match:
                cleaned = match.group(1).strip()
            else:
                cleaned = re.sub(r"^```[a-zA-Z]*", "", cleaned).strip()
                cleaned = re.sub(r"```$", "", cleaned).strip()

        # Step 2: Attempt standard JSON parse
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, (dict, list)):
                return parsed if isinstance(parsed, dict) else {"items": parsed}
        except Exception:
            pass

        # Step 3: Locate outer JSON object '{ ... }'
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            candidate = cleaned[start_idx : end_idx + 1]

            # Attempt direct parse on candidate
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

            # Step 4: Repair common JSON flaws (trailing commas, unescaped newlines in strings)
            # Remove trailing commas before closing braces/brackets
            repaired = re.sub(r",\s*([\}\]])", r"\1", candidate)

            try:
                parsed = json.loads(repaired)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        # Step 5: Check if root is a JSON array '[ ... ]'
        start_arr = cleaned.find("[")
        end_arr = cleaned.rfind("]")
        if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
            arr_candidate = cleaned[start_arr : end_arr + 1]
            arr_repaired = re.sub(r",\s*([\}\]])", r"\1", arr_candidate)
            try:
                parsed = json.loads(arr_repaired)
                if isinstance(parsed, list):
                    return {"items": parsed}
            except Exception:
                pass

        return None

    @staticmethod
    def validate_quiz_structure(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validates that quiz questions conform to the required MCQ schema:
        id, question, options (list of 4 dicts with key and text), correct_answer, explanation.
        Discards or repairs non-conforming items.
        """
        questions_raw = data.get("questions") or data.get("items") or []
        if not isinstance(questions_raw, list):
            return []

        validated_questions = []
        for idx, q in enumerate(questions_raw, start=1):
            if not isinstance(q, dict):
                continue

            q_text = str(q.get("question") or "").strip()
            if not q_text:
                continue

            # Process options
            raw_options = q.get("options")
            options = []
            if isinstance(raw_options, list):
                for opt_idx, opt in enumerate(raw_options):
                    key = ["A", "B", "C", "D"][opt_idx] if opt_idx < 4 else chr(65 + opt_idx)
                    if isinstance(opt, dict):
                        opt_key = str(opt.get("key", key)).upper().strip()
                        opt_text = str(opt.get("text") or opt.get("option") or "").strip()
                    elif isinstance(opt, str):
                        opt_key = key
                        opt_text = opt.strip()
                    else:
                        continue
                    if opt_text:
                        options.append({"key": opt_key, "text": opt_text})
            elif isinstance(raw_options, dict):
                for k, v in raw_options.items():
                    options.append({"key": str(k).upper().strip(), "text": str(v).strip()})

            if len(options) < 2:
                continue

            # Ensure options have standard A, B, C, D keys
            for i, opt in enumerate(options[:4]):
                opt["key"] = ["A", "B", "C", "D"][i]

            correct_ans = str(q.get("correct_answer") or "A").upper().strip()
            if correct_ans not in ["A", "B", "C", "D"]:
                correct_ans = "A"

            explanation = str(q.get("explanation") or f"The correct option is {correct_ans}.").strip()

            validated_questions.append({
                "id": idx,
                "question": q_text,
                "options": options[:4],
                "correct_answer": correct_ans,
                "explanation": explanation,
            })

        return validated_questions


validation_service = ValidationService()
