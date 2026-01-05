"""LangGraph workflow for Scout travel agent."""
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from .state import TravelState
from .nodes import (
    intake_node,
    research_node,
    compare_node,
    finalize_node,
    should_use_tools,
)
from scout.tools import (
    search_flights,
    search_hotels,
    create_trip_event,
    store_preference,
    recall_preferences,
)


def create_agent():
    """Create and compile the Scout travel agent graph."""

    # Define tools
    tools = [
        search_flights,
        search_hotels,
        create_trip_event,
        store_preference,
        recall_preferences,
    ]

    # Build graph
    workflow = StateGraph(TravelState)

    # Add nodes
    workflow.add_node("intake", intake_node)
    workflow.add_node("research", research_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("compare", compare_node)
    workflow.add_node("finalize", finalize_node)

    # Define edges
    workflow.set_entry_point("intake")
    workflow.add_edge("intake", "research")
    workflow.add_conditional_edges(
        "research", should_use_tools, {"tools": "tools", "compare": "compare"}
    )
    workflow.add_edge("tools", "research")  # Loop back after tool execution
    workflow.add_edge("compare", "finalize")
    workflow.add_edge("finalize", END)

    # Compile
    return workflow.compile()


# Create the agent instance
agent = create_agent()
