import shutil, datetime, os

ARQ = "frontend/src/app/dashboard/agendamento/page.tsx"

if os.path.exists(ARQ):
    bak = f"{ARQ}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy(ARQ, bak)
    print(f"[OK] Backup criado em: {bak}")
else:
    os.makedirs(os.path.dirname(ARQ), exist_ok=True)
    print(f"[INFO] Criando arquivo em: {ARQ}")

codigo = '''"use client";

import React, { useState, useMemo } from "react";
import {
  Calendar as CalendarIcon,
  Clock,
  User,
  Plus,
  Search,
  Filter,
  Phone,
  Mail,
  MapPin,
  CreditCard,
  Building,
  FileText,
  AlertCircle,
  CheckCircle2,
  Trash2,
  Save,
  X,
  ExternalLink,
  ShieldCheck,
  Stethoscope,
  ChevronRight,
  Edit,
  AlertTriangle
} from "lucide-react";

// ==========================================
// INTERFACES E TIPAGENS DO MÓDULO CLÍNICO
// ==========================================

export interface ProntuarioHistorico {
  id: string;
  data: string;
  medicoNome: string;
  medicoCrm: string;
  diagnostico: string;
  cid10: string;
  condutaPrescricao: string;
  procedimentoRealizado?: string;
}

export interface Paciente {
  id: string;
  nomeCompleto: string;
  cpf: string;
  dataNascimento: string;
  telefone: string;
  email: string;
  cep: string;
  logradouro: string;
  numero: string;
  complemento?: string;
  bairro: string;
  cidade: string;
  uf: string;
  tipoFaturamento: "PARTICULAR" | "CONVENIO";
  convenioOperadora?: string;
  convenioPlano?: string;
  carteirinhaNumero?: string;
  carteirinhaValidade?: string;
  historicoProntuarios: ProntuarioHistorico[];
  status: "ATIVO" | "INATIVO";
}

export interface AgendamentoSlot {
  id: string;
  pacienteId: string;
  pacienteNome: string;
  pacienteCpf: string;
  medicoId: string;
  medicoNome: string;
  consultorio: "Consultório 1 - Oftalmologia Geral" | "Consultório 2 - Retina e Vítreo" | "Consultório 3 - Córnea e Refrativa";
  dataHora: string;
  procedimentoTuss: string;
  tipoConsulta: "1a_CONSULTA" | "RETORNO" | "PROCEDIMENTO";
  tipoFaturamento: "PARTICULAR" | "CONVENIO";
  convenio?: string;
  statusAgendamento: "CONFIRMADO" | "AGENDADO" | "EM_CONSULTA" | "CANCELADO";
}

// ==========================================
// SEEDS E DADOS INICIAIS
// ==========================================

const MEDICOS_DISPONIVEIS = [
  { id: "med-1", nome: "Dr. Roberto Matos", crm: "CRM 54210/SP", especialidade: "Oftalmologia Geral e Córnea" },
  { id: "med-2", nome: "Dra. Camila Nogueira", crm: "CRM 61890/SP", especialidade: "Retina e Vítreo" },
  { id: "med-3", nome: "Dr. Henrique Pires", crm: "CRM 49201/SP", especialidade: "Córnea e Cirurgia Refrativa" },
  { id: "med-4", nome: "Dr. Carlos Eduardo de Miranda", crm: "CRM 12345/PR", especialidade: "Catarata e Cirurgia Geral" }
];

const CONSULTORIOS_LISTA = [
  "Consultório 1 - Oftalmologia Geral",
  "Consultório 2 - Retina e Vítreo",
  "Consultório 3 - Córnea e Refrativa"
] as const;

const PACIENTES_SEED: Paciente[] = [
  {
    id: "pac-101",
    nomeCompleto: "Maria Aparecida Santos",
    cpf: "123.456.789-00",
    dataNascimento: "1974-05-12",
    telefone: "(11) 98765-4321",
    email: "maria.aparecida@email.com",
    cep: "01310-100",
    logradouro: "Avenida Paulista",
    numero: "1500",
    complemento: "Apto 42",
    bairro: "Bela Vista",
    cidade: "São Paulo",
    uf: "SP",
    tipoFaturamento: "PARTICULAR",
    status: "ATIVO",
    historicoProntuarios: [
      {
        id: "pront-1",
        data: "2026-06-10",
        medicoNome: "Dr. Roberto Matos",
        medicoCrm: "CRM 54210/SP",
        diagnostico: "Miopia e Astigmatismo bilateral",
        cid10: "H52.1 / H52.2",
        condutaPrescricao: "Prescrição óptica para uso contínuo (OD -1.50 -0.50 180° / OE -0.75 -0.25 175°).",
        procedimentoRealizado: "10101012 - Consulta Oftalmológica"
      }
    ]
  },
  {
    id: "pac-102",
    nomeCompleto: "João Batista da Silva",
    cpf: "234.567.890-11",
    dataNascimento: "1968-11-20",
    telefone: "(11) 99876-1122",
    email: "joao.silva@email.com",
    cep: "04012-000",
    logradouro: "Rua Vergueiro",
    numero: "2100",
    bairro: "Vila Mariana",
    cidade: "São Paulo",
    uf: "SP",
    tipoFaturamento: "CONVENIO",
    convenioOperadora: "Bradesco Saúde",
    convenioPlano: "Nacional Top",
    carteirinhaNumero: "89201928301",
    carteirinhaValidade: "2027-10",
    status: "ATIVO",
    historicoProntuarios: [
      {
        id: "pront-2",
        data: "2026-08-15",
        medicoNome: "Dra. Camila Nogueira",
        medicoCrm: "CRM 61890/SP",
        diagnostico: "Suspeita de tração vítreo-retiniana",
        cid10: "H43.8",
        condutaPrescricao: "Solicitado mapeamento de retina e OCT bilateral de mácula.",
        procedimentoRealizado: "41301265 - Mapeamento de Retina"
      }
    ]
  },
  {
    id: "pac-103",
    nomeCompleto: "Ana Carolina Pereira",
    cpf: "345.678.901-22",
    dataNascimento: "1992-03-14",
    telefone: "(11) 97654-9988",
    email: "ana.pereira@email.com",
    cep: "04530-001",
    logradouro: "Rua Funchal",
    numero: "418",
    bairro: "Vila Olímpia",
    cidade: "São Paulo",
    uf: "SP",
    tipoFaturamento: "PARTICULAR",
    status: "ATIVO",
    historicoProntuarios: []
  }
];

const AGENDAMENTOS_SEED: AgendamentoSlot[] = [
  {
    id: "ag-1",
    pacienteId: "pac-101",
    pacienteNome: "Maria Aparecida Santos",
    pacienteCpf: "123.456.789-00",
    medicoId: "med-1",
    medicoNome: "Dr. Roberto Matos - CRM 54210/SP",
    consultorio: "Consultório 1 - Oftalmologia Geral",
    dataHora: "2026-09-28 14:47",
    procedimentoTuss: "10101012 - Consulta Oftalmológica",
    tipoConsulta: "RETORNO",
    tipoFaturamento: "PARTICULAR",
    statusAgendamento: "CONFIRMADO"
  },
  {
    id: "ag-2",
    pacienteId: "pac-102",
    pacienteNome: "João Batista da Silva",
    pacienteCpf: "234.567.890-11",
    medicoId: "med-2",
    medicoNome: "Dra. Camila Nogueira - CRM 61890/SP",
    consultorio: "Consultório 2 - Retina e Vítreo",
    dataHora: "2026-09-28 15:30",
    procedimentoTuss: "41301265 - Mapeamento de Retina",
    tipoConsulta: "PROCEDIMENTO",
    tipoFaturamento: "CONVENIO",
    convenio: "Bradesco Saúde",
    statusAgendamento: "CONFIRMADO"
  },
  {
    id: "ag-3",
    pacienteId: "pac-103",
    pacienteNome: "Ana Carolina Pereira",
    pacienteCpf: "345.678.901-22",
    medicoId: "med-3",
    medicoNome: "Dr. Henrique Pires - CRM 49201/SP",
    consultorio: "Consultório 3 - Córnea e Refrativa",
    dataHora: "2026-09-28 16:15",
    procedimentoTuss: "41301303 - Paquimetria Ultrassônica",
    tipoConsulta: "1a_CONSULTA",
    tipoFaturamento: "PARTICULAR",
    statusAgendamento: "CONFIRMADO"
  }
];

// ==========================================
// MÁSCARAS E VALIDAÇÃO MATEMÁTICA DE CPF
// ==========================================

function validarCPF(cpfLimpo: string): boolean {
  if (cpfLimpo.length !== 11 || !!cpfLimpo.match(/(\\d)\\1{10}/)) return false;
  const digits = cpfLimpo.split("").map(Number);
  const calc = (n: number) =>
    digits.slice(0, n).reduce((soma, num, idx) => soma + num * (n + 1 - idx), 0);
  const d1 = (calc(9) * 10) % 11 % 10;
  const d2 = (calc(10) * 10) % 11 % 10;
  return digits[9] === d1 && digits[10] === d2;
}

function mascaraCPF(val: string) {
  return val
    .replace(/\\D/g, "")
    .slice(0, 11)
    .replace(/(\\d{3})(\\d)/, "$1.$2")
    .replace(/(\\d{3})(\\d)/, "$1.$2")
    .replace(/(\\d{3})(\\d{1,2})$/, "$1-$2");
}

function mascaraTelefone(val: string) {
  return val
    .replace(/\\D/g, "")
    .slice(0, 11)
    .replace(/(\\d{2})(\\d)/, "($1) $2")
    .replace(/(\\d{5})(\\d{4})$/, "$1-$2");
}

function mascaraCEP(val: string) {
  return val
    .replace(/\\D/g, "")
    .slice(0, 8)
    .replace(/(\\d{5})(\\d)/, "$1-$2");
}

export default function CentralAgendamentosPage() {
  const [pacientes, setPacientes] = useState<Paciente[]>(PACIENTES_SEED);
  const [agendamentos, setAgendamentos] = useState<AgendamentoSlot[]>(AGENDAMENTOS_SEED);
  const [buscaTabela, setBuscaTabela] = useState("");

  // Estados do Modal
  const [modalAberto, setModalAberto] = useState(false);
  const [modoEdicao, setModoEdicao] = useState<"NOVO" | "EDITAR">("NOVO");
  const [agendamentoIdAtual, setAgendamentoIdAtual] = useState<string | null>(null);

  // Formulário do Modal
  const [formData, setFormData] = useState({
    nomeCompleto: "",
    cpf: "",
    dataNascimento: "",
    telefone: "",
    email: "",
    cep: "",
    logradouro: "",
    numero: "",
    complemento: "",
    bairro: "",
    cidade: "São Paulo",
    uf: "SP",
    tipoFaturamento: "PARTICULAR" as "PARTICULAR" | "CONVENIO",
    convenioOperadora: "Unimed Oftalmo",
    convenioPlano: "",
    carteirinhaNumero: "",
    carteirinhaValidade: "",
    medicoNome: MEDICOS_DISPONIVEIS[0].nome + " - " + MEDICOS_DISPONIVEIS[0].crm,
    consultorio: CONSULTORIOS_LISTA[0] as typeof CONSULTORIOS_LISTA[number],
    dataHora: "2026-09-28 14:00",
    procedimentoTuss: "10101012 - Consulta Oftalmológica",
    marcarTriagemInicial: true
  });

  const [cpfInvalidoAviso, setCpfInvalidoAviso] = useState(false);
  const [toastNotificacao, setToastNotificacao] = useState<string | null>(null);

  const dispararToast = (msg: string) => {
    setToastNotificacao(msg);
    setTimeout(() => setToastNotificacao(null), 4500);
  };

  // Identificação automática se é 1ª Consulta ou Retorno
  const pacienteExistente = useMemo(() => {
    const cpfLimpo = formData.cpf.replace(/\\D/g, "");
    if (cpfLimpo.length === 11) {
      return pacientes.find(p => p.cpf.replace(/\\D/g, "") === cpfLimpo) || null;
    }
    return null;
  }, [formData.cpf, pacientes]);

  const ehPrimeiraConsulta = !pacienteExistente || pacienteExistente.historicoProntuarios.length === 0;

  // Preenchimento de CEP automático
  const handleCepChange = (cepMascarado: string) => {
    const limpo = cepMascarado.replace(/\\D/g, "");
    setFormData(prev => ({ ...prev, cep: cepMascarado }));
    if (limpo === "01310100") {
      setFormData(prev => ({
        ...prev,
        logradouro: "Avenida Paulista",
        bairro: "Bela Vista",
        cidade: "São Paulo",
        uf: "SP"
      }));
    } else if (limpo === "04012000") {
      setFormData(prev => ({
        ...prev,
        logradouro: "Rua Vergueiro",
        bairro: "Vila Mariana",
        cidade: "São Paulo",
        uf: "SP"
      }));
    }
  };

  // Abrir Modal: Novo Paciente / Agendamento
  const abrirNovoModal = (consultorioPref?: typeof CONSULTORIOS_LISTA[number]) => {
    setModoEdicao("NOVO");
    setAgendamentoIdAtual(null);
    setFormData({
      nomeCompleto: "",
      cpf: "",
      dataNascimento: "",
      telefone: "",
      email: "",
      cep: "",
      logradouro: "",
      numero: "",
      complemento: "",
      bairro: "",
      cidade: "São Paulo",
      uf: "SP",
      tipoFaturamento: "PARTICULAR",
      convenioOperadora: "Unimed Oftalmo",
      convenioPlano: "",
      carteirinhaNumero: "",
      carteirinhaValidade: "",
      medicoNome: MEDICOS_DISPONIVEIS[0].nome + " - " + MEDICOS_DISPONIVEIS[0].crm,
      consultorio: consultorioPref || CONSULTORIOS_LISTA[0],
      dataHora: "2026-09-28 15:00",
      procedimentoTuss: "10101012 - Consulta Oftalmológica",
      marcarTriagemInicial: true
    });
    setCpfInvalidoAviso(false);
    setModalAberto(true);
  };

  // Abrir Modal: Editar Agendamento
  const abrirEdicaoModal = (ag: AgendamentoSlot) => {
    setModoEdicao("EDITAR");
    setAgendamentoIdAtual(ag.id);
    const pac = pacientes.find(p => p.id === ag.pacienteId);

    setFormData({
      nomeCompleto: pac ? pac.nomeCompleto : ag.pacienteNome,
      cpf: pac ? pac.cpf : ag.pacienteCpf,
      dataNascimento: pac?.dataNascimento || "",
      telefone: pac?.telefone || "",
      email: pac?.email || "",
      cep: pac?.cep || "",
      logradouro: pac?.logradouro || "",
      numero: pac?.numero || "",
      complemento: pac?.complemento || "",
      bairro: pac?.bairro || "",
      cidade: pac?.cidade || "São Paulo",
      uf: pac?.uf || "SP",
      tipoFaturamento: ag.tipoFaturamento,
      convenioOperadora: pac?.convenioOperadora || ag.convenio || "Unimed Oftalmo",
      convenioPlano: pac?.convenioPlano || "",
      carteirinhaNumero: pac?.carteirinhaNumero || "",
      carteirinhaValidade: pac?.carteirinhaValidade || "",
      medicoNome: ag.medicoNome,
      consultorio: ag.consultorio,
      dataHora: ag.dataHora,
      procedimentoTuss: ag.procedimentoTuss,
      marcarTriagemInicial: false
    });
    setCpfInvalidoAviso(false);
    setModalAberto(true);
  };

  // Salvar (Create / Update Otimista)
  const handleSalvar = (e: React.FormEvent) => {
    e.preventDefault();

    const cpfLimpo = formData.cpf.replace(/\\D/g, "");
    if (!validarCPF(cpfLimpo)) {
      setCpfInvalidoAviso(true);
      dispararToast("Erro: O CPF informado é inválido pelos dígitos verificadores.");
      return;
    }

    let pacId = pacienteExistente ? pacienteExistente.id : `pac-${Date.now()}`;
    const novoOuAtualizadoPac: Paciente = {
      id: pacId,
      nomeCompleto: formData.nomeCompleto.trim(),
      cpf: formData.cpf,
      dataNascimento: formData.dataNascimento,
      telefone: formData.telefone,
      email: formData.email.trim(),
      cep: formData.cep,
      logradouro: formData.logradouro,
      numero: formData.numero,
      complemento: formData.complemento,
      bairro: formData.bairro,
      cidade: formData.cidade,
      uf: formData.uf,
      tipoFaturamento: formData.tipoFaturamento,
      convenioOperadora: formData.tipoFaturamento === "CONVENIO" ? formData.convenioOperadora : undefined,
      convenioPlano: formData.tipoFaturamento === "CONVENIO" ? formData.convenioPlano : undefined,
      carteirinhaNumero: formData.tipoFaturamento === "CONVENIO" ? formData.carteirinhaNumero : undefined,
      carteirinhaValidade: formData.tipoFaturamento === "CONVENIO" ? formData.carteirinhaValidade : undefined,
      historicoProntuarios: pacienteExistente ? pacienteExistente.historicoProntuarios : [],
      status: "ATIVO"
    };

    setPacientes(prev => {
      const idx = prev.findIndex(p => p.id === pacId);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = novoOuAtualizadoPac;
        return copy;
      }
      return [...prev, novoOuAtualizadoPac];
    });

    if (modoEdicao === "EDITAR" && agendamentoIdAtual) {
      setAgendamentos(prev =>
        prev.map(a =>
          a.id === agendamentoIdAtual
            ? {
                ...a,
                pacienteNome: formData.nomeCompleto,
                pacienteCpf: formData.cpf,
                medicoNome: formData.medicoNome,
                consultorio: formData.consultorio,
                dataHora: formData.dataHora,
                procedimentoTuss: formData.procedimentoTuss,
                tipoFaturamento: formData.tipoFaturamento,
                convenio: formData.tipoFaturamento === "CONVENIO" ? formData.convenioOperadora : undefined
              }
            : a
        )
      );
      dispararToast("Agendamento e cadastro do paciente atualizados com sucesso!");
    } else {
      const novoAg: AgendamentoSlot = {
        id: `ag-${Date.now()}`,
        pacienteId: pacId,
        pacienteNome: formData.nomeCompleto,
        pacienteCpf: formData.cpf,
        medicoId: "med-sel",
        medicoNome: formData.medicoNome,
        consultorio: formData.consultorio,
        dataHora: formData.dataHora,
        procedimentoTuss: formData.procedimentoTuss,
        tipoConsulta: ehPrimeiraConsulta ? "1a_CONSULTA" : "RETORNO",
        tipoFaturamento: formData.tipoFaturamento,
        convenio: formData.tipoFaturamento === "CONVENIO" ? formData.convenioOperadora : undefined,
        statusAgendamento: "CONFIRMADO"
      };
      setAgendamentos(prev => [...prev, novoAg]);
      dispararToast("Novo agendamento reservado na grade com sucesso!");
    }

    setModalAberto(false);
  };

  // Exclusão / Cancelamento com Regra CFM/LGPD
  const handleAcaoExcluirOuInativar = (idParaCancelar?: string) => {
    const alvoId = idParaCancelar || agendamentoIdAtual;
    if (!alvoId) return;

    const ag = agendamentos.find(a => a.id === alvoId);
    const pac = pacientes.find(p => p.id === ag?.pacienteId);

    if (!pac || pac.historicoProntuarios.length === 0) {
      if (confirm("Este paciente não possui histórico clínico. Deseja remover o agendamento?")) {
        setAgendamentos(prev => prev.filter(a => a.id !== alvoId));
        dispararToast("Agendamento removido.");
        setModalAberto(false);
      }
    } else {
      const motivo = prompt(
        "CONFORMIDADE CFM / LGPD: Paciente com histórico clínico registrado. A remoção física é vedada.\\n\\nInforme o motivo do cancelamento para registrar na trilha de auditoria:",
        "Paciente solicitou cancelamento por motivos pessoais"
      );
      if (motivo) {
        setAgendamentos(prev =>
          prev.map(a =>
            a.id === alvoId ? { ...a, statusAgendamento: "CANCELADO" } : a
          )
        );
        dispararToast(`Agendamento cancelado e registrado na auditoria: "${motivo}"`);
        setModalAberto(false);
      }
    }
  };

  const agendamentosFiltrados = useMemo(() => {
    if (!buscaTabela) return agendamentos;
    const t = buscaTabela.toLowerCase();
    return agendamentos.filter(
      a =>
        a.pacienteNome.toLowerCase().includes(t) ||
        a.pacienteCpf.includes(t) ||
        a.medicoNome.toLowerCase().includes(t) ||
        a.procedimentoTuss.toLowerCase().includes(t)
    );
  }, [agendamentos, buscaTabela]);

  return (
    <div className="p-8 max-w-[1750px] mx-auto text-slate-100">
      {/* Toast Feedback */}
      {toastNotificacao && (
        <div className="fixed top-6 right-6 z-50 bg-slate-900 border border-blue-500/60 shadow-2xl rounded-2xl p-4 flex items-center gap-3 text-sm text-white animate-in fade-in">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>{toastNotificacao}</span>
        </div>
      )}

      {/* Topo do Módulo */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <CalendarIcon className="w-7 h-7 text-blue-400" /> Central de Agendamentos
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Controle de alocação de 15 médicos em 3 consultórios físicos com validação TUSS/TISS.
          </p>
        </div>

        {/* Botões de Ação Rápida */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => abrirNovoModal()}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition shadow-lg shadow-blue-900/40 cursor-pointer"
          >
            <Plus className="w-4 h-4" /> + Novo Paciente / Agendamento
          </button>
          <button className="px-4 py-2.5 bg-blue-700 hover:bg-blue-600 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition cursor-pointer">
            <CalendarIcon className="w-4 h-4" /> Calendário Mensal da Clínica
          </button>
          <button className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition cursor-pointer">
            <User className="w-4 h-4" /> Carga Diária & Lista de Pacientes
          </button>
        </div>
      </div>

      {/* Grid Principal: Reserva Rápida + Ocupação das Salas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        {/* Painel Esquerdo: Formulário Rápido da Reserva */}
        <div className="lg:col-span-8 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Nova Reserva de Consulta / Exame
            </h3>
            <span className="text-[11px] text-blue-400 cursor-pointer hover:underline" onClick={() => abrirNovoModal()}>
              + Abrir Ficha Cadastral Completa
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="md:col-span-2">
              <label className="text-slate-400 font-semibold mb-1 block">CPF do Paciente</label>
              <input
                type="text"
                placeholder="000.000.000-00"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
                onFocus={() => abrirNovoModal()}
              />
            </div>

            <div>
              <label className="text-slate-400 font-semibold mb-1 block">Consultório Físico (Trava de Sala)</label>
              <select
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
                defaultValue={CONSULTORIOS_LISTA[0]}
              >
                {CONSULTORIOS_LISTA.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold mb-1 block">Especialista / Médico</label>
              <select className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500">
                {MEDICOS_DISPONIVEIS.map(m => (
                  <option key={m.id} value={m.nome}>{m.nome} - {m.crm}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold mb-1 block">Data e Hora do Agendamento</label>
              <input
                type="text"
                defaultValue="28/09/2026, 14:47"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white font-mono focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="text-slate-400 font-semibold mb-1 block">Código TUSS de Procedimento</label>
              <input
                type="text"
                defaultValue="10101012 - Consulta oftalmológica"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <button
            onClick={() => abrirNovoModal()}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-xs transition shadow-lg shadow-blue-900/30 cursor-pointer mt-2"
          >
            Confirmar Reserva de Agenda
          </button>
        </div>

        {/* Painel Direito: Ocupação das Salas Físicas */}
        <div className="lg:col-span-4 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 pb-3 border-b border-slate-800 mb-4">
              <Clock className="w-4 h-4 text-blue-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                Ocupação das Salas
              </h3>
            </div>
            <p className="text-[11px] text-slate-500 mb-4">
              Regra rígida: máximo de 3 atendimentos simultâneos nos consultórios físicos.
            </p>

            <div className="space-y-3">
              {CONSULTORIOS_LISTA.map((c, i) => (
                <div
                  key={c}
                  onClick={() => abrirNovoModal(c)}
                  className="bg-slate-950 border border-slate-800 hover:border-blue-500/60 p-3.5 rounded-xl flex items-center justify-between cursor-pointer transition"
                >
                  <div>
                    <h4 className="font-bold text-white text-xs">{c.split(" - ")[0]}</h4>
                    <span className="text-[11px] text-slate-400">{c.split(" - ")[1]}</span>
                  </div>
                  <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-[10px] font-bold">
                    Disponível
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500">
            Tempo médio por consulta: <strong className="text-slate-300">30 min</strong>
          </div>
        </div>
      </div>

      {/* Grade de Agendamentos do Dia (Tabela) */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-950/60">
          <h3 className="text-xs font-black uppercase tracking-wider text-slate-300">
            Grade de Agendamentos do Dia ({agendamentosFiltrados.length} reservas)
          </h3>

          <div className="relative w-full md:w-72">
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Buscar por paciente, CPF ou médico..."
              value={buscaTabela}
              onChange={e => setBuscaTabela(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/40 text-slate-400 uppercase tracking-wider font-semibold">
                <th className="py-3 px-4">Data / Hora</th>
                <th className="py-3 px-4">Paciente / CPF</th>
                <th className="py-3 px-4">Consultório Físico</th>
                <th className="py-3 px-4">Médico</th>
                <th className="py-3 px-4">Procedimento TUSS</th>
                <th className="py-3 px-4 text-center">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {agendamentosFiltrados.map(ag => {
                const isCancelado = ag.statusAgendamento === "CANCELADO";
                return (
                  <tr key={ag.id} className={`hover:bg-slate-800/40 transition ${isCancelado ? "opacity-40" : ""}`}>
                    <td className="py-3.5 px-4 font-mono text-blue-400 whitespace-nowrap">
                      {ag.dataHora}
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-white">{ag.pacienteNome}</div>
                      <div className="text-[11px] text-slate-400 font-mono">CPF: {ag.pacienteCpf}</div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      {ag.consultorio}
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      {ag.medicoNome}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-300">
                      {ag.procedimentoTuss}
                    </td>
                    <td className="py-3.5 px-4 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={() => abrirEdicaoModal(ag)}
                          className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-[11px] font-semibold flex items-center gap-1 transition cursor-pointer"
                        >
                          <Edit className="w-3 h-3 text-blue-400" /> Alterar
                        </button>
                        <button
                          onClick={() => handleAcaoExcluirOuInativar(ag.id)}
                          className="px-2.5 py-1 bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-900/40 rounded-lg text-[11px] font-semibold flex items-center gap-1 transition cursor-pointer"
                        >
                          <Trash2 className="w-3 h-3" /> Cancelar
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* ======================================================== */}
      {/* MODAL RESPONSIVO: GESTÃO DO PACIENTE, AGENDA & HISTÓRICO */}
      {/* ======================================================== */}
      {modalAberto && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-6xl my-6 shadow-2xl flex flex-col max-h-[92vh]">
            {/* Topo do Modal */}
            <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60 rounded-t-2xl">
              <div className="flex items-center gap-3">
                <User className="w-6 h-6 text-blue-400" />
                <div>
                  <h2 className="text-lg font-black text-white">
                    {modoEdicao === "NOVO" ? "Cadastrar Paciente & Agendamento" : "Ficha Cadastral & Agendamento"}
                  </h2>
                  <p className="text-xs text-slate-400">
                    Dados pessoais, endereço, cobertura TISS e histórico clínico integrado.
                  </p>
                </div>
              </div>

              {/* Badge 1ª Consulta vs Retorno */}
              <div className="flex items-center gap-3">
                {ehPrimeiraConsulta ? (
                  <span className="px-3 py-1 bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 rounded-full font-black text-xs flex items-center gap-1.5 shadow-sm">
                    <CheckCircle2 className="w-3.5 h-3.5" /> [1ª CONSULTA - NOVO REGISTRO]
                  </span>
                ) : (
                  <span className="px-3 py-1 bg-blue-500/15 border border-blue-500/30 text-blue-400 rounded-full font-black text-xs flex items-center gap-1.5 shadow-sm">
                    <FileText className="w-3.5 h-3.5" /> [RETORNO / RECORRENTE - {pacienteExistente?.historicoProntuarios.length} ATENDIMENTOS]
                  </span>
                )}
                <button
                  onClick={() => setModalAberto(false)}
                  className="p-1.5 text-slate-400 hover:text-white rounded-lg transition cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Split View: Formulário (7 cols) + Histórico Clínico (5 cols) */}
            <form onSubmit={handleSalvar} className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 text-xs">
              <div className="lg:col-span-7 space-y-4">
                {/* A. Dados Pessoais */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <User className="w-3.5 h-3.5 text-blue-400" /> A. Identificação e Contato
                  </h4>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Nome Completo *</label>
                      <input
                        type="text"
                        required
                        value={formData.nomeCompleto}
                        onChange={e => setFormData({ ...formData, nomeCompleto: e.target.value })}
                        placeholder="Nome civil do paciente"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">CPF *</label>
                      <input
                        type="text"
                        required
                        value={formData.cpf}
                        onChange={e => {
                          const val = mascaraCPF(e.target.value);
                          setFormData({ ...formData, cpf: val });
                          if (val.replace(/\\D/g, "").length === 11) {
                            setCpfInvalidoAviso(!validarCPF(val.replace(/\\D/g, "")));
                          }
                        }}
                        placeholder="000.000.000-00"
                        className={`w-full bg-slate-900 border rounded-lg px-3 py-2 text-white focus:outline-none font-mono ${
                          cpfInvalidoAviso ? "border-rose-500" : "border-slate-800 focus:border-blue-500"
                        }`}
                      />
                      {cpfInvalidoAviso && (
                        <span className="text-[10px] text-rose-400 mt-1 block">
                          CPF matematicamente inválido.
                        </span>
                      )}
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block flex items-center justify-between">
                        <span>Telefone / WhatsApp *</span>
                        {formData.telefone.replace(/\\D/g, "").length >= 10 && (
                          <a
                            href={`https://wa.me/55${formData.telefone.replace(/\\D/g, "")}`}
                            target="_blank"
                            rel="noreferrer"
                            className="text-[10px] text-emerald-400 hover:underline flex items-center gap-0.5"
                          >
                            Abrir WhatsApp <ExternalLink className="w-2.5 h-2.5" />
                          </a>
                        )}
                      </label>
                      <input
                        type="text"
                        required
                        value={formData.telefone}
                        onChange={e => setFormData({ ...formData, telefone: mascaraTelefone(e.target.value) })}
                        placeholder="(00) 00000-0000"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">E-mail</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={e => setFormData({ ...formData, email: e.target.value })}
                        placeholder="paciente@exemplo.com.br"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                {/* B. Endereço */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-blue-400" /> B. Endereço Completo
                  </h4>

                  <div className="grid grid-cols-1 md:grid-cols-6 gap-3">
                    <div className="md:col-span-2">
                      <label className="text-slate-400 font-semibold mb-1 block">CEP</label>
                      <input
                        type="text"
                        value={formData.cep}
                        onChange={e => handleCepChange(mascaraCEP(e.target.value))}
                        placeholder="00000-000"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <div className="md:col-span-4">
                      <label className="text-slate-400 font-semibold mb-1 block">Logradouro / Rua</label>
                      <input
                        type="text"
                        value={formData.logradouro}
                        onChange={e => setFormData({ ...formData, logradouro: e.target.value })}
                        placeholder="Avenida, Rua..."
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="text-slate-400 font-semibold mb-1 block">Número</label>
                      <input
                        type="text"
                        value={formData.numero}
                        onChange={e => setFormData({ ...formData, numero: e.target.value })}
                        placeholder="123"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <div className="md:col-span-4">
                      <label className="text-slate-400 font-semibold mb-1 block">Bairro / Cidade</label>
                      <input
                        type="text"
                        value={formData.bairro}
                        onChange={e => setFormData({ ...formData, bairro: e.target.value })}
                        placeholder="Bairro ou referência"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                {/* C. Faturamento */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <CreditCard className="w-3.5 h-3.5 text-blue-400" /> C. Cobertura & Faturamento TISS
                  </h4>

                  <div className="flex items-center gap-4">
                    <label className="flex items-center gap-2 cursor-pointer font-medium text-slate-300">
                      <input
                        type="radio"
                        name="fat"
                        checked={formData.tipoFaturamento === "PARTICULAR"}
                        onChange={() => setFormData({ ...formData, tipoFaturamento: "PARTICULAR" })}
                        className="accent-blue-500"
                      />
                      Particular
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer font-medium text-slate-300">
                      <input
                        type="radio"
                        name="fat"
                        checked={formData.tipoFaturamento === "CONVENIO"}
                        onChange={() => setFormData({ ...formData, tipoFaturamento: "CONVENIO" })}
                        className="accent-blue-500"
                      />
                      Convênio / Operadora
                    </label>
                  </div>

                  {formData.tipoFaturamento === "CONVENIO" && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-slate-800">
                      <div>
                        <label className="text-slate-400 font-semibold mb-1 block">Operadora</label>
                        <select
                          value={formData.convenioOperadora}
                          onChange={e => setFormData({ ...formData, convenioOperadora: e.target.value })}
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                        >
                          <option value="Unimed Oftalmo">Unimed Oftalmo</option>
                          <option value="Bradesco Saúde">Bradesco Saúde</option>
                          <option value="Amil Assistência Médica">Amil Assistência Médica</option>
                          <option value="SulAmérica Saúde">SulAmérica Saúde</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-slate-400 font-semibold mb-1 block">Plano</label>
                        <input
                          type="text"
                          value={formData.convenioPlano}
                          onChange={e => setFormData({ ...formData, convenioPlano: e.target.value })}
                          placeholder="Ex: Nacional Top"
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                        />
                      </div>

                      <div>
                        <label className="text-slate-400 font-semibold mb-1 block">Nº Carteirinha</label>
                        <input
                          type="text"
                          value={formData.carteirinhaNumero}
                          onChange={e => setFormData({ ...formData, carteirinhaNumero: e.target.value })}
                          placeholder="Matrícula"
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:outline-none focus:border-blue-500"
                        />
                      </div>

                      <div>
                        <label className="text-slate-400 font-semibold mb-1 block">Validade</label>
                        <input
                          type="month"
                          value={formData.carteirinhaValidade}
                          onChange={e => setFormData({ ...formData, carteirinhaValidade: e.target.value })}
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                        />
                      </div>
                    </div>
                  )}
                </div>

                {/* D. Alocação de Sala & Médico */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-blue-400" /> D. Alocação de Consultório & Agenda
                  </h4>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Consultório</label>
                      <select
                        value={formData.consultorio}
                        onChange={e => setFormData({ ...formData, consultorio: e.target.value as any })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      >
                        {CONSULTORIOS_LISTA.map(c => (
                          <option key={c} value={c}>{c}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Médico</label>
                      <select
                        value={formData.medicoNome}
                        onChange={e => setFormData({ ...formData, medicoNome: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      >
                        {MEDICOS_DISPONIVEIS.map(m => (
                          <option key={m.id} value={`${m.nome} - ${m.crm}`}>
                            {m.nome} ({m.crm})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Data & Hora</label>
                      <input
                        type="text"
                        value={formData.dataHora}
                        onChange={e => setFormData({ ...formData, dataHora: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Procedimento TUSS</label>
                      <input
                        type="text"
                        value={formData.procedimentoTuss}
                        onChange={e => setFormData({ ...formData, procedimentoTuss: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white font-mono focus:outline-none focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Histórico Clínico (Lado Direito) */}
              <div className="lg:col-span-5 bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-blue-400" />
                      <h4 className="font-bold text-white text-xs uppercase tracking-wider">
                        Histórico Clínico & Prontuários
                      </h4>
                    </div>
                    <span className="text-[10px] text-slate-500">Conformidade CFM</span>
                  </div>

                  {ehPrimeiraConsulta ? (
                    <div className="py-12 px-4 text-center border border-dashed border-slate-800 rounded-xl bg-slate-900/30">
                      <div className="w-12 h-12 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto mb-3">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>
                      <h5 className="font-bold text-white text-sm">1º Atendimento na Unidade</h5>
                      <p className="text-slate-400 text-xs mt-1 max-w-xs mx-auto leading-relaxed">
                        Nenhum prontuário anterior localizado para este CPF. O paciente iniciará nova ficha clínica.
                      </p>

                      <label className="mt-4 inline-flex items-center gap-2 text-slate-300 font-medium cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.marcarTriagemInicial}
                          onChange={e => setFormData({ ...formData, marcarTriagemInicial: e.target.checked })}
                          className="rounded accent-emerald-500"
                        />
                        <span>Marcar como primeira triagem/anamnese completa</span>
                      </label>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="text-[11px] text-slate-400">
                        Total de <strong className="text-white">{pacienteExistente?.historicoProntuarios.length}</strong> consultas anteriores:
                      </div>

                      <div className="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
                        {pacienteExistente?.historicoProntuarios.map(pront => (
                          <div key={pront.id} className="relative bg-slate-900/80 p-3.5 rounded-xl border border-slate-800/80 space-y-2">
                            <span className="absolute -left-[23px] top-4 w-2.5 h-2.5 rounded-full bg-blue-500 border-2 border-slate-950"></span>

                            <div className="flex items-center justify-between text-[11px]">
                              <span className="font-bold text-blue-400 font-mono">{pront.data}</span>
                              <span className="text-slate-400">{pront.medicoNome}</span>
                            </div>

                            <div>
                              <span className="text-[10px] text-slate-500 uppercase font-bold block">Diagnóstico:</span>
                              <div className="font-semibold text-slate-200">{pront.diagnostico}</div>
                              <span className="text-[10px] text-emerald-400 font-mono font-bold">{pront.cid10}</span>
                            </div>

                            <div className="pt-2 border-t border-slate-800/60 text-[11px] text-slate-400">
                              <span className="font-semibold text-slate-300">Conduta: </span>
                              {pront.condutaPrescricao}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-4 mt-6 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
                  <span className="flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-blue-400" /> Acesso restrito a profissionais médicos (LGPD)
                  </span>
                  <a href="/dashboard/pep" className="text-blue-400 hover:underline font-bold">
                    Ir para PEP →
                  </a>
                </div>
              </div>
            </form>

            {/* Rodapé CRUD */}
            <div className="p-4 border-t border-slate-800 flex items-center justify-between bg-slate-950/80 rounded-b-2xl">
              <div>
                {modoEdicao === "EDITAR" && (
                  <button
                    type="button"
                    onClick={() => handleAcaoExcluirOuInativar()}
                    className="px-4 py-2 bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-800/60 rounded-xl text-xs font-bold flex items-center gap-2 transition cursor-pointer"
                  >
                    <Trash2 className="w-4 h-4" />
                    {!pacienteExistente || pacienteExistente.historicoProntuarios.length === 0
                      ? "Apagar Agendamento"
                      : "Inativar / Cancelar (CFM)"}
                  </button>
                )}
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => setModalAberto(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-medium transition cursor-pointer"
                >
                  Fechar
                </button>
                <button
                  type="button"
                  onClick={handleSalvar}
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition shadow-lg shadow-blue-900/40 cursor-pointer"
                >
                  <Save className="w-4 h-4" />
                  {modoEdicao === "NOVO" ? "Salvar Paciente & Agendamento" : "Salvar Alterações"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
'''

open(ARQ, "w", encoding="utf-8").write(codigo)
print(f"[OK] {ARQ} atualizado com sucesso!")
