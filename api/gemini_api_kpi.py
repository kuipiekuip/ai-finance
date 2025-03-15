from google import genai
from google.genai import types
import pathlib
import httpx

client = genai.Client(api_key="AIzaSyCoDA-zItxAAzQmAN_-kdKCEKc2lNDoTb8")
# Retrieve and encode the PDF byte
filepath = pathlib.Path('./Palantir Q4 2023 Business Update.pdf')

system_prompt = """You are an expert financial analyst. Your task is to extract specific KPIs and revenue breakdowns from a company's financial report.
Instructions:
1. Identify company-specific KPIs beyond standard financial metrics.
2. Provide the values for all KPIs you find, including percentages. If a value cannot be determined, state "Value cannot be determined from the report."
3. Provide a revenue breakdown.
4. Base your response ONLY on the information found in the provided document."""


prompt = """Based on the financial data in the document provided, extract key company-specific KPIs and revenue breakdown for Palantir.  
Please get the percentages and the numbers and state if the numbers can't be found in the report."""
response = client.models.generate_content(
  model="gemini-2.0-flash",
  config=types.GenerateContentConfig(
        system_instruction=system_prompt),
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)