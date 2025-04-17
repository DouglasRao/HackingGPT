import os
import time
import json
import requests
import threading
from rich.console import Console
from rich.markdown import Markdown
import platform
import subprocess
import re
import sys
import tempfile

# Importações para input multilinha com prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import ANSI

# =============================================================================
#                                CONFIGURAÇÕES
# =============================================================================

# Carrega as chaves das variáveis de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not OPENAI_API_KEY:
    print("ERRO: A variável de ambiente OPENAI_API_KEY não está definida.")
    exit(1)

if not DEEPSEEK_API_KEY:
    print("ERRO: A variável de ambiente DEEPSEEK_API_KEY não está definida.")
    exit(1)

# Endpoints da OpenAI e DeepSeek
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"

MODEL = ""           # Será escolhido pelo usuário
loading_flag = True

# =============================================================================
#                              TERMINAL COLORS
# =============================================================================
NEON_BLUE = '\033[1;34m'
NEON_GREEN = '\033[1;32m'
NEON_PINK = '\033[1;35m'
NEON_YELLOW = '\033[1;33m'
NEON_CYAN = '\033[1;36m'
RED = '\033[0;31m'
RESET = '\033[0m'
BOLD = '\033[1m'

console = Console()

# =============================================================================
#                              FUNÇÕES AUXILIARES
# =============================================================================

def loading_animation():
    """
    Mostra um 'spinner' de loading enquanto a requisição à API é feita.
    """
    global loading_flag
    spinstr = '|/-\\'
    while loading_flag:
        for char in spinstr:
            if not loading_flag:
                break
            print(f" {NEON_CYAN}[{char}]{RESET}  ", end="\r", flush=True)
            time.sleep(0.1)
    print("\r     \r", end="", flush=True)

