import ollama

def collector_agent(state: dict, tools: dict):
    prompt = f"""
    You are a senior market research analyst.

    Industry: {state['industry']}
    Date range: {state['from']} to {state['to']}

    Generate 6 HIGH-QUALITY search queries covering:
    - regulation
    - competitors
    - pricing
    - market trends
    - risks
    - opportunities

    Output ONLY as comma-separated queries.
    """

    # 🔴 MISSING STEP — LLM CALL
    

    queries = [
    f"{state['industry']} regulatory risks India",
    f"{state['industry']} market trends India",
    f"{state['industry']} opportunities India",
]


    urls = []
    for q in queries:
        try:
            urls.extend(tools["search_web"](q))
        except Exception as e:
            print("Search error:", e)

    return {
        "urls": tools["dedupe_items"](urls)
    }
