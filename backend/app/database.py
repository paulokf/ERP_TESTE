import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Resgata a URL do Docker Compose ou usa o padrão
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres:5432/clinicore")

# Criação do Motor Assíncrono
engine = create_async_engine(DATABASE_URL, echo=False)

# [FIX CIRÚRGICO]: class_=AsyncSession garante que a sessão suporta "async with" e "await"
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

# Gerador de sessão para injeção de dependência nas rotas da API (FastAPI)
async def get_db():
    async with SessionLocal() as session:
        yield session