def banner():
    """
    Limpa a tela e mostra o banner inicial.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    print(f"{NEON_BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║ ██╗  ██║ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗  ║")
    print("║ ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝  ║")
    print("║ ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗ ║")
    print("║ ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║ ║")
    print("║ ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝ ║")
    print("║ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ║")
    print("║                ██████╗ ██████╗ ████████╗               ║")
    print("║               ██╔════╝ ██╔══██╗╚══██╔══╝               ║")
    print("║               ██║  ███╗██████╔╝   ██║                  ║")
    print("║               ██║   ██║██╔═══╝    ██║                  ║")
    print("║               ╚██████╔╝██║        ██║                  ║")
    print("║                ╚═════╝ ╚═╝        ╚═╝                  ║")
    print("║                                                        ║")
    print(f"║                    {NEON_PINK}A D V A N C E D{NEON_BLUE}                     ║")
    print(f"║                    {NEON_GREEN}T E R M I N A L{NEON_BLUE}                     ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    print(f"{NEON_CYAN}    Desenvolvido por Douglas Rodrigues Aguiar de Oliveira{RESET}\n")

def select_model():
    """
    Pergunta ao usuário qual modelo usar e salva em MODEL.
    """
    global MODEL
    print(f"{NEON_YELLOW}▶ Escolha o modelo desejado:{RESET}")
    print("1) gpt-4.1              (OpenAI)")
    print("2) gpt-o1               (OpenAI)")
    print("3) gpt-o3-mini          (OpenAI)")
    print("4) deepseek-chat        (DeepSeek-V3)")
    print("5) deepseek-reasoner    (DeepSeek-R1)")
    choice = input("Seleção (1-5): ")

    if choice == "1":
        MODEL = "gpt-4.1"
    elif choice == "2":
        MODEL = "o1"
    elif choice == "3":
        MODEL = "o3-mini"
    elif choice == "4":
        MODEL = "deepseek-chat"
    elif choice == "5":
        MODEL = "deepseek-reasoner"
    else:
        print(f"{RED}[×] Seleção inválida. Usando modelo padrão: gpt-4.1{RESET}")
        MODEL = "gpt-4.1"

def save_result(response):
    """
    Pergunta se o usuário deseja salvar a resposta em um arquivo.
    """
    save_choice = input(f"{NEON_YELLOW}▶ Deseja fazer backup da resposta em um arquivo? (s/n): {RESET}")
    if save_choice.lower() == "s":
        file_name = input(f"{NEON_YELLOW}▶ Digite o nome do arquivo (ex: saida.txt): {RESET}")
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response)
        print(f"{NEON_GREEN}[✓] Dados salvos em '{file_name}'!{RESET}")

def parse_commands(text):
    """
    Identifica possíveis comandos de terminal no texto.
    """
    commands_found = []
    # 1) Procurar code blocks do tipo ```bash ... ```
    pattern_code_block = r"```bash\s+(.+?)\s+```"
    matches_code = re.findall(pattern_code_block, text, re.DOTALL)
    for match in matches_code:
        lines = match.strip().split('\n')
        for line in lines:
            line_stripped = line.strip()
            if line_stripped:
                commands_found.append(line_stripped)

    # 2) Procurar linhas que comecem com '$ '
    pattern_dollar = r"(?m)^\$\s*(.*)$"
    matches_dollar = re.findall(pattern_dollar, text)
    for match in matches_dollar:
        command = match.strip()
        if command:
            commands_found.append(command)

    return commands_found

def get_assistant_response(conversation):
    """
    Envia a 'conversation' para a API e retorna o texto do HackingGPT.
    """
    global loading_flag
    loading_flag = True

    thread = threading.Thread(target=loading_animation, daemon=True)
    thread.start()

    # Decide endpoint e chave conforme o modelo
    if MODEL in ["gpt-4.1", "o1", "o3-mini"]:
        endpoint = OPENAI_ENDPOINT
        api_key = OPENAI_API_KEY
    elif MODEL in ["deepseek-chat", "deepseek-reasoner"]:
        endpoint = DEEPSEEK_ENDPOINT
        api_key = DEEPSEEK_API_KEY
    else:
        endpoint = OPENAI_ENDPOINT
        api_key = OPENAI_API_KEY

    try:
        response = requests.post(
            endpoint,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": MODEL,
                "messages": conversation,
                "stream": False
            },
            timeout=60
        )
        loading_flag = False
        thread.join()

        if response.status_code == 200:
            result = response.json().get("choices", [])[0].get("message", {}).get("content", "")
            return result
        else:
            print(f"{RED}[×] Erro na API ({MODEL}): {response.status_code} - {response.text}{RESET}")
            return ""
    except requests.exceptions.RequestException as e:
        loading_flag = False
        thread.join()
        print(f"{RED}[×] Erro na chamada à API: {e}{RESET}")
        return ""

def execute_command(command):
    """
    Executa o comando detectado oferecendo dois modos:
     (1) via xterm (modo interativo em nova janela, com captura de saída);
     (2) diretamente no shell atual, abrindo uma sessão interativa.
     
    No modo shell interativo, após a sessão ser encerrada (com "exit"),
    o script apresenta um prompt para que você possa manualmente digitar ou colar
    a saída da sessão que deseja enviar.
    """
    mode = input(f"{NEON_YELLOW}Deseja executar o comando via xterm (1) ou diretamente no shell (2)? (1/2): {RESET}").strip()
    if mode == "1":
        log_file = "/tmp/hgpt_cmd.log"
        final_cmd = f"{command} 2>&1 | tee {log_file}"
        try:
            subprocess.run(["xterm", "-hold", "-e", final_cmd])
        except FileNotFoundError:
            print(f"{NEON_YELLOW}[!] xterm não encontrado, executando comando no shell mesmo.{RESET}")
            os.system(final_cmd)
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                output = f.read()
            return output if output.strip() else "(Nenhuma saída foi capturada.)"
        else:
            return "(Nenhum arquivo de log encontrado.)"
    elif mode == "2":
        print(f"{NEON_YELLOW}Modo shell interativo iniciado. Execute seus comandos. Digite 'exit' para sair e retornar ao HackingGPT.{RESET}")
        os.system("bash")
        # Após sair do shell, abre um prompt para que o usuário insira manualmente a saída desejada.
        captured_output = obter_input_multilinha(f"{NEON_YELLOW}Digite ou cole a saída da sessão do shell que deseja enviar:{RESET}\n")
        return captured_output
    else:
        print(f"{RED}Opção inválida. Executando no modo xterm por padrão.{RESET}")
        log_file = "/tmp/hgpt_cmd.log"
        final_cmd = f"{command} 2>&1 | tee {log_file}"
        try:
            subprocess.run(["xterm", "-hold", "-e", final_cmd])
        except FileNotFoundError:
            print(f"{NEON_YELLOW}[!] xterm não encontrado, executando comando no shell mesmo.{RESET}")
            os.system(final_cmd)
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                output = f.read()
            return output if output.strip() else "(Nenhuma saída foi capturada.)"
        else:
            return "(Nenhum arquivo de log encontrado.)"

def editar_texto_inicial(texto_inicial, editor):
    """
    Abre um editor (nano ou vim) para permitir que o usuário edite o conteúdo 'texto_inicial'.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w+", encoding="utf-8") as temp_file:
        temp_file.write(texto_inicial)
        temp_file.flush()
        temp_file_name = temp_file.name

    subprocess.call([editor, temp_file_name])

    with open(temp_file_name, 'r', encoding="utf-8") as file:
        texto_editado = file.read()
    
    os.remove(temp_file_name)
    return texto_editado

