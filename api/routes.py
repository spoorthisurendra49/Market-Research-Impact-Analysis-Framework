from fastapi import APIRouter
from orchestrator.graph import build_graph

router = APIRouter()

# Build the agent graph ONCE
graph = build_graph()

REPORT_STORE = {}

@router.post("/analyze")
def analyze(payload: dict):
    result = graph.invoke(payload)
    report_id = "R001"
    REPORT_STORE[report_id] = result
    return {
        "report_id": report_id,
        "report": result
    }

@router.post("/chat")
def chat(payload: dict):
    report = REPORT_STORE.get(payload["report_id"])
    if not report:
        return {"error": "Invalid report_id"}

    import ollama
    prompt = f"""
    Answer strictly using the report below.
    If not found, say "Not available in report".

    REPORT:
    {report}

    QUESTION:
    {payload['question']}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response["message"]["content"],
        "citations": report.get("sources", [])
    }

@router.get("/health")
def health():
    return {"status": "ok"}
