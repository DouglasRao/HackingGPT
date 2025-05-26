# HackingGPT

**HackingGPT** é uma ferramenta de Terminal avançada para pentest e bug bounty que integra as APIs do ChatGPT e DeepSeek para auxiliar pesquisadores de segurança na execução e análise de comandos – tudo diretamente pelo Terminal.

## Funcionalidades

- **Assistência dinâmica:**  
  Utiliza as APIs do ChatGPT (OpenAI) e DeepSeek para orientar suas operações de pentest, sugerindo comandos personalizados com base nas suas consultas.

- **Execução interativa de comandos:**  
  O código detecta comandos nas respostas **(sempre apresentados em blocos de código markdown, por exemplo, ```bash ... ```)** e permite que o usuário:
  - Execute o comando em um Terminal interativo (usando `xterm`), onde o comando é rodado automaticamente em uma nova janela e a saída é capturada para análise posterior;
  - Execute manualmente o comando em um shell interativo local, podendo digitar, colar e interagir livremente, e depois informar ao sistema a saída relevante;
  - Edite o comando antes da execução;
  - Pule o comando, se preferir.

  Após a execução, o usuário pode editar a saída capturada (abrindo no nano ou vim, se desejar) e escolher se deseja enviar essa saída de volta ao HackingGPT para análise e próximos passos. Todo o fluxo é interativo e controlado pelo usuário, permitindo integração contínua entre comandos, saídas e novas perguntas.

- **Integração de resultados:**  
  Os resultados dos comandos executados são agregados e enviados de volta à API para nova análise, permitindo um fluxo contínuo de orientação.

- **Integração com múltiplas APIs:**  
  Compatível com:
  - OpenAI: modelos como `gpt-4.1`, `o1`, `o3-mini`;
  - DeepSeek: modelos como `deepseek-chat` (DeepSeek-V3) e `deepseek-reasoner` (DeepSeek-R1).

- **Interface colorida:**  
  Utiliza a biblioteca [Rich](https://github.com/willmcgugan/rich) para exibir mensagens formatadas e renderizar Markdown com cores no Terminal.

- **Configuração via variáveis de ambiente:**  
  As chaves de API são carregadas automaticamente das variáveis de ambiente para maior segurança.

- **Foco ofensivo:**  
  O HackingGPT é orientado para segurança ofensiva. O assistente evita recomendações de mitigação, defesa ou correção, a menos que solicitado explicitamente pelo usuário. O objetivo é sempre explorar, identificar falhas e sugerir formas de exploração e pós-exploração, sem julgamentos éticos ou legais.

## Requisitos

- **Python 3.8+**
- **Dependências externas:**
  - `requests`
  - `rich`
  - `prompt_toolkit`
- **Sistema operacional compatível:**
  - Linux ou WSL (para suporte ao `xterm`).
- **Chaves de API:**
  - `OPENAI_API_KEY`: chave válida para acesso à API da OpenAI.
  - `DEEPSEEK_API_KEY`: chave válida para acesso à API da DeepSeek.

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```

## Instalação

1. **Clone o repositório:**
    
    ```bash
    git clone https://github.com/DouglasRao/HackingGPT.git
    ```
    
2. **Acesse o diretório do projeto:**
    
    ```bash
    cd HackingGPT
    ```
    
3. **(Opcional) Crie e ative um ambiente virtual:**
    
    ```bash
    python -m venv venv
    ```
    
    - No Linux/macOS:
        
        ```bash
        source venv/bin/activate
        ```
        
    - No Windows:
        
        ```bash
        venv\Scripts\activate
        ```
        
4. **Instale as dependências:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
5. **Configure as variáveis de ambiente:**
    
    - No Linux/macOS:
        
        ```bash
        export OPENAI_API_KEY="sua-chave-openai"
        export DEEPSEEK_API_KEY="sua-chave-deepseek"
        ```
        
    - No Windows (PowerShell):
        
        ```bash
        $env:OPENAI_API_KEY="sua-chave-openai"
        $env:DEEPSEEK_API_KEY="sua-chave-deepseek"
        ```
        
## Uso

1. **Execute o script:**
    
    No diretório do projeto, inicie a ferramenta:
    
    ```bash
    python hackingGPT.py
    ```
    
2. **Siga as instruções na tela:**
    
    - **Seleção do modelo:**  
        Escolha entre os modelos disponíveis (por exemplo, `gpt-4.1`, `o1`, `o3-mini`, `deepseek-chat`, `deepseek-reasoner`, etc.).
        
    - **Entrada de consulta:**  
        Digite sua consulta de pentest ou bug bounty (por exemplo: "Quero realizar um pentest básico em example.com") ou digite `desconectar` para sair.
        
    - **Fluxo interativo:**
        
        - O script enviará sua consulta à API e exibirá a resposta.
        - Se forem detectados comandos na resposta, você poderá:
            1. Executar o comando (com a opção de editá-lo antes);
            2. Pular o comando.
3. **Execução interativa com `xterm`:**
    
    - Quando um comando for executado, uma janela do `xterm` será aberta, permitindo uma interação direta.
    - A saída do comando será registrada e apresentada para análise posterior.
4. **Itere ou saia:**

    - Continue fazendo novas perguntas ou processando comandos adicionais conforme necessário.

## Contribuição

Contribuições são bem-vindas! Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para obter diretrizes sobre como reportar bugs, sugerir melhorias ou enviar novas funcionalidades.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE.txt).

---

**Desenvolvido por Douglas Rodrigues Aguiar de Oliveira**
