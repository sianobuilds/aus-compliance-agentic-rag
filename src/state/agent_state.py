from typing import List, TypedDict, Optional


class ComplianceGraphState(TypedDict):
    """
    Represents the internal execution state passed between LangGraph nodes.
    """
    question: str
    rephrased_query: Optional[str]
    documents: List[str]
    filtered_documents: List[str]
    generation: Optional[str]
    retry_count: int
    compliance_flag: Optional[str]
