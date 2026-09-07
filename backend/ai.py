import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

cache = {}


def get_recommendation(incident, delay):
    key = (incident, delay)

    if key in cache:
        return cache[key]

    prompt = f"""
You are the AI Production Director for a film production.

Current incident:
{incident}

Current schedule delay:
{delay} minutes

Give the production team one short practical recommendation.
Keep the response under 3 sentences.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        cache[key] = response.text

    except Exception:
        cache[key] = (
            "AI recommendation is temporarily unavailable. "
            "Continue the production recovery plan while the AI service reconnects."
        )

    return cache[key]