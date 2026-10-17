🇺🇸 [English](README.md) | 🇧🇷 Português

# Sistema de Gerenciamento de Biblioteca Pessoal

## Descrição
Um sistema de biblioteca pessoal feito em Python que roda diretamente no terminal (CLI) para ajudar os usuários a organizar seus livros. A aplicação se conecta à API do Google Books para buscar automaticamente os detalhes do livro (como título, autores e gêneros) durante o cadastro. Para manter a simplicidade, os dados são salvos localmente em um arquivo `storage.jsonl`, usando JSON Lines para persistência. Ela também gera gráficos com a biblioteca Matplotlib. Por fim, o projeto inclui testes automatizados em `test_project.py` com mocks, de modo que os testes rodam de forma independente, sem mexer no arquivo de armazenamento real e sem depender de a API do Google estar online.

---

## Funcionalidades

- **Busca Automática de Dados**: Consome a API do Google Books para buscar detalhes dos livros, recorrendo à digitação manual em caso de falha de rede ou de busca.
- **Persistência de Dados**: Armazena os registros dos livros em JSON Lines (`storage.jsonl`). Lê os dados usando um gerador Python (`yield`).
- **Visualização de Dados**: Gera um gráfico (`graphic.png`) mostrando a quantidade de livros disponíveis por gênero, usando `matplotlib`.
- **Validação de CLI**: O projeto inclui rotinas de validação personalizadas para tratar strings vazias, limites de opções numéricas e quantidades não positivas, de modo que o programa não quebre com entradas inválidas.
- **Testes Unitários Robustos**: Inclui uma suíte completa de testes `pytest` com 32 testes, usando `unittest.mock` para testar as funções principais e isolar operações de I/O de arquivo e requisições à API.

---

## Estrutura de Arquivos e Arquitetura do Sistema

- **`project.py`**: O ponto de entrada da aplicação. Contém o loop principal da CLI (`main()`), a seleção das opções do menu (`get_menu_choice()`), o fluxo de cadastro de livros (`register_new_book()`) e a lógica de geração de gráficos (`generate_graph()`).
- **`google_books_api.py`**: Cuida das consultas externas à API do Google Books usando `requests`. Inclui o tratamento de fallback da chave de API e timeouts de rede (`timeout=5`).
- **`models.py`**: Define a classe de modelo de dados `Book`, responsável por instanciar objetos de livro e converter o estado interno em representações de dicionário (`to_dict()`).
- **`storage.py`**: A camada de acesso a dados. Implementa operações de append no arquivo (`add_book`), o gerador de informações (`list_books`), o construtor de dicionário para a biblioteca Matplotlib (`dict_books_by_genre`) e as buscas por livro (`search_book_by_title`).
- **`validators.py`**: Fornece funções reutilizáveis de entrada (`get_string`, `get_answer_yes_no`, `get_positive_int`), garantindo tratamento defensivo de entradas e de exceções.
- **`test_project.py`**: A suíte de testes automatizados para o `pytest`. Testa lógica de negócio, validação de entrada, funções de armazenamento, rede da API e efeitos colaterais via `unittest.mock` (`patch`, `mock_open`, `monkeypatch` e `capsys`).
- **`requirements.txt`**: Lista as dependências necessárias para o funcionamento correto (`requests`, `matplotlib`, `python-dotenv`).
- **`requirements-dev.txt`**: Lista as dependências necessárias para desenvolvimento e testes (`pytest`, `pytest-cov`, `mypy`, `black`).
- **`.env.example`**: Modelo para a chave opcional da API do Google Books. Copie para `.env` e preencha com a sua chave.
- **`storage.example.jsonl`**: Dados de exemplo (um livro por linha) para experimentar o app sem precisar cadastrar livros antes.
- **`.gitignore`**: Mantém arquivos locais fora do repositório (`.env`, `storage.jsonl`, `graphic.png`, caches).

---

## Decisões de Design

1. **Separação de Responsabilidades (SoC)**: Cada função foi desenhada para ter apenas um trabalho, o que facilita os testes. Por exemplo: a camada de armazenamento (`storage.py`) não contém chamadas diretas a `print()` para listagens de dados, e devolve dicionários brutos via `yield`. A camada de apresentação (`project.py`) é a única responsável por exibir a saída ao usuário.
2. **Geradores para Tratamento de I/O**: `storage.list_books()` usa `yield` para ler o arquivo linha por linha, em vez de carregá-lo inteiro de uma vez.
3. **Defensividade da API**: As requisições HTTP externas tratam internamente exceções de conectividade (`RequestException`) e códigos de status HTTP (`raise_for_status()`), garantindo que a CLI continue estável mesmo que a API esteja fora do ar ou devolva respostas vazias.
4. **Type Hints**: Toda função tem type hints, o que torna o código mais fácil de ler e permite que o `mypy` detecte erros.

---

## Configuração e Execução

### Pré-requisitos
- Python 3.11+
- Ambiente virtual (`venv`)

### Instalação

1. **Clone o repositório e entre na pasta:**
   ```bash
   git clone https://github.com/PedroG021/library-system.git
   cd YOUR-REPOSITORY-NAME
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python3 -m venv .venv
   ```

3. **Ative o ambiente virtual:**
   - Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     .venv\Scripts\activate
     ```

4. **Instale as bibliotecas necessárias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **(Opcional) Adicione uma chave da API do Google Books.** O app funciona sem ela:
   ```bash
   cp .env.example .env
   ```
   Depois abra o `.env` e substitua `your_key_here` pela sua chave.

6. **(Opcional) Comece com dados de exemplo.** Caso contrário, o `storage.jsonl` é criado automaticamente quando você cadastrar o primeiro livro:
   ```bash
   cp storage.example.jsonl storage.jsonl
   ```

### Executando a Aplicação

```bash
python project.py
```

### Executando os Testes

```bash
pip install -r requirements-dev.txt
pytest test_project.py
```

---

## Uso

Ao rodar `python project.py`, um menu é exibido (o programa exibe o menu em inglês, exatamente como abaixo):

```text
Type 1 to register a new book.
Type 2 to list all registered books.
Type 3 to search for a book by title.
Type 4 to view a graphic of the available quantity books by genre.
Type 0 to exit the program.
```

O gráfico da opção 4 é salvo como `graphic.png` na pasta atual.

---

## Uso de IA

Todo o código desta aplicação foi escrito por mim. Assistentes de IA foram usados apenas como apoio ao aprendizado, para tirar dúvidas e explicar conceitos, e na documentação (estrutura do README e tradução para o português).

## Limitações Conhecidas

- Cadastrar o mesmo livro duas vezes cria duas entradas separadas.
- A busca por título exige o título exato (sem diferenciar maiúsculas de minúsculas).

---

## Roadmap (v2.0)

Próximas atualizações técnicas planejadas para este projeto:

* [ ] Migrar a persistência em arquivo JSON local para um banco de dados relacional (**PostgreSQL**) via **SQLAlchemy ORM**.
* [ ] Substituir a interface CLI por uma API RESTful construída com **FastAPI** e esquemas de validação do **Pydantic**.
* [ ] Containerizar o ambiente da aplicação usando **Docker** e **Docker Compose**.
