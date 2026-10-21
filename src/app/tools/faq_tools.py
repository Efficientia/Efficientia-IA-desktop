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

def _obter_caminho_faq_nav() -> str:
    _env_faq_nav = os.getenv("FAQ_NAV")
    candidatos = [
        Path(_env_faq_nav) if _env_faq_nav else None,
        Path(__file__).resolve().parent.parent.parent / "data" / "FAQ_NAV.md",
        Path(__file__).resolve().parent.parent.parent / "src" / "data" / "FAQ_NAV.md",
        Path("src/data/FAQ_NAV.md"),
        Path("data/FAQ_NAV.md"),
    ]
    for c in candidatos:
        if c and c.exists():
            return str(c)
    return str(Path(__file__).resolve().parent.parent.parent / "data" / "FAQ_NAV.md")

MD_NAV_PATH = _obter_caminho_faq_nav()
_faiss_nav_db = None

def _obter_cache_dir_faq_nav() -> Path:
    caminho = Path(_obter_caminho_faq_nav())
    return caminho.parent / ".faiss_nav_cache"

def _get_vectorstore_nav():
    global _faiss_nav_db
    if _faiss_nav_db is not None:
        return _faiss_nav_db

    caminho_str = _obter_caminho_faq_nav()
    caminho_path = Path(caminho_str)
    if not caminho_path.exists():
        return None

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GEMINI_API_KEY,
    )

    cache_dir = _obter_cache_dir_faq_nav()
    index_file = cache_dir / "index.faiss"
    pkl_file = cache_dir / "index.pkl"

    # Carrega cache local se existir e for válido
    if index_file.exists() and pkl_file.exists():
        try:
            if index_file.stat().st_mtime >= caminho_path.stat().st_mtime - 1:
                _faiss_nav_db = FAISS.load_local(
                    str(cache_dir),
                    embeddings,
                    allow_dangerous_deserialization=True,
                )
                return _faiss_nav_db
        except Exception:
            pass

    # Chunking semântico estruturado para documentação de navegação/fluxo
    import time
    loader = TextLoader(caminho_str, encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600,
        chunk_overlap=200,
        separators=["\n# ", "\n## ", "\n### ", "\n#### ", "\n---\n", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(docs)

    # Indexação em lotes com tolerância a limites de taxa
    batch_size = 20
    db = None
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        if db is None:
            db = FAISS.from_documents(batch, embeddings)
        else:
            db.add_documents(batch)
        if i + batch_size < len(chunks):
            time.sleep(1.5)

    _faiss_nav_db = db

    # Salva cache local para acelerar startups subsequentes
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        if _faiss_nav_db is not None:
            _faiss_nav_db.save_local(str(cache_dir))
    except Exception:
        pass

    return _faiss_nav_db

@tool
def faq_nav_retriever(query: str) -> str:
    """Busca informações no documento de FAQ de Navegação (FAQ_NAV.md) para responder a dúvidas sobre telas, menus, botões, rotas e navegação no aplicativo mobile e web."""
    try:
        query_limpa = query.strip().strip("\"'").strip()
        if "PERGUNTA_ORIGINAL=" in query_limpa:
            import re
            m = re.search(r"PERGUNTA_ORIGINAL=\[(.*?)\]", query_limpa, flags=re.DOTALL)
            if m:
                query_limpa = m.group(1).strip()
            else:
                query_limpa = query_limpa.split("PERGUNTA_ORIGINAL=", 1)[-1].strip()

        if not query_limpa:
            return "Pergunta vazia para consulta de navegação."

        db = _get_vectorstore_nav()
        if db is None:
            return "Documento de FAQ de navegação não encontrado no sistema."

        results = db.similarity_search(query_limpa, k=5)
        if not results:
            return "Não encontrei essa informação no FAQ de navegação do sistema."

        # Deduplicação preservando ordem
        conteudos_unicos = []
        vistos = set()
        for doc in results:
            txt = doc.page_content.strip()
            if txt not in vistos:
                vistos.add(txt)
                conteudos_unicos.append(txt)

        return "\n\n---\n\n".join(conteudos_unicos)
    except Exception as e:
        return f"Erro ao consultar FAQ de navegação: {str(e)}"