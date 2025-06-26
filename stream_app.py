import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

# Local imports
from model.llm import call_llm
from workflow.flow import create_workflow
from tools.mytools import add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant


# Streamlit page config
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# App Title and Instructions
st.title("🌍 AI Travel Planner Assistant")
st.markdown("Your smart agent to plan customized, real-time travel experiences around the world.")
st.markdown("---")

st.subheader("🧳 Plan Your Next Adventure")

# User input
user_query = st.text_area(
    "✈️ Tell me about your trip (destination, dates, budget, interests, etc.):",
    height=160,
    value="Type Here..."
)

# Create Workflow
workflow = create_workflow()

# Button to trigger agent
if st.button("🚀 Generate Trip Plan"):
    with st.spinner("Planning your trip..."):
        try:
            # Wrap the user query in a HumanMessage
            user_message = HumanMessage(content=user_query)
            
            # Execute the agentic workflow
            result = workflow.invoke({"messages": [user_message]}, config=RunnableConfig())

            # Display the response
            st.success("Here's your personalized trip plan:")
            st.write(result.get("messages")[-1].content)  # Assuming final agent response

        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")

# Optional: Sidebar to show tool status or history (if you track them)
st.sidebar.title("🛠️ Agent Info")
st.sidebar.markdown("Tools Available:")
st.sidebar.markdown("- ✅ Weather Info")
st.sidebar.markdown("- ✅ Tourist Attractions")
st.sidebar.markdown("- ✅ Hotel Finder")
st.sidebar.markdown("- ✅ Restaurant Suggestions")
st.sidebar.markdown("- ✅ Budget & Cost Estimator")
