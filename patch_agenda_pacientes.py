import shutil, datetime, os

# Localiza o arquivo da grade de salas & agenda
alvos = [
    "frontend/src/app/dashboard/page.tsx",
    "frontend/src/app/dashboard/agenda/page.tsx"
]

ARQ = None
for a in alvos:
    if os.path.exists(a):
        ARQ = a
        break

if not ARQ:
    ARQ = "frontend/src/app/dashboard/page.tsx"

if os.path.exists(ARQ):
    bak = f"{ARQ}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy(ARQ, bak)
    print(f"[OK] Backup criado em: {bak}")
else:
    os.makedirs(os.path.dirname(ARQ), exist_ok=True)
    print(f"[INFO] Criando novo arquivo em: {ARQ}")

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
  carteirinhaValidade?: string; // YYYY-MM
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
  consultorio: "Consultório 1" | "Consultório 2" | "Consultório 3";
  data: string; // YYYY-MM-DD
  horarioInicio: string; // HH:mm
  horarioFim: string; // HH:mm
  tipoConsulta: "1a_CONSULTA" | "RETORNO" | "PROCEDIMENTO";
  tipoFaturamento: "PARTICULAR" | "CONVENIO";
  convenio?: string;
  statusAgendamento: "CONFIRMADO" | "AGENDADO" | "EM_CONSULTA" | "CANCELADO";
}

// ==========================================
// SEEDS E DADOS INICIAIS REGULATÓRIOS
// ==========================================

const MEDICOS_DISPONIVEIS = [
  { id: "med-1", nome: "Dr. Roberto Matos", crm: "CRM 54210/SP", especialidade: "Oftalmologia Geral e Córnea" },
  { id: "med-2", nome: "Dra. Camila Vasconcellos", crm: "CRM 48920/SP", especialidade: "Retina e Vítreo" },
  { id: "med-3", nome: "Dr. Carlos Eduardo de Miranda", crm: "CRM 12345/PR", especialidade: "Cirurgia Refrativa e Catarata" },
  { id: "med-4", nome: "Dra. Mariana Costa", crm: "CRM 67890/PR", especialidade: "Glaucoma e Plástica Ocular" },
];

const PACIENTES_SEED: Paciente[] = [
  {
    id: "pac-101",
    nomeCompleto: "Paulo Pereira dos Santos",
    cpf: "123.456.789-01",
    dataNascimento: "1966-02-09",
    telefone: "(11) 98131-1111",
    email: "pkats@pktas.com",
    cep: "01310-100",
    logradouro: "Avenida Paulista",
    numero: "1500",
    complemento: "Apto 82",
    bairro: "Bela Vista",
    cidade: "São Paulo",
    uf: "SP",
    tipoFaturamento: "PARTICULAR",
    status: "ATIVO",
    historicoProntuarios: [
      {
        id: "pront-991",
        data: "2026-06-15",
        medicoNome: "Dr. Roberto Matos",
        medicoCrm: "CRM 54210/SP",
        diagnostico: "Miopia e Astigmatismo Miópico em ambos os olhos",
        cid10: "H52.1 / H52.2",
        condutaPrescricao: "Prescrição óptica para uso contínuo (OD -1.50 -0.50 180° / OE -0.75 -0.25 175°).",
        procedimentoRealizado: "Tonometria de aplanação e Mapeamento de Retina"
      },
      {
        id: "pront-820",
        data: "2025-11-10",
        medicoNome: "Dra. Camila Vasconcellos",
        medicoCrm: "CRM 48920/SP",
        diagnostico: "Sensação de corpo estranho e cefaleia postural",
        cid10: "H57.1",
        condutaPrescricao: "Lubrificante ocular colírio Carmelose 0.5% 4x ao dia."
      }
    ]
  },
  {
    id: "pac-102",
    nomeCompleto: "Maria Aparecida Santos",
    cpf: "854.912.449-01",
    dataNascimento: "1972-08-22",
    telefone: "(11) 97120-4455",
    email: "maria.santos@email.com",
    cep: "04012-000",
    logradouro: "Rua Vergueiro",
    numero: "2350",
    bairro: "Vila Mariana",
    cidade: "São Paulo",
    uf: "SP",
    tipoFaturamento: "CONVENIO",
    convenioOperadora: "Unimed Oftalmo Cooperativa",
    convenioPlano: "Nacional Superior",
    carteirinhaNumero: "00548912449101",
    carteirinhaValidade: "2027-12",
    status: "ATIVO",
    historicoProntuarios: [
      {
        id: "pront-940",
        data: "2026-09-21",
        medicoNome: "Dr. Roberto Matos",
        medicoCrm: "CRM 54210/SP",
        diagnostico: "Avaliação pré-operatória de facectomia com implante de LIO",
        cid10: "H25.0 - Catarata senil inicial",
        condutaPrescricao: "Solicitação de biometria óptica e microscopia especular.",
        procedimentoRealizado: "Biometria Ultrassônica Bilateral"
      }
    ]
  }
];

