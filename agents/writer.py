def writer_agent(state: dict, tools: dict):
    impacts = state.get("impacts", [])[:10]

    competitors = set()
    for item in state.get("extracted", []):
        ent = item.get("entities", {})
        if isinstance(ent, dict):
            for c in ent.get("competitors", []):
                competitors.add(c)

    industry = state.get("industry", "Target")

    report = {
        "summary": f"Market intelligence report for {industry} industry.",
        "drivers": ["Regulatory change", "Digital adoption", "Competitive pressure"],
        "competitors": list(competitors)[:5],
        "impact_radar": impacts,
        "opportunities": [
            "Digital lending expansion",
            "Compliance automation",
            "New market segments",
            "Strategic partnerships",
            "Product diversification"
        ],
        "risks": [
    "RBI regulatory tightening",
    "Higher compliance costs",
    "Frequent policy changes",
    "Audit and reporting burden",
    "Penalty risk for non-compliance"
],

        "90_day_plan": {
            "0_30": ["Compliance audit", "Risk assessment"],
            "30_60": ["Process optimization", "Technology upgrade"],
            "60_90": ["Automation rollout", "Performance review"]
        },
        "sources": [i["url"] for i in impacts if "url" in i]
    }

    return tools["generate_market_report"](report)
