import whois, requests, xmltodict
from urllib.parse import urlparse
from datetime import datetime
from textblob import TextBlob
from transformers import pipeline

# Zero‑shot fake vs real
_fake_news_clf = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

class Agent:
    def execute(self, query: dict) -> dict:
        raise NotImplementedError

class CredibilityScorer(Agent):
    def execute(self, query: dict) -> dict:
        url, text = query.get("url", ""), query.get("text", "")
        dom = urlparse(url).netloc

        # Domain age
        try:
            w = whois.whois(dom)
            dates = w.creation_date
            date  = dates[0] if isinstance(dates, list) else dates
            age_yrs = (datetime.now() - date).days / 365
        except:
            age_yrs = None

        # Alexa rank
        try:
            resp = requests.get(f"https://data.alexa.com/data?cli=10&url={dom}")
            doc  = xmltodict.parse(resp.text)
            alexa = int(doc["ALEXA"]["SD"][1]["POPULARITY"]["@TEXT"])
        except:
            alexa = None

        # Sentiment
        polarity = TextBlob(text).sentiment.polarity

        # Fake‑news
        result = _fake_news_clf(text[:512], candidate_labels=["fake", "real"])
        fn_label = result["labels"][0]
        fn_score = float(result["scores"][0])

        query["credibility"] = {
            "https":          urlparse(url).scheme == "https",
            "domain_age_yrs": age_yrs,
            "alexa_rank":     alexa,
            "sentiment":      polarity,
            "fake_news":      {"label": fn_label, "score": fn_score}
        }
        return query
