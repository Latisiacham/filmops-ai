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

    # Try Gemini up to 4 times if the service is temporarily busy
    for attempt in range(4):
        try:
            session_service = InMemorySessionService()

            await session_service.create_session(
                app_name="filmops",
                user_id="filmops-user",
                session_id=f"filmops-session-{attempt}"
            )

            runner = Runner(
                agent=root_agent,
                app_name="filmops",
                session_service=session_service
            )

            answer = ""

            async for event in runner.run_async(
                user_id="filmops-user",
                session_id=f"filmops-session-{attempt}",
                new_message=message
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            answer = part.text

            if answer:
                for _ in range(5):
                    cleaned = html.unescape(answer)

                    if cleaned == answer:
                        break

                    answer = cleaned

                cache[key] = answer
                return answer

        except Exception as error:
            print(
                f"Gemini attempt {attempt + 1} failed:",
                error
            )

            if attempt < 2:
                await asyncio.sleep(5)

    return (
        "AI recommendation is temporarily unavailable. "
        "Continue the production recovery plan while the AI service reconnects."
    )