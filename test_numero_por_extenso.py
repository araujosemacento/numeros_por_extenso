import pytest
from numero_por_extenso import Conversor, NumeroForaDoLimiteError, executar


# ==============================================================================
# 1. TESTES UNITÁRIOS: CASOS VÁLIDOS (0 A 999)
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (0, "zero"),
        # Unidades simples
        (1, "um"),
        (5, "cinco"),
        (9, "nove"),
        # Casos especiais de 10 a 19
        (10, "dez"),
        (11, "onze"),
        (15, "quinze"),
        (19, "dezenove"),
        # Dezenas exatas e compostas
        (20, "vinte"),
        (21, "vinte e um"),
        (45, "quarenta e cinco"),
        (99, "noventa e nove"),
        # Transição e comportamento de centenas
        (100, "cem"),
        (101, "cento e um"),
        (110, "cento e dez"),
        (115, "cento e quinze"),
        (120, "cento e vinte"),
        (125, "cento e vinte e cinco"),
        (200, "duzentos"),
        (542, "quinhentos e quarenta e dois"),
        (999, "novecentos e noventa e nove"),
    ],
)
def test_conversor_com_numeros_positivos_validos_ate_999(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (-1, "menos um"),
        (-16, "menos dezesseis"),
        (-100, "menos cem"),
        (-105, "menos cento e cinco"),
        (-999, "menos novecentos e noventa e nove"),
    ],
)
def test_conversor_com_numeros_negativos_validos_ate_999(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 2. TESTES UNITÁRIOS: MILHAR (1.000 A 999.999)
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        # Casos base de milhar
        (1_000, "mil"),
        (1_001, "mil e um"),
        (1_010, "mil e dez"),
        (1_100, "mil e cem"),
        (1_200, "mil e duzentos"),
        (1_234, "mil e duzentos e trinta e quatro"),
        # Multiplos de mil
        (2_000, "dois mil"),
        (2_001, "dois mil e um"),
        (10_000, "dez mil"),
        (12_345, "doze mil e trezentos e quarenta e cinco"),
        (100_000, "cem mil"),
        (101_000, "cento e um mil"),
        (101_001, "cento e um mil e um"),
        (999_999, "novecentos e noventa e nove mil e novecentos e noventa e nove"),
    ],
)
def test_conversor_com_milhar(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (-1_000, "menos mil"),
        (-1_001, "menos mil e um"),
        (-2_345, "menos dois mil e trezentos e quarenta e cinco"),
        (-100_000, "menos cem mil"),
        (-999_999, "menos novecentos e noventa e nove mil e novecentos e noventa e nove"),
    ],
)
def test_conversor_com_milhar_negativo(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 3. TESTES UNITÁRIOS: MILHÃO (1.000.000 A 999.999.999)
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (1_000_000, "um milhão"),
        (1_000_001, "um milhão e um"),
        (1_001_000, "um milhão e mil"),
        (2_000_000, "dois milhões"),
        (2_000_001, "dois milhões e um"),
        (3_141_592, "três milhões e cento e quarenta e um mil e quinhentos e noventa e dois"),
        (10_000_000, "dez milhões"),
        (100_000_000, "cem milhões"),
        (123_456_789, "cento e vinte e três milhões e quatrocentos e cinquenta e seis mil e setecentos e oitenta e nove"),
        (999_999_999, "novecentos e noventa e nove milhões e novecentos e noventa e nove mil e novecentos e noventa e nove"),
    ],
)
def test_conversor_com_milhao(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (-1_000_000, "menos um milhão"),
        (-1_000_001, "menos um milhão e um"),
        (-2_000_000, "menos dois milhões"),
    ],
)
def test_conversor_com_milhao_negativo(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 4. TESTES UNITÁRIOS: BILHÃO (1.000.000.000 A 999.999.999.999)
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (1_000_000_000, "um bilhão"),
        (1_000_000_001, "um bilhão e um"),
        (1_000_001_000, "um bilhão e mil"),
        (2_000_000_000, "dois bilhões"),
        (2_000_000_001, "dois bilhões e um"),
        (2_500_000_000, "dois bilhões e quinhentos milhões"),
        (10_000_000_000, "dez bilhões"),
        (100_000_000_000, "cem bilhões"),
        (999_999_999_999, "novecentos e noventa e nove bilhões e novecentos e noventa e nove milhões e novecentos e noventa e nove mil e novecentos e noventa e nove"),
    ],
)
def test_conversor_com_bilhao(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (-1_000_000_000, "menos um bilhão"),
        (-2_000_000_000, "menos dois bilhões"),
    ],
)
def test_conversor_com_bilhao_negativo(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 5. TESTES UNITÁRIOS: TRATAMENTO DE EXCEÇÕES
# ==============================================================================

@pytest.mark.parametrize("numero_fora", [
    1_000_000_000_000,          # 1 trilhao
    -1_000_000_000_000,         # -1 trilhao
    Conversor.LIMITE + 1,       # limite + 1
    Conversor.LIMITE + 100,     # limite + 100
    10_000_000_000_000,         # 10 trilhoes
])
def test_conversor_deve_lancar_excecao_customizada_fora_do_limite(numero_fora):
    """Garante que a classe dispara o erro customizado quando viola os limites de escopo."""
    with pytest.raises(NumeroForaDoLimiteError) as informacao_erro:
        Conversor.numero_por_extenso(numero_fora)

    assert "fora do limite suportado" in str(informacao_erro.value)


# ==============================================================================
# 6. TESTES DE INTEGRAÇÃO: INTERAÇÃO DA INTERFACE E RECUPERAÇÃO DE ERROS
# ==============================================================================

def test_fluxo_da_interface_encerramento_imediato(monkeypatch, capsys):
    """Simula o usuário digitando 'sair' logo de início para avaliar o encerramento limpo."""
    respostas_simuladas = iter(["sair"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas_simuladas))

    executar()

    saida_terminal = capsys.readouterr().out
    assert "Programa encerrado. Até mais!" in saida_terminal


def test_fluxo_da_interface_com_entradas_invalidas_e_recuperacao(monkeypatch, capsys):
    """Testa a integração total da aplicação simulando uma sessão de usuário real.

    Garante que o script trata erros de digitação e limites sem interromper o loop.
    """
    # Sequência de ações aleatórias de um usuário:
    # 1. Digita um texto inválido ("abc")      → Espera-se: Mensagem de Entrada Inválida.
    # 2. Digita um número estourado (acima do limite) → Espera-se: Mensagem do Erro de Limite.
    # 3. Digita um número válido (16)          → Espera-se: "16 = dezesseis".
    # 4. Encerra a aplicação ("sair")          → Espera-se: Fechamento regular.
    sequencia_entradas = iter(["abc", str(Conversor.LIMITE + 1), "16", "sair"])
    monkeypatch.setattr("builtins.input", lambda _: next(sequencia_entradas))

    executar()

    saida_terminal = capsys.readouterr().out

    # Valida se o sistema se comportou e se recuperou de cada erro na ordem correta
    assert "Por favor, digite apenas números inteiros." in saida_terminal
    assert "Erro de Limite" in saida_terminal
    assert "16 = dezesseis" in saida_terminal
    assert "Programa encerrado" in saida_terminal