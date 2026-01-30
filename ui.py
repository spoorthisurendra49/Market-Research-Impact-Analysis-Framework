import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Market Intelligence AI",
    layout="wide"
)

st.title("📊 Market Research & Impact Analysis Framework (Agentic AI + MCP)")
st.caption("Agentic AI System powered by LangGraph + Ollama")

# -------------------------
# Sidebar Inputs
# -------------------------
st.sidebar.header("Analysis Inputs")

industry = st.sidebar.text_input("Industry", value="NBFC")
from_date = st.sidebar.date_input("From Date")
to_date = st.sidebar.date_input("To Date")

run_analysis = st.sidebar.button("🚀 Generate Report")

# -------------------------
# Generate Report
# -------------------------
if run_analysis:
    with st.spinner("Running agentic analysis..."):
        payload = {
            "industry": industry,
            "from": str(from_date),
            "to": str(to_date)
        }

        response = requests.post(f"{API_BASE}/analyze", json=payload)

        if response.status_code == 200:
            data = response.json()
            st.session_state["report"] = data["report"]
            st.session_state["report_id"] = data["report_id"]
            st.success("Report generated successfully!")
        else:
            st.error("Failed to generate report")

# -------------------------
# Display Report
# -------------------------
if "report" in st.session_state:
    report = st.session_state["report"]

    st.header("📌 Executive Summary")
    st.write(report.get("summary", ""))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠️ Risks")
        for r in report.get("risks", []):
            st.write(f"- {r}")

    with col2:
        st.subheader("🌱 Opportunities")
        for o in report.get("opportunities", []):
            st.write(f"- {o}")

    st.subheader("📍 Impact Radar")
    for item in report.get("impact_radar", []):
        with st.expander(item.get("event", "Impact Event")):
            st.write(f"**Impact Level:** {item.get('impact_level')}")
            st.write(f"**Score:** {item.get('score')}")
            st.write("**Why:**")
            for w in item.get("why", []):
                st.write(f"- {w}")
            st.write("**Actions:**")
            for a in item.get("actions", []):
                st.write(f"- {a}")

    st.subheader("🗺️ 90-Day Action Plan")
    plan = report.get("90_day_plan", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**0–30 Days**")
        for i in plan.get("0_30", []):
            st.write(f"- {i}")
    with col2:
        st.write("**30–60 Days**")
        for i in plan.get("30_60", []):
            st.write(f"- {i}")
    with col3:
        st.write("**60–90 Days**")
        for i in plan.get("60_90", []):
            st.write(f"- {i}")

# -------------------------
# Chat Section
# -------------------------
if "report_id" in st.session_state:
    st.header("💬 Ask Questions About the Report")

    question = st.text_input("Enter your question")

    if st.button("Ask"):
        payload = {
            "report_id": st.session_state["report_id"],
            "question": question
        }

        response = requests.post(f"{API_BASE}/chat", json=payload)

        if response.status_code == 200:
            ans = response.json()
            st.write("**Answer:**")
            st.write(ans["answer"])
        else:
            st.error("Failed to get answer")
