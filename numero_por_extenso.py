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

