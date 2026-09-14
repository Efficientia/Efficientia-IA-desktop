import os
from pathlib import Path
from src.app.config import GEMINI_API_KEY
from langchain.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def _obter_caminho_faq() -> str:
    _env_faq = os.getenv("FAQ")
    candidatos = [
        Path(_env_faq) if _env_faq else None,
        Path(__file__).resolve().parent.parent.parent / "data" / "FAQ.md",
        Path(__file__).resolve().parent.parent.parent / "src" / "data" / "FAQ.md",
        Path("src/data/FAQ.md"),
        Path("data/FAQ.md"),
    ]
    for c in candidatos:
        if c and c.exists():
            return str(c)
    return str(Path(__file__).resolve().parent.parent.parent / "data" / "FAQ.md")

MD_PATH = _obter_caminho_faq()
_faiss_db = None

def _get_vectorstore():
    global _faiss_db
    if _faiss_db is None:
        caminho = _obter_caminho_faq()
        if not Path(caminho).exists():
            return None
        loader = TextLoader(caminho, encoding='utf-8')
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=GEMINI_API_KEY,
        )
        _faiss_db = FAISS.from_documents(chunks, embeddings)
    return _faiss_db

@tool
def faq_retriever(query: str) -> str:
    """Busca informações no documento de FAQ (MD) para responder a dúvidas do usuário sobre o sistema e suas especificações."""
    try:
        db = _get_vectorstore()
        if db is None:
            return "Documento de FAQ não encontrado no sistema."
        results = db.similarity_search(query, k=6)
        if not results:
            return "Não encontrei essa informação no FAQ do sistema."
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        return f"Erro ao consultar FAQ: {str(e)}"