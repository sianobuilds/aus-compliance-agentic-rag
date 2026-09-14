from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state.agent_state import ComplianceGraphState
from src.core.config import get_settings

settings = get_settings()


def generate_compliance_report(state: ComplianceGraphState) -> ComplianceGraphState:
    question = state["question"]
    context_chunks = state.get("filtered_documents", [])

    if not context_chunks:
        return {
            "generation": "Insufficient statutory context found under Commonwealth or State legislation to safely determine compliance.",
            "compliance_flag": "INSUFFICIENT_DATA"
        }

    formatted_context = "\n\n".join(context_chunks)
    llm = ChatOpenAI(model=settings.PRIMARY_MODEL, temperature=0.1)

    prompt = ChatPromptTemplate.from_template(
        "You are a Senior Regulatory Counsel specializing in Australian Commonwealth and State environmental mandates.\n"
        "Rely strictly on the provided statutory context to formulate your compliance assessment.\n"
        "Context:\n{context}\n\n"
        "Corporate Inquiry: {question}\n\n"
        "Structure your response with:\n"
        "1. Executive Summary & Applicable Acts\n"
        "2. Mandatory Obligations & Thresholds\n"
        "3. Recommended Legal Action"
    )

    rag_chain = prompt | llm
    response = rag_chain.invoke({"context": formatted_context, "question": question})

    return {
        "generation": response.content,
        "compliance_flag": "ACTION_REQUIRED" if "requires" in response.content.lower() else "COMPLIANT"
    }
