from pydantic import BaseModel
from agents import Agent
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."

    def __str__(self):
        return f"Search: '{self.query}' - Reason: {self.reason}"


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""

    def __str__(self):
        return f"Web Search Plan with {len(self.searches)} searches"


# Add logging wrapper to track agent's operation
def log_plan_creation(func):
    def wrapper(*args, **kwargs):
        logger.info("Creating new web search plan...")
        result = func(*args, **kwargs)
        logger.info(f"Created plan: {result}")
        for idx, search in enumerate(result.searches, 1):
            logger.info(f"Search {idx}: {search}")
        return result
    return wrapper


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)

# Add logging wrapper to the agent's main method
planner_agent.run = log_plan_creation(planner_agent.run)
