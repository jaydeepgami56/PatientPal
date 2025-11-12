"""
MedGemma Agent Module
====================
General medical query processing and diagnostic support using Google's MedGemma model.
Handles general medical questions, symptom analysis, and preliminary diagnostics.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from utils.agent_base import BaseHealthcareAgent, AgentConfig, AgentResponse
from utils.prompts import MEDGEMMA_PROMPT


class MedGemmaAgent(BaseHealthcareAgent):
    """
    MedGemma specialist agent for general medical queries.
    Inherits from BaseHealthcareAgent with Pydantic validation.
    """

    def initialize(self) -> bool:
        """Initialize MedGemma model from Hugging Face"""
        try:
            if self._is_initialized:
                return True

            self.logger.info(f"Initializing MedGemma with model: {self.model_id}")

            # Check for HuggingFace token
            hf_token = os.getenv("HUGGINGFACE_API_KEY")
            if not hf_token:
                self.logger.warning("No HUGGINGFACE_API_KEY found. Some models may not be accessible.")

            # Load model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                token=hf_token,
                trust_remote_code=True
            )
            model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                token=hf_token,
                trust_remote_code=True,
                device_map="auto"
            )

            # Create pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )

            self._llm = HuggingFacePipeline(pipeline=pipe)
            self._is_initialized = True
            self.logger.info("MedGemma initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize MedGemma: {str(e)}")
            return False

    def validate_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate input for medical queries using Pydantic-style validation

        Args:
            query: Medical query string
            context: Optional context dictionary

        Returns:
            bool: True if valid, False otherwise
        """
        if not query or len(query.strip()) < 5:
            self.logger.warning("Query too short or empty")
            return False

        # Additional validation
        if len(query) > 5000:
            self.logger.warning("Query exceeds maximum length")
            return False

        return True

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Process medical query with MedGemma

        Args:
            query: Medical question or symptom description
            context: Optional additional context

        Returns:
            AgentResponse: Pydantic model with response data
        """
        start_time = datetime.now()

        try:
            # Format prompt for medical context
            medical_prompt = MEDGEMMA_PROMPT.format(query=query)

            # Generate response
            result = self._llm.invoke(medical_prompt)

            processing_time = (datetime.now() - start_time).total_seconds()

            # Return Pydantic-validated response
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query,
                output=result,
                confidence=0.85,
                metadata={
                    "model_id": self.model_id,
                    "processing_time": processing_time,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens
                },
                processing_time=processing_time
            )

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query,
                output="",
                confidence=0.0,
                metadata={},
                error=str(e)
            )


def create_medgemma_agent(config: Optional[AgentConfig] = None) -> MedGemmaAgent:
    """
    Factory function to create MedGemma agent with default or custom config

    Args:
        config: Optional AgentConfig (Pydantic model)

    Returns:
        MedGemmaAgent: Configured agent instance
    """
    if config is None:
        config = AgentConfig(
            name="MedGemma",
            model_id="google/medgemma-7b",
            model_type="huggingface",
            description="General medical query processing and diagnostic support",
            capabilities=[
                "General medical questions",
                "Symptom analysis",
                "Preliminary diagnostics",
                "Medical education",
                "Health information"
            ],
            temperature=0.7,
            max_tokens=512
        )

    return MedGemmaAgent(config)
