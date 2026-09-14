from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state.agent_state import ComplianceGraphState
from src.core.config import get_settings

settings = get_settings()


def rewrite_compliance_query(state: ComplianceGraphState) -> ComplianceGraphState:
    question = state["question"]
    retry_count = state.get("retry_count", 0)

    llm = ChatOpenAI(model=settings.GRADER_MODEL, temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "You are an Australian environmental law query specialist.\n"
        "The previous query failed to retrieve relevant statutory sections from the EPBC or NGER Acts.\n"
        "Initial inquiry: {question}\n"
        "Generate a semantically enriched query targeted at statutory compliance and corporate legal obligations."
    )

    rewriter_chain = prompt | llm
    result = rewriter_chain.invoke({"question": question})

    return {
        "rephrased_query": result.content,
        "retry_count": retry_count + 1
    }
