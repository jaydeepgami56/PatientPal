"""
TxGemma Agent Module
===================
Treatment recommendation and medication guidance using Google's TxGemma model.
Specialized in therapeutic interventions and treatment planning.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from utils.agent_base import BaseHealthcareAgent, AgentConfig, AgentResponse
from utils.prompts import TXGEMMA_PROMPT


class TxGemmaAgent(BaseHealthcareAgent):
    """
    TxGemma specialist agent for treatment recommendations.
    Inherits from BaseHealthcareAgent with Pydantic validation.
    """

    def initialize(self) -> bool:
        """Initialize TxGemma model from Hugging Face"""
        try:
            if self._is_initialized:
                return True

            self.logger.info(f"Initializing TxGemma with model: {self.model_id}")

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
            self.logger.info("TxGemma initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize TxGemma: {str(e)}")
            return False

    def validate_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate input for treatment queries

        Args:
            query: Treatment query string
            context: Optional context dictionary

        Returns:
            bool: True if valid, False otherwise
        """
        if not query or len(query.strip()) < 5:
            self.logger.warning("Query too short or empty")
            return False

        if len(query) > 5000:
            self.logger.warning("Query exceeds maximum length")
            return False

        return True

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Process treatment query with TxGemma

        Args:
            query: Treatment or medication question
            context: Optional patient context

        Returns:
            AgentResponse: Pydantic model with response data
        """
        start_time = datetime.now()

        try:
            # Extract patient context if provided
            patient_info = ""
            if context and 'patient_data' in context:
                patient_info = f"\n\nPatient Context:\n{context['patient_data']}"

            # Format prompt for treatment recommendations
            treatment_prompt = TXGEMMA_PROMPT.format(query=query, patient_info=patient_info)

            # Generate response
            result = self._llm.invoke(treatment_prompt)

            processing_time = (datetime.now() - start_time).total_seconds()

            # Return Pydantic-validated response
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query,
                output=result,
                confidence=0.88,
                metadata={
                    "model_id": self.model_id,
                    "processing_time": processing_time,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                    "has_patient_context": bool(context and 'patient_data' in context)
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


def create_txgemma_agent(config: Optional[AgentConfig] = None) -> TxGemmaAgent:
    """
    Factory function to create TxGemma agent with default or custom config

    Args:
        config: Optional AgentConfig (Pydantic model)

    Returns:
        TxGemmaAgent: Configured agent instance
    """
    if config is None:
        config = AgentConfig(
            name="TxGemma",
            model_id="google/txgemma-7b",
            model_type="huggingface",
            description="Treatment recommendations and medication guidance",
            capabilities=[
                "Treatment planning",
                "Medication information",
                "Therapy options",
                "Drug interactions",
                "Dosage guidance"
            ],
            temperature=0.7,
            max_tokens=512
        )

    return TxGemmaAgent(config)
