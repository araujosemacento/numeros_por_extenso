import os
import platform
import subprocess
import sys


class NumeroForaDoLimiteError(ValueError):
    """Exceção retornada em caso de números fora do limite suportado."""
    pass


class Conversor:
    LIMITE = 999_999_999_999

    UNIDADES = [
        "",
        "um",
        "dois",
        "três",
        "quatro",
        "cinco",
        "seis",
        "sete",
        "oito",
        "nove",
    ]
    DEZ_A_DEZENOVE = [
        "dez",
        "onze",
        "doze",
        "treze",
        "catorze",
        "quinze",
        "dezesseis",
        "dezessete",
        "dezoito",
        "dezenove",
    ]
    DEZENAS = [
        "",
        "",
        "vinte",
        "trinta",
        "quarenta",
        "cinquenta",
        "sessenta",
        "setenta",
        "oitenta",
        "noventa",
    ]
    CENTENAS = [
        "",
        "cento",
        "duzentos",
        "trezentos",
        "quatrocentos",
        "quinhentos",
        "seiscentos",
        "setecentos",
        "oitocentos",
        "novecentos",
    ]

    ESCALAS = ["", "mil", "milhão", "bilhão"]
    ESCALAS_PLURAL = ["", "mil", "milhões", "bilhões"]

    @staticmethod
    def _ate_999(num):
        """Converte um número de 0 até 999 para extenso."""
        if num == 0:
            return ""

        if num == 100:
            return "cem"

        c = num // 100
        d = (num % 100) // 10
        u = num % 10

        partes = []

        if c > 0:
            partes.append(Conversor.CENTENAS[c])

        if d == 1:
            partes.append(Conversor.DEZ_A_DEZENOVE[u])
        else:
            if d > 1:
                partes.append(Conversor.DEZENAS[d])
            if u > 0:
                partes.append(Conversor.UNIDADES[u])

        return " e ".join(partes)

    @staticmethod
    def _extenso_com_escala(num, indice_escala):
        """Converte chunk * escala. Para mil, omite 'um'."""
        if num == 0:
            return ""

        if num == 1 and indice_escala == 1:
            return "mil"

        extenso = Conversor._ate_999(num)

        if indice_escala == 0:
            return extenso

        escala = Conversor.ESCALAS[indice_escala]
        escala_pl = Conversor.ESCALAS_PLURAL[indice_escala]

        return f"{extenso} {escala if num == 1 else escala_pl}"

    @staticmethod
    def numero_por_extenso(num):
        """Converte um número para extenso (até 999.999.999.999)."""

        if num == 0:
            return "zero"

        if abs(num) > Conversor.LIMITE:
            raise NumeroForaDoLimiteError(
                f"O número {num} está fora do limite suportado (deve ser entre "
                f"-{Conversor.LIMITE} e {Conversor.LIMITE})."
            )

        if num < 0:
            return "menos " + Conversor.numero_por_extenso(abs(num))

        chunks = []
        n = num
        while n > 0:
            chunks.append(n % 1000)
            n //= 1000

        resultados = []
        for i, chunk in enumerate(chunks):
            if chunk > 0:
                extenso = Conversor._extenso_com_escala(chunk, i)
                if extenso:
                    resultados.append(extenso)

        return " e ".join(reversed(resultados))


def executar():
    limite_formatado = f"{Conversor.LIMITE:,}".replace(",", ".")
    print(f"--- Conversor de Números (Até {limite_formatado}) ---")

    while True:
        entrada = input(
            "Digite um número inteiro (ou 'sair' para encerrar): "
        ).strip()

        if entrada.lower() == "sair":
            print("Programa encerrado. Até mais!")
            break

        try:
            numero = int(entrada)
            extenso = Conversor.numero_por_extenso(numero)
            print(f"\n{numero} = {extenso}\n")

        except NumeroForaDoLimiteError as e:
            print(f"\nErro de Limite: {e}\n")

        except ValueError:
            print(
                "\nEntrada inválida. Por favor, digite apenas números inteiros.\n"
            )

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}\n")


def configurar_ambiente():
    so_nome = platform.system()
    so_id = os.name
    diretorio = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(diretorio, ".venv")

    print("=" * 50)
    print("  Configuracao do Ambiente Virtual")
    print("=" * 50)
    print(f"  SO detectado: {so_nome} (os.name={so_id})")
    print(f"  Projeto:      {diretorio}")
    print(f"  venv:         .venv")
    print("=" * 50)
    print()

    python_cmd = sys.executable

    if not os.path.exists(venv_path):
        print("[VENV] Criando ambiente virtual...")
        subprocess.check_call([python_cmd, "-m", "venv", venv_path])
        print("[VENV] Ambiente virtual criado.\n")
    else:
        print("[VENV] Ambiente virtual ja existe.\n")

    requirements = os.path.join(diretorio, "requirements.txt")
    pip_cmd = os.path.join(venv_path, "Scripts" if so_id == "nt" else "bin", "pip")

    if os.path.exists(requirements):
        print("[PIP] Instalando dependencias de requirements.txt...")
        subprocess.check_call([pip_cmd, "install", "-r", requirements])
    else:
        print("[PIP] Nenhum requirements.txt encontrado.")

    print()
    print("=" * 50)
    print("  Ambiente configurado com sucesso!")
    print("=" * 50)
    print()
    print("Para ativar manualmente, execute:")
    if so_id == "nt":
        print("    .venv\\Scripts\\Activate.ps1")
    else:
        print("    source .venv/bin/activate")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        configurar_ambiente()
    else:
        executar()
