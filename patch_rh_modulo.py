import shutil, datetime

ARQ = "frontend/src/app/dashboard/rh/page.tsx"
bak = f"{ARQ}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}"
shutil.copy(ARQ, bak)
print(f"[OK] Backup criado em: {bak}")

codigo = '''"use client";

import React, { useState, useEffect, useMemo } from "react";
import {
  Users,
  Calendar,
  Clock,
  PlusCircle,
  AlertTriangle,
  CheckCircle2,
  X,
  Search,
  Building,
  UserCheck,
  Stethoscope,
  Briefcase,
  MapPin,
  Phone,
  Mail,
  ShieldAlert
} from "lucide-react";

// Tipagens Estritas
export type Cargo =
  | "Médico"
  | "Cirurgião"
  | "Instrumentador(a)"
  | "Anestesiologista"
  | "Recepção"
  | "Financeiro"
  | "Faturamento"
  | "Farmácia"
  | "Admin";

export type Especialidade =
  | "Retina"
  | "Glaucoma"
  | "Refrativa"
  | "Oftalmopediatria"
  | "Estrabismo"
  | "Plástica"
  | "Outros";

export type DiaSemana = "Seg" | "Ter" | "Qua" | "Qui" | "Sex" | "Sáb";

export interface Colaborador {
  id: string;
  nome: string;
  cargo: Cargo;
  cpf: string;
  rg: string;
  registroConselho?: string;
  ufConselho?: string;
  especialidade?: string;
  telefone: string;
  email: string;
  cep: string;
  logradouro: string;
  numero: string;
  complemento?: string;
  bairro: string;
  cidade: string;
  uf: string;
}

export interface PlantaoEscala {
  id: string;
  colaboradorId: string;
  diasSemana: DiaSemana[];
  horaEntrada: string; // "08:00"
  horaSaida: string;   // "17:00"
  localAlocacao: string; // "Consultório 1", "Centro Cirúrgico - Sala 1", etc.
  observacoes?: string;
}

const DIAS_SEMANA: DiaSemana[] = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

const SEED_COLABORADORES: Colaborador[] = [
  {
    id: "colab-1",
    nome: "Dr. Roberto Matos",
    cargo: "Médico",
    cpf: "123.456.789-01",
    rg: "12.345.678-9",
    registroConselho: "CRM 54210",
    ufConselho: "SP",
    especialidade: "Retina",
    telefone: "(11) 98123-4567",
    email: "roberto.matos@clinicore.com.br",
    cep: "01310-100",
    logradouro: "Av. Paulista",
    numero: "1000",
    bairro: "Bela Vista",
    cidade: "São Paulo",
    uf: "SP"
  },
  {
    id: "colab-2",
    nome: "Dra. Camila Vasconcelos",
    cargo: "Cirurgião",
    cpf: "234.567.890-12",
    rg: "23.456.789-0",
    registroConselho: "CRM 68920",
    ufConselho: "SP",
    especialidade: "Glaucoma",
    telefone: "(11) 97234-5678",
    email: "camila.vasconcelos@clinicore.com.br",
    cep: "04001-000",
    logradouro: "Rua Vergueiro",
    numero: "500",
    bairro: "Paraíso",
    cidade: "São Paulo",
    uf: "SP"
  },
  {
    id: "colab-3",
    nome: "Patrícia Souza",
    cargo: "Recepção",
    cpf: "345.678.901-23",
    rg: "34.567.890-1",
    telefone: "(11) 96345-6789",
    email: "patricia.souza@clinicore.com.br",
    cep: "01502-001",
    logradouro: "Rua da Glória",
    numero: "250",
    bairro: "Liberdade",
    cidade: "São Paulo",
    uf: "SP"
  }
];

const SEED_ESCALAS: PlantaoEscala[] = [
  {
    id: "esc-1",
    colaboradorId: "colab-1",
    diasSemana: ["Seg", "Qua", "Sex"],
    horaEntrada: "08:00",
    horaSaida: "14:00",
    localAlocacao: "Consultório 1"
  },
  {
    id: "esc-2",
    colaboradorId: "colab-2",
    diasSemana: ["Ter", "Qui"],
    horaEntrada: "07:30",
    horaSaida: "13:30",
    localAlocacao: "Centro Cirúrgico - Sala 1"
  },
  {
    id: "esc-3",
    colaboradorId: "colab-3",
    diasSemana: ["Seg", "Ter", "Qua", "Qui", "Sex"],
    horaEntrada: "08:00",
    horaSaida: "17:00",
    localAlocacao: "Recepção Central"
  }
];

export default function ModuloRHPage() {
  const [colaboradores, setColaboradores] = useState<Colaborador[]>(SEED_COLABORADORES);
  const [escalas, setEscalas] = useState<PlantaoEscala[]>(SEED_ESCALAS);

  // Controle de Modais
  const [modalColaborador, setModalColaborador] = useState(false);
  const [modalEscalas, setModalEscalas] = useState(false);

  // Form Colaborador
  const [formColab, setFormColab] = useState<Partial<Colaborador>>({
    cargo: "Médico",
    uf: "SP",
    ufConselho: "SP"
  });
  const [especialidadeOutros, setEspecialidadeOutros] = useState("");
  const [loadingCep, setLoadingCep] = useState(false);
  const [salvandoColab, setSalvandoColab] = useState(false);
  const [erroFormColab, setErroFormColab] = useState("");

  // Form Escala
  const [formEscala, setFormEscala] = useState<Partial<PlantaoEscala>>({
    colaboradorId: "",
    diasSemana: ["Seg"],
    horaEntrada: "08:00",
    horaSaida: "14:00",
    localAlocacao: "Consultório 1"
  });
  const [filtroColabEscala, setFiltroColabEscala] = useState("");
  const [conflitoAlerta, setConflitoAlerta] = useState<string | null>(null);

  // Carregar do localStorage se existir
  useEffect(() => {
    try {
      const colabLocal = localStorage.getItem("rh_colaboradores");
      const escalasLocal = localStorage.getItem("rh_escalas");
      if (colabLocal) setColaboradores(JSON.parse(colabLocal));
      if (escalasLocal) setEscalas(JSON.parse(escalasLocal));
    } catch (e) {
      console.error(e);
    }
  }, []);

  const salvarColaboradoresLocal = (lista: Colaborador[]) => {
    setColaboradores(lista);
    localStorage.setItem("rh_colaboradores", JSON.stringify(lista));
  };

  const salvarEscalasLocal = (lista: PlantaoEscala[]) => {
    setEscalas(lista);
    localStorage.setItem("rh_escalas", JSON.stringify(lista));
  };

  // Mascaras
  const maskCPF = (v: string) =>
    v.replace(/\D/g, "").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2").slice(0, 14);

  const maskPhone = (v: string) =>
    v.replace(/\D/g, "").replace(/(\d{2})(\d)/, "($1) $2").replace(/(\d{5})(\d{4})$/, "$1-$2").slice(0, 15);

  const maskCEP = (v: string) =>
    v.replace(/\D/g, "").replace(/(\d{5})(\d)/, "$1-$2").slice(0, 9);

  // Busca de CEP
  const handleBuscarCep = async (cepRaw: string) => {
    const cepLimpo = cepRaw.replace(/\D/g, "");
    if (cepLimpo.length !== 8) return;
    setLoadingCep(true);
    try {
      const res = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
      const data = await res.json();
      if (!data.erro) {
        setFormColab(prev => ({
          ...prev,
          logradouro: data.logradouro || "",
          bairro: data.bairro || "",
          cidade: data.localidade || "",
          uf: data.uf || ""
        }));
      }
    } catch (err) {
      console.warn("Falha ao buscar CEP online", err);
    } finally {
      setLoadingCep(false);
    }
  };

  // Submissão do Colaborador
  const handleSalvarColaborador = (e: React.FormEvent) => {
    e.preventDefault();
    setErroFormColab("");

    if (!formColab.nome || !formColab.cpf || !formColab.cargo) {
      setErroFormColab("Preencha todos os campos obrigatórios (Nome, Cargo, CPF).");
      return;
    }

    const exigeConselho = ["Médico", "Cirurgião", "Anestesiologista", "Instrumentador(a)"].includes(formColab.cargo);
    if (exigeConselho && !formColab.registroConselho) {
      setErroFormColab("Registro profissional (CRM/COREN) é obrigatório para esta função.");
      return;
    }

    const ehMedico = ["Médico", "Cirurgião"].includes(formColab.cargo);
    let especialidadeFinal = formColab.especialidade;
    if (ehMedico) {
      if (!especialidadeFinal) {
        setErroFormColab("Selecione a especialidade médica.");
        return;
      }
      if (especialidadeFinal === "Outros") {
        if (!especialidadeOutros.trim()) {
          setErroFormColab("Informe a especialidade personalizada em 'Outros'.");
          return;
        }
        especialidadeFinal = especialidadeOutros.trim();
      }
    }

    setSalvandoColab(true);
    setTimeout(() => {
      const novo: Colaborador = {
        id: `colab-${Date.now()}`,
        nome: formColab.nome!,
        cargo: formColab.cargo!,
        cpf: formColab.cpf!,
        rg: formColab.rg || "",
        registroConselho: formColab.registroConselho,
        ufConselho: formColab.ufConselho,
        especialidade: especialidadeFinal,
        telefone: formColab.telefone || "",
        email: formColab.email || "",
        cep: formColab.cep || "",
        logradouro: formColab.logradouro || "",
        numero: formColab.numero || "",
        complemento: formColab.complemento || "",
        bairro: formColab.bairro || "",
        cidade: formColab.cidade || "",
        uf: formColab.uf || "SP"
      };

      salvarColaboradoresLocal([...colaboradores, novo]);
      setSalvandoColab(false);
      setModalColaborador(false);
      setFormColab({ cargo: "Médico", uf: "SP", ufConselho: "SP" });
      setEspecialidadeOutros("");
    }, 400);
  };

  // Validação de Conflito de Escala
  const checarConflito = (novaEscala: Partial<PlantaoEscala>): string | null => {
    if (!novaEscala.colaboradorId || !novaEscala.diasSemana || !novaEscala.horaEntrada || !novaEscala.horaSaida) {
      return null;
    }

    const [entH, entM] = novaEscala.horaEntrada.split(":").map(Number);
    const [saiH, saiM] = novaEscala.horaSaida.split(":").map(Number);
    const minEnt = entH * 60 + entM;
    const minSai = saiH * 60 + saiM;

    if (minSai <= minEnt) {
      return "A hora de saída deve ser posterior ao horário de entrada.";
    }

    for (const esc of escalas) {
      const mesmoDia = esc.diasSemana.some(d => novaEscala.diasSemana!.includes(d));
      if (!mesmoDia) continue;

      const [eH, eM] = esc.horaEntrada.split(":").map(Number);
      const [sH, sM] = esc.horaSaida.split(":").map(Number);
      const curEnt = eH * 60 + eM;
      const curSai = sH * 60 + sM;

      const sobrepoeHorario = Math.max(minEnt, curEnt) < Math.min(minSai, curSai);

      if (sobrepoeHorario) {
        // Conflito 1: O mesmo colaborador com escala sobreposta
        if (esc.colaboradorId === novaEscala.colaboradorId) {
          const colab = colaboradores.find(c => c.id === esc.colaboradorId);
          return `O colaborador ${colab?.nome || ""} já possui plantão alocado neste horário em dia coincidente (${esc.horaEntrada} - ${esc.horaSaida}).`;
        }

        // Conflito 2: Dois profissionais no mesmo consultório/sala
        if (esc.localAlocacao && novaEscala.localAlocacao && esc.localAlocacao === novaEscala.localAlocacao) {
          return `Conflito de Sala: A sala "${novaEscala.localAlocacao}" já está ocupada no mesmo horário (${esc.horaEntrada} - ${esc.horaSaida}).`;
        }
      }
    }

    return null;
  };

  const handleSalvarEscala = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formEscala.colaboradorId || !formEscala.diasSemana?.length) {
      alert("Selecione um colaborador e ao menos um dia da semana.");
      return;
    }

    const conflito = checarConflito(formEscala);
    if (conflito) {
      setConflitoAlerta(conflito);
      return;
    }

    const nova: PlantaoEscala = {
      id: `esc-${Date.now()}`,
      colaboradorId: formEscala.colaboradorId!,
      diasSemana: formEscala.diasSemana!,
      horaEntrada: formEscala.horaEntrada || "08:00",
      horaSaida: formEscala.horaSaida || "14:00",
      localAlocacao: formEscala.localAlocacao || "Consultório 1"
    };

    salvarEscalasLocal([...escalas, nova]);
    setConflitoAlerta(null);
    setFormEscala(prev => ({
      ...prev,
      diasSemana: ["Seg"]
    }));
  };

  const removerEscala = (id: string) => {
    salvarEscalasLocal(escalas.filter(e => e.id !== id));
  };

  // Colaborador Selecionado no form de escala
  const colabSelecionadoEscala = useMemo(() => {
    return colaboradores.find(c => c.id === formEscala.colaboradorId);
  }, [formEscala.colaboradorId, colaboradores]);

  return (
    <div className="p-8 max-w-[1600px] mx-auto text-slate-100">
      {/* Cabeçalho do Módulo */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <div className="flex items-center gap-3">
            <Users className="w-8 h-8 text-blue-400" />
            <h1 className="text-2xl font-black text-white">Recursos Humanos & Escala Médica</h1>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Gestão dos 15 médicos especialistas e alocação para os 3 consultórios físicos da clínica.
          </p>
        </div>

        {/* Botões de Ação Principais */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setModalColaborador(true)}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-bold flex items-center gap-2 transition shadow-lg shadow-blue-900/30 cursor-pointer"
          >
            <PlusCircle className="w-4 h-4" /> Novo Colaborador
          </button>
          <button
            onClick={() => setModalEscalas(true)}
            className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-bold flex items-center gap-2 transition shadow-lg shadow-indigo-900/30 cursor-pointer"
          >
            <Calendar className="w-4 h-4" /> Plantões & Horários
          </button>
        </div>
      </div>

      {/* Cards de Métricas Originais Preservados */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Corpo Clínico Ativo</span>
          <div className="text-3xl font-black text-white mt-2">15 Médicos</div>
          <div className="text-xs text-blue-400 mt-1">Oftalmologia Geral e Cirúrgica</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Salas Físicas</span>
          <div className="text-3xl font-black text-emerald-400 mt-2">3 Consultórios</div>
          <div className="text-xs text-emerald-500/80 mt-1">Sem conflito de agenda</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Plantões & Escalas</span>
          <div className="text-3xl font-black text-purple-400 mt-2">48 Turnos/Mês</div>
          <div className="text-xs text-purple-400/80 mt-1">Alocação 100% preenchida</div>
        </div>
      </div>

      {/* Matriz Semanal Embutida na Visão Geral */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white">Visualização Matricial da Escala Semanal</h2>
          </div>
          <span className="text-xs text-slate-400">Distribuição por consultórios e setores</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider">
                <th className="py-3 px-4 w-64">Setor / Colaborador</th>
                {DIAS_SEMANA.map(d => (
                  <th key={d} className="py-3 px-4 text-center">{d}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {colaboradores.map(c => {
                const escalasColab = escalas.filter(e => e.colaboradorId === c.id);
                return (
                  <tr key={c.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4">
                      <div className="font-bold text-white flex items-center gap-2">
                        {c.nome}
                        {c.cargo === "Cirurgião" && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 font-semibold">Cirurgia</span>
                        )}
                        {c.cargo === "Médico" && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 font-semibold">{c.especialidade}</span>
                        )}
                      </div>
                      <div className="text-xs text-slate-400">{c.cargo} {c.registroConselho ? `• ${c.registroConselho}` : ""}</div>
                    </td>
                    {DIAS_SEMANA.map(dia => {
                      const escalaDia = escalasColab.find(e => e.diasSemana.includes(dia));
                      return (
                        <td key={dia} className="py-3 px-4 text-center">
                          {escalaDia ? (
                            <div className="inline-flex flex-col items-center bg-slate-800/80 border border-slate-700/80 rounded-xl px-2.5 py-1 text-xs">
                              <span className="font-bold text-emerald-400">{escalaDia.horaEntrada} - {escalaDia.horaSaida}</span>
                              <span className="text-[10px] text-slate-400">{escalaDia.localAlocacao}</span>
                            </div>
                          ) : (
                            <span className="text-slate-600 text-xs">—</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* ======================================================== */}
      {/* MODAL 1: CADASTRO DE COLABORADOR */}
      {/* ======================================================== */}
      {modalColaborador && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl my-8 p-6 shadow-2xl relative">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
              <div className="flex items-center gap-2.5">
                <UserCheck className="w-5 h-5 text-blue-400" />
                <h3 className="text-lg font-black text-white">Cadastrar Novo Colaborador</h3>
              </div>
              <button
                onClick={() => setModalColaborador(false)}
                className="text-slate-400 hover:text-white transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {erroFormColab && (
              <div className="mb-4 p-3 bg-red-950/60 border border-red-800/80 rounded-xl flex items-center gap-2 text-red-300 text-xs">
                <AlertTriangle className="w-4 h-4 shrink-0" />
                <span>{erroFormColab}</span>
              </div>
            )}

            <form onSubmit={handleSalvarColaborador} className="space-y-6">
              {/* Seção 1: Dados Pessoais & Função */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                  <Briefcase className="w-3.5 h-3.5 text-blue-400" /> 1. Dados Pessoais & Função
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-xs font-medium text-slate-300 mb-1">Nome Completo *</label>
                    <input
                      type="text"
                      required
                      placeholder="Ex: Dr. Carlos Eduardo de Miranda"
                      value={formColab.nome || ""}
                      onChange={e => setFormColab({ ...formColab, nome: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Posição / Cargo *</label>
                    <select
                      value={formColab.cargo || "Médico"}
                      onChange={e => setFormColab({ ...formColab, cargo: e.target.value as Cargo })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="Médico">Médico</option>
                      <option value="Cirurgião">Cirurgião</option>
                      <option value="Instrumentador(a)">Instrumentador(a)</option>
                      <option value="Anestesiologista">Anestesiologista</option>
                      <option value="Recepção">Recepção</option>
                      <option value="Financeiro">Financeiro</option>
                      <option value="Faturamento">Faturamento</option>
                      <option value="Farmácia">Farmácia</option>
                      <option value="Admin">Admin</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">CPF *</label>
                    <input
                      type="text"
                      required
                      placeholder="000.000.000-00"
                      value={formColab.cpf || ""}
                      onChange={e => setFormColab({ ...formColab, cpf: maskCPF(e.target.value) })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">RG</label>
                    <input
                      type="text"
                      placeholder="00.000.000-0"
                      value={formColab.rg || ""}
                      onChange={e => setFormColab({ ...formColab, rg: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  {/* Registro Profissional Condicional */}
                  {["Médico", "Cirurgião", "Anestesiologista", "Instrumentador(a)"].includes(formColab.cargo || "") && (
                    <div className="grid grid-cols-3 gap-2">
                      <div className="col-span-2">
                        <label className="block text-xs font-medium text-amber-300 mb-1">Registro (CRM/COREN) *</label>
                        <input
                          type="text"
                          required
                          placeholder="Ex: CRM 12345"
                          value={formColab.registroConselho || ""}
                          onChange={e => setFormColab({ ...formColab, registroConselho: e.target.value })}
                          className="w-full bg-slate-950 border border-amber-900/50 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-amber-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-amber-300 mb-1">UF Conselho</label>
                        <input
                          type="text"
                          maxLength={2}
                          placeholder="SP"
                          value={formColab.ufConselho || "SP"}
                          onChange={e => setFormColab({ ...formColab, ufConselho: e.target.value.toUpperCase() })}
                          className="w-full bg-slate-950 border border-amber-900/50 rounded-xl px-3 py-2.5 text-sm text-white uppercase text-center focus:outline-none focus:border-amber-500"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Seção 2: Especialidade Médica Condicional */}
              {["Médico", "Cirurgião"].includes(formColab.cargo || "") && (
                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <Stethoscope className="w-3.5 h-3.5 text-blue-400" /> 2. Especialidade Oftalmológica
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-medium text-slate-300 mb-1">Especialidade *</label>
                      <select
                        value={formColab.especialidade || ""}
                        onChange={e => setFormColab({ ...formColab, especialidade: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                      >
                        <option value="">Selecione...</option>
                        <option value="Retina">Retina</option>
                        <option value="Glaucoma">Glaucoma</option>
                        <option value="Refrativa">Refrativa</option>
                        <option value="Oftalmopediatria">Oftalmopediatria</option>
                        <option value="Estrabismo">Estrabismo</option>
                        <option value="Plástica">Plástica Ocular</option>
                        <option value="Outros">Outros</option>
                      </select>
                    </div>

                    {formColab.especialidade === "Outros" && (
                      <div>
                        <label className="block text-xs font-medium text-indigo-300 mb-1">Especifique a Especialidade *</label>
                        <input
                          type="text"
                          required
                          placeholder="Ex: Córnea / Neuroftalmologia"
                          value={especialidadeOutros}
                          onChange={e => setEspecialidadeOutros(e.target.value)}
                          className="w-full bg-slate-950 border border-indigo-700/60 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-400"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Seção 3: Endereço Completo */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-blue-400" /> 3. Endereço Completo
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">CEP</label>
                    <div className="relative">
                      <input
                        type="text"
                        placeholder="00000-000"
                        value={formColab.cep || ""}
                        onChange={e => {
                          const val = maskCEP(e.target.value);
                          setFormColab({ ...formColab, cep: val });
                          if (val.replace(/\D/g, "").length === 8) handleBuscarCep(val);
                        }}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                      />
                      {loadingCep && (
                        <span className="absolute right-3 top-3 text-[10px] text-blue-400 animate-pulse">Buscando...</span>
                      )}
                    </div>
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-xs font-medium text-slate-300 mb-1">Logradouro / Rua</label>
                    <input
                      type="text"
                      placeholder="Rua, Avenida, etc."
                      value={formColab.logradouro || ""}
                      onChange={e => setFormColab({ ...formColab, logradouro: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Número</label>
                    <input
                      type="text"
                      placeholder="123"
                      value={formColab.numero || ""}
                      onChange={e => setFormColab({ ...formColab, numero: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Complemento</label>
                    <input
                      type="text"
                      placeholder="Apto, Sala, Bloco"
                      value={formColab.complemento || ""}
                      onChange={e => setFormColab({ ...formColab, complemento: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Bairro</label>
                    <input
                      type="text"
                      placeholder="Bairro"
                      value={formColab.bairro || ""}
                      onChange={e => setFormColab({ ...formColab, bairro: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Cidade</label>
                    <input
                      type="text"
                      placeholder="São Paulo"
                      value={formColab.cidade || ""}
                      onChange={e => setFormColab({ ...formColab, cidade: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">UF</label>
                    <input
                      type="text"
                      maxLength={2}
                      placeholder="SP"
                      value={formColab.uf || "SP"}
                      onChange={e => setFormColab({ ...formColab, uf: e.target.value.toUpperCase() })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white uppercase text-center focus:outline-none focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* Seção 4: Contato */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                  <Phone className="w-3.5 h-3.5 text-blue-400" /> 4. Informações de Contato
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Telefone / WhatsApp</label>
                    <input
                      type="text"
                      placeholder="(11) 90000-0000"
                      value={formColab.telefone || ""}
                      onChange={e => setFormColab({ ...formColab, telefone: maskPhone(e.target.value) })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">E-mail Corporativo / Pessoal</label>
                    <input
                      type="email"
                      placeholder="colaborador@clinicore.com.br"
                      value={formColab.email || ""}
                      onChange={e => setFormColab({ ...formColab, email: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* Ações */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setModalColaborador(false)}
                  className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-sm font-semibold transition cursor-pointer"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={salvandoColab}
                  className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-bold transition flex items-center gap-2 shadow-lg shadow-blue-900/30 cursor-pointer disabled:opacity-60"
                >
                  {salvandoColab ? (
                    <>Salvando...</>
                  ) : (
                    <>
                      <CheckCircle2 className="w-4 h-4" /> Salvar Colaborador
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* MODAL 2: GESTÃO DE PLANTÕES & HORÁRIOS */}
      {/* ======================================================== */}
      {modalEscalas && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-5xl my-8 p-6 shadow-2xl relative">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
              <div className="flex items-center gap-2.5">
                <Calendar className="w-5 h-5 text-indigo-400" />
                <h3 className="text-lg font-black text-white">Alocação de Plantões & Horários</h3>
              </div>
              <button
                onClick={() => setModalEscalas(false)}
                className="text-slate-400 hover:text-white transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Alerta de Conflito em Tempo Real */}
            {conflitoAlerta && (
              <div className="mb-6 p-4 bg-amber-950/70 border border-amber-700 rounded-xl flex items-start gap-3 text-amber-300 text-sm">
                <ShieldAlert className="w-5 h-5 shrink-0 mt-0.5 text-amber-400" />
                <div>
                  <span className="font-bold">Atenção - Conflito Identificado:</span>
                  <p className="mt-0.5 text-amber-200/90 text-xs">{conflitoAlerta}</p>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Formulário de Criação de Escala */}
              <form onSubmit={handleSalvarEscala} className="lg:col-span-5 space-y-5 bg-slate-950/40 p-5 rounded-2xl border border-slate-800/80">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <Clock className="w-4 h-4 text-indigo-400" /> Nova Alocação de Turno
                </h4>

                {/* Seleção do Colaborador com Busca */}
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Selecionar Colaborador *</label>
                  <div className="space-y-2">
                    <div className="relative">
                      <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
                      <input
                        type="text"
                        placeholder="Filtrar por nome..."
                        value={filtroColabEscala}
                        onChange={e => setFiltroColabEscala(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                      />
                    </div>
                    <select
                      required
                      value={formEscala.colaboradorId || ""}
                      onChange={e => {
                        const id = e.target.value;
                        const c = colaboradores.find(item => item.id === id);
                        let localPadrao = "Consultório 1";
                        if (c?.cargo === "Cirurgião") localPadrao = "Centro Cirúrgico - Sala 1";
                        if (["Recepção", "Financeiro", "Farmácia", "Admin"].includes(c?.cargo || "")) {
                          localPadrao = `${c?.cargo} Geral`;
                        }

                        setFormEscala(prev => ({
                          ...prev,
                          colaboradorId: id,
                          localAlocacao: localPadrao
                        }));
                        setConflitoAlerta(null);
                      }}
                      className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500"
                    >
                      <option value="">Selecione o profissional...</option>
                      {colaboradores
                        .filter(c => c.nome.toLowerCase().includes(filtroColabEscala.toLowerCase()))
                        .map(c => (
                          <option key={c.id} value={c.id}>
                            {c.nome} ({c.cargo}{c.especialidade ? ` - ${c.especialidade}` : ""})
                          </option>
                        ))}
                    </select>
                  </div>
                </div>

                {/* Dias da Semana (Checkboxes Múltiplos) */}
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">Dias da Semana *</label>
                  <div className="grid grid-cols-6 gap-1.5">
                    {DIAS_SEMANA.map(dia => {
                      const ativo = formEscala.diasSemana?.includes(dia);
                      return (
                        <button
                          key={dia}
                          type="button"
                          onClick={() => {
                            const atuais = formEscala.diasSemana || [];
                            const novos = ativo
                              ? atuais.filter(d => d !== dia)
                              : [...atuais, dia];
                            setFormEscala({ ...formEscala, diasSemana: novos });
                          }}
                          className={`py-2 text-xs font-bold rounded-xl transition border cursor-pointer ${
                            ativo
                              ? "bg-indigo-600 border-indigo-500 text-white"
                              : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700"
                          }`}
                        >
                          {dia}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Horários (24h) */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Entrada *</label>
                    <input
                      type="time"
                      required
                      value={formEscala.horaEntrada || "08:00"}
                      onChange={e => setFormEscala({ ...formEscala, horaEntrada: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Saída *</label>
                    <input
                      type="time"
                      required
                      value={formEscala.horaSaida || "14:00"}
                      onChange={e => setFormEscala({ ...formEscala, horaSaida: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                {/* Local de Alocação Condicional por Cargo */}
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">
                    Local de Alocação{" "}
                    {colabSelecionadoEscala && (
                      <span className="text-[11px] text-indigo-400">({colabSelecionadoEscala.cargo})</span>
                    )}
                  </label>

                  {colabSelecionadoEscala?.cargo === "Cirurgião" ? (
                    <select
                      value={formEscala.localAlocacao || "Centro Cirúrgico - Sala 1"}
                      onChange={e => setFormEscala({ ...formEscala, localAlocacao: e.target.value })}
                      className="w-full bg-slate-900 border border-indigo-700/60 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none"
                    >
                      <option value="Centro Cirúrgico - Sala 1">Centro Cirúrgico - Sala 1</option>
                      <option value="Centro Cirúrgico - Sala 2">Centro Cirúrgico - Sala 2</option>
                      <option value="Atendimento Hospitalar Externo">Atendimento Hospitalar Externo</option>
                    </select>
                  ) : colabSelecionadoEscala?.cargo === "Médico" ? (
                    <select
                      value={formEscala.localAlocacao || "Consultório 1"}
                      onChange={e => setFormEscala({ ...formEscala, localAlocacao: e.target.value })}
                      className="w-full bg-slate-900 border border-blue-700/60 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none"
                    >
                      <option value="Consultório 1">Consultório 1 (Oftalmologia Geral)</option>
                      <option value="Consultório 2">Consultório 2 (Exames / Retina)</option>
                      <option value="Consultório 3">Consultório 3 (Glaucoma / Lentes)</option>
                    </select>
                  ) : (
                    <input
                      type="text"
                      placeholder="Ex: Recepção Central, Sala Financeiro..."
                      value={formEscala.localAlocacao || ""}
                      onChange={e => setFormEscala({ ...formEscala, localAlocacao: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none"
                    />
                  )}
                </div>

                <button
                  type="submit"
                  className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-bold transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-900/30 cursor-pointer"
                >
                  <PlusCircle className="w-4 h-4" /> Alocar na Escala
                </button>
              </form>

              {/* Lista e Gestão das Escalas Ativas */}
              <div className="lg:col-span-7 flex flex-col justify-between">
                <div>
                  <h4 className="text-sm font-bold text-white mb-3 flex items-center justify-between">
                    <span>Plantões & Escalas Atribuídas ({escalas.length})</span>
                    <span className="text-xs text-slate-400 font-normal">Exclusão e visualização de turnos</span>
                  </h4>

                  <div className="space-y-2.5 max-h-[440px] overflow-y-auto pr-1">
                    {escalas.map(esc => {
                      const c = colaboradores.find(col => col.id === esc.colaboradorId);
                      return (
                        <div
                          key={esc.id}
                          className="bg-slate-950/60 border border-slate-800 rounded-xl p-3 flex items-center justify-between hover:border-slate-700 transition"
                        >
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-white text-sm">{c?.nome || "Colaborador"}</span>
                              <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-900/40 text-indigo-300 border border-indigo-700/50">
                                {c?.cargo}
                              </span>
                            </div>
                            <div className="text-xs text-slate-400 mt-1 flex items-center gap-3">
                              <span className="text-emerald-400 font-medium">
                                {esc.horaEntrada} - {esc.horaSaida}
                              </span>
                              <span>•</span>
                              <span className="text-slate-300 font-medium">{esc.localAlocacao}</span>
                              <span>•</span>
                              <span className="text-slate-400">Dias: {esc.diasSemana.join(", ")}</span>
                            </div>
                          </div>

                          <button
                            onClick={() => removerEscala(esc.id)}
                            className="p-1.5 text-slate-500 hover:text-red-400 hover:bg-red-950/30 rounded-lg transition cursor-pointer"
                            title="Remover Plantão"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-800 flex justify-end">
                  <button
                    onClick={() => setModalEscalas(false)}
                    className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-sm font-semibold transition cursor-pointer"
                  >
                    Fechar
                  </button>
                </div>
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
print("[OK] Modulo RH atualizado com sucesso com os dois modais e validacoes.")
