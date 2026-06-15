# Conversor de Números por Extenso

Este programa transforma números inteiros em texto por extenso, em português.

## O que ele faz

Converte valores como `1234` em **"mil, duzentos e trinta e quatro"**. Aceita números de **zero até 999.999.999.999** (999 bilhões), incluindo negativos.

## Como usar

### 1. Configurar o ambiente

Execute o script de configuração. Ele cria automaticamente o ambiente virtual e instala o que for necessário:

```bash
python setup_venv.py
```

> **Nota:** Em sistemas Windows, você pode precisar executar o terminal como administrador se o script reportar falta de permissão.

### 2. Ativar o ambiente virtual

- **Windows (PowerShell):**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

  Se aparecer um erro de política de execução, rode antes:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **Windows (CMD):**

  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Linux / macOS:**

  ```bash
  source .venv/bin/activate
  ```

### 3. Executar o programa

```bash
python numero_por_extenso.py
```

Depois, digite qualquer número inteiro válido. Exemplos de entrada:

- `42` → **quarenta e dois**
- `1011` → **mil e onze**
- `1111` → **mil, cento e onze**
- `-500` → **menos quinhentos**
- `1.000.000` → **um milhão**

Digite `sair` para encerrar.

### Como usar no seu próprio código

```python
from numero_por_extenso import Conversor

# Número simples
print(Conversor.numero_por_extenso(1234))
# → mil, duzentos e trinta e quatro

# Com separadores de milhar (string)
print(Conversor.numero_por_extenso("1.000.000"))
# → um milhão

# Negativo
print(Conversor.numero_por_extenso(-42))
# → menos quarenta e dois
```

## Executar os testes

Com o ambiente virtual ativado, execute:

```bash
python -m pytest tests/ -v
```

O parâmetro `-v` mostra o resultado de cada teste individual.

Se quiser ver apenas os que falharam:

```bash
python -m pytest tests/ -v --tb=short
```

### Sobre os testes

O arquivo `tests/test_numero_por_extenso.py` contém os seguinte grupos de verificações:

| Grupo | O que verifica | Exemplo |
| ------- | ---------------- | --------- |
| **Unidades (0 a 999)** | Números simples, dezenas, centenas | `100` → "cem", `99` → "noventa e nove" |
| **Milhar** | Milhares de todas as formas | `1.234` → "mil, duzentos e trinta e quatro" |
| **Milhão** | Milhões e combinações | `3.141.592` → "três milhões, cento e quarenta e um mil, quinhentos e noventa e dois" |
| **Bilhão** | Grandes valores | `999.999.999.999` → "novecentos e noventa e nove bilhões, novecentos e noventa e nove milhões, novecentos e noventa e nove mil, novecentos e noventa e nove" |
| **Separadores** | Aceita strings com `.` e `,` | `"1.000.000"` funciona |
| **Floats** | Números com casa decimal zero | `1000.0` → "mil" |
| **Buracos entre grandezas** | Quando alguma grandeza é zero | `1.300` → "mil e trezentos" |
| **Exceções** | Comportamento com limites excedidos | `1.000.000.000.000` lança erro |
| **Interface** | Entrada do usuário e recuperação de erros | `"abc"` e saída do programa |

#### Testes de integração da interface

Dois testes específicos verificam o fluxo completo do programa, simulando um usuário digitando comandos:

- **Encerramento imediato:** o usuário digita `sair` logo de início e o programa encerra corretamente.
- **Recuperação de erros:** o usuário digita entradas inválidas (`abc`, número fora do limite), depois um número válido (`16`), e finalmente `sair`. O programa deve tratar cada caso sem travar.

#### Testes de conectivo dinâmico

Quando um número tem partes compostas, o conectivo entre elas adapta-se:

| Entrada | Resultado | Regra |
| --------- | ----------- | ------- |
| `1.011` | mil e onze | Sem centena → **"e"** |
| `1.111` | mil, cento e onze | Com centena → **vírgula** |
| `1.000.001` | um milhão e um | Apenas duas grandezas → **"e"** |
| `999.999` | novecentos e noventa e nove mil, novecentos e noventa e nove | Ambas as partes tem "e" → **vírgula** |

## Limitações

- Apenas números **inteiros**
- Limite: **zero até 999.999.999.999** (999 bilhões)
- Não aceita números decimais (ex: `1.5` gera erro)

## Estrutura do projeto

```bash
numeros_por_extenso/
├── numero_por_extenso.py           # Código principal
├── setup_venv.py                   # Configura o ambiente virtual
├── tests/
│   ├── conftest.py                 # Configuração do pytest
│   └── test_numero_por_extenso.py  # Testes completos
│   └── ...
└── README.md                       # Este arquivo
```

## Licença

Este projeto é livre para uso pessoal e educacional.
