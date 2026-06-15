"""
Configuração global dos testes: garante que pytest consiga importar
o módulo numero_por_extenso, que está na raiz do projeto.
"""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
