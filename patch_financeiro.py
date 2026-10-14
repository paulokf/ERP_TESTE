import re, shutil, datetime, sys

ARQ = "frontend/src/app/dashboard/financeiro/page.tsx"
src = open(ARQ, encoding="utf-8").read()
bak = f"{ARQ}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
shutil.copy(ARQ, bak)
print(f"[OK] Backup: {bak}")

if "CRITERIOS_ENTRADA_SEED" in src:
    print("[AVISO] Patch ja aplicado."); sys.exit(0)

# ---------- LISTAS DAS PLANILHAS ----------
ENTRADA = [
 "X1 - Dinheiro","XND - NFs debito de diretores","XNC - NFs credito de diretores",
 "XN - Notas do EYE para TDMX","XN1 - Troca de notas entre PJ","X - Cheque/depositos/boletos",
 "XC - Cartao de credito","XD - Cartao de debito","XR1 - Credito c.c.tx (tdmx)",
 "XR2 - Credito c.c. lio (tdmx)","YH - Convenio hospital","YT - Convenio terceiros/diretos",
 "YHV - Credito faturamento de hospital","YTN - Recibos entre hospital-clinica",
 "YTA - Convenio Direto faturado pelo Ana Rosa",
]
SAIDA = [
 "A1 - Salarios","A2 - Pagamento inicial PF/Complemento PF","A3 - Encargos",
 "A4 - Beneficios (VT,VR,VA,PLASAC), Uniforme","A5 - Medicina do Trabalho","A6 - Contabilidade",
 "A7 - Pgtos colab. Externos","A8 - Plano de Saude (diretoria)","A9 - Emprestimo REFRATIVA FUNCIONARIO",
 "AM1 - Medicos","AM2 - Anestesista","AM3 - Instrumentador(a)","AM4 - Assistencia / aux.",
 "AM6 - Repasse de C.D.O.","AM7 - Indicacao de fora","AM8 - Credito e debito de medicos terceiros CDO",
 "C1 - Manutencao GERAL","C2 - Manutencao Equipamento Oftalmologico","C3 - Locacao cilindro + esterilizacao",
 "C4 - Ambulancia","C5 - Manutencao Informatica","C6 - Sistemas (sivoe,simpro,EMED)",
 "C7 - Dedetizacao e Manutencao de aquario","C8 - Manutencao - Seguranca","C9 - Seguro de responsabilidade civil",
 "F1 - Marketing","F2 - Marketing - grafica","G1 - Sindicatos","G2 - Tributos (Referente a empresa)",
 "I1 - Imovel","I2 - Contas de consumo","I3 - Armazenamento","I4 - Aluguel OCT (Interno)",
 "I5 - ELLEX (Repasse utilizacao socios)","I6 - Aluguel - Ceratocone (Dra. Mayumi)",
 "J1 - Impostos bancarios","J2 - Tarifas bancarias",
 "K1 - Lentes Intraoculares - LIO","K2 - Insumos","K3 - Injecao","K4 - Papelaria e limpeza",
 "K5 - Grafica","K6 - Locacao de Equipamento","K7 - Refrativa Laser","K8 - Medicamentos",
 "k9 - Plastica (Dra. Dani)","K10 - Lente de Contato","K11 - Outras cirurgias",
 "L1 - Bens de consumo geral","L2 - Transporte","L3 - Diversos",
 "R1 - C.C. TX (EYE)","R2 - C.C. LIO (EYE)","R4 - Rental Laser (empresa)",
 "R5 - Boleto do Hospital para Dr. Takashi - ELLEX",
 "T1 - PAGAMENTO SOCIO 1","DA1 - PAGAMENTO SOCIO 2","Z1 - PAGAMENTO SOCIO 3",
 "P1 - Aplicacao","P2 - Resgate","P3 - Correcao Juros Aplicacao","P4 - Compra de US$",
 "P5 - IOF (Impostos sobre rendimentos)",
 "N1 - Leva/Traz","N2 - DR. 1","N3 - DR. 2","N4 - DR. 3","N5 - DR. 4",
 "O1 - Doacoes HSC (Confraternizacao)","O2 - Eventos",
 "D1 - Ativo Equipamento CLINICA","D2 - Ativo Equipamento MEDICO1","D3 - Ativo Equipamento MEDICO2",
 "E1 - REFORMA 1","E2 - REFORMA 2","E3 - REFORMA 3","E4 - REFORMA GERAL","E5 - REFORMA EQUIPAMENTO",
 "OBR - Custos de Obra","OBRD - Custos de Ativos de Obra",
 "U1 - Aporte contrato mutuo","U2 - Transferencia PF-PJ mesma","U3 - Transferencia PJ-PJ mesma",
 "TM1 - Distrib. de lucros","TM - Distribuicao de lucros",
 "EKT - DL Socio 1","EKD - DL Socio 2","EKZ - DL Socio 3",
]

