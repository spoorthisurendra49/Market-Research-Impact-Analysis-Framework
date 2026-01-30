def extractor_agent(state: dict, tools: dict):
    extracted = []

    for url in state["urls"]:
        try:
            raw = tools["fetch_url"](url)
            clean = tools["clean_extract"](raw)

            entities = tools["extract_entities"](clean)

            # 🔒 SAFETY: enforce dict shape
            if not isinstance(entities, dict):
                entities = {
                    "competitors": [],
                    "themes": [],
                    "risks": [],
                    "opportunities": []
                }

            extracted.append({
                "url": url,
                "text": clean,
                "entities": entities
            })

        except Exception as e:
            print("Extractor error:", e)

    return {"extracted": extracted}
