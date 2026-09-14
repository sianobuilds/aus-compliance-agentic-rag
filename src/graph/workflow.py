from langgraph.graph import StateGraph, END
from src.state.agent_state import ComplianceGraphState
from src.nodes.retriever import retrieve_regulations
from src.nodes.grader import grade_retrieved_documents
from src.nodes.generator import generate_compliance_report
from src.nodes.rewriter import rewrite_compliance_query
from src.core.config import get_settings

settings = get_settings()


def evaluate_routing_decision(state: ComplianceGraphState) -> str:
    filtered_docs = state.get("filtered_documents", [])
    retry_count = state.get("retry_count", 0)

    if not filtered_docs:
        if retry_count < settings.MAX_RETRY_LIMIT:
            return "rewrite_query"
        return "generate_fallback"
    return "generate_report"


def create_compliance_graph():
    builder = StateGraph(ComplianceGraphState)

    builder.add_node("retrieve", retrieve_regulations)
    builder.add_node("grade_documents", grade_retrieved_documents)
    builder.add_node("rewrite_query", rewrite_compliance_query)
    builder.add_node("generate_report", generate_compliance_report)

    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "grade_documents")
    
    builder.add_conditional_edges(
        "grade_documents",
        evaluate_routing_decision,
        {
            "rewrite_query": "rewrite_query",
            "generate_report": "generate_report",
            "generate_fallback": "generate_report"
        }
    )
    
    builder.add_edge("rewrite_query", "retrieve")
    builder.add_edge("generate_report", END)

    return builder.compile()

compliance_agent = create_compliance_graph()
