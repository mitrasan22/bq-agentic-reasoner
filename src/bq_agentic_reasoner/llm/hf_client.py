import os
import logging
from huggingface_hub import InferenceClient
from bq_agentic_reasoner.config import load_config

class HuggingFaceClient:
    def __init__(self):
        config = load_config()
        self.model = config["hf_models"]["model"]
        self.timeout = config["hf_models"]["request"]["timeout_seconds"]
        self._client = None

    def _ensure_initialized(self):
        if self._client is None:
            token = os.getenv("HF_API_TOKEN")
            if not token:
                raise RuntimeError("HF_API_TOKEN environment variable not set")
            # Log masked token for verification
            logging.info(f"Initializing HF Client with token: {token[:4]}...{token[-4:]}")
            self._client = InferenceClient(model=self.model, token=token, timeout=self.timeout)

    def generate(self, prompt: str) -> str:
        self._ensure_initialized()
        try:
            response = self._client.chat_completion(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_new_tokens=512,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"HF Error: {str(e)}")
            if "429" in str(e):
                return "Rate limit hit. Please wait 5 mins."
            return f"Enrichment failed: {str(e)}"