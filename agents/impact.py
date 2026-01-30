import ollama

def impact_agent(state: dict, tools: dict):
    impacts = []

    for item in state["extracted"]:
        prompt = f"""
        Industry: {state['industry']}
        Event:
        {item['text'][:500]}

        Assign:
        - Impact Level (High/Medium/Low)
        - Score (0–100)
        - 2 reasons
        - 2 actions

        Output as JSON.
        """

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        impact = tools["impact_score"](
            {
                "event": item["text"][:120],
                "url": item["url"],
                "llm_output": response["message"]["content"]
            },
            context={"industry": state["industry"]}
        )

        impacts.append(impact)

    return {"impacts": impacts}
