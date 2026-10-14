import re, shutil, datetime, sys

ARQ = "frontend/src/app/dashboard/farmacia/page.tsx"
src = open(ARQ, encoding="utf-8").read()

bak = f"{ARQ}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
shutil.copy(ARQ, bak)
print(f"[OK] Backup criado: {bak}")

if "modalEntrada" in src:
    print("[AVISO] Patch ja aplicado. Nada a fazer."); sys.exit(0)

# 1) ESTADOS + HANDLERS - inserir apos a linha do editItem
alvo = "  const [editItem, setEditItem] = useState<Insumo | null>(null);"
if alvo not in src:
    print("[ERRO] Nao achei a linha do editItem. Abortando."); sys.exit(1)

bloco_estados = alvo + """

  // Movimentacao de estoque (entrada/saida)
  const [modalEntrada, setModalEntrada] = useState(false);
  const [modalSaida, setModalSaida] = useState(false);
  const [movInsumoId, setMovInsumoId] = useState('');
  const [movQtd, setMovQtd] = useState(1);
  const [movMotivo, setMovMotivo] = useState('Uso Cirurgico');

  const handleEntrada = (e: React.FormEvent) => {
    e.preventDefault();
    if (!movInsumoId) { alert('Selecione o insumo!'); return; }
    if (movQtd <= 0) { alert('Quantidade deve ser maior que zero!'); return; }
    setInsumos(insumos.map(i => i.id === movInsumoId ? { ...i, saldo: i.saldo + Number(movQtd) } : i));
    const alvoIns = insumos.find(i => i.id === movInsumoId);
    setModalEntrada(false);
    setNotificacao(`ENTRADA registrada: +${movQtd} ${alvoIns?.unidade ?? ''} de ${alvoIns?.nome ?? ''} (rastreabilidade ANVISA).`);
    setMovQtd(1); setMovInsumoId('');
    setTimeout(() => setNotificacao(''), 4000);
  };

  const handleSaida = (e: React.FormEvent) => {
    e.preventDefault();
    if (!movInsumoId) { alert('Selecione o insumo!'); return; }
    if (movQtd <= 0) { alert('Quantidade deve ser maior que zero!'); return; }
    const alvoIns = insumos.find(i => i.id === movInsumoId);
    if (!alvoIns) { alert('Insumo nao encontrado!'); return; }
    if (movQtd > alvoIns.saldo) {
      alert(`Saldo insuficiente! Disponivel: ${alvoIns.saldo} ${alvoIns.unidade}.`);
      return;
    }
    setInsumos(insumos.map(i => i.id === movInsumoId ? { ...i, saldo: i.saldo - Number(movQtd) } : i));
    setModalSaida(false);
    setNotificacao(`SAIDA registrada: -${movQtd} ${alvoIns.unidade} de ${alvoIns.nome} (${movMotivo}).`);
    setMovQtd(1); setMovInsumoId(''); setMovMotivo('Uso Cirurgico');
    setTimeout(() => setNotificacao(''), 4000);
  };
"""
src = src.replace(alvo, bloco_estados, 1)
print("[OK] Estados e handlers de entrada/saida adicionados.")

# 2) BOTOES no topo - inserir antes do botao "+ Registrar Lote"
btn_registrar = '''          onClick={() => setModalNovo(true)}'''
if btn_registrar not in src:
    print("[ERRO] Nao achei o botao Registrar Lote (onClick). Abortando."); sys.exit(1)

# Procura a tag <button ...> que contem o onClick do modalNovo, para inserir 2 botoes antes dela.
idx = src.find(btn_registrar)
inicio_btn = src.rfind("<button", 0, idx)
if inicio_btn == -1:
    print("[ERRO] Nao localizei a abertura do <button> do Registrar Lote. Abortando."); sys.exit(1)

botoes_mov = '''<button
          onClick={() => setModalEntrada(true)}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Entrada de Insumo</span>
        </button>
        <button
          onClick={() => setModalSaida(true)}
          className="px-4 py-2 bg-orange-600 hover:bg-orange-500 text-white rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer"
        >
          <Package className="w-4 h-4" />
          <span>Saida de Insumo</span>
        </button>
        '''
