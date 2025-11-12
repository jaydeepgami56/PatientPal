"""
CXR Foundation Agent Module
===========================
Chest X-ray analysis and interpretation using CXR Foundation model.
Specialized in thoracic radiology and lung condition detection.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from transformers import AutoModelForImageClassification, AutoProcessor, pipeline

from utils.agent_base import BaseHealthcareAgent, AgentConfig, AgentResponse
from utils.prompts import CXR_PROMPT


class CXRFoundationAgent(BaseHealthcareAgent):
    """
    CXR Foundation specialist agent for chest X-ray analysis.
    Inherits from BaseHealthcareAgent with Pydantic validation.
    Requires chest X-ray image input for analysis.
    """

    def initialize(self) -> bool:
        """Initialize CXR Foundation model from Hugging Face"""
        try:
            if self._is_initialized:
                return True

            self.logger.info(f"Initializing CXR Foundation with model: {self.model_id}")

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
            self.logger.info("CXR Foundation initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize CXR Foundation: {str(e)}")
            return False

    def validate_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate input for chest X-ray analysis
        Requires image in context

        Args:
            query: Clinical question about chest X-ray
            context: Must contain 'image' key with PIL Image

        Returns:
            bool: True if valid (has image), False otherwise
        """
        # Require image in context
        if not context or 'image' not in context:
            self.logger.warning("Chest X-ray image required for analysis")
            return False

        # Validate image type
        try:
            image = context['image']
            if not hasattr(image, 'size'):
                self.logger.warning("Invalid image format")
                return False
        except Exception as e:
            self.logger.error(f"Error validating image: {str(e)}")
            return False

        return True

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Process chest X-ray image with CXR Foundation

        Args:
            query: Clinical question or indication for CXR
            context: Must contain 'image' (PIL Image) and optional clinical data

        Returns:
            AgentResponse: Pydantic model with response data
        """
        start_time = datetime.now()

        try:
            if not context or 'image' not in context:
                raise ValueError("Chest X-ray image required for analysis")

            # Get image from context
            image = context['image']

            # Analyze image
            results = self._llm(image, top_k=5)

            # Format results
            findings = []
            for result in results:
                findings.append(f"- {result['label']}: {result['score']*100:.1f}% confidence")

            # Format output using prompt template
            findings_text = "\n".join(findings)
            query_text = query if query else 'Automated chest X-ray analysis using CXR Foundation model.'
            output = CXR_PROMPT.format(findings=findings_text, query=query_text)

            processing_time = (datetime.now() - start_time).total_seconds()

            # Return Pydantic-validated response
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query if query else "Automated chest X-ray analysis",
                output=output,
                confidence=max([r['score'] for r in results]) if results else 0.0,
                metadata={
                    "model_id": self.model_id,
                    "processing_time": processing_time,
                    "findings": results,
                    "image_analyzed": True,
                    "modality": "chest_xray"
                },
                processing_time=processing_time
            )

        except Exception as e:
            self.logger.error(f"Error processing CXR query: {str(e)}")
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.now(),
                input_query=query,
                output="",
                confidence=0.0,
                metadata={},
                error=str(e)
            )


def create_cxr_agent(config: Optional[AgentConfig] = None) -> CXRFoundationAgent:
    """
    Factory function to create CXR Foundation agent with default or custom config

    Args:
        config: Optional AgentConfig (Pydantic model)

    Returns:
        CXRFoundationAgent: Configured agent instance
    """
    if config is None:
        config = AgentConfig(
            name="CXR Foundation",
            model_id="google/cxr-foundation",
            model_type="huggingface",
            description="Chest X-ray analysis and interpretation",
            capabilities=[
                "Chest X-ray interpretation",
                "Lung condition detection",
                "Cardiac assessment",
                "Pneumonia detection",
                "Abnormality screening"
            ],
            temperature=0.5,
            max_tokens=512
        )

    return CXRFoundationAgent(config)
