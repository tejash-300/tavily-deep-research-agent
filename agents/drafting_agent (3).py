import logging
from abc import ABC, abstractmethod
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

class Agent(ABC):
    @abstractmethod
    def execute(self, query: dict) -> dict:
        pass

class DraftingAgent(Agent):
    def __init__(self, retriever, openai_api_key: str):
        self.chain = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=openai_api_key, temperature=0.0),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    def execute(self, query: dict) -> dict:
        try:
            question = query.get("question", "")
            logging.info(f"[DraftingAgent] Generating answer for: {question}")
            result = self.chain({"query": question})
            query["answer"] = result["result"]
            query["source_documents"] = result["source_documents"]
        except Exception as e:
            logging.error(f"[DraftingAgent] Error: {e}", exc_info=True)
            query["answer"] = ""
            query["source_documents"] = []
        return query
