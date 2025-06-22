from tools.mytools import add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant
from model.llm import call_llm
from langgraph.graph import StateGraph, MessagesState, END, START, add_messages
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

def create_workflow() -> StateGraph:
    """ For creating the workflow graph for the travel planning agent."""
    workflow=StateGraph(MessagesState)
    tools=[add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant]
    
    workflow.add_node("Travel_Agent",call_llm)
    workflow.add_node("tools",ToolNode(tools))
    
    workflow.add_edge(START, "Travel_Agent")
    workflow.add_conditional_edges("Travel_Agent", tools_condition,)
    workflow.add_edge("tools","Travel_Agent")
    workflow.add_edge("Travel_Agent",END)

    app=workflow.compile()
    return app    