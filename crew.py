# crew.py
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool
import os
from dotenv import load_dotenv # You might need to run: pip install python-dotenv

load_dotenv() # This loads the variables from your .env file

# Now you use the variables like this:
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def run_swedish_scout(niche, city):
    # Initialize the tools the agents will use
    search_tool = SerperDevTool()
    web_tool = WebsiteSearchTool()

# 1. THE SCOUT: Finds the companies with a "Values" focus
    scout = Agent(
        role='Social Impact Business Scout',
        goal=f'Identify 5 companies in {niche} in {city} with strong CSR potential.',
        backstory="""You search for established Swedish companies. You prioritize 
        those that mention 'Sustainability', 'Social Responsibility', or 'Community' 
        on their websites, as they are the best candidates to sponsor BLING.""",
        tools=[search_tool],
        verbose=True,
        allow_delegation=False
    )
    
# Use Serper for both searching AND direct scraping
    search_tool = SerperDevTool() 

    # 2. THE ANALYST: Stronger instructions for deep scraping
    analyst = Agent(
        role='Swedish Financial Auditor',
        goal='Extract the exact Omsättning (Revenue) from Allabolag.se.',
        backstory="""You are a precise data auditor. When you get a company URL, 
        you scrape the 'Bokslut' (Financials) section. If you see 'Omsättning', 
        capture that exact number. If you cannot find it after 3 attempts, 
        you MUST report 'Data not public'—never invent a number.""",
        tools=[search_tool], # Serper is often better at scraping than WebsiteSearchTool
        verbose=True,
        max_iter=5 # Gives the agent more "retries" if it fails initially
    )

 # TASK 1: The Scout must be a simple list-maker
    task1 = Task(
        description=f"Find exactly 5 companies in {niche} in {city}. Provide their Legal Name and Org.nr.",
        expected_output="A simple bulleted list of 5 company names with their Swedish Org.nr.",
        agent=scout
    )
# TASK 2: Deep Intelligence & Contact Discovery
    task2 = Task(
        description="""For each company found by the scout:
        1. Verify their latest 'Omsättning' (Revenue) and 'Resultat' (Profit) on Allabolag.se.
        2. Provide the direct Source URL for verification.
        3. Search for a 'Key Contact': Look for the name and title of the Sustainability Manager, 
           Marketing Director, or CEO. 
        4. Identify 'Strategic Alignment': Briefly explain how their business industry 
           aligns with social impact goals (e.g., diversity, local community growth).""",
        expected_output="""A professional data sheet for 5 companies including:
        - Company Name & Org.nr
        - Revenue & Profit (SEK)
        - Source URL
        - Key Contact: [Name & Job Title]
        - Strategic Alignment: [2-3 sentences]""",
        agent=analyst
    )

 # In your crew.py
    crew = Crew(
    agents=[scout, analyst],
    tasks=[task1, task2],
    verbose=True,
    memory=True, # This allows agents to learn from failed searches during the task
    cache=True   # This saves you money on API calls
)
    
    # Start the process and return the final text to the website
    return crew.kickoff(inputs={'niche': niche, 'city': city})