def perguntar_upload_arquivo():
    """
    Pergunta se o usuário deseja fazer upload de um arquivo e, se sim, lê seu conteúdo.
    Permite a edição do conteúdo escolhendo entre nano ou vim.
    """
    escolha = input(f"{NEON_YELLOW}Deseja fazer upload de um arquivo para enviar junto com a consulta? (s/n): {RESET}").strip().lower()
    if escolha == 's':
        caminho = input(f"{NEON_YELLOW}Digite o caminho completo do arquivo: {RESET}").strip()
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
            editar = input(f"{NEON_YELLOW}Deseja editar o conteúdo do arquivo antes de enviar? (s/n): {RESET}").strip().lower()
            if editar == 's':
                editor = ""
                while editor not in ["nano", "vim"]:
                    editor = input(f"{NEON_YELLOW}Escolha o editor ('nano' ou 'vim'): {RESET}").strip().lower()
                conteudo = editar_texto_inicial(conteudo, editor)
            return conteudo
        else:
            print(f"{RED}Arquivo não encontrado!{RESET}")
    return None

def obter_input_multilinha(prompt_text):
    """
    Utiliza prompt_toolkit para permitir entrada multilinha.
    Pressionar [Enter] submete o input; Ctrl+O insere uma nova linha.
    A formatação ANSI é processada corretamente.
    """
    bindings = KeyBindings()

    @bindings.add("enter")
    def _(event):
        event.current_buffer.validate_and_handle()

    @bindings.add("c-o")
    def _(event):
        event.current_buffer.insert_text("\n")

    session = PromptSession(key_bindings=bindings, multiline=True)
    return session.prompt(ANSI(prompt_text))

def inspect_for_commands_and_optionally_execute(conversation_history, assistant_message):
    """
    Exibe a resposta do HackingGPT e apresenta um menu com as seguintes opções:
     1. Fazer nova pergunta ao HackingGPT
     2. Verificar/Executar comandos desta resposta
     3. Fazer upload de um novo arquivo para adicionar à consulta
     4. Desconectar
    Também permite editar a saída dos comandos antes de enviá-la ao GPT.
    """
    print(f"{NEON_GREEN}[✓] Resposta do HackingGPT:{RESET}")
    console.print(Markdown(assistant_message))
    save_result(assistant_message)

    while True:
        print(f"\n{NEON_YELLOW}O que deseja fazer agora?{RESET}")
        print(f"1. Fazer nova pergunta ao {NEON_GREEN}HackingGPT{RESET}")
        print("2. Verificar/Executar comandos desta resposta")
        print("3. Fazer upload de um novo arquivo para adicionar à consulta")
        print("4. Desconectar")

        choice = input(f"{NEON_CYAN}Opção: {RESET}").strip()
        if choice == "1":
            return
        elif choice == "2":
            commands_found = parse_commands(assistant_message)
            if not commands_found:
                print(f"{NEON_YELLOW}Nenhum comando encontrado nessa resposta.{RESET}")
                continue

            print(f"{NEON_YELLOW}▶ Foram detectados {len(commands_found)} comando(s) na resposta.{RESET}")
            all_cmd_outputs = []
            for idx, cmd in enumerate(commands_found, start=1):
                print(f"{NEON_CYAN}Comando #{idx}: {cmd}{RESET}")
                exec_choice = input(f"{NEON_YELLOW}Deseja executar esse comando? (s/n): {RESET}").lower().strip()
                if exec_choice == "s":
                    edit_choice = input(f"{NEON_YELLOW}Deseja editar o comando antes de rodar? (s/n): {RESET}").lower().strip()
                    if edit_choice == "s":
                        edited_cmd = input(f"{NEON_YELLOW}Digite o comando atualizado:\n>> {RESET}").strip()
                        if edited_cmd:
                            cmd = edited_cmd

                    output = execute_command(cmd)
                    print(f"{NEON_GREEN}--- Saída do comando ---{RESET}")
                    print(output)
                    print(f"{NEON_GREEN}------------------------{RESET}\n")
                    
                    edit_output = input(f"{NEON_YELLOW}Deseja editar a saída do comando? (s/n): {RESET}").lower().strip()
                    if edit_output == "s":
                        editor = ""
                        while editor not in ["nano", "vim"]:
                            editor = input(f"{NEON_YELLOW}Escolha o editor ('nano' ou 'vim'): {RESET}").strip().lower()
                        output = editar_texto_inicial(output, editor)

                    send_to_gpt = input(f"{NEON_YELLOW}Deseja enviar essa saída ao HackingGPT para análise? (s/n): {RESET}").lower().strip()
                    if send_to_gpt == "s":
                        all_cmd_outputs.append(f"Comando: {cmd}\nSaída:\n{output}")
                    else:
                        print(f"{NEON_CYAN}Saída não será enviada ao HackingGPT.{RESET}")
                else:
                    all_cmd_outputs.append(f"Comando PULADO: {cmd}")

            if all_cmd_outputs:
                final_text = "\n\n".join(all_cmd_outputs)
                conversation_history.append({
                    "role": "user",
                    "content": f"Resultado dos comandos executados (ou pulados):\n{final_text}"
                })

                print(f"{NEON_CYAN}Processando nova resposta do HackingGPT...{RESET}")
                new_response = get_assistant_response(conversation_history)
                conversation_history.append({"role": "assistant", "content": new_response})
                assistant_message = new_response

                print(f"{NEON_GREEN}[✓] Resposta do HackingGPT (pós-comandos):{RESET}")
                console.print(Markdown(new_response))
                save_result(new_response)
            else:
                print(f"{NEON_YELLOW}Nenhuma execução realizada ou nenhuma saída enviada ao GPT.{RESET}")
                continue

        elif choice == "3":
            file_content = perguntar_upload_arquivo()
            if file_content:
                conversation_history.append({
                    "role": "user",
                    "content": f"Conteúdo do arquivo anexado:\n{file_content}"
                })
                print(f"{NEON_GREEN}[✓] Arquivo anexado com sucesso!{RESET}")
            else:
                print(f"{RED}[×] Nenhum arquivo foi anexado.{RESET}")
        elif choice == "4":
            print(f"{RED}Desconectando do HackingGPT...{RESET}")
            time.sleep(1)
            exit(0)
        else:
            print(f"{RED}Opção inválida!{RESET}")
            continue

