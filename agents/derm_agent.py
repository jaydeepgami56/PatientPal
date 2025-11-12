"""
Derm Foundation Agent Module
============================
Dermatological assessment and skin condition analysis using Derm Foundation model.
Specialized in skin lesion classification and dermatological diagnostics.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from transformers import AutoModelForImageClassification, AutoProcessor, pipeline

from utils.agent_base import BaseHealthcareAgent, AgentConfig, AgentResponse
from utils.prompts import DERM_PROMPT


class DermFoundationAgent(BaseHealthcareAgent):
    """
    Derm Foundation specialist agent for dermatological analysis.
    Inherits from BaseHealthcareAgent with Pydantic validation.
    Requires image input for analysis.
    """

    def initialize(self) -> bool:
        """Initialize Derm Foundation model from Hugging Face"""
        try:
            if self._is_initialized:
                return True

            self.logger.info(f"Initializing Derm Foundation with model: {self.model_id}")

            # Check for HuggingFace token
            hf_token = os.getenv("HUGGINGFACE_API_KEY")
            if not hf_token:
                self.logger.warning("No HUGGINGFACE_API_KEY found. Some models may not be accessible.")

            # Load processor and model for image analysis
            self.processor = AutoProcessor.from_pretrained(
                self.model_id,
                token=hf_token,
                trust_remote_code=True
            )
            model = AutoModelForImageClassification.from_pretrained(
                self.model_id,
                token=hf_token,
                trust_remote_code=True,
                device_map="auto"
            )

            # Create vision pipeline
            self._llm = pipeline(
                "image-classification",
                model=model,
                feature_extractor=self.processor,
                device_map="auto"
            )

            self._is_initialized = True
            self.logger.info("Derm Foundation initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Derm Foundation: {str(e)}")
            return False

    def validate_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate input for dermatological analysis
        Requires image in context

        Args:
            query: Description or question about skin lesion
            context: Must contain 'image' key with PIL Image

        Returns:
            bool: True if valid (has image), False otherwise
        """
        # Require image in context
        if not context or 'image' not in context:
            self.logger.warning("Image required for dermatological analysis")
            return False

        # Validate image type (PIL Image expected)
        try:
            image = context['image']
            # Check if it has basic image attributes
            if not hasattr(image, 'size'):
                self.logger.warning("Invalid image format")
                return False
        except Exception as e:
            self.logger.error(f"Error validating image: {str(e)}")
            return False

        return True

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Process skin lesion image with Derm Foundation

        Args:
            query: Clinical question or description
            context: Must contain 'image' (PIL Image) and optional 'lesion_characteristics'

        Returns:
            AgentResponse: Pydantic model with response data
        """
        start_time = datetime.now()

        try:
            if not context or 'image' not in context:
                raise ValueError("Image required for dermatological analysis")

            # Get image from context
            image = context['image']

            # Analyze image
            results = self._llm(image, top_k=5)

            # Format results
            findings = []
            for result in results:
                findings.append(f"- {result['label']}: {result['score']*100:.1f}% confidence")

            # Extract lesion characteristics if provided
            lesion_info = context.get('lesion_characteristics', '')
            lesion_info_text = f"Lesion Characteristics: {lesion_info}" if lesion_info else ""

            # Format output using prompt template
            findings_text = "\n".join(findings)
            query_text = query if query else 'Automated analysis of skin lesion using Derm Foundation model.'
            output = DERM_PROMPT.format(
                findings=findings_text,
                lesion_info=lesion_info_text,
                query=query_text
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            # Return Pydantic-validated response
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query if query else "Automated dermatological analysis",
                output=output,
                confidence=max([r['score'] for r in results]) if results else 0.0,
                metadata={
                    "model_id": self.model_id,
                    "processing_time": processing_time,
                    "findings": results,
                    "image_analyzed": True,
                    "lesion_characteristics": lesion_info
                },
                processing_time=processing_time
            )

        except Exception as e:
            self.logger.error(f"Error processing dermatological query: {str(e)}")
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query,
                output="",
                confidence=0.0,
                metadata={},
                error=str(e)
            )


def create_derm_agent(config: Optional[AgentConfig] = None) -> DermFoundationAgent:
    """
    Factory function to create Derm Foundation agent with default or custom config

    Args:
        config: Optional AgentConfig (Pydantic model)

    Returns:
        DermFoundationAgent: Configured agent instance
    """
    if config is None:
        config = AgentConfig(
            name="Derm Foundation",
            model_id="google/derm-foundation",
            model_type="huggingface",
            description="Dermatological assessment and skin condition analysis",
            capabilities=[
                "Skin lesion classification",
                "Dermatological condition detection",
                "Melanoma screening",
                "Rash assessment",
                "Clinical correlation"
            ],
            temperature=0.5,
            max_tokens=512
        )

    return DermFoundationAgent(config)
