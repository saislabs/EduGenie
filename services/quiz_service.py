"""Domain service for Quiz generation, session management, and evaluation."""

import uuid
from typing import Any, Dict, List, Optional
from models.quiz_models import (
    QuestionResultDetail,
    QuizEvaluationResult,
    QuizGenerateRequest,
    QuizOption,
    QuizQuestionClient,
    QuizSessionData,
)
from prompts.quiz_prompts import QUIZ_SYSTEM_PROMPT, QUIZ_USER_PROMPT_TEMPLATE
from services.ai_service import ai_service
from services.storage_service import storage
from services.validation_service import validation_service


class QuizService:
    def generate_quiz(self, req: QuizGenerateRequest) -> QuizSessionData:
        """Generates a structured quiz from Gemini, caches answers in DB, and returns client questions."""
        passage_clause = f"\nReference Passage:\n\"\"\"\n{req.passage.strip()}\n\"\"\"" if req.passage and req.passage.strip() else ""
        
        user_prompt = QUIZ_USER_PROMPT_TEMPLATE.format(
            topic=req.topic,
            difficulty=req.difficulty,
            num_questions=req.num_questions,
            passage_clause=passage_clause,
        )

        raw_result = ai_service.generate_json_response(
            system_prompt=QUIZ_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
        )

        validated_questions = validation_service.validate_quiz_structure(raw_result)
        
        # If AI generated fewer questions than requested or validation failed, ensure we have at least 1 question
        if not validated_questions:
            # Fallback to academic synthesizer
            fallback_res = ai_service._generate_academic_fallback(QUIZ_SYSTEM_PROMPT, user_prompt)
            validated_questions = validation_service.validate_quiz_structure(fallback_res)

        quiz_id = str(uuid.uuid4())
        model_used = raw_result.get("_model_used", "gemini")

        # Save to database (including correct answers & explanations for secure server-side evaluation)
        storage.store_quiz(
            quiz_id=quiz_id,
            topic=req.topic,
            difficulty=req.difficulty,
            num_questions=len(validated_questions),
            questions=validated_questions,
        )

        # Prepare client questions (strip correct answers and explanations so user cannot inspect network payload)
        client_questions: List[QuizQuestionClient] = []
        for q in validated_questions:
            options = [QuizOption(key=opt["key"], text=opt["text"]) for opt in q["options"]]
            client_questions.append(
                QuizQuestionClient(
                    id=q["id"],
                    question=q["question"],
                    options=options,
                )
            )

        return QuizSessionData(
            quiz_id=quiz_id,
            topic=req.topic,
            difficulty=req.difficulty,
            total_questions=len(client_questions),
            questions=client_questions,
            model_used=model_used,
        )

    def evaluate_quiz(self, quiz_id: str, user_answers: Dict[int, str]) -> QuizEvaluationResult:
        """Evaluates student submissions against cached quiz and records score to history & progress."""
        quiz_record = storage.get_quiz(quiz_id)
        if not quiz_record:
            raise ValueError("Quiz session not found or has expired. Please generate a new quiz.")

        stored_questions = quiz_record["questions"]
        total_questions = len(stored_questions)
        correct_count = 0
        details: List[QuestionResultDetail] = []

        for q in stored_questions:
            q_id = int(q["id"])
            correct_ans = str(q["correct_answer"]).upper().strip()
            # user_answers can have string or int keys
            user_ans = user_answers.get(q_id) or user_answers.get(str(q_id))
            user_ans_str = str(user_ans).upper().strip() if user_ans else None
            
            is_correct = (user_ans_str == correct_ans)
            if is_correct:
                correct_count += 1

            options = [QuizOption(key=opt["key"], text=opt["text"]) for opt in q["options"]]
            details.append(
                QuestionResultDetail(
                    question_id=q_id,
                    question=q["question"],
                    options=options,
                    user_answer=user_ans_str,
                    correct_answer=correct_ans,
                    is_correct=is_correct,
                    explanation=q.get("explanation", ""),
                )
            )

        incorrect_count = total_questions - correct_count
        score_pct = round((correct_count / total_questions) * 100.0, 1) if total_questions > 0 else 0.0
        passed = score_pct >= 60.0

        if score_pct >= 90:
            feedback = "Outstanding! You have demonstrated exceptional mastery of this material."
        elif score_pct >= 70:
            feedback = "Great job! You have a solid grasp of this concept. Review the missed questions below to sharpen your knowledge."
        elif score_pct >= 50:
            feedback = "Good effort! You understand the foundational basics. Review the detailed explanations below to strengthen weak areas."
        else:
            feedback = "Don't worry! Learning is an iterative process. Review the concepts below and try again."

        # Mark quiz completed in database
        storage.complete_quiz(
            quiz_id=quiz_id,
            user_answers=user_answers,
            score=correct_count,
            accuracy=score_pct,
        )

        # Record activity for real analytics dashboard
        storage.record_activity(
            activity_type="quiz",
            title=f"Quiz: {quiz_record['topic']}",
            subtitle=f"Score: {correct_count}/{total_questions} ({score_pct}%)",
            payload={
                "quiz_id": quiz_id,
                "topic": quiz_record["topic"],
                "difficulty": quiz_record["difficulty"],
                "total_questions": total_questions,
                "correct_count": correct_count,
                "score_pct": score_pct,
                "results": [d.model_dump() for d in details],
            },
            score=correct_count,
            accuracy=score_pct,
        )

        return QuizEvaluationResult(
            quiz_id=quiz_id,
            topic=quiz_record["topic"],
            difficulty=quiz_record["difficulty"],
            total_questions=total_questions,
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            score_percentage=score_pct,
            passed=passed,
            results=details,
            feedback=feedback,
        )


quiz_service = QuizService()
