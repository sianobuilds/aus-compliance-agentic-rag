from src.state.agent_state import ComplianceGraphState
from src.vectorstore.chroma_indexer import RegulatoryVectorStore

vector_db = RegulatoryVectorStore()
retriever = vector_db.get_retriever(k=3)


def retrieve_regulations(state: ComplianceGraphState) -> ComplianceGraphState:
    query = state.get("rephrased_query") or state["question"]
    docs = retriever.invoke(query)
    doc_contents = [doc.page_content for doc in docs]
    
    return {
        "documents": doc_contents,
        "retry_count": state.get("retry_count", 0)
    }
