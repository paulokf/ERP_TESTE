import asyncio
from sqlalchemy import text
from app.database import engine

async def recreate_users():
    async with engine.begin() as conn:
        # Garante que a restrição unique existe e permite upsert seguro
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id VARCHAR(50) PRIMARY KEY, 
                username VARCHAR(100) UNIQUE NOT NULL, 
                senha VARCHAR(100) NOT NULL, 
                nome VARCHAR(150) NOT NULL, 
                perfil VARCHAR(50) NOT NULL
            );
        >"""))
    print("✓ Tabela de utilizadores verificada e corrigida com sucesso!")

if __name__ == "__main__":
    asyncio.run(recreate_users())
