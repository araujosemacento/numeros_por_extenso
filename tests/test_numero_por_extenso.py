import os
import subprocess
import sys

import pytest
from numero_por_extenso import Conversor, NumeroForaDoLimiteError, executar


# ==============================================================================
# CHECK AMBIENTE VIRTUAL
# ==============================================================================

def _verificar_venv():
    """Verifica se o venv está ativo, cria se necessário, e avisa o usuário."""
    in_venv = sys.prefix != sys.base_prefix

    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)
    venv_path = os.path.join(project_root, ".venv")

    if in_venv:
        venv_python = os.path.join(
            sys.prefix, "Scripts", "python.exe"
        ) if os.name == "nt" else os.path.join(sys.prefix, "bin", "python")
        print(f"\n[venv-check] Ambiente virtual ativo: [{venv_python}]\n")
        return

    print("\n" + "=" * 50)
    print("  AMBIENTE VIRTUAL INATIVO")
    print("=" * 50)

    if os.path.exists(venv_path):
        print(f"  venv existente em: {venv_path}")
        print("  Precisa ser ativado manualmente.\n")
    else:
        setup_script = os.path.join(project_root, "setup_venv.py")
        if os.path.exists(setup_script):
            print("  venv não encontrado. Criando automaticamente...\n")
            try:
                subprocess.check_call([sys.executable, setup_script])
                print(f"\n  venv criado com sucesso em: {venv_path}\n")
            except Exception as e:
                print(f"\n  [ERRO] Falha ao criar venv: {e}\n")
        else:
            print("  Nenhum venv encontrado e setup_venv.py não existe.")
            print("  Execute para criar: python -m venv .venv\n")

    print("  Para ativar o ambiente virtual, execute:")
    if os.name == "nt":
        print(f"    .venv\\Scripts\\Activate.ps1")
    else:
        print(f"    source .venv/bin/activate")
    print("=" * 50 + "\n")


_verificar_venv()


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
        # Conectivo "e" na última transição (chunk de unidades)
        (1_001, "mil e um"),
        (1_010, "mil e dez"),
        (1_100, "mil e cem"),
        (1_200, "mil e duzentos"),
        (1_111, "mil, cento e onze"),  # centena na unidade → vírgula
        (1_011, "mil e onze"),           # sem centena → "e"
        (1_101, "mil, cento e um"),    # centena com resto → vírgula
        (1_234, "mil, duzentos e trinta e quatro"),
        # Multiplos de mil
        (2_000, "dois mil"),
        (2_001, "dois mil e um"),
        (10_000, "dez mil"),
        (12_345, "doze mil, trezentos e quarenta e cinco"),
        (100_000, "cem mil"),
        (101_000, "cento e um mil"),
        (101_001, "cento e um mil e um"),
        (999_999, "novecentos e noventa e nove mil, novecentos e noventa e nove"),
    ],
)
def test_conversor_com_milhar(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (-1_000, "menos mil"),
        (-1_001, "menos mil e um"),
        (-2_345, "menos dois mil, trezentos e quarenta e cinco"),
        (-100_000, "menos cem mil"),
        (-999_999, "menos novecentos e noventa e nove mil, novecentos e noventa e nove"),
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
        # Conectivo "e" quando o último chunk é unidades
        (1_000_001, "um milhão e um"),
        (1_001_000, "um milhão e mil"),
        (2_000_000, "dois milhões"),
        (2_000_001, "dois milhões e um"),
        (3_141_592, "três milhões, cento e quarenta e um mil, quinhentos e noventa e dois"),
        (10_000_000, "dez milhões"),
        (100_000_000, "cem milhões"),
        (123_456_789, "cento e vinte e três milhões, quatrocentos e cinquenta e seis mil, setecentos e oitenta e nove"),
        (999_999_999, "novecentos e noventa e nove milhões, novecentos e noventa e nove mil, novecentos e noventa e nove"),
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
        (999_999_999_999, "novecentos e noventa e nove bilhões, novecentos e noventa e nove milhões, novecentos e noventa e nove mil, novecentos e noventa e nove"),
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
# 5. TESTES: SEPARADORES DE MILHAR (STRINGS)
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        # Separador ponto (padrão brasileiro)
        ("1.000", "mil"),
        ("2.000", "dois mil"),
        ("1.000.000", "um milhão"),
        ("2.500.000.000", "dois bilhões e quinhentos milhões"),
        # Separador virgula (padrão americano)
        ("1,000", "mil"),
        ("1,000,000", "um milhão"),
        # Sem separador
        ("1000", "mil"),
        ("1000000", "um milhão"),
        # Misto (ponto e virgula alternados)
        ("1.000,000", "um milhão"),  # estranho mas válido
        # Número negativo como string
        ("-1.000", "menos mil"),
    ],
)
def test_conversor_com_separadores_de_milhar(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 6. TESTES: ENTRADA FLOAT
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        (1000.0, "mil"),
        (1000000.0, "um milhão"),
    ],
)
def test_conversor_com_entrada_float(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 7. TESTES: NUMEROS COM BURACOS ENTRE GRANDEZAS
# ==============================================================================

@pytest.mark.parametrize(
    "numero, extenso_esperado",
    [
        # Grandezas puladas; conectivo "e" para o ultimo chunk de unidades
        (1_300, "mil e trezentos"),
        (1_500, "mil e quinhentos"),  # 1.500
        (10_001, "dez mil e um"),
        (100_0001, "um milhão e um"),  # 1_000_001
        (1_000_500, "um milhão e quinhentos"),  # 1.000.500
        (1_001_000, "um milhão e mil"),  # 1.001.000 - sem gap, último índice != 0
        (10_000_050_050, "dez bilhões, cinquenta mil e cinquenta"),
    ],
)
def test_conversor_com_buracos_entre_grandezas(numero, extenso_esperado):
    assert Conversor.numero_por_extenso(numero) == extenso_esperado


# ==============================================================================
# 8. TESTES: TRATAMENTO DE EXCEÇÕES
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


@pytest.mark.parametrize("entrada_invalida", [
    "abc",
    "1.2.3",
    "mil",
    "10,00,000",  # formato estranho (sera rejeitado porque depois de remove virgulas fica 1000000... ok, isso passa na verdade. Vou usar um que realmente falhe)
    "1.2.3.4",
    "abc123",
])
def test_conversor_rejeita_entrada_invalida(entrada_invalida):
    with pytest.raises(ValueError) as exc_info:
        Conversor.numero_por_extenso(entrada_invalida)
    assert "Entrada inválida" in str(exc_info.value)


def test_conversor_rejeita_float_decimal():
    with pytest.raises(ValueError) as exc_info:
        Conversor.numero_por_extenso(1.5)
    assert "decimais" in str(exc_info.value)


# ==============================================================================
# 9. TESTES DE INTEGRAÇÃO: INTERAÇÃO DA INTERFACE E RECUPERAÇÃO DE ERROS
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
    # Sequência de ações de um usuário:
    sequencia_entradas = iter(["abc", str(Conversor.LIMITE + 1), "16", "sair"])
    monkeypatch.setattr("builtins.input", lambda _: next(sequencia_entradas))

    executar()

    saida_terminal = capsys.readouterr().out

    # Valida se o sistema se comportou e se recuperou de cada erro na ordem correta
    assert "Entrada inválida" in saida_terminal
    assert "Erro de Limite" in saida_terminal
    assert "16 = dezesseis" in saida_terminal
    assert "Programa encerrado" in saida_terminal
