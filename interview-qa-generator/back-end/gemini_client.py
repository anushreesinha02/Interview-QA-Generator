# gemini_client.py

import os
import requests
import json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_llm_response(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",  # Or any model from openrouter.ai
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        # Try to parse as JSON if possible
        try:
            return json.loads(content)
        except Exception:
            return content
    except Exception as e:
        print("Error in get_llm_response:", e)
        return ""