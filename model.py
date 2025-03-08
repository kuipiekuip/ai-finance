import os
import json
import fitz  # PyMuPDF for PDF extraction
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq

# -------------------------------
# Step 1: Extract Text from the PDF
# -------------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

pdf_path = "./palantir_q4.pdf"  # Replace with your PDF file path
full_text = extract_text_from_pdf(pdf_path)

# -------------------------------
# Step 2: Split Text into Chunks
# -------------------------------
def split_text(text, max_length=500):
    words = text.split()
    chunks = []
    chunk = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(" ".join(chunk))
            chunk = [word]
            current_length = len(word) + 1
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

chunks = split_text(full_text, max_length=500)

# -------------------------------
# Step 3: Vectorize Chunks and Build FAISS Index
# -------------------------------
embedder = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedder.encode(chunks)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def retrieve_relevant_chunks(query, k=5):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    # Combine the retrieved chunks into a single context string
    relevant_chunks = [chunks[i] for i in indices[0]]
    return "\n".join(relevant_chunks)

# -------------------------------
# Step 4: Initialize Groq API and Define CrewAI Agents
# -------------------------------
# Set Groq API key
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual Groq API key

# Initialize Groq-powered LLM (e.g., using the "mixtral-8x7b" model)
llm_groq = LLM(model="groq/llama3-8b-8192")

# Define agents for revenue, profit, and cash flow
revenue_agent = Agent(
    role="Revenue Extraction Specialist",
    goal="Extract revenue figures including quarterly and full-year revenue values, YoY and QoQ growth percentages, and revenue segments.",
    backstory="An expert in financial data analysis focused on revenue trends.",
    allow_delegation=False,
    verbose=True,
    llm=llm_groq
)

# profit_agent = Agent(
#     role="Profit Extraction Specialist",
#     goal="Extract profit figures including quarterly and full-year net income, operating income, and profit margins.",
#     backstory="An expert in analyzing corporate profitability.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm_groq
# )

# cash_flow_agent = Agent(
#     role="Cash Flow Extraction Specialist",
#     goal="Extract cash flow metrics including quarterly and full-year operating cash flow and free cash flow.",
#     backstory="An expert in liquidity and cash flow analysis.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm_groq
# )

# -------------------------------
# Step 5: Retrieve Relevant Context for Each Financial Metric
# -------------------------------
revenue_context = retrieve_relevant_chunks("revenue figures quarterly full-year YoY QoQ growth revenue segments", k=5)
# profit_context = retrieve_relevant_chunks("net income operating income profit margins quarterly full-year", k=5)
# cash_flow_context = retrieve_relevant_chunks("operating cash flow free cash flow quarterly full-year", k=5)

# -------------------------------
# Step 6: Define CrewAI Tasks with the Retrieved Context
# -------------------------------
revenue_task = Task(
    description=(
        f"Given the following extracted context from a financial report:\n\n{revenue_context}\n\n"
        "Extract revenue figures, including quarterly and full-year revenue values rounded to nearest million, YoY and QoQ growth percentages, and any relevant revenue segments.\n"
        "Return the data strictly in JSON format as follows:\n"
        '{\n  "Revenue": {\n    "Q4_2024": {"Amount": "X Million", "YoY_Growth": "X%", "QoQ_Growth": "X%"},\n'
        '    "FY_2024": {"Amount": "X Million", "YoY_Growth": "X%"},\n'
        '    "Segments": {"U.S_Commercial": "X", "Government": "X"}\n  }\n}'
    ),
    agent=revenue_agent,
    expected_output="Valid JSON format with revenue figures"
)

# profit_task = Task(
#     description=(
#         f"Given the following extracted context from a financial report:\n\n{profit_context}\n\n"
#         "Extract profit figures, including quarterly and full-year net income, operating income, and their respective profit margins.\n"
#         "Return the data in JSON format as follows:\n"
#         '{\n  "Profitability": {\n    "Net_Income": {\n'
#         '      "Q4_2024": {"Amount": "X", "Net_Margin": "X%"},\n'
#         '      "FY_2024": {"Amount": "X", "Net_Margin": "X%"}\n    },\n'
#         '    "Operating_Income": {\n      "Q4_2024": {"Amount": "X", "Margin": "X%"},\n'
#         '      "FY_2024": {"Amount": "X", "Margin": "X%"}\n    }\n  }\n}'
#     ),
#     agent=profit_agent,
#     expected_output="Valid JSON format with profit figures"
# )

# cash_flow_task = Task(
#     description=(
#         f"Given the following extracted context from a financial report:\n\n{cash_flow_context}\n\n"
#         "Extract cash flow data, including quarterly and full-year operating cash flow and free cash flow.\n"
#         "Return the data in JSON format as follows:\n"
#         '{\n  "Cash_Flow": {\n    "Operating_Cash_Flow": {"Q4_2024": "X", "FY_2024": "X"},\n'
#         '    "Free_Cash_Flow": {"Q4_2024": "X", "FY_2024": "X"}\n  }\n}'
#     ),
#     agent=cash_flow_agent,
#     expected_output="Valid JSON format with cash flow figures"
# )

# -------------------------------
# Step 7: Create Crew and Run the Pipeline
# -------------------------------
crew = Crew(
    agents=[revenue_agent,],
    tasks=[revenue_task,]
)

results = crew.kickoff()

# Convert aggregated results to JSON and print
final_json = json.dumps(results, indent=2)
print(final_json)
