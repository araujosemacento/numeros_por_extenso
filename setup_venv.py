#!/usr/bin/env python3
"""
setup_venv.py - Script cross-platform para configurar o ambiente virtual.
Detecta o SO e executa o setup apropriado.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path


class ConfiguradorVenv:
    VENV_NOME = ".venv"

    def __init__(self):
        self.so = platform.system()
        self.diretorio = Path(__file__).parent.resolve()
        self.venv_path = self.diretorio / self.VENV_NOME

    def _python_cmd(self):
        return sys.executable

    def _criar_venv(self):
        if self.venv_path.exists():
            print(f"[VENV] Ambiente virtual ja existe em {self.VENV_NOME}.\n")
            return

        print(f"[VENV] Criando ambiente virtual em {self.VENV_NOME}...")
        subprocess.check_call([self._python_cmd(), "-m", "venv", str(self.venv_path)])
        print("[VENV] Ambiente virtual criado com sucesso.\n")

    def _instalar_deps(self):
        requirements = self.diretorio / "requirements.txt"
        pip = self._caminho_pip()

        if requirements.exists():
            print("[PIP] Instalando dependencias de requirements.txt...")
            subprocess.check_call([str(pip), "install", "-r", str(requirements)])
        else:
            print("[PIP] Instalando pytest (dependencia padrao)...")
            subprocess.check_call([str(pip), "install", "pytest"])
        print("[PIP] Dependencias instaladas.\n")

    def _caminho_python(self):
        if self.so == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        return self.venv_path / "bin" / "python"

    def _caminho_pip(self):
        if self.so == "Windows":
            return self.venv_path / "Scripts" / "pip.exe"
        return self.venv_path / "bin" / "pip"

    def _comando_ativacao(self):
        if self.so == "Windows":
            return f"{self.VENV_NOME}\\Scripts\\Activate.ps1"
        return f"source {self.VENV_NOME}/bin/activate"

    def _script_setup(self):
        if self.so == "Windows":
            return self.diretorio / "setup_venv.ps1"
        return self.diretorio / "setup_venv.sh"

    def executar(self):
        print("=" * 50)
        print("  Configuracao do Ambiente Virtual")
        print(f"  SO detectado: {self.so}")
        print(f"  Projeto: {self.diretorio}")
        print("=" * 50)
        print()

        self._criar_venv()
        self._instalar_deps()

        print("=" * 50)
        print("  Ambiente configurado com sucesso!")
        print(f"  Python venv: {self._caminho_python()}")
        print("=" * 50)
        print()
        print("Para ativar manualmente, execute:")
        print(f"    {self._comando_ativacao()}")
        print()


def main():
    configurador = ConfiguradorVenv()
    configurador.executar()


if __name__ == "__main__":
    main()