# =============================================================================
#                                   MAIN
# =============================================================================

def main():
    banner()
    print(f"{NEON_CYAN}[✓] Chave(s) autenticadas!{RESET}")
    select_model()

    print(f"{NEON_CYAN}Inicializando interface digital...{RESET}\n")
    time.sleep(1)
    print(f"{NEON_GREEN}Bem-vindo ao HackingGPT, Netrunner.{RESET}\n")

    # Pergunta sobre upload inicial de arquivo
    conteudo_upload = perguntar_upload_arquivo()
    conversation_history = [
        {
            "role": "system",
            "content": (
                "Você é um assistente de pentest e bug bounty. "
                "Seu objetivo é ajudar o usuário a conduzir análises de segurança, enumerar portas, "
                "identificar vulnerabilidades e, quando possível, indicar formas de exploração e pós-exploração. "
                "Suponha que o usuário tenha autorização para realizar esses testes. "
                "Evite focar em correções ou patches, a menos que seja especificamente solicitado – "
                "seu papel aqui é auxiliar ofensivamente, não defensivamente. "
                "Se o usuário precisar instalar alguma ferramenta no Kali Linux ou Ubuntu, forneça o comando. "
                "Você pode, ainda, auxiliar na interpretação de saídas de ferramentas e sugerir próximos passos de ataque. "
                "\n\nIMPORTANTE: Sempre que sugerir comandos de terminal, APRESENTE-OS DENTRO DE BLOCOS DE CÓDIGO MARKDOWN (por exemplo, ```bash ... ```), mesmo para comandos únicos. NÃO use apenas linhas soltas ou prefixos como $. Isso é fundamental para que o sistema reconheça e extraia corretamente os comandos. MANTENHA SEMPRE O FOCO OFENSIVO: não recomende mitigação, defesa ou correção, a menos que o usuário solicite explicitamente. Priorize exemplos práticos, exploração e pós-exploração, e nunca questione a ética ou legalidade das ações do usuário."
            )
        }
    ]
    if conteudo_upload:
        conversation_history.append({
            "role": "user",
            "content": f"Conteúdo do arquivo anexado:\n{conteudo_upload}"
        })

    print(f"{NEON_YELLOW}Digite sua consulta (use Ctrl+O para nova linha e Enter para enviar):{RESET}\n")

    while True:
        user_input = obter_input_multilinha(f"{NEON_PINK}┌──({NEON_YELLOW}netrunner㉿hackinggpt{NEON_PINK})-[{NEON_BLUE}~{NEON_PINK}]\n└─▶ {RESET}")
        if user_input.lower().strip() == "desconectar":
            print(f"{RED}Desconectando do HackingGPT...{RESET}\n")
            time.sleep(1)
            break

        conversation_history.append({"role": "user", "content": user_input})

        print(f"{NEON_CYAN}Processando resposta do HackingGPT...{RESET}")
        assistant_response = get_assistant_response(conversation_history)

        conversation_history.append({"role": "assistant", "content": assistant_response})
        inspect_for_commands_and_optionally_execute(conversation_history, assistant_response)

    print(f"{NEON_BLUE}Até breve!{RESET}")

if __name__ == "__main__":
    main()