def js_arr(lst):
    return "[\n" + ",\n".join("  '" + x.replace("'", "\\'") + "'" for x in lst) + "\n]"

seed_block = f"""
// ===== Criterios financeiros (seed das planilhas) =====
const CRITERIOS_ENTRADA_SEED: string[] = {js_arr(ENTRADA)};
const CRITERIOS_SAIDA_SEED: string[] = {js_arr(SAIDA)};

function loadCriterios(chave: string, seed: string[]): string[] {{
  if (typeof window === 'undefined') return seed;
  try {{
    const raw = localStorage.getItem(chave);
    if (raw) return JSON.parse(raw);
  }} catch (e) {{}}
  return seed;
}}
function saveCriterios(chave: string, lista: string[]) {{
  if (typeof window !== 'undefined') localStorage.setItem(chave, JSON.stringify(lista));
}}
"""

# 1) Inserir seed logo apos os imports (antes da 1a interface/const)
anchor = "export interface LancamentoCaixa"
if anchor not in src:
    print("[ERRO] Nao achei 'export interface LancamentoCaixa'."); sys.exit(1)
src = src.replace(anchor, seed_block + "\n" + anchor, 1)
print("[OK] Seed de criterios inserido.")

# 2) Estados dos criterios + CRUD - inserir apos 'const [mensagem, setMensagem]'
alvo_estado = "  const [mensagem, setMensagem] = useState('');"
if alvo_estado not in src:
    print("[ERRO] Nao achei o estado mensagem."); sys.exit(1)
estados_crud = alvo_estado + """

  // Criterios (entrada/saida) com CRUD em localStorage
  const [criteriosEntrada, setCriteriosEntrada] = useState<string[]>(CRITERIOS_ENTRADA_SEED);
  const [criteriosSaida, setCriteriosSaida] = useState<string[]>(CRITERIOS_SAIDA_SEED);
  const [modalCriterios, setModalCriterios] = useState(false);
  const [abaCriterio, setAbaCriterio] = useState<'ENTRADA' | 'SAIDA'>('ENTRADA');
  const [novoCriterio, setNovoCriterio] = useState('');
  const [editIdxCrit, setEditIdxCrit] = useState<number | null>(null);
  const [editTextoCrit, setEditTextoCrit] = useState('');

  React.useEffect(() => {
    setCriteriosEntrada(loadCriterios('criterios_entrada', CRITERIOS_ENTRADA_SEED));
    setCriteriosSaida(loadCriterios('criterios_saida', CRITERIOS_SAIDA_SEED));
  }, []);

  const listaAtual = abaCriterio === 'ENTRADA' ? criteriosEntrada : criteriosSaida;
  const setListaAtual = (nova: string[]) => {
    if (abaCriterio === 'ENTRADA') { setCriteriosEntrada(nova); saveCriterios('criterios_entrada', nova); }
    else { setCriteriosSaida(nova); saveCriterios('criterios_saida', nova); }
  };
  const addCriterio = () => {
    const t = novoCriterio.trim();
    if (!t) return;
    if (listaAtual.includes(t)) { alert('Criterio ja existe!'); return; }
    setListaAtual([...listaAtual, t]); setNovoCriterio('');
  };
  const salvarEditCrit = (idx: number) => {
    const t = editTextoCrit.trim();
    if (!t) return;
    const nova = [...listaAtual]; nova[idx] = t; setListaAtual(nova);
    setEditIdxCrit(null); setEditTextoCrit('');
  };
  const apagarCriterio = (idx: number) => {
    if (!confirm('Apagar este criterio?')) return;
    setListaAtual(listaAtual.filter((_, i) => i !== idx));
  };
  const criteriosDoTipo = categoria === 'RECEITA' ? criteriosEntrada : criteriosSaida;
"""
src = src.replace(alvo_estado, estados_crud, 1)
print("[OK] Estados e funcoes CRUD adicionados.")

