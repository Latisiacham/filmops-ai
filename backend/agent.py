from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models import Gemini


load_dotenv()


root_agent = Agent(
    name="production_director",
    model=Gemini(
        model="gemini-3.6-flash"
    ),
    instruction="""
You are the FilmOps AI Production Director.

Your job is to help a film production team respond to production incidents.

Given an incident and schedule delay:
- understand the production impact
- recommend one practical action
- keep the recommendation short
- do not exceed 3 sentences
"""
)