const AGENDAMENTOS_SEED: AgendamentoSlot[] = [
  {
    id: "ag-01",
    pacienteId: "pac-101",
    pacienteNome: "Paulo Pereira dos Santos",
    pacienteCpf: "123.456.789-01",
    medicoId: "med-1",
    medicoNome: "Dr. Roberto Matos",
    consultorio: "Consultório 1",
    data: "2026-09-28",
    horarioInicio: "09:00",
    horarioFim: "09:30",
    tipoConsulta: "RETORNO",
    tipoFaturamento: "PARTICULAR",
    statusAgendamento: "CONFIRMADO"
  },
  {
    id: "ag-02",
    pacienteId: "pac-102",
    pacienteNome: "Maria Aparecida Santos",
    pacienteCpf: "854.912.449-01",
    medicoId: "med-2",
    medicoNome: "Dra. Camila Vasconcellos",
    consultorio: "Consultório 2",
    data: "2026-09-28",
    horarioInicio: "10:00",
    horarioFim: "10:45",
    tipoConsulta: "PROCEDIMENTO",
    tipoFaturamento: "CONVENIO",
    convenio: "Unimed Oftalmo",
    statusAgendamento: "CONFIRMADO"
  }
];

// ==========================================
// FUNÇÕES UTILITÁRIAS E VALIDADORES
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

