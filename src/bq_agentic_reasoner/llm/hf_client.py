import os
import requests
import logging
from bq_agentic_reasoner.config import load_config

class HuggingFaceClient:
    """
    Updated HuggingFace Inference API client for Gemma-2.
    Uses the modern router.huggingface.co endpoint.
    """

    def __init__(self):
        config = load_config()
        self.model = config["hf_models"]["model"]
        self.timeout = config["hf_models"]["request"]["timeout_seconds"]

        self._token = None
        self._headers = None
        
        # ✅ FIX: Use the modern router endpoint instead of api-inference
        self._endpoint = f"https://router.huggingface.co/hf-inference/models/{self.model}"

    def _ensure_initialized(self):
        if self._token is None:
            token = os.getenv("HF_API_TOKEN")
            if not token:
                raise RuntimeError("HF_API_TOKEN environment variable not set")

            self._token = token
            self._headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "user-agent": "bq-agentic-reasoner-gcp-function"
            }

    def generate(self, prompt: str) -> str:
        self._ensure_initialized()

        # Gemma-2 expects a chat-like structure or a clean prompt
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.2,
                "top_p": 0.9,
                "return_full_text": False,
            },
            "options": {
                "wait_for_model": True
            }
        }

        try:
            resp = requests.post(
                self._endpoint,
                headers=self._headers,
                json=payload,
                timeout=self.timeout,
            )

            # If the model is loading, HF returns a 503 with an 'estimated_time'
            if resp.status_code == 503:
                logging.warning("Model is loading on HF, retrying...")
                return "AI recommendation is currently warming up. Please try again in a few seconds."

            resp.raise_for_status()
            data = resp.json()

            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "").strip()
            
            # Some new router responses return a direct dict
            if isinstance(data, dict):
                return data.get("generated_text", str(data)).strip()

            return str(data)

        except Exception as e:
            logging.error(f"HF Generation Error: {str(e)}")
            return f"Enrichment failed: {str(e)}"