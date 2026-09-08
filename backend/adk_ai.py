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

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name="filmops",
        user_id="filmops-user",
        session_id="filmops-session"
    )

    runner = Runner(
        agent=root_agent,
        app_name="filmops",
        session_service=session_service
    )

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

    answer = ""

    try:
        async for event in runner.run_async(
            user_id="filmops-user",
            session_id="filmops-session",
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
        else:
            cache[key] = (
                "AI recommendation is temporarily unavailable. "
                "Continue the production recovery plan while the AI service reconnects."
            )

    except Exception:
        cache[key] = (
            "AI recommendation is temporarily unavailable. "
            "Continue the production recovery plan while the AI service reconnects."
        )

    return cache[key]