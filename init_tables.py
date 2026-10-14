import asyncio
from app.database import engine, Base
from app.models.core_models import PacienteModel, AgendamentoModel, EvolucaoPEPModel, LaudoModel

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas baseadas em Core Models garantidas!")

asyncio.run(init())
