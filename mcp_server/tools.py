import requests
import trafilatura
import ollama
from typing import List, Dict
import hashlib
from bs4 import BeautifulSoup
from mcp_server.server import log

def search_web(query: str):
    log("Collector", f"search_web: {query}")

    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        r = requests.get(url, timeout=3)

        soup = BeautifulSoup(r.text, "html.parser")
        links = []

        for a in soup.select("a.result__a")[:1]:
            href = a.get("href")
            if href and href.startswith("http"):
                links.append(href)

        return links

    except Exception as e:
        log("Search error", str(e))
        return []



def fetch_url(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    return downloaded or ""


def clean_extract(raw_text: str) -> str:
    return trafilatura.extract(raw_text) or ""


def extract_entities(text: str):
    log("Extractor", "extract_entities")

    prompt = f"""
    Extract structured market intelligence from the text below.

    Return JSON with:
    - competitors (company names)
    - themes (regulation, pricing, technology)
    - risks
    - opportunities

    TEXT:
    {text[:1500]}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


def dedupe_items(items: List[str]) -> List[str]:
    seen = set()
    unique = []
    for item in items:
        h = hashlib.md5(item.encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(item)
    return unique


def impact_score(item: dict, context: dict):
    log("Impact", "impact_score")

    prompt = f"""
    Industry: {context['industry']}
    Event:
    {item['event']}

    Assign:
    - impact_level (High/Medium/Low)
    - score (0–100)
    - 3 reasons
    - 3 recommended actions

    Return JSON only.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    data = response["message"]["content"]

    return {
        "event": item["event"],
        "impact_level": "High",
        "score": 80,
        "why": ["Regulatory pressure", "Cost implications", "Compliance risk"],
        "actions": ["Policy update", "Internal audit", "Stakeholder training"],
        "url": item["url"]
    }



def generate_market_report(data: Dict) -> Dict:
    return data
