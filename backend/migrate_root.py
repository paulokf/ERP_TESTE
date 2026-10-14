import asyncio
from app.database import engine, Base
from app.models.core_models import PacienteModel, AgendamentoModel, EvolucaoPEPModel, LaudoModel

async def run_migration():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tabelas integradas com sucesso no PostgreSQL (Raiz)!")

if __name__ == "__main__":
    asyncio.run(run_migration())
