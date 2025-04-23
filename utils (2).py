import os
import openai

def chunk_text(text: str, max_chars: int = 1000) -> list[str]:
    """Split text into ≤ max_chars chunks, preserving paragraph breaks."""
    paras, chunks, cur = text.split("\n\n"), [], ""
    for p in paras:
        if len(cur) + len(p) + 2 <= max_chars:
            cur = (cur + "\n\n" + p).strip() if cur else p
        else:
            if cur:
                chunks.append(cur)
            if len(p) <= max_chars:
                cur = p
            else:
                for i in range(0, len(p), max_chars):
                    chunks.append(p[i : i + max_chars])
                cur = ""
    if cur:
        chunks.append(cur)
    return chunks

def embed_text(text: str) -> list[float]:
    """Get text embedding via OpenAI’s text-embedding-ada-002."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    resp = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return resp["data"][0]["embedding"]
