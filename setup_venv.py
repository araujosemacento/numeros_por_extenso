#!/usr/bin/env python3
"""
setup_venv.py - Script cross-platform para configurar o ambiente virtual.
Cria o .venv, instala dependências e reporta problemas com clareza.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path


class ConfiguradorVenv:
    VENV_NOME = ".venv"

    def __init__(self):
        self.diretorio = Path(__file__).parent.resolve()
        self.venv_path = self.diretorio / self.VENV_NOME

    def _python_cmd(self):
        return sys.executable

    def _criar_venv(self):
        if self.venv_path.exists():
            print(f"[VENV] Ambiente virtual ja existe em {self.VENV_NOME}.\n")
            return

        print(f"[VENV] Criando ambiente virtual em {self.VENV_NOME}...")
        try:
            subprocess.check_call(
                [self._python_cmd(), "-m", "venv", str(self.venv_path)]
            )
            print("[VENV] Ambiente virtual criado com sucesso.\n")
        except FileNotFoundError:
            print("\n[ERRO] Python nao foi encontrado no PATH.")
            print("       Verifique se o Python esta instalado e disponível.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"\n[ERRO] Falha ao criar o ambiente virtual (codigo {e.returncode}).")
            print("       Possiveis causas:")
            print("       - Permissões insuficientes para criar diretorios.")
            print("       - O modulo 'venv' nao esta instalado ou esta corrompido.")
            print(f"       Comando executado: {e.cmd}")
            sys.exit(1)

    def _instalar_deps(self):
        requirements = self.diretorio / "requirements.txt"
        pip_bin = "Scripts" if os.name == "nt" else "bin"
        pip_path = self.venv_path / pip_bin / ("pip.exe" if os.name == "nt" else "pip")

        if not pip_path.exists():
            print("\n[AVISO] Pip nao encontrado dentro do venv.")
            print("        Tentando instalar com ensurepip...")
            try:
                subprocess.check_call(
                    [self._python_cmd(), "-m", "ensurepip", "--upgrade"]
                )
            except subprocess.CalledProcessError:
                print("[ERRO] Nao foi possível instalar o pip no ambiente virtual.")
                sys.exit(1)

        try:
            if requirements.exists():
                print("[PIP] Instalando dependencias de requirements.txt...")
                subprocess.check_call(
                    [str(pip_path), "install", "-r", str(requirements)]
                )
            else:
                print("[PIP] Instalando pytest (dependencia padrao)...")
                subprocess.check_call([str(pip_path), "install", "pytest"])
            print("[PIP] Dependencias instaladas.\n")
        except subprocess.CalledProcessError as e:
            print(f"\n[ERRO] Falha ao instalar dependencias (codigo {e.returncode}).")
            print("       Possiveis causas:")
            print("       - Problemas de conexão com a internet.")
            print("       - Firewall ou proxy bloqueando o PyPI.")
            print("       - Versão do pip incompatível.")
            sys.exit(1)

    def executar(self):
        print("=" * 50)
        print("  Configuracao do Ambiente Virtual")
        print(f"  SO:      {platform.system()}")
        print(f"  Projeto: {self.diretorio}")
        print("=" * 50)
        print()

        self._criar_venv()
        self._instalar_deps()

        print("=" * 50)
        print("  Ambiente configurado com sucesso!")
        print("=" * 50)
        print()
        print("Para ativar manualmente, execute:")
        if os.name == "nt":
            print(f"    .{os.sep}{self.VENV_NOME}\\Scripts\\Activate.ps1")
        else:
            print(f"    source {self.VENV_NOME}/bin/activate")
        print()


def main():
    configurador = ConfiguradorVenv()
    configurador.executar()


if __name__ == "__main__":
    main()