src = src[:inicio_btn] + botoes_mov + src[inicio_btn:]
print("[OK] Botoes 'Entrada' e 'Saida' inseridos no topo.")

# 3) MODAIS - inserir antes do fechamento final do componente
modais = r'''
      {modalEntrada && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setModalEntrada(false)}>
          <form onSubmit={handleEntrada} className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-black text-white">Entrada de Insumo (Recebimento)</h2>
              <button type="button" onClick={() => setModalEntrada(false)} className="text-slate-400 hover:text-white cursor-pointer"><X className="w-5 h-5" /></button>
            </div>
            <label className="block text-xs font-bold text-slate-400 mb-1">Insumo</label>
            <select value={movInsumoId} onChange={(e) => setMovInsumoId(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white mb-3">
              <option value="">Selecione o insumo...</option>
              {insumos.map(i => (<option key={i.id} value={i.id}>{i.nome} (Lote {i.lote}) - saldo {i.saldo} {i.unidade}</option>))}
            </select>
            <label className="block text-xs font-bold text-slate-400 mb-1">Quantidade recebida</label>
            <input type="number" min="1" value={movQtd} onChange={(e) => setMovQtd(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white text-center font-mono mb-4" />
            <div className="flex gap-3 justify-end">
              <button type="button" onClick={() => setModalEntrada(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl font-bold cursor-pointer">Cancelar</button>
              <button type="submit" className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-bold cursor-pointer">Confirmar Entrada</button>
            </div>
          </form>
        </div>
      )}

      {modalSaida && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setModalSaida(false)}>
          <form onSubmit={handleSaida} className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-black text-white">Saida de Insumo (Consumo)</h2>
              <button type="button" onClick={() => setModalSaida(false)} className="text-slate-400 hover:text-white cursor-pointer"><X className="w-5 h-5" /></button>
            </div>
            <label className="block text-xs font-bold text-slate-400 mb-1">Insumo</label>
            <select value={movInsumoId} onChange={(e) => setMovInsumoId(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white mb-3">
              <option value="">Selecione o insumo...</option>
              {insumos.map(i => (<option key={i.id} value={i.id}>{i.nome} (Lote {i.lote}) - saldo {i.saldo} {i.unidade}</option>))}
            </select>
            <label className="block text-xs font-bold text-slate-400 mb-1">Quantidade</label>
            <input type="number" min="1" value={movQtd} onChange={(e) => setMovQtd(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white text-center font-mono mb-3" />
            <label className="block text-xs font-bold text-slate-400 mb-1">Motivo</label>
            <select value={movMotivo} onChange={(e) => setMovMotivo(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-white mb-4">
              <option>Uso Cirurgico</option>
              <option>Consumo Ambulatorial</option>
              <option>Perda / Quebra</option>
              <option>Vencimento</option>
              <option>Transferencia</option>
            </select>
            <div className="flex gap-3 justify-end">
              <button type="button" onClick={() => setModalSaida(false)} className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl font-bold cursor-pointer">Cancelar</button>
              <button type="submit" className="px-4 py-2 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-bold cursor-pointer">Confirmar Saida</button>
            </div>
          </form>
        </div>
      )}
'''

padrao = re.compile(r"(\n\s*</div>\s*\n\s*\);\s*\n\s*}\s*)$")
m = padrao.search(src.rstrip() + "\n")
if not m:
    print("[ERRO] Nao encontrei o fechamento do return/componente. Salvo apenas o backup."); sys.exit(1)
pos = m.start()
src = src[:pos] + "\n" + modais + src[pos:]
print("[OK] Modais de entrada e saida inseridos.")

open(ARQ, "w", encoding="utf-8").write(src)
print("[OK] Arquivo salvo com sucesso.")
print("\nProximo passo: docker compose build frontend && docker compose up -d frontend")
