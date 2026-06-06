class NumeroForaDoLimiteError(ValueError):
    """Exceção retornada em caso de números fora do limite suportado (menores que 1000)."""

    pass


class Conversor:
    # Listas compartilhadas pela classe
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

    @staticmethod
    def numero_por_extenso(num):
        """Converte um número de -999 até 999 para extenso."""

        if num == 0:
            return "zero"

        if abs(num) >= 1000:
            raise NumeroForaDoLimiteError(
                f"O número {num} está fora do limite suportado (deve ser entre -999 e 999)."
            )

        if num < 0:
            return "menos " + Conversor.numero_por_extenso(abs(num))

        if num == 100:
            return "cem"

        c = num // 100
        d = (num % 100) // 10
        u = n % 10 if (n := num) else 0

        partes = []

        # 1. Centena
        if c > 0:
            partes.append(Conversor.CENTENAS[c])

        # 2. Dezena e Unidade
        if d == 1:
            partes.append(Conversor.DEZ_A_DEZENOVE[u])
        else:
            if d > 1:
                partes.append(Conversor.DEZENAS[d])
            if u > 0:
                partes.append(Conversor.UNIDADES[u])

        return " e ".join(partes)


# --- SCRIPT DE BACKGROUND ---
if __name__ == "__main__":
    print("--- Conversor de Números Nativo (Até 999) ---")

    while True:
        entrada = input(
            "Digite um número inteiro (ou 'sair' para encerrar): "
        ).strip()

        if entrada.lower() == "sair":
            print("Programa encerrado. Até mais!")
            break

        try:
            # 1. Tenta converter a entrada para inteiro (pode gerar ValueError)
            numero = int(entrada)

            # 2. Tenta gerar o extenso (pode gerar NumeroForaDoLimiteError)
            extenso = Conversor.numero_por_extenso(numero)
            print(f"\n{numero} = {extenso}\n")

        except NumeroForaDoLimiteError as e:
            # Captura especificamente a exceção customizada
            print(f"\n⚠️ Erro de Limite: {e}\n")

        except ValueError as e:
            # Captura se o usuário digitar letras ou símbolos inválidos
            print(
                "\nEntrada inválida. Por favor, digite apenas números inteiros.\n"
            )

        except Exception as e:
            # Captura qualquer outro erro inesperado
            print(f"Ocorreu um erro inesperado: {e}\n")