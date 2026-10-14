import os

# 1. Localiza a pasta dashboard
dash_dir = None
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.next', '.git']):
        continue
    if 'agendamento' in dirs:
        dash_dir = root
        break

if not dash_dir:
    for cand in ['./frontend/src/app/dashboard', './src/app/dashboard', './frontend/app/dashboard', './app/dashboard']:
        if os.path.exists(cand):
            dash_dir = cand
            break

if not dash_dir:
    print("[-] Erro: pasta dashboard não encontrada.")
    exit(1)

print(f"[+] Pasta dashboard: {dash_dir}")

# -------------------------------------------------------------
# 2. ATUALIZAR AGENDAMENTO COM "+ NOVO PACIENTE" E TODOS OS RECURSOS
# -------------------------------------------------------------
agendamento_file = os.path.join(dash_dir, 'agendamento', 'page.tsx')
os.makedirs(os.path.dirname(agendamento_file), exist_ok=True)

code_agendamento = """'use client';

import React, { useState } from 'react';
import { 
  Calendar as CalendarIcon, Users, ShieldCheck, 
  X, UserCheck, CheckCircle2, UserPlus, Save
} from 'lucide-react';

interface PacienteAgendado {
  horario: string;
  nome: string;
  medico: string;
  sala: string;
  tuss: string;
  convenio: string;
}

interface DiaAgenda {
  dia: number;
  medicos: string[];
  totalPacientes: number;
  pacientes: PacienteAgendado[];
}

const DADOS_SETEMBRO_2026: Record<number, DiaAgenda> = {
  1: {
    dia: 1,
    medicos: ['Dr. Roberto Matos', 'Dra. Camila Nogueira'],
    totalPacientes: 18,
    pacientes: [
      { horario: '08:00', nome: 'Carlos Eduardo Lima', medico: 'Dr. Roberto Matos', sala: 'Cons. 1', tuss: '10101012 - Consulta', convenio: 'Unimed' },
      { horario: '08:30', nome: 'Ana Paula Silveira', medico: 'Dr. Roberto Matos', sala: 'Cons. 1', tuss: '20101020 - Tonometria', convenio: 'Bradesco' },
      { horario: '09:00', nome: 'Marcos Vinícius Prado', medico: 'Dra. Camila Nogueira', sala: 'Cons. 2', tuss: '20101039 - Mapeamento', convenio: 'Particular' },
    ]
  },
  21: {
    dia: 21,
    medicos: ['Dr. Roberto Matos', 'Dra. Camila Nogueira', 'Dr. Henrique Pires'],
    totalPacientes: 26,
    pacientes: [
      { horario: '08:00', nome: 'Maria Aparecida Santos', medico: 'Dr. Roberto Matos', sala: 'Cons. 1 (Oftalmo Geral)', tuss: '10101012 - Consulta Especializada', convenio: 'Unimed' },
      { horario: '08:30', nome: 'João Batista da Silva', medico: 'Dra. Camila Nogueira', sala: 'Cons. 2 (Retina)', tuss: '20101039 - Mapeamento de Retina', convenio: 'Bradesco' },
      { horario: '09:15', nome: 'Helena Ribeiro Fernandes', medico: 'Dr. Henrique Pires', sala: 'Cons. 3 (Córnea)', tuss: '20101020 - Tonometria', convenio: 'Particular' },
      { horario: '10:00', nome: 'Antônio Carlos Meireles', medico: 'Dr. Roberto Matos', sala: 'Cons. 1 (Oftalmo Geral)', tuss: '10101012 - Consulta', convenio: 'Amil' },
      { horario: '10:45', nome: 'Luciana Queiroz Prado', medico: 'Dra. Camila Nogueira', sala: 'Cons. 2 (Retina)', tuss: '20101055 - Gonioscopia', convenio: 'SulAmérica' },
      { horario: '11:30', nome: 'Roberto Duarte Filho', medico: 'Dr. Henrique Pires', sala: 'Cons. 3 (Córnea)', tuss: '10101012 - Consulta', convenio: 'Unimed' }
    ]
  },
  22: {
    dia: 22,
    medicos: ['Dr. Roberto Matos', 'Dra. Vanessa Luz'],
    totalPacientes: 19,
    pacientes: [
      { horario: '08:00', nome: 'Sônia Regina Esteves', medico: 'Dr. Roberto Matos', sala: 'Cons. 1', tuss: '10101012 - Consulta', convenio: 'Bradesco' },
      { horario: '09:00', nome: 'Cláudio Manuel Fontes', medico: 'Dra. Vanessa Luz', sala: 'Cons. 3', tuss: '20101047 - Paquimetria', convenio: 'Amil' },
    ]
  }
};

export default function AgendamentoPage() {
  const [cpf, setCpf] = useState('');
  const [sala, setSala] = useState('');
  const [medico, setMedico] = useState('');
  const [dataHora, setDataHora] = useState('');
  const [tuss, setTuss] = useState('');
  const [notificacao, setNotificacao] = useState('');

  // Modais de Visualização Preservados
  const [modalMesAberto, setModalMesAberto] = useState(false);
  const [modalDiaAberto, setModalDiaAberto] = useState(false);
  const [diaSelecionado, setDiaSelecionado] = useState<number>(21);

  // NOVO MODAL: CADASTRO DE NOVO PACIENTE
  const [modalNovoPaciente, setModalNovoPaciente] = useState(false);
  const [novoNome, setNovoNome] = useState('');
  const [novoCpf, setNovoCpf] = useState('');
  const [novoNascimento, setNovoNascimento] = useState('');
  const [novoTelefone, setNovoTelefone] = useState('');
  const [novoConvenio, setNovoConvenio] = useState('Particular');
  const [novaCarteirinha, setNovaCarteirinha] = useState('');

  const diasDoMes = Array.from({ length: 30 }, (_, i) => i + 1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setNotificacao('Reserva confirmada com sucesso e consultório alocado!');
    setTimeout(() => setNotificacao(''), 4000);
  };

  const handleSalvarNovoPaciente = (e: React.FormEvent) => {
    e.preventDefault();
    if (!novoNome || !novoCpf) {
      alert('Por favor, informe o Nome Completo e o CPF do paciente.');
      return;
    }
    setCpf(novoCpf);
    setModalNovoPaciente(false);
    setNotificacao(`Paciente ${novoNome} cadastrado com sucesso! CPF inserido no agendamento.`);
    setNovoNome('');
    setNovoCpf('');
    setNovoNascimento('');
    setNovoTelefone('');
    setNovaCarteirinha('');
    setTimeout(() => setNotificacao(''), 4000);
  };

  return (
    <div className="space-y-6 text-slate-100">
      {/* Top Header com os Três Botões */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2">
            Central de Agendamentos
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Controle de alocação de 15 médicos em 3 consultórios físicos com validação TUSS/TISS.
          </p>
        </div>

        {/* GRUPO DE BOTÕES: CADASTRO + CALENDÁRIO + CARGA */}
        <div className="flex flex-wrap items-center gap-3">
          {/* NOVO BOTÃO: NOVO PACIENTE */}
          <button
            type="button"
            onClick={() => setModalNovoPaciente(true)}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-black transition flex items-center gap-2 shadow-lg shadow-blue-600/30 active:scale-95 cursor-pointer"
          >
            <UserPlus className="w-4 h-4" />
            <span>+ Novo Paciente</span>
          </button>

          {/* BOTÃO CALENDÁRIO MENSAL */}
          <button
            type="button"
            onClick={() => setModalMesAberto(true)}
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-black transition flex items-center gap-2 active:scale-95 cursor-pointer"
          >
            <CalendarIcon className="w-4 h-4 text-blue-400" />
            <span>Calendário Mensal</span>
          </button>

          {/* BOTÃO CARGA DIÁRIA & LISTA */}
          <button
            type="button"
            onClick={() => {
              setDiaSelecionado(21);
              setModalDiaAberto(true);
            }}
            className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-black transition flex items-center gap-2 shadow-lg shadow-emerald-600/30 active:scale-95 cursor-pointer"
          >
            <Users className="w-4 h-4" />
            <span>Carga Diária &amp; Lista</span>
          </button>
        </div>
      </div>

      {notificacao && (
        <div className="p-4 bg-emerald-950/70 border border-emerald-500 rounded-xl text-emerald-200 text-xs flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <span>{notificacao}</span>
        </div>
      )}

      {/* Grade Principal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-5">
          <div className="flex justify-between items-center">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">Nova Reserva de Consulta / Exame</h2>
            <button
              type="button"
              onClick={() => setModalNovoPaciente(true)}
              className="text-xs text-blue-400 hover:underline flex items-center gap-1 font-semibold cursor-pointer"
            >
              <UserPlus className="w-3.5 h-3.5" /> Não encontrou? Cadastrar Paciente
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-xs font-semibold text-slate-400 block mb-1">CPF do Paciente</label>
              <input
                type="text"
                placeholder="000.000.000-00"
                value={cpf}
                onChange={(e) => setCpf(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-400 block mb-1">Consultório Físico (Trava de Sala)</label>
                <select
                  value={sala}
                  onChange={(e) => setSala(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="">Selecione o consultório...</option>
                  <option value="1">Consultório 1 - Oftalmologia Geral</option>
                  <option value="2">Consultório 2 - Retina e Vítreo</option>
                  <option value="3">Consultório 3 - Córnea e Refração</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-400 block mb-1">Especialista / Médico</label>
                <select
                  value={medico}
                  onChange={(e) => setMedico(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="">Selecione o especialista...</option>
                  <option value="matos">Dr. Roberto Matos - CRM 54210/SP</option>
                  <option value="nogueira">Dra. Camila Nogueira - CRM 61890/SP</option>
                  <option value="pires">Dr. Henrique Pires - CRM 49201/SP</option>
                  <option value="luz">Dra. Vanessa Luz - CRM 58112/SP</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-400 block mb-1">Data e Hora</label>
                <input
                  type="datetime-local"
                  value={dataHora}
                  onChange={(e) => setDataHora(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-400 block mb-1">Código TUSS de Procedimento</label>
                <input
                  type="text"
                  placeholder="10101012 - Consulta Oftalmológica"
                  value={tuss}
                  onChange={(e) => setTuss(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold text-sm transition shadow-lg shadow-blue-600/30 active:scale-95 cursor-pointer"
            >
              Confirmar Reserva de Agenda
            </button>
          </form>
        </div>

        {/* Status das Salas */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-blue-500" /> Ocupação das Salas
            </h2>
            <p className="text-[11px] text-slate-400 mt-1">Capacidade de 3 consultórios simultâneos.</p>
          </div>

          <div className="space-y-3">
            {[
              { nome: 'Consultório 1', desc: 'Oftalmologia Geral', status: 'Disponível' },
              { nome: 'Consultório 2', desc: 'Retina e Vítreo', status: 'Disponível' },
              { nome: 'Consultório 3', desc: 'Córnea e Refração', status: 'Disponível' }
            ].map((c, i) => (
              <div key={i} className="p-3.5 bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-slate-200">{c.nome}</div>
                  <div className="text-[11px] text-slate-500">{c.desc}</div>
                </div>
                <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full text-[11px] font-bold">
                  {c.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* MODAL NOVO: CADASTRO DE PACIENTE */}
      {modalNovoPaciente && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl max-w-2xl w-full p-6 shadow-2xl space-y-5 max-h-[92vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-blue-600/20 text-blue-400 flex items-center justify-center font-black">
                  <UserPlus className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-white">Cadastrar Novo Paciente</h2>
                  <p className="text-xs text-slate-400">Inserção cadastral imediata no sistema.</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setModalNovoPaciente(false)}
                className="p-2 text-slate-400 hover:text-white rounded-xl bg-slate-800 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSalvarNovoPaciente} className="space-y-4 text-xs">
              <div>
                <label className="text-slate-300 font-semibold block mb-1">Nome Completo do Paciente *</label>
                <input
                  type="text"
                  required
                  placeholder="Ex: Carlos Eduardo de Oliveira"
                  value={novoNome}
                  onChange={(e) => setNovoNome(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-slate-300 font-semibold block mb-1">CPF *</label>
                  <input
                    type="text"
                    required
                    placeholder="000.000.000-00"
                    value={novoCpf}
                    onChange={(e) => setNovoCpf(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="text-slate-300 font-semibold block mb-1">Data de Nascimento</label>
                  <input
                    type="date"
                    value={novoNascimento}
                    onChange={(e) => setNovoNascimento(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-slate-300 font-semibold block mb-1">WhatsApp / Telefone</label>
                  <input
                    type="tel"
                    placeholder="(11) 99999-9999"
                    value={novoTelefone}
                    onChange={(e) => setNovoTelefone(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="text-slate-300 font-semibold block mb-1">Convênio / Plano de Saúde</label>
                  <select
                    value={novoConvenio}
                    onChange={(e) => setNovoConvenio(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="Particular">Particular</option>
                    <option value="Unimed Oftalmo">Unimed Oftalmo</option>
                    <option value="Bradesco Saúde">Bradesco Saúde</option>
                    <option value="Amil Saúde">Amil Saúde</option>
                    <option value="SulAmérica">SulAmérica</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-slate-300 font-semibold block mb-1">Nº da Carteirinha do Convênio</label>
                <input
                  type="text"
                  placeholder="0000.0000.0000-00 (deixe em branco se particular)"
                  value={novaCarteirinha}
                  onChange={(e) => setNovaCarteirinha(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white font-mono focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setModalNovoPaciente(false)}
                  className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-bold cursor-pointer"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-black shadow-lg shadow-blue-600/30 flex items-center gap-2 cursor-pointer"
                >
                  <Save className="w-4 h-4" />
                  <span>Cadastrar e Prosseguir</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL CALENDÁRIO MENSAL */}
      {modalMesAberto && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-5xl w-full p-6 shadow-2xl space-y-5 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-lg font-black text-white flex items-center gap-2">
                  <CalendarIcon className="w-5 h-5 text-blue-500" />
                  Calendário Mensal de Atendimentos — Setembro / 2026
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">Escala médica e quantitativo total de pacientes.</p>
              </div>
              <button onClick={() => setModalMesAberto(false)} className="p-2 text-slate-400 hover:text-white rounded-xl bg-slate-800 cursor-pointer">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2 text-xs">
              {['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'].map(d => (
                <div key={d} className="text-center font-bold text-slate-500 uppercase text-[10px] pb-1">{d}</div>
              ))}
              {diasDoMes.map(dia => {
                const info = DADOS_SETEMBRO_2026[dia];
                return (
                  <div key={dia} className={`min-h-[85px] p-2 rounded-xl border flex flex-col justify-between ${
                    dia === 21 ? 'bg-blue-950/40 border-blue-500' : info ? 'bg-slate-950 border-slate-800' : 'bg-slate-950/40 border-slate-900 opacity-60'
                  }`}>
                    <div className="flex justify-between items-center">
                      <span className={`font-mono font-bold text-xs ${dia === 21 ? 'text-blue-400' : 'text-slate-300'}`}>{dia}</span>
                      {info && <span className="text-[9px] bg-blue-600/30 text-blue-300 px-1.5 py-0.5 rounded font-bold font-mono">{info.totalPacientes} pac.</span>}
                    </div>
                    <div className="mt-1 space-y-1">
                      {info ? info.medicos.slice(0, 2).map((m, idx) => (
                        <div key={idx} className="text-[9px] text-slate-300 truncate bg-slate-900 px-1 py-0.5 rounded">👨‍⚕️ {m.replace('Dr. ', '').replace('Dra. ', '')}</div>
                      )) : <span className="text-[9px] text-slate-600">Sem escala</span>}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="flex justify-end pt-2">
              <button onClick={() => setModalMesAberto(false)} className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold cursor-pointer">
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL CARGA DIÁRIA */}
      {modalDiaAberto && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-5xl w-full p-6 shadow-2xl space-y-5 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-lg font-black text-white flex items-center gap-2">
                  <Users className="w-5 h-5 text-emerald-400" />
                  Carga Diária &amp; Lista Nominal de Pacientes
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">Clique no dia para carregar a lista nominal.</p>
              </div>
              <button onClick={() => setModalDiaAberto(false)} className="p-2 text-slate-400 hover:text-white rounded-xl bg-slate-800 cursor-pointer">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex gap-2 overflow-x-auto pb-2">
              {diasDoMes.map(d => {
                const qtd = DADOS_SETEMBRO_2026[d]?.totalPacientes || 0;
                const isSel = diaSelecionado === d;
                return (
                  <button
                    key={d}
                    onClick={() => setDiaSelecionado(d)}
                    className={`flex-shrink-0 px-3 py-2 rounded-2xl border text-center transition flex flex-col items-center min-w-[64px] cursor-pointer ${
                      isSel ? 'bg-emerald-600 border-emerald-400 text-white font-bold' : 'bg-slate-950 border-slate-800 text-slate-300'
                    }`}
                  >
                    <span className="text-xs font-mono">Dia {d}</span>
                    <span className={`text-[10px] mt-0.5 font-bold px-1.5 py-0.5 rounded-full ${isSel ? 'bg-emerald-800' : 'bg-slate-900 text-emerald-400'}`}>
                      {qtd} pac.
                    </span>
                  </button>
                );
              })}
            </div>

            <div className="bg-slate-950 rounded-2xl border border-slate-800 p-5 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <UserCheck className="w-4 h-4 text-emerald-400" />
                Pacientes Agendados — {diaSelecionado} de Setembro de 2026
              </h3>

              {DADOS_SETEMBRO_2026[diaSelecionado]?.pacientes.length ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px]">
                        <th className="py-2.5 px-3">Horário</th>
                        <th className="py-2.5 px-3">Paciente</th>
                        <th className="py-2.5 px-3">Médico</th>
                        <th className="py-2.5 px-3">Consultório</th>
                        <th className="py-2.5 px-3">TUSS</th>
                        <th className="py-2.5 px-3">Convênio</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-900 font-mono">
                      {DADOS_SETEMBRO_2026[diaSelecionado].pacientes.map((p, idx) => (
                        <tr key={idx} className="hover:bg-slate-900/60 transition">
                          <td className="py-2.5 px-3 font-bold text-blue-400">{p.horario}</td>
                          <td className="py-2.5 px-3 font-sans font-bold text-white">{p.nome}</td>
                          <td className="py-2.5 px-3 text-slate-300 font-sans">{p.medico}</td>
                          <td className="py-2.5 px-3 text-emerald-400 font-semibold">{p.sala}</td>
                          <td className="py-2.5 px-3 text-slate-400">{p.tuss}</td>
                          <td className="py-2.5 px-3"><span className="px-2 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-800 text-[10px]">{p.convenio}</span></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="py-8 text-center text-slate-500 text-xs">Nenhum atendimento cadastrado para este dia.</div>
              )}
            </div>

            <div className="flex justify-end pt-2">
              <button onClick={() => setModalDiaAberto(false)} className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold cursor-pointer">
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

with open(agendamento_file, 'w', encoding='utf-8') as f:
    f.write(code_agendamento)
print(f"[✓] Gravado com sucesso: {agendamento_file}")

# -------------------------------------------------------------
# 3. CORRIGIR RH (/dashboard/rh) PARA TER ESTILO DARK PERFEITO
# -------------------------------------------------------------
rh_file = os.path.join(dash_dir, 'rh', 'page.tsx')
os.makedirs(os.path.dirname(rh_file), exist_ok=True)

code_rh = """'use client';

