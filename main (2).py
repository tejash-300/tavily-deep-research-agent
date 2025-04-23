import os
from dotenv import load_dotenv

from agents.research_agent    import ResearchAgent
from agents.translation_agent import TranslationAgent
from agents.graph_ingestor    import GraphIngestorWithCred
from agents.graph_retriever   import GraphRetriever
from agents.drafting_agent    import DraftingAgent

from langgraph.sync import get_sync_client

# Load API keys from .env
load_dotenv()
TAVILY_KEY    = os.getenv("TAVILY_API_KEY")
LANGGRAPH_KEY = os.getenv("LANGGRAPH_API_KEY")
OPENAI_KEY    = os.getenv("OPENAI_API_KEY")
assert all([TAVILY_KEY, LANGGRAPH_KEY, OPENAI_KEY]), "Missing one or more API keys"

# 1) Research using Tavily’s extract API
qry = {
    "seed_urls": [
        "https://en.wikipedia.org/wiki/AI_ethics",
        "https://www.brookings.edu/research/principles-for-accountable-algorithms/",
        "https://www.technologyreview.com/2023/09/05/ai-ethics/"
    ],
}
qry = ResearchAgent(api_key=TAVILY_KEY).execute(qry)

# 2) Translate each snippet to English
for doc in qry["docs"]:
    translated = TranslationAgent().execute({"text": doc["text"]})
    doc["text"] = translated["translated_text"]

# 3) Ingest into LangGraph (with credibility scoring)
#    Replace the URL below with your actual LangGraph endpoint.
GraphIngestorWithCred(
    endpoint="https://YOUR_LANGGRAPH_URL",   # e.g. https://api.kairon.langgraph.cloud
    api_key=LANGGRAPH_KEY
).execute(qry)

# 4) Build a sync-mode graph client and create your retriever
graph_client = get_sync_client(
    url="https://YOUR_LANGGRAPH_URL",        # same URL here
    api_key=LANGGRAPH_KEY
)
gr        = GraphRetriever(graph_client=graph_client)
qry       = gr.execute(qry)
retriever = qry["retriever"]

# 5) Draft your answer
draft_q = {
    "question":  "What are the key ethical concerns around AI according to recent discussions?",
    "retriever": retriever
}
out = DraftingAgent(retriever, openai_api_key=OPENAI_KEY).execute(draft_q)

# 6) Print
print("Answer:\n", out["answer"])
print("\nSources:")
for src in out["source_documents"]:
    key     = src.metadata.get("source_key") or src.metadata.get("source", "unknown")
    snippet = src.page_content.replace("\n", " ")[:200]
    print(f"- {key}: {snippet}…")
