import os
import requests
from bq_agentic_reasoner.config import load_config


class HuggingFaceClient:
    """
    Minimal HuggingFace Inference API client.
    Cloud Functions safe.
    """

    def __init__(self):
        config = load_config()
        self.model = config["hf_models"]["model"]
        self.timeout = config["hf_models"]["request"]["timeout_seconds"]

        self._token = None
        self._headers = None
        self._endpoint = f"https://api-inference.huggingface.co/models/{self.model}"

    def _ensure_initialized(self):
        if self._token is None:
            token = os.getenv("HF_API_TOKEN")
            if not token:
                raise RuntimeError("HF_API_TOKEN environment variable not set")

            self._token = token
            self._headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

    def generate(self, prompt: str) -> str:
        self._ensure_initialized()

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.2,
                "return_full_text": False,
            },
        }

        resp = requests.post(
            self._endpoint,
            headers=self._headers,
            json=payload,
            timeout=self.timeout,
        )

        resp.raise_for_status()

        data = resp.json()
        if isinstance(data, list):
            return data[0].get("generated_text", "").strip()

        return str(data)
