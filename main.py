import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool # Added WebsiteSearchTool
from dotenv import load_dotenv

load_dotenv()

# Initialize tools
search_tool = SerperDevTool()
web_tool = WebsiteSearchTool() # This is the new "Reading" tool


# AGENT 1: The Philanthropy Researcher
scout = Agent(
    role='Partnership Researcher',
    goal='Identify 3 Swedish Family Offices or Corporations with active CSR/Social Impact programs.',
    backstory='You specialize in the Swedish "Impact Investing" landscape. You find organizations that care about entrepreneurship in underrepresented areas.',
    tools=[search_tool],
    verbose=True
)

# AGENT 2: The Value Proposition Analyst
analyst = Agent(
    role='Swedish Financial Investigator',
    goal='Find the Orgnr and then the revenue (omsättning) on Allabolag.se for {company_name}.',
    backstory="""You are an expert at Swedish corporate research. 
    1. First, search for the company name + 'allabolag' to find their financial profile.
    2. If that fails, find the company's official website and look at the footer for an 'Organisationsnummer'.
    3. Use that number to find the 'Omsättning' (Revenue) and 'Resultat' (Profit) for the last 3 years.
    4. If the data is missing, report 'Data not public' rather than guessing.""",
    tools=[search_tool, web_tool], # Use Serper to search and WebTool to "read" the footer
    verbose=True
)

# TASK 1: Find the targets
task1 = Task(
    description='Find 3 Swedish organizations (Family Offices or large companies like Volvo, Spotify, etc.) that have publicly supported social entrepreneurship in 2025-2026.',
    expected_output='A list of 3 names and their specific social impact focus.',
    agent=scout
)

# TASK 2: The Strategic Hook & Financial Verification
task2 = Task(
    description="""1. For each organization in task1, find their 'Organisationsnummer'.
    2. Use that number to find their latest 'Omsättning' (Revenue) on Allabolag.se.
    3. Find the name of their CSR Manager, Sustainability Lead, or Marketing Director.
    4. Identify one specific social project they supported in the last 24 months to use as a 'Hook'.""",
    expected_output="""A report for each organization including: 
    - Company Name & Org. Nr
    - Revenue (MSEK)
    - Key Contact Name & Title
    - The Hook: 'They previously supported [Project X], which aligns with BLING because...'""",
    agent=analyst
)

qualifier = Agent(
    role='M&A Qualifier',
    goal='Score each deal from 1-10 based on acquisition potential.',
    backstory='You look at the revenue and history. Companies with 10M-50M SEK revenue and 20+ years of history get a score of 9/10.',
    verbose=True
)

# New Task for this Agent
task3 = Task(
    description='Analyze the findings from the Analyst. Rank the companies from best to worst based on financial stability.',
    expected_output='A final ranked list with a "Verdict" for each company.',
    agent=qualifier
)


crew = Crew(agents=[scout, analyst, qualifier], tasks=[task1, task2, task3])

# RUN IT
result = crew.kickoff()

print("\n\n########################")
print("## BLING SPONSORSHIP STRATEGY ##")
print("########################\n")
print(result)