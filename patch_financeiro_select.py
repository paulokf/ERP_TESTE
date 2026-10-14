import shutil, datetime, sys

ARQ = "frontend/src/app/dashboard/financeiro/page.tsx"
src = open(ARQ, encoding="utf-8").read()
bak = f"{ARQ}.bak-select-{datetime.datetime.now():%Y%m%d-%H%M%S}"
shutil.copy(ARQ, bak)
print(f"[OK] Backup: {bak}")

# Confere que o patch de criterios ja rodou
if "criteriosEntrada" not in src:
    print("[ERRO] O patch_financeiro.py (criteriosEntrada) nao foi aplicado. Rode-o antes."); sys.exit(1)

trocas = [
    # (linha 260) valor inicial do estado
    ("const [tipoMovimentacao, setTipoMovimentacao] = useState(TIPOS_ENTRADA[0]);",
     "const [tipoMovimentacao, setTipoMovimentacao] = useState(CRITERIOS_ENTRADA_SEED[0]);"),
    # (linha 280) reset ao abrir novo lancamento
    ("setTipoMovimentacao(TIPOS_ENTRADA[0]);",
     "setTipoMovimentacao(criteriosEntrada[0]);"),
    # (linha 928) botao RECEITA
    ("onClick={() => { setCategoria('RECEITA'); setTipoMovimentacao(TIPOS_ENTRADA[0]); }}",
     "onClick={() => { setCategoria('RECEITA'); setTipoMovimentacao(criteriosEntrada[0]); }}"),
    # (linha 939) botao DESPESA
    ("onClick={() => { setCategoria('DESPESA'); setTipoMovimentacao(TIPOS_SAIDA[0]); }}",
     "onClick={() => { setCategoria('DESPESA'); setTipoMovimentacao(criteriosSaida[0]); }}"),
    # (linha 998) o map do select
    ("(categoria === 'RECEITA' ? TIPOS_ENTRADA : TIPOS_SAIDA).map(opt =>",
     "(categoria === 'RECEITA' ? criteriosEntrada : criteriosSaida).map(opt =>"),
]

for antigo, novo in trocas:
    if antigo not in src:
        print(f"[AVISO] Nao encontrei (pode ja estar trocado): {antigo[:60]}...")
        continue
    src = src.replace(antigo, novo, 1)
    print(f"[OK] Trocado: {antigo[:55]}...")

open(ARQ, "w", encoding="utf-8").write(src)
print("[OK] Arquivo salvo. Select agora usa os criterios das planilhas.")
