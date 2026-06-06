import pytest
from numero_por_extenso import Conversor, NumeroForaDoLimiteError, executar


# ==============================================================================
# 1. TESTES UNITÁRIOS: CASOS VÁLIDOS
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
def test_conversor_com_numeros_positivos_validos(numero, extenso_esperado):
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
def test_conversor_com_numeros_negativos_validos(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 2. TESTES UNITÁRIOS: TRATAMENTO DE EXCEÇÕES DA CLASSE
# ==============================================================================

@pytest.mark.parametrize("numero_fora", [1000, 1500, -1000, -2500])
def test_conversor_deve_lancar_excecao_customizada_fora_do_limite(numero_fora):
    """Garante que a classe dispara o erro customizado quando viola os limites de escopo."""
    with pytest.raises(NumeroForaDoLimiteError) as informacao_erro:
        Conversor.numero_por_extenso(numero_fora)

    assert "fora do limite suportado" in str(informacao_erro.value)


# ==============================================================================
# 3. TESTES DE INTEGRAÇÃO: INTERAÇÃO DA INTERFACE E RECUPERAÇÃO DE ERROS
# ==============================================================================

def test_fluxo_da_interface_encerramento_imediato(monkeypatch, capsys):
    """Simula o usuário digitando 'sair' logo de início para avaliar o encerramento limpo."""
    # Ferramenta para injetar a resposta que o comando input() deve ler
    respostas_simuladas = iter(["sair"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas_simuladas))

    executar()

    # Ferramenta para capturar o que foi exibido no prompt do terminal
    saida_terminal = capsys.readouterr().out
    assert "Programa encerrado. Até mais!" in saida_terminal


def test_fluxo_da_interface_com_entradas_invalidas_e_recuperacao(monkeypatch, capsys):
    """Testa a integração total da aplicação simulando uma sessão de usuário real.

    Garante que o script trata erros de digitação e limites sem interromper o loop.
    """
    # Sequência de ações aleatórias de um usuário:
    # 1. Digita um texto inválido ("abc")  -> Espera-se: Mensagem de Entrada Inválida.
    # 2. Digita um número estourado (1200) -> Espera-se: Mensagem do Erro de Limite.
    # 3. Digita um número válido (16)      -> Espera-se: "16 = dezesseis".
    # 4. Encerra a aplicação ("sair")      -> Espera-se: Fechamento regular.
    sequencia_entradas = iter(["abc", "1200", "16", "sair"])
    monkeypatch.setattr("builtins.input", lambda _: next(sequencia_entradas))

    executar()

    saida_terminal = capsys.readouterr().out

    # Valida se o sistema se comportou e se recuperou de cada erro na ordem correta
    assert "Por favor, digite apenas números inteiros." in saida_terminal
    assert "Erro de Limite" in saida_terminal
    assert "16 = dezesseis" in saida_terminal
    assert "Programa encerrado" in saida_terminal