import React from 'react';
import { Users, Calendar, ShieldCheck } from 'lucide-react';

export default function RhPage() {
  const especialistas = [
    { nome: 'Dr. Roberto Matos', crm: '54210/SP', esp: 'Oftalmologia Geral', sala: 'Consultório 1', turno: 'Manhã / Tarde' },
    { nome: 'Dra. Camila Nogueira', crm: '61890/SP', esp: 'Retina e Vítreo', sala: 'Consultório 2', turno: 'Manhã' },
    { nome: 'Dr. Henrique Pires', crm: '49201/SP', esp: 'Córnea e Refração', sala: 'Consultório 3', turno: 'Tarde' },
    { nome: 'Dra. Vanessa Luz', crm: '58112/SP', esp: 'Glaucoma', sala: 'Consultório 1', turno: 'Plantão Noturno' },
  ];

  return (
    <div className="space-y-6 text-slate-100">
      <div className="flex justify-between items-center border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2">
            <Users className="w-6 h-6 text-blue-500" />
            Recursos Humanos &amp; Escala Médica
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Gestão dos 15 médicos especialistas e alocação dinâmica para os 3 consultórios físicos.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {especialistas.map((esp, idx) => (
          <div key={idx} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20">
                CRM {esp.crm}
              </span>
              <span className="text-[10px] text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                {esp.sala}
              </span>
            </div>
            <div>
              <h3 className="font-bold text-sm text-white">{esp.nome}</h3>
              <p className="text-xs text-slate-400">{esp.esp}</p>
            </div>
            <div className="text-[11px] text-slate-400 pt-2 border-t border-slate-800/80 flex items-center justify-between">
              <span>Turno alocado:</span>
              <span className="font-semibold text-slate-200">{esp.turno}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
"""

with open(rh_file, 'w', encoding='utf-8') as f:
    f.write(code_rh)
print(f"[✓] Gravado com sucesso: {rh_file}")
