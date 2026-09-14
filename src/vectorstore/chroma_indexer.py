from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


class RegulatoryVectorStore:
    """
    Mock Vector Store pre-seeded with Australian Environment Protection and 
    Biodiversity Conservation Act 1999 (EPBC Act) regulatory guidelines.
    """
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = Chroma(
            collection_name="aus_epbc_regulations",
            embedding_function=self.embeddings
        )
        self._seed_sample_regulations()

    def _seed_sample_regulations(self):
        sample_chunks = [
            Document(
                page_content="Under the Environment Protection and Biodiversity Conservation Act 1999 (EPBC Act), any mining action likely to have a significant impact on Matters of National Environmental Significance (MNES) requires formal referral to the Australian Commonwealth Environment Minister prior to project commencement.",
                metadata={"source": "EPBC_Act_1999_Part3", "jurisdiction": "Commonwealth of Australia"}
            ),
            Document(
                page_content="Western Australia Environmental Protection Authority (EPA) Part IV requires mining operators to submit a detailed Environmental Management Plan (EMP) addressing groundwater extraction, stygofauna habitats, and rehabilitation surety bonds.",
                metadata={"source": "WA_EPA_PartIV", "jurisdiction": "Western Australia"}
            ),
            Document(
                page_content="National Greenhouse and Energy Reporting (NGER) Act 2007 mandates facilities emitting over 25 kilotonnes of CO2 equivalent per annum to register and report Scope 1 and Scope 2 emissions by October 31 annually to the Clean Energy Regulator.",
                metadata={"source": "NGER_Act_2007_Sec19", "jurisdiction": "Commonwealth of Australia"}
            )
        ]
        self.vector_store.add_documents(sample_chunks)

    def get_retriever(self, k: int = 3):
        return self.vector_store.as_retriever(search_kwargs={"k": k})
