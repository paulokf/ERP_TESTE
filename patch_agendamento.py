file_path = "./backend/app/routers/core_api.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

nova_regra = """
            # Regra Anti-Duplicação: Impede clones do mesmo plantão
            if a.medico_id == agd.medico_id and a.room_id == agd.room_id:
                raise HTTPException(
                    status_code=400, 
                    detail="Este médico já está escalado para esta sala neste exato dia."
                )

            # Regra de Exclusividade do Médico"""

# Injeta a nova regra logo acima da Regra do Médico
if "# Regra Anti-Duplicação" not in content:
    content = content.replace("            # Regra de Exclusividade do Médico", nova_regra.lstrip('\n'))
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Correção aplicada com sucesso no core_api.py!")
else:
    print("⚠️ A correção já havia sido aplicada anteriormente.")
