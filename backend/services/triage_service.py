"""
Triage Service
==============
Business logic for triage operations, extracted from Streamlit pages
"""

from typing import List, Tuple, Dict, Any
import time
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
import re

from utils.prompts import TRIAGE_PROMPT, INTERVIEW_PROMPT, REPORT_PROMPT
from backend.models.triage import InterviewMessage, TriageAnalysisResponse
from backend.config import settings


class TriageService:
    """Service for handling triage operations"""

    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name=settings.openai_model,
            openai_api_key=settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        )

    async def process_interview(
        self,
        session_id: str,
        user_message: str,
        messages: List[InterviewMessage]
    ) -> Tuple[str, bool]:
        """
        Process interview message and determine if interview is complete

        Returns:
            Tuple of (agent_response, is_complete)
        """
        try:
            # Build conversation history
            conversation = [SystemMessage(content=INTERVIEW_PROMPT)]

            for msg in messages:
                if msg.role == "user":
                    conversation.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    conversation.append(AIMessage(content=msg.content))

            # Get LLM response
            response = self.llm.invoke(conversation)
            agent_message = response.content

            # Check if interview is complete (look for completion markers)
            is_complete = self._check_interview_complete(messages, agent_message)

            return agent_message, is_complete

        except Exception as e:
            raise Exception(f"Error processing interview: {str(e)}")

    def _check_interview_complete(
        self,
        messages: List[InterviewMessage],
        latest_response: str
    ) -> bool:
        """Check if interview has gathered sufficient information"""

        # Simple heuristic: if we have enough exchanges and key info
        if len(messages) < 6:  # Need at least 3 exchanges
            return False

        # Check for completion indicators in response
        completion_indicators = [
            "have all the information",
            "proceed with",
            "complete the assessment",
            "generate the report",
            "that's all i need"
        ]

        response_lower = latest_response.lower()
        return any(indicator in response_lower for indicator in completion_indicators)

    async def perform_analysis(
        self,
        session_id: str,
        messages: List[InterviewMessage]
    ) -> TriageAnalysisResponse:
        """
        Perform triage analysis on interview data

        Returns:
            TriageAnalysisResponse with ATS category, report, etc.
        """
        start_time = time.time()

        try:
            # Extract interview content
            interview_text = "\n".join([
                f"{msg.role.upper()}: {msg.content}"
                for msg in messages
            ])

            # Generate RACGP report
            report = await self._generate_report(interview_text)

            # Perform ATS triage
            triage_result = await self._perform_ats_triage(interview_text)

            # Extract key information
            chief_complaint = self._extract_chief_complaint(messages)
            symptoms = self._extract_symptoms(messages)

            processing_time = time.time() - start_time

            return TriageAnalysisResponse(
                session_id=session_id,
                ats_category=triage_result["category"],
                urgency=triage_result["urgency"],
                chief_complaint=chief_complaint,
                symptoms=symptoms,
                recommended_action=triage_result["action"],
                report=report,
                confidence=triage_result["confidence"],
                processing_time=processing_time,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "model": settings.openai_model
                }
            )

        except Exception as e:
            raise Exception(f"Error performing analysis: {str(e)}")

    async def _generate_report(self, interview_text: str) -> str:
        """Generate RACGP-compliant report"""
        try:
            prompt = REPORT_PROMPT.format(interview_text=interview_text)
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            raise Exception(f"Error generating report: {str(e)}")

    async def _perform_ats_triage(self, interview_text: str) -> Dict[str, Any]:
        """Perform ATS triage analysis"""
        try:
            prompt = TRIAGE_PROMPT.format(interview_text=interview_text)
            response = self.llm.invoke([HumanMessage(content=prompt)])

            # Parse response for ATS category
            content = response.content
            category = self._extract_ats_category(content)
            urgency = self._map_ats_to_urgency(category)
            action = self._extract_recommended_action(content)

            return {
                "category": category,
                "urgency": urgency,
                "action": action,
                "confidence": 0.85  # TODO: Calculate actual confidence
            }

        except Exception as e:
            raise Exception(f"Error performing triage: {str(e)}")

    def _extract_ats_category(self, content: str) -> str:
        """Extract ATS category from LLM response"""
        patterns = [
            r"ATS\s*Category\s*[:-]?\s*(\d)",
            r"Category\s*[:-]?\s*(\d)",
            r"ATS\s*[:-]?\s*(\d)"
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return f"Category {match.group(1)}"

        return "Category 3"

    def _map_ats_to_urgency(self, category: str) -> str:
        """Map ATS category to urgency level"""
        mapping = {
            "Category 1": "Immediate (Life-threatening)",
            "Category 2": "Emergency (Imminently life-threatening)",
            "Category 3": "Urgent (Potentially life-threatening)",
            "Category 4": "Semi-urgent (Potentially serious)",
            "Category 5": "Non-urgent (Less urgent)"
        }
        return mapping.get(category, "Urgent")

    def _extract_recommended_action(self, content: str) -> str:
        """Extract recommended action from triage response"""
        if "recommend" in content.lower():
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "recommend" in line.lower():
                    return "\n".join(lines[i:i+3])
        return "Seek immediate medical attention"

    def _extract_chief_complaint(self, messages: List[InterviewMessage]) -> str:
        """Extract chief complaint from interview"""
        for msg in messages:
            if msg.role == "user" and len(msg.content) > 20:
                return msg.content[:200]
        return "No chief complaint recorded"

    def _extract_symptoms(self, messages: List[InterviewMessage]) -> List[str]:
        """Extract symptoms mentioned in interview"""
        symptoms = []
        common_symptoms = [
            "pain", "fever", "cough", "headache", "nausea", "vomiting",
            "dizziness", "shortness of breath", "chest pain", "bleeding",
            "rash", "fatigue", "weakness"
        ]

        interview_text = " ".join([msg.content.lower() for msg in messages if msg.role == "user"])

        for symptom in common_symptoms:
            if symptom in interview_text:
                symptoms.append(symptom.title())

        return symptoms[:5]