export default function GradeSalasAgendaPage() {
  const [pacientes, setPacientes] = useState<Paciente[]>(PACIENTES_SEED);
  const [agendamentos, setAgendamentos] = useState<AgendamentoSlot[]>(AGENDAMENTOS_SEED);
  const [dataSelecionada, setDataSelecionada] = useState("2026-09-28");
  const [filtroConsultorio, setFiltroConsultorio] = useState<string>("TODOS");

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
    convenioOperadora: "Unimed Oftalmo Cooperativa",
    convenioPlano: "",
    carteirinhaNumero: "",
    carteirinhaValidade: "",
    // Dados da Grade
    medicoId: MEDICOS_DISPONIVEIS[0].id,
    consultorio: "Consultório 1" as "Consultório 1" | "Consultório 2" | "Consultório 3",
    horarioInicio: "08:30",
    horarioFim: "09:00",
    marcarTriagemInicial: true
  });

  const [cpfInvalidoAviso, setCpfInvalidoAviso] = useState(false);
  const [toastNotificacao, setToastNotificacao] = useState<string | null>(null);

  // Disparador de Notificação
  const dispararToast = (msg: string) => {
    setToastNotificacao(msg);
    setTimeout(() => setToastNotificacao(null), 4500);
  };

  // Paciente selecionado ou identificado pelo CPF
  const pacienteExistente = useMemo(() => {
    const cpfLimpo = formData.cpf.replace(/\\D/g, "");
    if (cpfLimpo.length === 11) {
      return pacientes.find(p => p.cpf.replace(/\\D/g, "") === cpfLimpo) || null;
    }
    return null;
  }, [formData.cpf, pacientes]);

  const ehPrimeiraConsulta = !pacienteExistente || pacienteExistente.historicoProntuarios.length === 0;

  // Busca rápida de CEP simulada / auto-fill
  const preencherCEP = async (cepLimpo: string) => {
    if (cepLimpo.length === 8) {
      if (cepLimpo === "01310100") {
        setFormData(prev => ({
          ...prev,
          logradouro: "Avenida Paulista",
          bairro: "Bela Vista",
          cidade: "São Paulo",
          uf: "SP"
        }));
      } else if (cepLimpo === "04012000") {
        setFormData(prev => ({
          ...prev,
          logradouro: "Rua Vergueiro",
          bairro: "Vila Mariana",
          cidade: "São Paulo",
          uf: "SP"
        }));
      }
    }
  };

  // Abrir Modal para Novo Agendamento
  const abrirNovoAgendamento = (consultorio?: "Consultório 1" | "Consultório 2" | "Consultório 3", horario?: string) => {
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
      convenioOperadora: "Unimed Oftalmo Cooperativa",
      convenioPlano: "",
      carteirinhaNumero: "",
      carteirinhaValidade: "",
      medicoId: MEDICOS_DISPONIVEIS[0].id,
      consultorio: consultorio || "Consultório 1",
      horarioInicio: horario || "08:30",
      horarioFim: horario ? `${parseInt(horario.split(":")[0])}:${parseInt(horario.split(":")[1]) + 30}` : "09:00",
      marcarTriagemInicial: true
    });
    setCpfInvalidoAviso(false);
    setModalAberto(true);
  };

  // Abrir Modal para Visualizar / Editar Agendamento Existente
  const abrirEdicaoAgendamento = (ag: AgendamentoSlot) => {
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
      convenioOperadora: pac?.convenioOperadora || ag.convenio || "Unimed Oftalmo Cooperativa",
      convenioPlano: pac?.convenioPlano || "",
      carteirinhaNumero: pac?.carteirinhaNumero || "",
      carteirinhaValidade: pac?.carteirinhaValidade || "",
      medicoId: ag.medicoId,
      consultorio: ag.consultorio,
      horarioInicio: ag.horarioInicio,
      horarioFim: ag.horarioFim,
      marcarTriagemInicial: false
    });
    setCpfInvalidoAviso(false);
    setModalAberto(true);
  };

  // ==========================================
  // SALVAR / ATUALIZAR (CREATE & UPDATE OTIMISTA)
  // ==========================================
  const handleSalvar = (e: React.FormEvent) => {
    e.preventDefault();

    const cpfLimpo = formData.cpf.replace(/\\D/g, "");
    if (!validarCPF(cpfLimpo)) {
      setCpfInvalidoAviso(true);
      dispararToast("Erro: O CPF informado é matematicamente inválido.");
      return;
    }

    // Validação de conflito de sala/horário
    const conflito = agendamentos.find(
      a =>
        a.id !== agendamentoIdAtual &&
        a.data === dataSelecionada &&
        a.consultorio === formData.consultorio &&
        a.horarioInicio === formData.horarioInicio
    );

    if (conflito) {
      dispararToast(`Conflito: ${formData.consultorio} já está reservado no horário ${formData.horarioInicio}.`);
      return;
    }

    const medicoSel = MEDICOS_DISPONIVEIS.find(m => m.id === formData.medicoId)!;

    // Atualização / Criação do Paciente
    let pacId = pacienteExistente ? pacienteExistente.id : `pac-${Date.now()}`;
    const novoOuAtualizadoPaciente: Paciente = {
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
        copy[idx] = novoOuAtualizadoPaciente;
        return copy;
      }
      return [...prev, novoOuAtualizadoPaciente];
    });

    // Atualização do Agendamento na Grade
    if (modoEdicao === "EDITAR" && agendamentoIdAtual) {
      setAgendamentos(prev =>
        prev.map(a =>
          a.id === agendamentoIdAtual
            ? {
                ...a,
                pacienteNome: formData.nomeCompleto,
                pacienteCpf: formData.cpf,
                medicoId: medicoSel.id,
                medicoNome: medicoSel.nome,
                consultorio: formData.consultorio,
                horarioInicio: formData.horarioInicio,
                horarioFim: formData.horarioFim,
                tipoFaturamento: formData.tipoFaturamento,
                convenio: formData.tipoFaturamento === "CONVENIO" ? formData.convenioOperadora : undefined
              }
            : a
        )
      );
      dispararToast("Agendamento e cadastro atualizados com sucesso!");
    } else {
      const novoAg: AgendamentoSlot = {
        id: `ag-${Date.now()}`,
        pacienteId: pacId,
        pacienteNome: formData.nomeCompleto,
        pacienteCpf: formData.cpf,
        medicoId: medicoSel.id,
        medicoNome: medicoSel.nome,
        consultorio: formData.consultorio,
        data: dataSelecionada,
        horarioInicio: formData.horarioInicio,
        horarioFim: formData.horarioFim,
        tipoConsulta: ehPrimeiraConsulta ? "1a_CONSULTA" : "RETORNO",
        tipoFaturamento: formData.tipoFaturamento,
        convenio: formData.tipoFaturamento === "CONVENIO" ? formData.convenioOperadora : undefined,
        statusAgendamento: "CONFIRMADO"
      };
      setAgendamentos(prev => [...prev, novoAg]);
      dispararToast("Novo paciente e agendamento salvos na grade!");
    }

    setModalAberto(false);
  };

  // ==========================================
  // APAGAR / INATIVAR / CANCELAR COM REGRA CFM/LGPD
  // ==========================================
  const handleAcaoExcluirOuInativar = () => {
    if (!agendamentoIdAtual) return;

    if (!pacienteExistente || pacienteExistente.historicoProntuarios.length === 0) {
      // Paciente sem prontuários: remoção permitida com confirmação
      if (confirm("Este paciente não possui prontuários prévios. Deseja realmente remover o agendamento e o registro?")) {
        setAgendamentos(prev => prev.filter(a => a.id !== agendamentoIdAtual));
        dispararToast("Agendamento removido com sucesso.");
        setModalAberto(false);
      }
    } else {
      // Paciente com histórico clínico: CFM proíbe exclusão física.
      const motivo = prompt(
        "CONFORMIDADE CFM / LGPD: Pacientes com prontuários não podem ser deletados fisicamente.\\n\\nInforme o motivo do cancelamento para registro na Trilha de Auditoria:",
        "Paciente solicitou cancelamento por motivos pessoais"
      );

      if (motivo) {
        setAgendamentos(prev =>
          prev.map(a =>
            a.id === agendamentoIdAtual ? { ...a, statusAgendamento: "CANCELADO" } : a
          )
        );
        dispararToast(`Agendamento cancelado e registrado na auditoria: "${motivo}"`);
        setModalAberto(false);
      }
    }
  };

  // Horários da Grade Operacional
  const HORARIOS_OPERACIONAIS = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
  ];

  const CONSULTORIOS: ("Consultório 1" | "Consultório 2" | "Consultório 3")[] = [
    "Consultório 1",
    "Consultório 2",
    "Consultório 3"
  ];

  return (
    <div className="p-8 max-w-[1750px] mx-auto text-slate-100">
      {/* Toast Notification Flutuante */}
      {toastNotificacao && (
        <div className="fixed top-6 right-6 z-50 bg-slate-900 border border-blue-500/50 shadow-2xl rounded-2xl p-4 flex items-center gap-3 text-sm text-white animate-in fade-in slide-in-from-top-4">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>{toastNotificacao}</span>
        </div>
      )}

      {/* Cabeçalho da Grade */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-3">
            <CalendarIcon className="w-8 h-8 text-blue-400" />
            <h1 className="text-2xl font-black text-white">Grade de Salas & Agenda Médica</h1>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Alocação de 15 médicos em 3 consultórios físicos, controle bilateral de conflitos e gestão rápida de prontuários.
          </p>
        </div>

        {/* Botão de Destaque - Ponto de Entrada Principal */}
        <div className="flex items-center gap-3">
          <input
            type="date"
            value={dataSelecionada}
            onChange={e => setDataSelecionada(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
          />

          <button
            onClick={() => abrirNovoAgendamento()}
            className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition shadow-lg shadow-blue-900/40 cursor-pointer"
          >
            <Plus className="w-4 h-4" /> Novo Paciente / Agendamento
          </button>
        </div>
      </div>

      {/* Barra de Filtros Rápidos da Grade */}
      <div className="flex items-center justify-between bg-slate-900/80 border border-slate-800 rounded-xl p-3.5 mb-6 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 font-semibold flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5 text-blue-400" /> Consultório:
          </span>
          {["TODOS", "Consultório 1", "Consultório 2", "Consultório 3"].map(c => (
            <button
              key={c}
              onClick={() => setFiltroConsultorio(c)}
              className={`px-3 py-1.5 rounded-lg transition font-medium cursor-pointer ${
                filtroConsultorio === c
                  ? "bg-blue-600 text-white font-bold"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200"
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-4 text-slate-400">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> 1ª Consulta
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-400"></span> Retorno
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Procedimento
          </span>
        </div>
      </div>

      {/* Grade de Horários por Consultório */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {CONSULTORIOS.filter(c => filtroConsultorio === "TODOS" || filtroConsultorio === c).map(cons => (
          <div key={cons} className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
              <div className="flex items-center gap-2">
                <Building className="w-4 h-4 text-blue-400" />
                <h3 className="font-bold text-white text-sm">{cons}</h3>
              </div>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                100% Climatizado
              </span>
            </div>

            <div className="space-y-3">
              {HORARIOS_OPERACIONAIS.map(hora => {
                const ag = agendamentos.find(
                  a => a.consultorio === cons && a.horarioInicio === hora && a.data === dataSelecionada
                );

                if (ag) {
                  const isCancelado = ag.statusAgendamento === "CANCELADO";
                  return (
                    <div
                      key={hora}
                      onClick={() => abrirEdicaoAgendamento(ag)}
                      className={`p-3.5 rounded-xl border transition cursor-pointer flex flex-col justify-between gap-2 ${
                        isCancelado
                          ? "bg-slate-950/40 border-slate-800/40 opacity-50"
                          : ag.tipoConsulta === "1a_CONSULTA"
                          ? "bg-emerald-950/20 border-emerald-800/40 hover:border-emerald-500"
                          : "bg-blue-950/20 border-blue-800/40 hover:border-blue-500"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-xs font-bold text-white flex items-center gap-1.5">
                          <Clock className="w-3.5 h-3.5 text-slate-400" /> {ag.horarioInicio} - {ag.horarioFim}
                        </span>
                        <span
                          className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${
                            ag.tipoConsulta === "1a_CONSULTA"
                              ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                              : "bg-blue-500/20 text-blue-400 border-blue-500/30"
                          }`}
                        >
                          {ag.tipoConsulta === "1a_CONSULTA" ? "1ª CONSULTA" : "RETORNO"}
                        </span>
                      </div>

                      <div>
                        <div className="font-bold text-white text-xs">{ag.pacienteNome}</div>
                        <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                          <Stethoscope className="w-3 h-3 text-blue-400" /> {ag.medicoNome}
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-1 border-t border-slate-800/60 text-[10px]">
                        <span className="text-slate-400">{ag.tipoFaturamento === "CONVENIO" ? ag.convenio : "Particular"}</span>
                        <span className="text-blue-400 font-semibold flex items-center gap-0.5">
                          Ver cadastro <ChevronRight className="w-3 h-3" />
                        </span>
                      </div>
                    </div>
                  );
                }

                // Slot Vago
                return (
                  <button
                    key={hora}
                    onClick={() => abrirNovoAgendamento(cons, hora)}
                    className="w-full p-2.5 rounded-xl border border-dashed border-slate-800 hover:border-blue-500/60 bg-slate-950/20 hover:bg-slate-800/30 transition flex items-center justify-between text-xs text-slate-500 hover:text-slate-200 cursor-pointer"
                  >
                    <span className="font-mono flex items-center gap-1.5">
                      <Clock className="w-3 h-3 text-slate-600" /> {hora}
                    </span>
                    <span className="text-[11px] font-medium">+ Reservar Horário</span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* ======================================================== */}
      {/* MODAL DE GESTÃO DO PACIENTE, CADASTRO & HISTÓRICO        */}
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
                    {modoEdicao === "NOVO" ? "Cadastrar Paciente & Agendamento" : "Ficha do Paciente & Agendamento"}
                  </h2>
                  <p className="text-xs text-slate-400">
                    Gestão cadastral, faturamento e integração bilateral com o prontuário.
                  </p>
                </div>
              </div>

              {/* Badge de Status 1ª Consulta vs Retorno */}
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

            {/* Corpo com Split View (Formulário + Histórico Clínico) */}
            <form onSubmit={handleSalvar} className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 text-xs">
              {/* Lado Esquerdo: Formulário Cadastral e da Grade (7 colunas) */}
              <div className="lg:col-span-7 space-y-5">
                {/* Seção A: Identificação & Dados Pessoais */}
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
                        placeholder="Nome civil completo do paciente"
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
                          CPF matematicamente inválido segundo dígitos verificadores.
                        </span>
                      )}
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Data de Nascimento</label>
                      <input
                        type="date"
                        value={formData.dataNascimento}
                        onChange={e => setFormData({ ...formData, dataNascimento: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      />
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
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 font-mono"
                      />
                    </div>

                    <div className="md:col-span-2">
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

                {/* Seção B: Endereço Completo */}
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
                        onChange={e => {
                          const v = mascaraCEP(e.target.value);
                          setFormData({ ...formData, cep: v });
                          preencherCEP(v.replace(/\\D/g, ""));
                        }}
                        placeholder="00000-000"
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 font-mono"
                      />
                    </div>

                    <div className="md:col-span-4">
                      <label className="text-slate-400 font-semibold mb-1 block">Logradouro / Rua</label>
                      <input
                        type="text"
                        value={formData.logradouro}
                        onChange={e => setFormData({ ...formData, logradouro: e.target.value })}
                        placeholder="Rua, Avenida, Praça..."
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
                      <label className="text-slate-400 font-semibold mb-1 block">Complemento / Bairro</label>
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

                {/* Seção C: Faturamento & Cobertura */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <CreditCard className="w-3.5 h-3.5 text-blue-400" /> C. Cobertura & Faturamento TISS
                  </h4>

                  <div className="flex items-center gap-4">
                    <label className="flex items-center gap-2 cursor-pointer font-medium text-slate-300">
                      <input
                        type="radio"
                        name="faturamento"
                        checked={formData.tipoFaturamento === "PARTICULAR"}
                        onChange={() => setFormData({ ...formData, tipoFaturamento: "PARTICULAR" })}
                        className="accent-blue-500"
                      />
                      Atendimento Particular
                    </label>

                    <label className="flex items-center gap-2 cursor-pointer font-medium text-slate-300">
                      <input
                        type="radio"
                        name="faturamento"
                        checked={formData.tipoFaturamento === "CONVENIO"}
                        onChange={() => setFormData({ ...formData, tipoFaturamento: "CONVENIO" })}
                        className="accent-blue-500"
                      />
                      Convênio / Operadora TISS
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
                          <option value="Unimed Oftalmo Cooperativa">Unimed Oftalmo Cooperativa</option>
                          <option value="Bradesco Saúde">Bradesco Saúde</option>
                          <option value="Amil Assistência Médica">Amil Assistência Médica</option>
                          <option value="SulAmérica Saúde">SulAmérica Saúde</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-slate-400 font-semibold mb-1 block">Nome do Plano</label>
                        <input
                          type="text"
                          value={formData.convenioPlano}
                          onChange={e => setFormData({ ...formData, convenioPlano: e.target.value })}
                          placeholder="Ex: Especial 100 / Nacional"
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                        />
                      </div>

                      <div>
                        <label className="text-slate-400 font-semibold mb-1 block">Nº da Carteirinha</label>
                        <input
                          type="text"
                          value={formData.carteirinhaNumero}
                          onChange={e => setFormData({ ...formData, carteirinhaNumero: e.target.value })}
                          placeholder="Matrícula alfanumérica"
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 font-mono"
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

                {/* Seção D: Contexto do Atendimento na Grade */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-blue-400" /> D. Alocação de Horário & Especialista
                  </h4>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Médico Especialista</label>
                      <select
                        value={formData.medicoId}
                        onChange={e => setFormData({ ...formData, medicoId: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      >
                        {MEDICOS_DISPONIVEIS.map(m => (
                          <option key={m.id} value={m.id}>
                            {m.nome} ({m.crm})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Consultório Alocado</label>
                      <select
                        value={formData.consultorio}
                        onChange={e => setFormData({ ...formData, consultorio: e.target.value as any })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                      >
                        {CONSULTORIOS.map(c => (
                          <option key={c} value={c}>{c}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Horário Início</label>
                      <input
                        type="time"
                        value={formData.horarioInicio}
                        onChange={e => setFormData({ ...formData, horarioInicio: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 font-mono"
                      />
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Horário Fim (Estimado)</label>
                      <input
                        type="time"
                        value={formData.horarioFim}
                        onChange={e => setFormData({ ...formData, horarioFim: e.target.value })}
                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500 font-mono"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Lado Direito: Histórico Clínico e Prontuários (5 colunas) */}
              <div className="lg:col-span-5 bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-blue-400" />
                      <h4 className="font-bold text-white text-xs uppercase tracking-wider">
                        Histórico Clínico & Prontuários
                      </h4>
                    </div>
                    <span className="text-[10px] text-slate-500">Conformidade CFM / PEP</span>
                  </div>

                  {ehPrimeiraConsulta ? (
                    /* Empty State: 1ª Consulta */
                    <div className="py-12 px-4 text-center border border-dashed border-slate-800 rounded-xl bg-slate-900/30">
                      <div className="w-12 h-12 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto mb-3">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>
                      <h5 className="font-bold text-white text-sm">1º Atendimento na Unidade</h5>
                      <p className="text-slate-400 text-xs mt-1 max-w-xs mx-auto leading-relaxed">
                        Nenhum registro clínico prévio localizado para este CPF. O paciente iniciará nova ficha clínica.
                      </p>

                      <label className="mt-4 inline-flex items-center gap-2 text-slate-300 font-medium cursor-pointer">
                        <input
                          type="checkbox"
                          checked={formData.marcarTriagemInicial}
                          onChange={e => setFormData({ ...formData, marcarTriagemInicial: e.target.checked })}
                          className="rounded accent-emerald-500"
                        />
                        <span>Gerar guia de triagem e anamnese inicial</span>
                      </label>
                    </div>
                  ) : (
                    /* Timeline Cronológica de Prontuários */
                    <div className="space-y-4">
                      <div className="text-[11px] text-slate-400">
                        Total de <strong className="text-white">{pacienteExistente?.historicoProntuarios.length}</strong> prontuários registrados para este paciente:
                      </div>

                      <div className="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
                        {pacienteExistente?.historicoProntuarios.map((pront, idx) => (
                          <div key={pront.id} className="relative bg-slate-900/80 p-3.5 rounded-xl border border-slate-800/80 space-y-2">
                            <span className="absolute -left-[23px] top-4 w-2.5 h-2.5 rounded-full bg-blue-500 border-2 border-slate-950"></span>

                            <div className="flex items-center justify-between text-[11px]">
                              <span className="font-bold text-blue-400 font-mono">{pront.data}</span>
                              <span className="text-slate-400">{pront.medicoNome} ({pront.medicoCrm})</span>
                            </div>

                            <div>
                              <span className="text-[10px] text-slate-500 uppercase font-bold block">Diagnóstico Principal:</span>
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
                    <ShieldCheck className="w-3.5 h-3.5 text-blue-400" /> Acesso restrito a profissionais médicos
                  </span>
                  <a href="/dashboard/pep" className="text-blue-400 hover:underline font-bold">
                    Abrir Módulo PEP →
                  </a>
                </div>
              </div>
            </form>

            {/* Rodapé e Ciclo de Vida CRUD */}
            <div className="p-4 border-t border-slate-800 flex items-center justify-between bg-slate-950/80 rounded-b-2xl">
              <div>
                {modoEdicao === "EDITAR" && (
                  <button
                    type="button"
                    onClick={handleAcaoExcluirOuInativar}
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
                  {modoEdicao === "NOVO" ? "Salvar Paciente & Horário" : "Salvar Alterações"}
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
print(f"[OK] Grade de Salas & Agenda atualizada com sucesso em: {ARQ}")
