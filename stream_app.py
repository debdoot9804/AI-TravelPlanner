import os
import streamlit as st
from datetime import date,datetime
from langchain_core.messages import HumanMessage
from model.llm import call_llm
from workflow.flow import create_workflow
from tools.mytools import add, pro, divide, get_weather, search_attractions, search_hotels, search_restaurant


st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.title("🌍 AI TravelPlanner")
st.markdown("Your smart assistant for planning comprehensive trips worldwide!")

st.markdown("---")
st.subheader("Plan Your Next Adventure!")

user_query = st.text_area(
    "Tell me about your trip (e.g., destination, dates, budget, interests, travelers):", 
    height=150,
    value=f"Hey there! I'm planning a 4-day trip to Delhi,India from 1st July to 5th July . My hotel budget is around 1500 per night. I’d like to know what the weather is now, what places I can visit, and how much the whole trip might cost.  I prefer local food and public transportation. Can you plan it all for me?")

if st.button("Generate Trip Plan"):
    
