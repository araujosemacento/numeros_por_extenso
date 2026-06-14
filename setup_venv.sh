#!/usr/bin/env bash
# setup_venv.sh - Configura e ativa o ambiente virtual Python (Linux/macOS)

set -e

DIR_PROJETO="$(cd "$(dirname "$0")" && pwd)"
VENV_NOME=".venv"
VENV_CAMINHO="$DIR_PROJETO/$VENV_NOME"

echo "========================================"
echo "  Configuração do Ambiente Virtual"
echo "  SO: $(uname -s)"
echo "  Projeto: $DIR_PROJETO"
echo "========================================"

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Instale e adicione ao PATH."
    exit 1
fi

echo ""
echo "Python encontrado: $(which python3)"

# Cria o venv se não existir
if [ ! -d "$VENV_CAMINHO" ]; then
    echo ""
    echo "[VENV] Criando ambiente virtual em $VENV_NOME..."
    python3 -m venv "$VENV_CAMINHO"
    echo "Ambiente virtual criado."
else
    echo ""
    echo "[VENV] Ambiente virtual já existe em $VENV_NOME."
fi

# Ativa e instala
source "$VENV_CAMINHO/bin/activate"

echo ""
if [ -f "$DIR_PROJETO/requirements.txt" ]; then
    echo "[PIP] Instalando dependências de requirements.txt..."
    pip install -r "$DIR_PROJETO/requirements.txt"
else
    echo "[PIP] Instalando pytest (padrão)..."
    pip install pytest
fi

echo ""
echo "========================================"
echo "  Ambiente configurado com sucesso!"
echo "  Python: $(which python)"
echo "  venv:   $VENV_CAMINiders -v>/dev/null; then
    uname -a
elif command -v apt &> /dev/null; then
    lsb_release -d | cut -f2
fi

echo ""
echo "Para ativar manualmente, execute:"
echo "    source $VENV_NOME/bin/activate"
echo ""
