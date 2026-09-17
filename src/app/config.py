import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR aponta para migracao_fastAPI/. Montado a partir da localização
# do próprio arquivo: não depende da pasta de onde você rodou o uvicorn.
BASE_DIR     = Path(__file__).resolve().parent
PROJECT_DIR  = BASE_DIR.parent
DATA_DIR     = PROJECT_DIR / "data"

load_dotenv(BASE_DIR / ".env")
load_dotenv(PROJECT_DIR / ".env")

_faq_env = os.getenv("FAQ")
if _faq_env and Path(_faq_env).exists():
    FAQ_PATH = Path(_faq_env)
elif (DATA_DIR / "FAQ.md").exists():
    FAQ_PATH = DATA_DIR / "FAQ.md"
elif (PROJECT_DIR / "src" / "data" / "FAQ.md").exists():
    FAQ_PATH = PROJECT_DIR / "src" / "data" / "FAQ.md"
else:
    FAQ_PATH = DATA_DIR / "FAQ.md"


GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY  = os.getenv("GOOGLE_API_KEY", GEMINI_API_KEY)
DATABASE_URL    = os.getenv("DATABASE_URL")
MONGO_URI     = os.getenv("MONGO_URI")
MONGO_DB_NAME   = os.getenv("MONGO_DB_NAME", "eficientia_db")
MONGO_IP        = os.getenv("MONGO_IP")
MONGO_USER      = os.getenv("MONGO_USER")
MONGO_PASSWORD  = os.getenv("MONGO_PASSWORD")

OBRIGATORIAS = {
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "GROQ_API_KEY":   GROQ_API_KEY,
    "GOOGLE_API_KEY": GOOGLE_API_KEY,
    "DATABASE_URL":   DATABASE_URL,
    "MONGO_URI":      MONGO_URI,
    "MONGO_DB_NAME":  MONGO_DB_NAME,
    "MONGO_IP":       MONGO_IP,
    "MONGO_USER":     MONGO_USER,
    "MONGO_PASSWORD": MONGO_PASSWORD,
}


def validar_config() -> list[str]:
    """Devolve a lista de problemas de configuração (vazia = tudo certo)."""
    problemas = []
    for nome, valor in OBRIGATORIAS.items():
        if not valor:
            problemas.append(f"Variável ausente no .env: {nome}")
    if not FAQ_PATH.exists():
        problemas.append(f"FAQ não encontrado em: {FAQ_PATH}")
    return problemas