# agents/graph_retriever.py

import os
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from utils import chunk_text

class Agent:
    def execute(self, query: dict) -> dict:
        raise NotImplementedError

class GraphRetriever(Agent):
    def __init__(self, graph_client=None, persist_dir="graph_chroma"):
        self.graph_client = graph_client
        embed_fn = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.vdb = Chroma(persist_directory=persist_dir, embedding_function=embed_fn)

    def execute(self, query: dict) -> dict:
        docs = []
        if self.graph_client:
            entries = self.graph_client.store.search(
                namespace=["documents","chunks"], limit=1000
            )
            for e in entries:
                docs.append(Document(
                    page_content=e["value"]["content"],
                    metadata={"source_key": e["key"]}
                ))
        else:
            for doc in query.get("docs", []):
                for idx, chunk in enumerate(chunk_text(doc.get("text",""))):
                    docs.append(Document(
                        page_content=chunk,
                        metadata={"source": doc.get("url")}
                    ))

        # add to Chroma
        self.vdb.add_documents(docs)

        # ← HERE’S THE FIX: use .as_retriever() so you get a BaseRetriever
        query["retriever"] = self.vdb.as_retriever()
        return query
