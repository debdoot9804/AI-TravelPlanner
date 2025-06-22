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
import requests

load_dotenv()

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
    
    api_key = os.getenv("OPEN_WEATHER_API")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    
    import requests
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    
    weather_info = {
        "city": data.get("name"),   
        "temperature": data["main"].get("temp"),
        "humidity": data["main"].get("humidity"),
        "weather": data["weather"][0].get("description") if data.get("weather") else "No description available"
    }
    return weather_info

    
    
    
    
@tool
def search_hotel(city:str,check_in:str,check_out:str,adults:int)-> dict:
    """ For searching hotels in a city using Google Serp API
        Args:
            city (str): The name of the city.
            check_in (str): Check-in date in 'YYYY-MM-DD' format.
            check_out (str): Check-out date in 'YYYY-MM-DD' format.
            adults (int): Number of adults.
            Returns:
            dict: Hotel search results.
    """
    
    
        
    baseurl="https://serpapi.com/search"
    params = {
    "engine": "google_hotels",
    "q": f"best hotels in {city} for {adults} adults",
    "check_in_date": check_in,     
    "check_out_date": check_out,   
    "api_key": os.getenv("SERP_API_KEY"),
    "num": 5
}

    search=requests.get(baseurl,params=params)
    response=search.json()
    properties = response.get('properties')
    if not properties:
        return {"error": "No hotel data found. Response: " + str(response)}

    results = {
    property['name']: property.get("total_rate","N/A")
    for property in properties
    if property.get('type') == 'hotel'
}

       
    return results

@tool
def search_attractions(city:str)->dict:
    """ For searching attractions in a city using Google Serp API
        Args:
            city (str): The name of the city.
        Returns:
            dict: Attraction search results.
    """
    
    print("Search Local attractions...")
    
    baseurl="https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "q": f"top attractions in {city}",
        "location":f"{city}",
        "api_key": os.getenv("SERP_API_KEY"),
        "num": 5
    }
    search=requests.get(baseurl,params=params)
    response=search.json()
    attractions = response.get('local_results', [])
    if not attractions:
        return {"error": "No attractions data found. Response: " + str(response)}
    results = {
        attraction['title']: {
            "address": attraction.get("address", "N/A"),
            "rating": attraction.get("rating", "N/A"),
            "reviews": attraction.get("reviews", "N/A")
        }
        for attraction in attractions
    }   
    
    return results

@tool
def search_restaurant(city:str)->dict:
    """For searching restaurants in the city using Google Serp API
        Args:
            city (str): The name of the city.
        Returns:
            dict: Restaurant search results.
    """ 
    print("Searching Local Restaurants...")
    baseurl="https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "q": f"good food,dining restaurants in {city}",
        "location":f"{city}",
        "api_key": os.getenv("SERP_API_KEY"),
        "num": 5
    }
    search=requests.get(baseurl,params=params)
    response=search.json()
    restaurants = response.get('local_results', [])
    if not restaurants:
        return {"error": "No restaurant data found. Response: " + str(response)}
    results = {
        restaurant['title']: {
            "address": restaurant.get("address", "N/A"),
            "rating": restaurant.get("rating", "N/A"),
            "reviews": restaurant.get("reviews", "N/A")
        }
        for restaurant in restaurants
    }
    return results


       
    

    





