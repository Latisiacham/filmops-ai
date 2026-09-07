from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agent import root_agent


async def get_adk_recommendation(incident, delay):
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

    async for event in runner.run_async(
        user_id="filmops-user",
        session_id="filmops-session",
        new_message=message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    answer = part.text

    return answer