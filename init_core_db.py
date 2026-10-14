import asyncio
from app.database import engine, Base
from app.models.core_models import PacienteModel, AgendamentoModel
async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(init())
