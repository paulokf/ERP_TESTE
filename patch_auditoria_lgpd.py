import shutil, datetime

ARQ = "frontend/src/app/dashboard/auditoria/page.tsx"
bak = f"{ARQ}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
shutil.copy(ARQ, bak)
print(f"[OK] Backup criado em: {bak}")

codigo = '''"use client";

import React, { useState, useMemo, useEffect } from "react";
import {
  ShieldCheck,
  Search,
  Filter,
  Calendar,
  Clock,
  User,
  FileText,
  Download,
  Eye,
  AlertTriangle,
  CheckCircle2,
  X,
  RefreshCw,
  HardDrive,
  FileSpreadsheet,
  Printer,
  ChevronLeft,
  ChevronRight,
  Fingerprint,
  Lock,
  ArrowRight
} from "lucide-react";

// ==========================================
// TIPAGENS E ENUMS ESTREITOS - LGPD & FORENSE
// ==========================================

export type TipoOperacao =
  | "READ"
  | "CREATE"
  | "UPDATE"
  | "DELETE"
  | "EXPORT"
  | "AUTH_EVENT";

export type ModuloEntidade =
  | "Prontuário Médico"
  | "Dados Pessoais/Cadastrais"
  | "Financeiro/Faturamento"
  | "Agenda/Escala"
  | "Prescrição & Farmácia";

export type NivelSensibilidade = "GERAL" | "DADO_SENSIVEL";

export interface AuditDiffField {
  campo: string;
  anterior: string | null;
  novo: string | null;
  sensivel?: boolean;
}

export interface AuditLogEntry {
  id: string;
  timestamp: string; // ISO 8601
  operadorNome: string;
  operadorIdentificador: string; // CPF ou Matrícula
  operadorCargo: string;
  operadorEmail: string;
  acaoDescricao: string;
  modulo: ModuloEntidade;
  objetoAfetado: string;
  tipoOperacao: TipoOperacao;
  nivelSensibilidade: NivelSensibilidade;
  ipOrigem: string;
  userAgent: string;
  sha256Hash: string;
  baseLegalLGPD: string;
  diffAlteracoes?: AuditDiffField[];
  statusIntegridade: "VERIFIED" | "ALERT";
}

export interface AuditFilterParams {
  dataInicio: string;
  dataFim: string;
  termoDescricao: string;
  operadorQuery: string;
  perfilCargo: string;
  tipoOperacao: string;
  modulo: string;
  nivelSensibilidade: string;
}

// ==========================================
// SEED AUDITÁVEL (HISTÓRICO REALÍSTICO PRESERVADO)
// ==========================================

const SEED_LOGS: AuditLogEntry[] = [
  {
    id: "LOG-2026-9081",
    timestamp: "2026-09-28T14:15:30",
    operadorNome: "Dr. Carlos Eduardo de Miranda",
    operadorIdentificador: "CRM 12345-PR / CPF: 890.***.***-11",
    operadorCargo: "Médico",
    operadorEmail: "carlos.miranda@clinicore.com.br",
    acaoDescricao: "Assinatura digital e emissão de laudo oftalmológico com fechamento de consulta bilateral.",
    modulo: "Prontuário Médico",
    objetoAfetado: "Laudo Oftalmológico #8841 (Paciente: Paulo Pereira)",
    tipoOperacao: "CREATE",
    nivelSensibilidade: "DADO_SENSIVEL",
    ipOrigem: "192.168.1.45",
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 CliniCoreDesktop/2.6",
    sha256Hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    baseLegalLGPD: "Art. 7º, VIII c/c Art. 11, II, f - Tutela da Saúde por Profissionais Médicos",
    statusIntegridade: "VERIFIED"
  },
  {
    id: "LOG-2026-9080",
    timestamp: "2026-09-28T13:40:12",
    operadorNome: "Recepção Central (Patrícia Souza)",
    operadorIdentificador: "MAT-0492 / CPF: 345.***.***-23",
    operadorCargo: "Recepção",
    operadorEmail: "patricia.souza@clinicore.com.br",
    acaoDescricao: "Cancelamento de 12 agendamentos em lote devido à ausência médica imprevista com envio de SMS.",
    modulo: "Agenda/Escala",
    objetoAfetado: "Grade de Consultas - Consultório 1 (Dr. Fernando Lima)",
    tipoOperacao: "UPDATE",
    nivelSensibilidade: "GERAL",
    ipOrigem: "192.168.1.12",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0",
    sha256Hash: "8f4811985fed2d142109e25d2c256037e90eb2165a25039ca7b5247963ef55ef",
    baseLegalLGPD: "Art. 7º, V - Execução de Contrato e Prestação de Serviços de Saúde",
    diffAlteracoes: [
      { campo: "Status da Grade", anterior: "CONFIRMADO_ATIVO (12 pacientes)", novo: "CANCELADO_LOTE_AUSENCIA_MEDICA" },
      { campo: "Alerta de Notificação", anterior: "Pendente", novo: "Disparado via Mensageria Local" }
    ],
    statusIntegridade: "ALERT"
  },
  {
    id: "LOG-2026-9079",
    timestamp: "2026-09-28T11:22:05",
    operadorNome: "Dra. Mariana Costa",
    operadorIdentificador: "CRM 67890-PR / CPF: 456.***.***-89",
    operadorCargo: "Médico",
    operadorEmail: "mariana.costa@clinicore.com.br",
    acaoDescricao: "Acesso de leitura detalhado aos exames prévios de mapeamento de retina e tonometria de aplanação.",
    modulo: "Prontuário Médico",
    objetoAfetado: "Prontuário Eletrônico ID: pac-771 (Maria Aparecida Santos)",
    tipoOperacao: "READ",
    nivelSensibilidade: "DADO_SENSIVEL",
    ipOrigem: "192.168.1.50",
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) Firefox/130.0",
    sha256Hash: "bfb8830154823a0709b1f09c6db11e03a987627443fb721867c48833989be044",
    baseLegalLGPD: "Art. 7º, VIII - Tutela da Saúde",
    statusIntegridade: "VERIFIED"
  },
  {
    id: "LOG-2026-9078",
    timestamp: "2026-09-27T16:04:19",
    operadorNome: "Marcos Vinicius (Faturamento)",
    operadorIdentificador: "MAT-0118 / CPF: 678.***.***-34",
    operadorCargo: "Faturamento",
    operadorEmail: "faturamento@clinicore.com.br",
    acaoDescricao: "Alteração de valor e status de guia TISS de Facectomia após conferência de OPME (LIO Dobrável).",
    modulo: "Financeiro/Faturamento",
    objetoAfetado: "Guia TISS #20260901001 (Operadora: Unimed)",
    tipoOperacao: "UPDATE",
    nivelSensibilidade: "GERAL",
    ipOrigem: "192.168.1.28",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0",
    sha256Hash: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
    baseLegalLGPD: "Art. 7º, II - Cumprimento de Obrigação Legal ou Regulatória (ANS)",
    diffAlteracoes: [
      { campo: "Valor Total da Guia", anterior: "R$ 4.250,00", novo: "R$ 4.800,00" },
      { campo: "Insumo Vinculado", anterior: "LIO Monofocal Padrão", novo: "LIO AcrySof IQ SN60WF (+21.5 D)" }
    ],
    statusIntegridade: "VERIFIED"
  },
  {
    id: "LOG-2026-9077",
    timestamp: "2026-09-26T10:15:00",
    operadorNome: "Carlos Mendes (Farmácia)",
    operadorIdentificador: "CRF 34102-SP / CPF: 789.***.***-55",
    operadorCargo: "Farmácia",
    operadorEmail: "farmacia@clinicore.com.br",
    acaoDescricao: "Exportação em lote do inventário de LIOs e insumos sob temperatura controlada (Cadeia Fria 2-8°C).",
    modulo: "Prescrição & Farmácia",
    objetoAfetado: "Relatório de Rastreabilidade ANVISA RDC 157",
    tipoOperacao: "EXPORT",
    nivelSensibilidade: "GERAL",
    ipOrigem: "192.168.1.33",
    userAgent: "Mozilla/5.0 (X11; Linux x86_64) Chrome/128.0",
    sha256Hash: "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
    baseLegalLGPD: "Art. 7º, II - Cumprimento de Obrigação Legal (ANVISA)",
    statusIntegridade: "VERIFIED"
  },
  {
    id: "LOG-2026-9076",
    timestamp: "2026-09-25T18:50:41",
    operadorNome: "Admin Geral do Sistema",
    operadorIdentificador: "ADMIN-01 / CPF: 000.***.***-00",
    operadorCargo: "Admin",
    operadorEmail: "seguranca@clinicore.com.br",
    acaoDescricao: "Tentativa de login com credencial incorreta bloqueada após 3 falhas consecutivas.",
    modulo: "Dados Pessoais/Cadastrais",
    objetoAfetado: "Sessão Administrativa de Autenticação",
    tipoOperacao: "AUTH_EVENT",
    nivelSensibilidade: "GERAL",
    ipOrigem: "189.40.112.5",
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    sha256Hash: "a189f30b91df01b7a2d8e4f16421948eb3a699c4d216503c80ff524e4604e389",
    baseLegalLGPD: "Art. 7º, IX - Legítimo Interesse (Segurança da Informação e Prevenção à Fraude)",
    statusIntegridade: "ALERT"
  }
];

export default function ModuloAuditoriaLGPDPage() {
  const [logs] = useState<AuditLogEntry[]>(SEED_LOGS);
  const [logSelecionado, setLogSelecionado] = useState<AuditLogEntry | null>(null);

  // Estados dos Filtros
  const [filtros, setFiltros] = useState<AuditFilterParams>({
    dataInicio: "",
    dataFim: "",
    termoDescricao: "",
    operadorQuery: "",
    perfilCargo: "TODOS",
    tipoOperacao: "TODOS",
    modulo: "TODOS",
    nivelSensibilidade: "TODOS"
  });

  // Debounce auxiliar para campos de texto
  const [termoTemp, setTermoTemp] = useState("");
  const [operadorTemp, setOperadorTemp] = useState("");

  useEffect(() => {
    const handler = setTimeout(() => {
      setFiltros(prev => ({
        ...prev,
        termoDescricao: termoTemp,
        operadorQuery: operadorTemp
      }));
    }, 300);
    return () => clearTimeout(handler);
  }, [termoTemp, operadorTemp]);

  // Paginação
  const [paginaAtual, setPaginaAtual] = useState(1);
  const ITENS_POR_PAGINA = 5;

  // Sanitizador simples para proteção contra injeções de string
  const sanitizar = (texto: string) => texto.replace(/[<>\'"%;()&+]/g, "").trim();

  // Presets de Intervalos Rápidos
  const aplicarPreset = (tipo: "HOJE" | "24H" | "7DIAS" | "MES") => {
    const agora = new Date("2026-09-28T23:59:59");
    let inicio = new Date("2026-09-28T00:00:00");

    if (tipo === "24H") {
      inicio = new Date(agora.getTime() - 24 * 60 * 60 * 1000);
    } else if (tipo === "7DIAS") {
      inicio = new Date(agora.getTime() - 7 * 24 * 60 * 60 * 1000);
    } else if (tipo === "MES") {
      inicio = new Date("2026-09-01T00:00:00");
    }

    const fmt = (d: Date) => d.toISOString().slice(0, 19);
    setFiltros(prev => ({
      ...prev,
      dataInicio: fmt(inicio),
      dataFim: fmt(agora)
    }));
  };

  const limparFiltros = () => {
    setTermoTemp("");
    setOperadorTemp("");
    setFiltros({
      dataInicio: "",
      dataFim: "",
      termoDescricao: "",
      operadorQuery: "",
      perfilCargo: "TODOS",
      tipoOperacao: "TODOS",
      modulo: "TODOS",
      nivelSensibilidade: "TODOS"
    });
    setPaginaAtual(1);
  };

  // Filtragem Otimizada com useMemo
  const logsFiltrados = useMemo(() => {
    return logs.filter(log => {
      // Data Início e Fim
      if (filtros.dataInicio && new Date(log.timestamp) < new Date(filtros.dataInicio)) {
        return false;
      }
      if (filtros.dataFim && new Date(log.timestamp) > new Date(filtros.dataFim)) {
        return false;
      }

      // Descrição Full-Text
      if (filtros.termoDescricao) {
        const termo = sanitizar(filtros.termoDescricao.toLowerCase());
        const matchDesc = log.acaoDescricao.toLowerCase().includes(termo);
        const matchObj = log.objetoAfetado.toLowerCase().includes(termo);
        if (!matchDesc && !matchObj) return false;
      }

      // Operador (Nome, CPF ou E-mail)
      if (filtros.operadorQuery) {
        const op = sanitizar(filtros.operadorQuery.toLowerCase());
        const matchNome = log.operadorNome.toLowerCase().includes(op);
        const matchIdent = log.operadorIdentificador.toLowerCase().includes(op);
        const matchEmail = log.operadorEmail.toLowerCase().includes(op);
        if (!matchNome && !matchIdent && !matchEmail) return false;
      }

      // Cargo
      if (filtros.perfilCargo !== "TODOS" && log.operadorCargo !== filtros.perfilCargo) {
        return false;
      }

      // Tipo de Operação
      if (filtros.tipoOperacao !== "TODOS" && log.tipoOperacao !== filtros.tipoOperacao) {
        return false;
      }

      // Módulo
      if (filtros.modulo !== "TODOS" && log.modulo !== filtros.modulo) {
        return false;
      }

      // Sensibilidade LGPD
      if (filtros.nivelSensibilidade !== "TODOS" && log.nivelSensibilidade !== filtros.nivelSensibilidade) {
        return false;
      }

      return true;
    });
  }, [logs, filtros]);

  // Paginação dos resultados filtrados
  const totalPaginas = Math.ceil(logsFiltrados.length / ITENS_POR_PAGINA) || 1;
  const logsPaginados = useMemo(() => {
    const inicio = (paginaAtual - 1) * ITENS_POR_PAGINA;
    return logsFiltrados.slice(inicio, inicio + ITENS_POR_PAGINA);
  }, [logsFiltrados, paginaAtual]);

  // Exportação em formato CSV Auditável
  const exportarCSV = () => {
    const cabecalho = "ID_LOG;DATA_HORA;OPERADOR;CARGO;CPF_MATRICULA;MODULO;ACAO;OBJETO;OPERACAO;SENSIBILIDADE;BASE_LEGAL;IP;HASH_SHA256\\n";
    const linhas = logsFiltrados.map(l =>
      `"${l.id}";"${l.timestamp}";"${l.operadorNome}";"${l.operadorCargo}";"${l.operadorIdentificador}";"${l.modulo}";"${l.acaoDescricao.replace(/"/g, '""')}";"${l.objetoAfetado}";"${l.tipoOperacao}";"${l.nivelSensibilidade}";"${l.baseLegalLGPD}";"${l.ipOrigem}";"${l.sha256Hash}"`
    ).join("\\n");

    const relatorioFinal = `RELATORIO DE CONFORMIDADE LGPD - CLINICORE ERP\\nEMISSAO: 2026-09-28 23:59:59 (BRT)\\nSOLICITANTE: DPO / Seguranca da Informacao\\nTOTAL REGISTROS FILTRADOS: ${logsFiltrados.length}\\n\\n` + cabecalho + linhas;

    const blob = new Blob([relatorioFinal], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `trilha_auditoria_lgpd_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Cores semânticas para tipo de operação
  const getBadgeOperacao = (tipo: TipoOperacao) => {
    switch (tipo) {
      case "CREATE":
        return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">CRIAÇÃO</span>;
      case "READ":
        return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-blue-500/15 text-blue-400 border border-blue-500/30">LEITURA</span>;
      case "UPDATE":
        return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30">EDIÇÃO</span>;
      case "DELETE":
        return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30">EXCLUSÃO</span>;
      case "EXPORT":
        return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-purple-500/15 text-purple-400 border border-purple-500/30">EXPORTAÇÃO</span>;
      case "AUTH_EVENT":
        return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-orange-500/15 text-orange-400 border border-orange-500/30">SEGURANÇA</span>;
    }
  };

  return (
    <div className="p-8 max-w-[1700px] mx-auto text-slate-100">
      {/* Cabeçalho da Trilha de Auditoria */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-3">
            <ShieldCheck className="w-8 h-8 text-blue-400" />
            <h1 className="text-2xl font-black text-white">Trilha de Auditoria & Conformidade LGPD</h1>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Rastreabilidade imutável de acessos a prontuários (Art. 5º, II da LGPD), assinaturas com hash SHA-256 e segurança regulatória.
          </p>
        </div>

        {/* Botões de Exportação */}
        <div className="flex items-center gap-3">
          <button
            onClick={exportarCSV}
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-bold flex items-center gap-2 transition cursor-pointer"
          >
            <FileSpreadsheet className="w-4 h-4 text-emerald-400" /> Exportar CSV
          </button>
          <button
            onClick={() => window.print()}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 transition shadow-lg shadow-blue-900/30 cursor-pointer"
          >
            <Printer className="w-4 h-4" /> Relatório Imprimível / PDF
          </button>
        </div>
      </div>

      {/* ======================================================== */}
      {/* 1. BARRA DE FILTROS AVANÇADA */}
      {/* ======================================================== */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 mb-6 backdrop-blur-sm space-y-4">
        {/* Linha 1: Intervalos Rápidos e Datas */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-blue-400" /> Período:
            </span>
            <button
              onClick={() => aplicarPreset("HOJE")}
              className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition cursor-pointer"
            >
              Hoje
            </button>
            <button
              onClick={() => aplicarPreset("24H")}
              className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition cursor-pointer"
            >
              Últimas 24h
            </button>
            <button
              onClick={() => aplicarPreset("7DIAS")}
              className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition cursor-pointer"
            >
              Últimos 7 dias
            </button>
            <button
              onClick={() => aplicarPreset("MES")}
              className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition cursor-pointer"
            >
              Mês Atual
            </button>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <input
              type="datetime-local"
              value={filtros.dataInicio}
              onChange={e => setFiltros({ ...filtros, dataInicio: e.target.value })}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-blue-500"
            />
            <span className="text-slate-500">até</span>
            <input
              type="datetime-local"
              value={filtros.dataFim}
              onChange={e => setFiltros({ ...filtros, dataFim: e.target.value })}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={limparFiltros}
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition cursor-pointer"
              title="Limpar todos os filtros"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Linha 2: Busca por Usuário, Full-text e Dropdowns Regulatórios */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
          {/* Busca por Operador */}
          <div className="md:col-span-3 relative">
            <User className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Operador (Nome, CPF ou E-mail)..."
              value={operadorTemp}
              onChange={e => setOperadorTemp(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Busca Textual Livre na Ação */}
          <div className="md:col-span-4 relative">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Descrição do feito ou objeto afetado (Full-text)..."
              value={termoTemp}
              onChange={e => setTermoTemp(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Dropdown Operação */}
          <div className="md:col-span-2">
            <select
              value={filtros.tipoOperacao}
              onChange={e => setFiltros({ ...filtros, tipoOperacao: e.target.value })}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
            >
              <option value="TODOS">Todas Operações</option>
              <option value="READ">Visualização (Read)</option>
              <option value="CREATE">Criação (Create)</option>
              <option value="UPDATE">Edição (Update)</option>
              <option value="DELETE">Exclusão (Delete)</option>
              <option value="EXPORT">Exportação</option>
              <option value="AUTH_EVENT">Segurança / Login</option>
            </select>
          </div>

          {/* Dropdown Módulo */}
          <div className="md:col-span-3">
            <select
              value={filtros.modulo}
              onChange={e => setFiltros({ ...filtros, modulo: e.target.value })}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
            >
              <option value="TODOS">Todos os Módulos</option>
              <option value="Prontuário Médico">Prontuário Médico</option>
              <option value="Dados Pessoais/Cadastrais">Dados Pessoais/Cadastrais</option>
              <option value="Financeiro/Faturamento">Financeiro/Faturamento</option>
              <option value="Agenda/Escala">Agenda/Escala</option>
              <option value="Prescrição & Farmácia">Prescrição & Farmácia</option>
            </select>
          </div>
        </div>

        {/* Linha 3: Filtro de Sensibilidade LGPD */}
        <div className="flex items-center justify-between pt-1 text-xs">
          <div className="flex items-center gap-2">
            <span className="text-slate-400 font-semibold">Sensibilidade LGPD:</span>
            <button
              onClick={() => setFiltros({ ...filtros, nivelSensibilidade: "TODOS" })}
              className={`px-2.5 py-0.5 rounded-full transition cursor-pointer font-bold ${
                filtros.nivelSensibilidade === "TODOS"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200"
              }`}
            >
              Todos
            </button>
            <button
              onClick={() => setFiltros({ ...filtros, nivelSensibilidade: "DADO_SENSIVEL" })}
              className={`px-2.5 py-0.5 rounded-full transition cursor-pointer font-bold flex items-center gap-1 ${
                filtros.nivelSensibilidade === "DADO_SENSIVEL"
                  ? "bg-rose-600 text-white"
                  : "bg-slate-800 text-rose-300 hover:bg-slate-700"
              }`}
            >
              <Lock className="w-3 h-3" /> Art. 5º, II (Dado Sensível de Saúde)
            </button>
            <button
              onClick={() => setFiltros({ ...filtros, nivelSensibilidade: "GERAL" })}
              className={`px-2.5 py-0.5 rounded-full transition cursor-pointer font-bold ${
                filtros.nivelSensibilidade === "GERAL"
                  ? "bg-slate-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200"
              }`}
            >
              Dado Pessoal Geral
            </button>
          </div>

          <div className="text-slate-400">
            Total filtrado: <span className="font-bold text-white">{logsFiltrados.length}</span> eventos
          </div>
        </div>
      </div>

      {/* ======================================================== */}
      {/* 2. TABELA DE AUDITORIA DE ALTA DENSIDADE */}
      {/* ======================================================== */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/60 text-slate-400 uppercase tracking-wider font-semibold">
                <th className="py-3 px-4">Data / Hora</th>
                <th className="py-3 px-4">Operação</th>
                <th className="py-3 px-4">Usuário / Responsável</th>
                <th className="py-3 px-4">Ação Realizada</th>
                <th className="py-3 px-4">Entidade Afetada</th>
                <th className="py-3 px-4">IP / Origem</th>
                <th className="py-3 px-4 text-center">Integridade</th>
                <th className="py-3 px-4 text-center">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {logsPaginados.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-500">
                    Nenhum registro de auditoria encontrado para os critérios selecionados.
                  </td>
                </tr>
              ) : (
                logsPaginados.map(log => (
                  <tr key={log.id} className="hover:bg-slate-800/40 transition">
                    {/* Timestamp */}
                    <td className="py-3.5 px-4 font-mono text-slate-300 whitespace-nowrap">
                      {log.timestamp.replace("T", " ")}
                    </td>

                    {/* Tag da Operação */}
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      {getBadgeOperacao(log.tipoOperacao)}
                    </td>

                    {/* Operador */}
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-white">{log.operadorNome}</div>
                      <div className="text-[11px] text-slate-400">{log.operadorCargo} • {log.operadorIdentificador}</div>
                    </td>

                    {/* Descrição da Ação */}
                    <td className="py-3.5 px-4 max-w-sm truncate text-slate-200" title={log.acaoDescricao}>
                      {log.acaoDescricao}
                    </td>

                    {/* Objeto Afetado */}
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-slate-300">{log.objetoAfetado}</div>
                      <span className="text-[10px] text-blue-400">{log.modulo}</span>
                    </td>

                    {/* IP & Dispositivo */}
                    <td className="py-3.5 px-4 font-mono text-slate-400 whitespace-nowrap">
                      <div>{log.ipOrigem}</div>
                      <div className="text-[10px] text-slate-500 truncate max-w-[120px]" title={log.userAgent}>
                        {log.userAgent.includes("Linux") ? "Linux Mint" : log.userAgent.includes("Windows") ? "Windows" : "Web"}
                      </div>
                    </td>

                    {/* Integridade Hash */}
                    <td className="py-3.5 px-4 text-center whitespace-nowrap">
                      {log.statusIntegridade === "VERIFIED" ? (
                        <span className="inline-flex items-center gap-1 text-[11px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full font-mono">
                          <CheckCircle2 className="w-3 h-3" /> SUCCESS
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[11px] text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full font-mono">
                          <AlertTriangle className="w-3 h-3" /> ALERT
                        </span>
                      )}
                    </td>

                    {/* Ação */}
                    <td className="py-3.5 px-4 text-center">
                      <button
                        onClick={() => setLogSelecionado(log)}
                        className="p-1.5 bg-slate-800 hover:bg-blue-600 hover:text-white text-slate-300 rounded-lg transition cursor-pointer"
                        title="Inspecionar Detalhes do Log (Forense & LGPD)"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Rodapé e Paginação */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-slate-800 bg-slate-950/40 text-xs">
          <span className="text-slate-400">
            Mostrando página <strong className="text-white">{paginaAtual}</strong> de <strong className="text-white">{totalPaginas}</strong> ({logsFiltrados.length} registros no total)
          </span>

          <div className="flex items-center gap-2">
            <button
              disabled={paginaAtual <= 1}
              onClick={() => setPaginaAtual(prev => Math.max(1, prev - 1))}
              className="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 disabled:opacity-40 transition cursor-pointer"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-mono text-slate-300 px-2">{paginaAtual}</span>
            <button
              disabled={paginaAtual >= totalPaginas}
              onClick={() => setPaginaAtual(prev => Math.min(totalPaginas, prev + 1))}
              className="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 disabled:opacity-40 transition cursor-pointer"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* ======================================================== */}
      {/* 3. MODAL DE INSPEÇÃO FORENSE & DETALHES LGPD */}
      {/* ======================================================== */}
      {logSelecionado && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl my-8 p-6 shadow-2xl relative">
            {/* Header Modal */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
              <div className="flex items-center gap-2.5">
                <Fingerprint className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-black text-white">Inspeção Forense & Detalhes do Log LGPD</h3>
              </div>
              <button
                onClick={() => setLogSelecionado(null)}
                className="text-slate-400 hover:text-white transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-6 text-xs">
              {/* Metadados Básicos */}
              <div className="grid grid-cols-2 gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div>
                  <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Identificador do Evento</span>
                  <div className="font-mono font-bold text-white text-sm mt-0.5">{logSelecionado.id}</div>
                </div>
                <div>
                  <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Data & Hora Exata (ISO)</span>
                  <div className="font-mono text-emerald-400 text-sm mt-0.5">{logSelecionado.timestamp.replace("T", " ")}</div>
                </div>
                <div>
                  <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Operador Responsável</span>
                  <div className="font-bold text-white mt-0.5">{logSelecionado.operadorNome}</div>
                  <div className="text-slate-400 text-[11px]">{logSelecionado.operadorIdentificador} ({logSelecionado.operadorEmail})</div>
                </div>
                <div>
                  <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Tipo de Operação & Módulo</span>
                  <div className="mt-1 flex items-center gap-2">
                    {getBadgeOperacao(logSelecionado.tipoOperacao)}
                    <span className="text-slate-300 font-semibold">{logSelecionado.modulo}</span>
                  </div>
                </div>
              </div>

              {/* Base Legal e Sensibilidade LGPD */}
              <div className="bg-blue-950/30 border border-blue-800/60 p-4 rounded-xl">
                <div className="flex items-center gap-2 text-blue-300 font-bold mb-1">
                  <ShieldCheck className="w-4 h-4 text-blue-400" />
                  <span>Enquadramento Legal & Justificativa (LGPD):</span>
                </div>
                <p className="text-slate-300 leading-relaxed font-mono text-[11px]">
                  {logSelecionado.baseLegalLGPD}
                </p>
                <div className="mt-2 flex items-center gap-2">
                  <span className="text-[10px] uppercase font-bold text-slate-400">Classificação:</span>
                  {logSelecionado.nivelSensibilidade === "DADO_SENSIVEL" ? (
                    <span className="text-rose-400 font-bold">Dado Pessoal Sensível de Saúde (Art. 5º, II da LGPD)</span>
                  ) : (
                    <span className="text-slate-300 font-semibold">Dado Cadastral / Administrativo</span>
                  )}
                </div>
              </div>

              {/* Diff Viewer (Antes vs. Depois) se for Update */}
              {logSelecionado.diffAlteracoes && logSelecionado.diffAlteracoes.length > 0 && (
                <div>
                  <h4 className="font-bold text-white mb-2 flex items-center gap-1.5">
                    <FileText className="w-4 h-4 text-amber-400" /> Comparativo de Alteração (Diff Viewer)
                  </h4>
                  <div className="border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800 bg-slate-950">
                    {logSelecionado.diffAlteracoes.map((diff, idx) => (
                      <div key={idx} className="p-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-red-950/20 border border-red-900/40 p-2.5 rounded-lg">
                          <span className="text-[10px] text-red-400 font-bold uppercase tracking-wider block mb-1">
                            [-] Valor Anterior ({diff.campo}):
                          </span>
                          <span className="font-mono text-red-200">{diff.anterior || "(vazio)"}</span>
                        </div>
                        <div className="bg-emerald-950/20 border border-emerald-900/40 p-2.5 rounded-lg">
                          <span className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider block mb-1 flex items-center gap-1">
                            <ArrowRight className="w-3 h-3 text-emerald-400" /> [+] Novo Valor:
                          </span>
                          <span className="font-mono text-emerald-200 font-semibold">{diff.novo}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Informações Técnicas e Hash SHA-256 */}
              <div className="space-y-2 bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-[11px]">
                <div className="flex flex-col gap-1">
                  <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Assinatura de Integridade (SHA-256)</span>
                  <span className="text-emerald-400 break-all bg-slate-900 p-2 rounded-lg border border-slate-800 select-all">
                    {logSelecionado.sha256Hash}
                  </span>
                </div>
                <div className="flex flex-col gap-1 pt-2">
                  <span className="text-slate-500 uppercase tracking-wider text-[10px] font-bold">Endereço IP & Dispositivo / User-Agent</span>
                  <span className="text-slate-300">IP: {logSelecionado.ipOrigem}</span>
                  <span className="text-slate-500 text-[10px] break-all">{logSelecionado.userAgent}</span>
                </div>
              </div>
            </div>

            {/* Ações Modal */}
            <div className="flex justify-end pt-5 border-t border-slate-800 mt-6">
              <button
                onClick={() => setLogSelecionado(null)}
                className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold transition cursor-pointer"
              >
                Fechar Inspeção
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
'''

open(ARQ, "w", encoding="utf-8").write(codigo)
print("[OK] Modulo Auditoria & Trilha de Logs LGPD atualizado com sucesso.")
