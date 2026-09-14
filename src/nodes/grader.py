from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from src.state.agent_state import ComplianceGraphState
from src.core.config import get_settings

settings = get_settings()


class GradeAssessment(BaseModel):
    binary_score: str = Field(
        description="Relevance score: 'yes' if document contains Australian regulatory context for the inquiry, else 'no'"
    )


def grade_retrieved_documents(state: ComplianceGraphState) -> ComplianceGraphState:
    question = state["question"]
    docs = state["documents"]

    llm = ChatOpenAI(model=settings.GRADER_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(GradeAssessment)

    prompt = ChatPromptTemplate.from_template(
        "You are an Australian compliance legal officer evaluating document relevance.\n"
        "Inquiry: {question}\n"
        "Retrieved Document Snippet: {context}\n"
        "Assess whether this document contains regulatory information to address the inquiry. Return 'yes' or 'no'."
    )

    grader_chain = prompt | structured_llm
    relevant_docs = []

    for doc in docs:
        score = grader_chain.invoke({"question": question, "context": doc})
        if score.binary_score.lower() == "yes":
            relevant_docs.append(doc)

    return {"filtered_documents": relevant_docs}