# 3) Botao "Gerenciar Criterios" antes do "Novo Lancamento"
alvo_btn = "onClick={abrirNovoLancamento}"
if alvo_btn not in src:
    print("[ERRO] Nao achei onClick abrirNovoLancamento."); sys.exit(1)
idx = src.find(alvo_btn)
ini = src.rfind("<button", 0, idx)
if ini == -1:
    print("[ERRO] Nao achei abertura do botao Novo Lancamento."); sys.exit(1)
btn_ger = '''<button
            onClick={() => setModalCriterios(true)}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-xl text-sm font-bold transition flex items-center gap-2 cursor-pointer"
          >
            <FileSpreadsheet className="w-4 h-4" /> Gerenciar Criterios
          </button>
          '''
src = src[:ini] + btn_ger + src[ini:]
print("[OK] Botao 'Gerenciar Criterios' inserido.")

# 4) Modal CRUD antes do fechamento do componente
modal_crud = r'''
      {modalCriterios && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setModalCriterios(false)}>
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto p-6" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-black text-white">Gerenciar Criterios (Entrada / Saida)</h2>
              <button onClick={() => setModalCriterios(false)} className="text-slate-400 hover:text-white cursor-pointer"><X className="w-5 h-5" /></button>
            </div>
            <div className="flex gap-2 mb-4">
              <button onClick={() => { setAbaCriterio('ENTRADA'); setEditIdxCrit(null); }} className={`px-4 py-2 rounded-xl text-sm font-bold cursor-pointer ${abaCriterio === 'ENTRADA' ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-400'}`}>Entradas ({criteriosEntrada.length})</button>
              <button onClick={() => { setAbaCriterio('SAIDA'); setEditIdxCrit(null); }} className={`px-4 py-2 rounded-xl text-sm font-bold cursor-pointer ${abaCriterio === 'SAIDA' ? 'bg-orange-600 text-white' : 'bg-slate-800 text-slate-400'}`}>Saidas ({criteriosSaida.length})</button>
            </div>
            <div className="flex gap-2 mb-4">
              <input value={novoCriterio} onChange={(e) => setNovoCriterio(e.target.value)} placeholder="Ex: X1 - Dinheiro" className="flex-1 bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white text-sm" />
              <button onClick={addCriterio} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-bold cursor-pointer">Adicionar</button>
            </div>
            <div className="space-y-1.5">
              {listaAtual.map((c, idx) => (
                <div key={idx} className="flex items-center gap-2 bg-slate-800/50 border border-slate-700 rounded-xl px-3 py-2">
                  {editIdxCrit === idx ? (
                    <>
                      <input value={editTextoCrit} onChange={(e) => setEditTextoCrit(e.target.value)} className="flex-1 bg-slate-950 border border-slate-700 rounded-lg p-1.5 text-white text-sm" />
                      <button onClick={() => salvarEditCrit(idx)} className="text-emerald-400 hover:text-emerald-300 cursor-pointer"><CheckCircle2 className="w-4 h-4" /></button>
                      <button onClick={() => setEditIdxCrit(null)} className="text-slate-400 hover:text-white cursor-pointer"><X className="w-4 h-4" /></button>
                    </>
                  ) : (
                    <>
                      <span className="flex-1 text-sm text-slate-200">{c}</span>
                      <button onClick={() => { setEditIdxCrit(idx); setEditTextoCrit(c); }} className="text-blue-400 hover:text-blue-300 cursor-pointer"><Edit2 className="w-4 h-4" /></button>
                      <button onClick={() => apagarCriterio(idx)} className="text-red-400 hover:text-red-300 cursor-pointer"><Trash2 className="w-4 h-4" /></button>
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
'''
padrao = re.compile(r"(\n\s*</div>\s*\n\s*\);\s*\n\s*}\s*)$")
m = padrao.search(src.rstrip() + "\n")
if not m:
    print("[ERRO] Nao achei fechamento do componente. Salvo so o backup."); sys.exit(1)
pos = m.start()
src = src[:pos] + "\n" + modal_crud + src[pos:]
print("[OK] Modal CRUD inserido.")

open(ARQ, "w", encoding="utf-8").write(src)
print("[OK] Arquivo salvo com sucesso.")
print("\nATENCAO: falta ligar o <select> de tipoMovimentacao a 'criteriosDoTipo' no JSX do modal Novo Lancamento (passo manual - ver instrucao).")
