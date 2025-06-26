import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

# Your imports
from model.llm import call_llm
from workflow.flow import create_workflow
from tools.mytools import add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant


st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")
st.title("🌍 AI Travel Planner Assistant")
st.markdown("Your smart assistant to help plan unforgettable trips.")
st.markdown("---")

# Create the agentic workflow
workflow = create_workflow()

# Initialize session state for messages and submission flag
if "messages" not in st.session_state:
    st.session_state.messages = []

if "trip_started" not in st.session_state:
    st.session_state.trip_started = False

# Button to clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.trip_started = False
    st.experimental_rerun()

# === INITIAL TEXT AREA FOR FIRST PROMPT ===
if not st.session_state.trip_started:
    st.subheader("🧳 Plan Your Initial Trip")
    user_query = st.text_area(
        "✈️ Tell me about your trip (destination, dates, budget, interests, etc.):",
        height=160,
        value=""
    )

    if st.button("🚀 Plan My Trip"):
        if user_query.strip():
            user_msg = HumanMessage(content=user_query)
            st.session_state.messages.append(user_msg)
            st.session_state.trip_started = True  # switch to chat mode

            with st.spinner("Planning your trip..."):
                try:
                    result = workflow.invoke({"messages": st.session_state.messages}, config=RunnableConfig())
                    final_response = result["messages"][-1].content
                    ai_msg = AIMessage(content=final_response)
                    st.session_state.messages.append(ai_msg)
                    st.rerun()  # reload into chat interface
                except Exception as e:
                    st.error(f"Error occurred: {e}")
        else:
            st.warning("Please describe your trip before continuing.")

# === CHAT UI SECTION ===
else:
    for msg in st.session_state.messages:
        with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
            st.markdown(msg.content)

    # Follow-up chat
    user_input = st.chat_input("Ask a follow-up question...")

    if user_input:
        user_msg = HumanMessage(content=user_input)
        st.session_state.messages.append(user_msg)

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = workflow.invoke({"messages": st.session_state.messages}, config=RunnableConfig())
                    final_response = result["messages"][-1].content
                    ai_msg = AIMessage(content=final_response)
                    st.session_state.messages.append(ai_msg)
                    st.markdown(final_response)
                except Exception as e:
                    st.error(f"Error: {e}")


# Optional: Sidebar to show tool status or history (if you track them)
st.sidebar.title("🛠️ Agent Info")
st.sidebar.markdown("Tools Available:")
st.sidebar.markdown("- ✅ Weather Info")
st.sidebar.markdown("- ✅ Tourist Attractions")
st.sidebar.markdown("- ✅ Hotel Finder")
st.sidebar.markdown("- ✅ Restaurant Suggestions")
st.sidebar.markdown("- ✅ Budget & Cost Estimator")                
