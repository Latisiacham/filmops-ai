import asyncio
import html

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agent import root_agent


cache = {}


async def get_adk_recommendation(incident, delay):
    key = (incident, delay)

    if key in cache:
        return cache[key]

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    f"Incident: {incident}. "
                    f"Schedule delay: {delay} minutes. "
                    "Give one short practical recommendation."
                )
            )
        ]
    )

    for attempt in range(4):
    try:
        # your Gemini / ADK request here

        if answer:
            cache[key] = answer
            return answer

    except Exception as error:
        print(
            f"Gemini attempt {attempt + 1} failed:",
            error
        )

        if attempt < 3:
            wait_time = 5 * (attempt + 1)

            print(
                f"Retrying Gemini in {wait_time} seconds..."
            )

            await asyncio.sleep(wait_time)

    return (
        "AI recommendation is temporarily unavailable. "
        "Continue the production recovery plan while the AI service reconnects."
    )