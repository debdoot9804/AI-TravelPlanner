from langchain_core.tools import tool
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate  
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, MessagesState, END, START, add_messages
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
from tools.mytools import add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant

load_dotenv()

llm=AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.1,
    max_retries=2
    
)
#llm= ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
              #temperature=0.3)
SYSTEM_PROMPT = """

You are an AI Travel Planner and Expense Manager. Your task is to assist users in planning trips to any city worldwide using reasoning and tools.

You follow the **ReAct pattern**:
1. Think about what the user needs.
2. Decide which tool to use and why.
3. Call the tool using the correct arguments.
4. Observe the result.
5. Repeat reasoning and tool usage as needed.
6. Finally, return a complete, friendly, and well-organized travel plan.
7. Try Use the provided tools before trying for generic web_search tool
8. For the total cost try to use the add and product tools as appropriate to get the overall cost.

Be thoughtful and structured. Use tools only when required. Wait for tool results before deciding the next step.

If the user provides a destination and number of days, start by gathering key information like attractions, weather, and hotels. Calculate costs, convert currency, generate an itinerary, and end with a trip summary.
Correctly calcuate the trip days . check the local weather during the time.Add a plan to visit nearby attractions.
Do not make any assumption
Your final response must be complete and organized, using markdown formatting (headers, bullet points) for easy reading. You should never hallucinate data — always use tools to get real-time or accurate info.
In the end try to give them a day-wise itenerary.
Let's get started.


"""

def call_llm(state:MessagesState) -> MessagesState:
    """Call the LLM with the current state messages."""
    tools=[add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant]
    llm_with_tools=llm.bind_tools(tools)
    response= llm_with_tools.invoke([SYSTEM_PROMPT]+state['messages'])
    return {'messages':[response]}
