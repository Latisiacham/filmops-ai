import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agent import root_agent


async def run_agent():
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name="filmops",
        session_service=session_service
    )

    await session_service.create_session(
        app_name="filmops",
        user_id="filmops-user",
        session_id="test-session"
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Camera 03 has failed during Scene 18. "
                    "The production is delayed by 45 minutes. "
                    "Give one short recommendation."
                )
            )
        ]
    )

    async for event in runner.run_async(
        user_id="filmops-user",
        session_id="test-session",
        new_message=message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)


asyncio.run(run_agent())