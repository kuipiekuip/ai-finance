from crewai import Agent, Task, Crew, Process, LLM
import os
from BraveSearchTool import BraveSearchTool

os.environ["GROQ_API_KEY"] = ""

# 使用 crewai 的 LLM
llm = LLM(model="groq/llama-3.3-70b-versatile")
# llm = LLM(model="groq/llama3-8b-8192")

search_tool = BraveSearchTool()
company_name = "Palantir"
# company_name = "ING Bank"

# Define the search agent
search_agent = Agent(
    role="Financial Report Researcher",
    # goal= f"Gather all company-specific kpi's for {company_name} while ignoring standard kpi's",
    goal= f"Gather all needed documents for {company_name} to collect the important company-specific kpis",
    backstory="An expert financial researcher with extensive experience in finding company financial documents.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool]
)

# Define the search task
search_task = Task(
    # description=f"Search for {company_name}'s Q1 2024 financial performance and latest stock price.",
    description=f"Search for the document for {company_name}'s Q4 2024 financial performance, it should include important company-specific kpis.",
    agent=search_agent,
    expected_output="Show me the closest document url in pdf format (e.g .pdf is inside the url), including all important company-specific kpis."
)

# Create a Crew with the agents
crew = Crew(
    agents=[search_agent],
    tasks=[search_task],
    process=Process.sequential,
    verbose=True
)

# Run the analysis
result = crew.kickoff()
print("url:", result)

# print(f"\nFinancial Analysis Report for {company_name}:\n", result)

from google import genai
from google.genai import types
import pathlib
import httpx

client = genai.Client(api_key="")

doc_url = f"{result}" # Replace with the actual URL of your PDF, (a problem: some companies have no pdf url)

# Retrieve and encode the PDF byte
doc_data = httpx.get(doc_url).content

prompt = "Summarize this document"
response = client.models.generate_content(
  model="gemini-1.5-flash",
  contents=[
      types.Part.from_bytes(
        data=doc_data,
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)

