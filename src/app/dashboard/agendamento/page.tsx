'use client';

import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Calendar as CalendarIcon, Users } from 'lucide-react';

export default function AgendamentoPage() {
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [isPatientListOpen, setIsPatientListOpen] = useState(false);

  return (
    <div className="space-y-6 p-6 text-slate-100">
      {/* Cabeçalho com Título e Botões de Ação */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Central de Agendamentos
          </h1>
          <p className="text-sm text-slate-400">
            Controle de alocação de 15 médicos em 3 consultórios físicos com validação TUSS/TISS.
          </p>
        </div>

        {/* Toolbar de Ações: Calendário e Carga Diária */}
        <div className="flex items-center gap-3">
          {/* Botão 1: Calendário Mensal */}
          <button
            type="button"
            onClick={() => {
              console.log('Abrindo Calendário Mensal...');
              setIsCalendarOpen(true);
            }}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-sm transition-colors cursor-pointer"
          >
            <CalendarIcon className="w-4 h-4" />
            Calendário Mensal da Clínica
          </button>

          {/* Botão 2: Carga Diária & Lista de Pacientes */}
          <button
            type="button"
            onClick={() => {
              console.log('Abrindo Carga Diária...');
              setIsPatientListOpen(true);
            }}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition-colors cursor-pointer"
          >
            <Users className="w-4 h-4" />
            Carga Diária & Lista de Pacientes
          </button>
        </div>
      </div>

      {/* Modal 1: Calendário Mensal */}
      <Dialog open={isCalendarOpen} onOpenChange={setIsCalendarOpen}>
        <DialogContent className="max-w-2xl bg-slate-900 border border-slate-800 text-white">
          <DialogHeader>
            <DialogTitle className="text-lg font-semibold flex items-center gap-2">
              <CalendarIcon className="w-5 h-5 text-blue-500" />
              Calendário Mensal da Clínica
            </DialogTitle>
          </DialogHeader>
          <div className="py-4 text-sm text-slate-300">
            Visão mensal das escalas e disponibilidade dos 3 consultórios físicos.
          </div>
        </DialogContent>
      </Dialog>

      {/* Modal 2: Carga Diária & Lista de Pacientes */}
      <Dialog open={isPatientListOpen} onOpenChange={setIsPatientListOpen}>
        <DialogContent className="max-w-3xl bg-slate-900 border border-slate-800 text-white">
          <DialogHeader>
            <DialogTitle className="text-lg font-semibold flex items-center gap-2">
              <Users className="w-5 h-5 text-emerald-500" />
              Carga Diária de Atendimentos
            </DialogTitle>
          </DialogHeader>
          <div className="py-4 text-sm text-slate-300">
            Relação dos agendamentos do dia por consultório e fila de espera da recepção.
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
