# shared_memory.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_shared_memory():
    """
    Creates and returns a FAISS vector store
    with safe default content.
    """

   
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [
        "This is the shared memory for agent orchestration framework.",
        "LangChain agents collaborate using shared vector memory.",
        "This memory stores important intermediate agent information."
    ]

    if not texts:
        raise ValueError("Shared memory texts cannot be empty.")

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings
    )

    return vectorstore
