import requests
import os

API_URL = os.getenv("API_URL")


def send_question(question: str) -> str:
    try:
        response = requests.request(
            "POST", f"{API_URL}/query", json={"question": question}, timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
