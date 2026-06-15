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
    def _validar_separadores(s, separador):
        """Verifica se o separador é usado a cada 3 dígitos a partir da direita."""
        partes = s.replace("-", "").split(separador)
        if len(partes) <= 1:
            return True
        for i, parte in enumerate(partes):
            if i == 0:
                if len(parte) == 0 or len(parte) > 3:
                    return False
            else:
                if len(parte) != 3:
                    return False
        return True

    @staticmethod
    def _parse_entrada(num):
        """Converte entrada em int, aceitando strings com separadores."""
        if isinstance(num, float):
            if not num.is_integer():
                raise ValueError("Números decimais não são suportados. Digite um inteiro.")
            return int(num)

        if isinstance(num, str):
            # Remove separadores de milhar comuns no Brasil e Portugal
            num_limpo = num.replace(".", "").replace(",", "")
            if not num_limpo.lstrip("-").isdigit():
                raise ValueError(f"Entrada inválida: '{num}'. Digite apenas números inteiros.")

            # Valida formato de separadores (exceto quando ambos aparecem, como 1.000,000)
            has_dot = "." in num
            has_comma = "," in num
            if not (has_dot and has_comma):
                sep = "." if has_dot else ","
                if not Conversor._validar_separadores(num, sep):
                    raise ValueError(f"Entrada inválida: '{num}'. Formato de separadores incorreto.")

            return int(num_limpo)

        return int(num)

    @staticmethod
    def numero_por_extenso(num):
        """Converte um número para extenso (até 999.999.999.999).

        Aceita int, str (com ou sem separadores de milhar) e float.
        """
        num = Conversor._parse_entrada(num)

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
                    resultados.append((i, chunk, extenso))

        # Ordena do maior índice (maior escala) para o menor
        resultados = list(reversed(resultados))

        if not resultados:
            return "zero"

        if len(resultados) == 1:
            return resultados[0][2]

        # Junta os resultados com conectivo dinâmico:
        # - Vírgula por padrão entre grandezas
        # - " e " na última transição se o último chunk é de unidades (índice 0)
        texto_final = resultados[0][2]
        for i in range(1, len(resultados) - 1):
            texto_final += ", " + resultados[i][2]

        if len(resultados) > 1:
            ultimo_idx, ultimo_val, ultimo_ext = resultados[-1]
            penultimo_idx, penultimo_val, penultimo_ext = resultados[-2]

            if len(resultados) == 2 and (penultimo_idx, ultimo_idx) == (1, 0):
                # Milhar + Unidades: vírgula se ambos os lados já contêm
                # o conectivo " e " internamente, senão use " e "
                # Extrai o texto base do chunk de milhar (sem a escala)
                sufixo = f" {Conversor.ESCALAS[penultimo_idx]}"
                if penultimo_ext.endswith(sufixo):
                    texto_penultimo = penultimo_ext[:-len(sufixo)]
                else:
                    sufixo_pl = f" {Conversor.ESCALAS_PLURAL[penultimo_idx]}"
                    if penultimo_ext.endswith(sufixo_pl):
                        texto_penultimo = penultimo_ext[:-len(sufixo_pl)]
                    else:
                        texto_penultimo = penultimo_ext

                if " e " in texto_penultimo and " e " in ultimo_ext:
                    separador_ultimo = ", "
                elif ultimo_val >= 100 and ultimo_val % 100 != 0:
                    # Chunk de unidades com centena e resto (ex: 101, 234)
                    # Já contém " e " interno; separa com vírgula
                    separador_ultimo = ", "
                else:
                    separador_ultimo = " e "
            elif len(resultados) == 2:
                # Apenas 2 ordens de grandeza (consecutivas): sempre "e"
                separador_ultimo = " e "
            else:
                # 3+ chunks: vírgula por padrão, " e " se último é unidades
                separador_ultimo = " e " if ultimo_idx == 0 else ", "

            texto_final += separador_ultimo + ultimo_ext

        return texto_final


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
            extenso = Conversor.numero_por_extenso(entrada)
            print(f"\n{entrada} = {extenso}\n")

        except NumeroForaDoLimiteError as e:
            print(f"\nErro de Limite: {e}\n")

        except ValueError as e:
            print(f"\nEntrada inválida: {e}\n")

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}\n")


if __name__ == "__main__":
    executar()
