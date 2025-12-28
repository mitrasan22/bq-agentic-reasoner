import os
import logging
from huggingface_hub import InferenceClient
from bq_agentic_reasoner.config import load_config

class HuggingFaceClient:
    """
    Modern HuggingFace Inference API client using the official SDK.
    """

    def __init__(self):
        config = load_config()
        # Recommended: google/gemma-2-9b-it
        self.model = config["hf_models"]["model"]
        self.timeout = config["hf_models"]["request"]["timeout_seconds"]
        self._client = None

    def _ensure_initialized(self):
        if self._client is None:
            token = os.getenv("HF_API_TOKEN")
            if not token:
                raise RuntimeError("HF_API_TOKEN environment variable not set")
            
            # The client automatically handles the routing and headers
            self._client = InferenceClient(
                model=self.model,
                token=token,
                timeout=self.timeout
            )

    def generate(self, prompt: str) -> str:
        self._ensure_initialized()

        try:
            response = self._client.text_generation(
                prompt,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.9,
                stop_sequences=["\n\n"],
            )
            
            return response.strip()

        except Exception as e:
            logging.error(f"HuggingFace InferenceClient Error: {str(e)}")
            if "503" in str(e):
                return "AI recommendation is warming up. Please refresh in a moment."
            return f"Enrichment failed: {str(e)}"