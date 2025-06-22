from dotenv import load_dotenv
import os
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, MessagesState,END, START, add_messages
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph.state import CompiledStateGraph
from IPython.display import display, Image


@tool
def add(a: float , b:float) -> float:
    """
        To add given two mumbers
         Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
    """
    print("add two numbers")
    return a+b

@tool
def pro(a:float,b:float)-> float:
    """ For finding product of two numbers
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
    """
    print("multiply two numbers")
    return a*b

@tool
def divide(a:float,b:float)-> float:
    """ For finding division of two numbers
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
    """
    print("divide two numbers")
    return a/b

@tool
def get_weather(city:str)-> dict:
    """ For getting weather of a city
        Args:
            city (str): The name of the city.
        Returns:
            dict: Weather information for the specified city.
    """
    load_dotenv()
    api_key = os.getenv("OPEN_WEATHER_API")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    
    import requests
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    
    
     response.json().main
    
@tool
def search    
    

    





