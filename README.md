# Trabalho 1 de Processamento de de Imagens
### Aluno: Luis A V Franklin
### Professor: Dr. Thelmo Pontes

Esta é uma aplicação de desktop desenvolvida em Python com a biblioteca Tkinter, para a disciplina de Processamento de Imagens do Programa de Pós-Graduação em Ciência da Computação (PPgCC) da Universidade Estadual do Ceará (UECE).
Ela permite que usuários selecionem imagens de um diretório e apliquem diversas operações, tanto lógicas (binarizadas) quanto aritméticas (em tons de cinza).

## Funcionalidades

-   **Seleção de Diretório:** Escolha uma pasta para listar todas as imagens compatíveis.
-   **Seleção de Imagens:** Selecione uma ou duas imagens da lista para operar.
-   **Modos de Operação:**
    -   **Lógico:** As imagens são binarizadas (preto e branco) com base em um limiar ajustável antes da operação.
    -   **Aritmético:** As operações são aplicadas diretamente nos valores dos pixels em tons de cinza.
-   **Operações Aritméticas:** Adição, Subtração, Multiplicação e Divisão.
-   **Operações Lógicas:** AND, OR, XOR e NOT.
-   **Pré-visualização em Tempo Real:** Veja as imagens de entrada (já processadas pelo modo e limiar) e o resultado da operação.
-   **Salvar Resultado:** O resultado pode ser salvo como um novo arquivo de imagem.

## Estrutura do Projeto

O código é modularizado para facilitar a manutenção e a leitura.

```
trabalho/
├── install_and_run.bat  # Script para instalar e rodar no Windows
├── README.md            # Esta documentação
├── requirements.txt     # Dependências do Python
├── run.py               # Ponto de entrada da aplicação
└── modules/             # Pacote com a lógica principal
    ├── ui.py            # Contém a classe e a lógica da interface Tkinter
    ├── ops.py           # Funções de processamento e operações de imagem
    └── utils.py         # Funções utilitárias (listar arquivos, conversões, etc.)
```

## Pré-requisitos

-   Python 3.8 ou superior
-   `pip` (gerenciador de pacotes do Python)

## Instalação e Execução

Existem duas maneiras de executar o projeto:

### Método 1: Usando o Script (Windows)

1.  Baixe ou clone todos os arquivos do projeto.
2.  Dê um duplo clique no arquivo `install_and_run.bat`.
3.  O script irá automaticamente instalar as bibliotecas necessárias e iniciar a aplicação.

### Método 2: Manualmente (Qualquer Sistema Operacional)

1.  Abra um terminal ou prompt de comando na pasta `trabalho`.

2.  **(Opcional, mas recomendado)** Crie um ambiente virtual para isolar as dependências do projeto:
    ```sh
    python -m venv venv
    ```
    E ative-o:
    -   No Windows: `venv\Scripts\activate`
    -   No Linux/macOS: `source venv/bin/activate`

3.  Instale as dependências listadas no `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

4.  Execute a aplicação:
    ```sh
    python run.py
    ```