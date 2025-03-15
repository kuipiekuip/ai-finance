from google import genai
from google.genai import types


import PIL.Image

image = PIL.Image.open('./data/db_schema.png')

client = genai.Client(api_key="AIzaSyCoDA-zItxAAzQmAN_-kdKCEKc2lNDoTb8")
# Retrieve and encode the PDF byte

system_prompt = """You get a list of kpis and their according values and transform them into a json format according to the schema provided:
{
  "database_schema": {
    "tables": [
      {
        "name": "companies",
        "columns": [
          "company_id", "name", "ticker_symbol", "country", "founded_year", "ceo_name", "website_url", "headquarters", "created_at"
        ]
      },
      {
        "name": "company_kpis",
        "columns": ["company_kpi_id", "company_id", "kpi_id"]
      },
      {
        "name": "kpis",
        "columns": ["kpi_id", "name", "description"]
      },
      {
        "name": "kpi_components",
        "columns": ["kpi_component_id", "company_kpi_id", "name", "description"]
      },
      {
        "name": "kpi_component_values",
        "columns": ["value_id", "kpi_component_id", "period_id", "value", "reported_at", "created_at"]
      },
      {
        "name": "company_sectors",
        "columns": ["company_sector_id", "company_id", "sector_id"]
      },
      {
        "name": "sectors",
        "columns": ["sector_id", "name"]
      },
      {
        "name": "company_sector_metrics",
        "columns": ["company_sector_metric_id", "company_sector_id", "metric_id"]
      },
      {
        "name": "financial_metrics",
        "columns": ["metric_id", "parent_metric_id", "name", "unit", "description"]
      },
      {
        "name": "metric_values",
        "columns": ["value_id", "company_sector_metric_id", "period_id", "value", "reported_at", "created_at"]
      },
      {
        "name": "reporting_periods",
        "columns": ["period_id", "year", "quarter", "start_date", "end_date"]
      }
    ]
  }
}"""


prompt = """Okay, here's the breakdown of Palantir's KPIs and revenue information extracted from the provided document:
**Company-Specific KPIs:**
*   **Rule of 40 Score:** 81%
*   **U.S. Commercial Total Contract Value (TCV) Growth (Year-over-Year):** 134%
*   **U.S. Commercial Total Contract Value (TCV) Growth (Quarter-over-Quarter):** 170%
*   **U.S. Commercial Remaining Deal Value (RDV) Growth (Year-over-Year):** 99%
*   **U.S. Commercial Remaining Deal Value (RDV) Growth (Quarter-over-Quarter):** 47%
*   **Customer Count Growth (Year-over-Year):** 43%
*   **Customer Count Growth (Quarter-over-Quarter):** 13%
*   **Deals Closed:** 129 deals of at least $1 million, 58 deals of at least $5 million, and 32 deals of at least $10 million
**Revenue Breakdown (Q4 2024):**
*   **Total Revenue:** $828 million
    *   **U.S. Revenue:** $558 million
        *   **U.S. Commercial Revenue:** $214 million
        *   **U.S. Government Revenue:** $343 million
**Revenue Breakdown (FY 2024):**
*   **Total Revenue:** $2.87 billion
    *   **U.S. Revenue:** $1.90 billion
        *   **U.S. Commercial Revenue:** $702 million
        *   **U.S. Government Revenue:** $1.20 billion

**Other KPIs and Margins:**

* **Cash from Operations Margin (Q4 2024):** 56%
* **Adjusted Free Cash Flow Margin (Q4 2024):** 63%
* **GAAP Net Income Margin (Q4 2024):** 10%
* **Net Income Margin when excluding one-time SAR-related expenses (Q4 2024):** 20%
* **GAAP Income from Operations Margin (Q4 2024):** 1%
*   **Income from Operations Margin when excluding one-time SAR-related expenses (Q4 2024):** 17%
* **Adjusted Income from Operations Margin (Q4 2024):** 45%
* **Cash from Operations Margin (FY 2024):** 40%
* **Adjusted Free Cash Flow Margin (FY 2024):** 44%
* **GAAP Net Income Margin (FY 2024):** 16%
* **GAAP Income from Operations Margin (FY 2024):** 11%
*   **Income from Operations Margin when excluding one-time SAR-related expenses (FY 2024):** 15%
* **Adjusted Income from Operations Margin (FY 2024):** 39%

**Earnings Per Share:**
*   **GAAP EPS (Q4 2024):** $0.03
    *   **GAAP EPS when excluding one-time SAR-related expenses (Q4 2024):** $0.07
*   **Adjusted EPS (Q4 2024):** $0.14
*   **GAAP EPS (FY 2024):** $0.19
*   **Adjusted EPS (FY 2024):** $0.41

**Cash and Equivalents:**

*   **Cash, cash equivalents, and short-term U.S. Treasury securities:** $5.2 billion
I have only used the information contained within the provided document to create this report."""
response = client.models.generate_content(
  model="gemini-2.0-flash",
  config=types.GenerateContentConfig(
        system_instruction=system_prompt),
  contents=[prompt])
print(response.text)