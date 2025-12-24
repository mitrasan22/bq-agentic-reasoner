import os
import requests
from typing import Dict, Any
from bq_agentic_reasoner.config import load_config
from dotenv import load_dotenv
load_dotenv()


class HuggingFaceClient:
    """
    Minimal HuggingFace Inference API client.
    """

    def __init__(self):
        config = load_config()
        self.model = config["hf_models"]["model"]
        self.timeout = config["hf_models"]["request"]["timeout_seconds"]

        token = os.getenv("HF_API_TOKEN")
        print(token)
        if not token:
            raise RuntimeError("HF_API_TOKEN environment variable not set")

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        self.endpoint = f"https://api-inference.huggingface.co/models/{self.model}"

    def generate(self, prompt: str) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.2,
                "return_full_text": False,
            },
        }

        resp = requests.post(
            self.endpoint,
            headers=self.headers,
            json=payload,
            timeout=self.timeout,
        )

        resp.raise_for_status()

        data = resp.json()
        if isinstance(data, list):
            return data[0].get("generated_text", "").strip()

        return str(data)
