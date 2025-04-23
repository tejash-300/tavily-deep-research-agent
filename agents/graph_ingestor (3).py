# agents/graph_ingestor.py

import logging
from langgraph_sdk import get_sync_client
from utils import chunk_text, embed_text
from agents.credibility_scorer import CredibilityScorer
import httpx

class Agent:
    def execute(self, query: dict) -> dict:
        raise NotImplementedError

class GraphIngestorWithCred(Agent):
    def __init__(self, endpoint: str, api_key: str):
        # You can keep passing whatever endpoint you like here;
        # we’ll catch errors at runtime.
        self.client = get_sync_client(url=endpoint, api_key=api_key)
        self.scorer = CredibilityScorer()

    def execute(self, query: dict) -> dict:
        docs = query.get("docs", [])

        for doc in docs:
            # 1) Score credibility
            scored = self.scorer.execute(doc)
            doc_id = scored["url"]

            # 2) Try storing metadata
            try:
                self.client.store.put_item(
                    ["documents", "meta"],
                    doc_id,
                    {
                        "url":         scored["url"],
                        "title":       scored.get("title", ""),
                        "language":    scored.get("language", ""),
                        "credibility": scored["credibility"]
                    }
                )
            except Exception as e:
                logging.warning(f"[GraphIngestor] Skipping metadata for {doc_id}: {e}")
                # Skip embedding/chunking if metadata fails
                continue

            # 3) Chunk & embed, then store each chunk
            text_to_chunk = scored.get("translated_text") or scored.get("text", "")
            for idx, chunk in enumerate(chunk_text(text_to_chunk)):
                try:
                    vec = embed_text(chunk)
                    self.client.store.put_item(
                        ["documents", "chunks"],
                        f"{doc_id}#{idx}",
                        {
                            "content":   chunk,
                            "embedding": vec
                        }
                    )
                except Exception as e:
                    logging.warning(
                        f"[GraphIngestor] Skipping chunk {doc_id}#{idx}: {e}"
                    )
                    # move on to next chunk

        return query
