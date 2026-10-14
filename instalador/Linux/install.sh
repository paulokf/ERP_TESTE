#!/usr/bin/env bash
set -e

# Garante permissão de execução
chmod +x setup_system.py 2>/dev/null || true

# Executa pelo Python 3
if command -v python3 &>/dev/null; then
    python3 setup_system.py "$@"
elif command -v python &>/dev/null; then
    python setup_system.py "$@"
else
    echo "Erro: Python 3 não foi encontrado. Instale o Python 3 para rodar a instalação."
    exit 1
fi