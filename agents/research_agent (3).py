# agents/research_agent.py

import logging
from abc import ABC, abstractmethod
from tavily import TavilyClient
from tavily.errors import BadRequestError

class Agent(ABC):
    @abstractmethod
    def execute(self, query: dict) -> dict:
        pass

class ResearchAgent(Agent):
    def __init__(self, api_key: str):
        # TavilyClient for both extract and search
        self.client = TavilyClient(api_key=api_key)

    def execute(self, query: dict) -> dict:
        """
        1) If `seed_urls` present, use TavilyClient.extract to fetch raw_content.
        2) Else if `query["query"]` present, use TavilyClient.search.
        Populates query["docs"] = [{"url", "title", "text", "images"(opt)}, ...].
        """
        docs = []
        try:
            seed_urls = query.get("seed_urls", [])
            if seed_urls:
                logging.info(f"[ResearchAgent] Extracting URLs via Tavily: {seed_urls}")
                # Use Tavily's extract API (up to 20 URLs at once)
                resp = self.client.extract(
                    urls=seed_urls,
                    include_images=query.get("include_images", False)
                )
                for item in resp.get("results", []):
                    docs.append({
                        "url":   item.get("url", ""),
                        "title": "",                  # extract() doesn’t return titles
                        "text":  item.get("raw_content", ""),
                        "images": item.get("images", [])
                    })
                # You could also check resp.get("failed_results", []) here

            else:
                terms = query.get("query", "").strip()
                if not terms:
                    raise ValueError(
                        "ResearchAgent requires either 'seed_urls' or a non-empty 'query'"
                    )
                logging.info(f"[ResearchAgent] Searching Tavily for: {terms}")
                resp = self.client.search(
                    query=terms,
                    max_results=query.get("max_results", 10),
                    include_raw_content=True
                )
                for item in resp.get("results", []):
                    docs.append({
                        "url":   item.get("url", ""),
                        "title": item.get("title", ""),
                        "text":  item.get("raw_content", "")
                    })

        except BadRequestError as e:
            logging.error(f"[ResearchAgent] Tavily BadRequestError: {e}", exc_info=True)
        except Exception as e:
            logging.error(f"[ResearchAgent] Unexpected error: {e}", exc_info=True)

        query["docs"] = docs
        return query

