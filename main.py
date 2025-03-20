from colored import fg
import requests
import time
import sys
import os
import random

r = fg(241)   # Cinza escuro
r2 = fg(255)  # Branco
b = fg(31)    # Azul
red = fg(196) # Vermelho
green = fg(82) # Verde

def clear_console():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Exibe o banner centralizado."""
    clear_console()
    banner_lines = [
        " ██ ▄█▀ ██▓  ██████   ██████ ",
        " ██▄█▒ ▓██▒▒██    ▒ ▒██    ▒ ",
        "▓███▄░ ▒██▒░ ▓██▄   ░ ▓██▄   ",
        "▓██ █▄ ░██░  ▒   ██▒  ▒   ██▒",
        "▒██▒ █▄░██░▒██████▒▒▒██████▒▒",
        "▒ ▒▒ ▓▒░▓  ▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░",
        "░ ░▒ ▒░ ▒ ░░ ░▒  ░ ░░ ░▒  ░ ░",
        "░ ░░ ░  ▒ ░░  ░  ░  ░  ░  ░  ",
        "░  ░    ░        ░        ░  ",
    ]

    terminal_width = os.get_terminal_size().columns
    print("\n" * 2)
    for line in banner_lines:
        print(f"{red}{line.center(terminal_width)}{r2}")
    
    print(f"\n{green}{'Painel Clear DM **Developed by @gqai**'.center(terminal_width)}{r2}\n")

def progressbar(it, prefix="Progresso:", size=60, file=sys.stdout):
    """Exibe uma barra de progresso com porcentagem."""
    count = len(it)

    def show(i):
        percent = (i / count) * 100
        filled_length = int(size * i // count)
        bar = '■' * filled_length + '.' * (size - filled_length)
        file.write(f"\r{prefix} [{green}{bar}{r2}] {percent:6.2f}%")
        file.flush()

    show(0)
    for i, item in enumerate(it, 1):
        yield item
        show(i)
    file.write("\n")
    file.flush()

def fetch_messages(headers, channel_id, author_id):
    """Busca todas as mensagens do usuário no canal."""
    messages = []
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    print(f"{b}Buscando mensagens...{r2}")

    while True:
        params = {"limit": 100}
        if messages:
            params["before"] = messages[-1]
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code != 200:
                print(f"{red}Erro ao acessar o canal. Status Code: {response.status_code}{r2}")
                return []

            data = response.json()
            if not data:
                break

            # Adiciona IDs das mensagens enviadas pelo usuário
            user_messages = [msg["id"] for msg in data if msg["author"]["id"] == author_id]
            messages.extend(user_messages)

            # Caso não encontre mensagens, encerra o loop
            if len(data) < 100:
                break

        except requests.RequestException as e:
            print(f"{red}Erro na requisição: {e}{r2}")
            break

    print(f"{green}Encontradas {len(messages)} mensagens.{r2}")
    return messages

def delete_messages(headers, channel_id, messages):
    """Deleta mensagens com intervalo aleatório."""
    url_template = f"https://discord.com/api/v9/channels/{channel_id}/messages/{{}}"
    
    for msg_id in progressbar(messages, "Deletando mensagens:"):
        try:
            response = requests.delete(url_template.format(msg_id), headers=headers, timeout=10)
            
            if response.status_code != 204:
                print(f"\n{red}Falha ao deletar mensagem {msg_id}. Status: {response.status_code}{r2}")

            wait_time = random.uniform(1.0, 1.9)
            time.sleep(wait_time)
        
        except requests.RequestException as e:
            print(f"\n{red}Erro ao tentar deletar: {e}{r2}")

def clear_messages(token, channel_id):
    """Gerencia o processo de exclusão das mensagens."""
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        user_response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        
        if user_response.status_code != 200:
            print(f"{red}Erro ao obter ID do usuário. Status: {user_response.status_code}{r2}")
            return

        author_id = user_response.json().get("id")
        
        messages = fetch_messages(headers, channel_id, author_id)

        if messages:
            print(f"{green}Iniciando exclusão...{r2}")
            delete_messages(headers, channel_id, messages)
            print(f"\n{green}Todas as mensagens foram deletadas com sucesso!{r2}")
        else:
            print(f"{red}Nenhuma mensagem encontrada para deletar.{r2}")

    except requests.RequestException as e:
        print(f"{red}Erro na conexão: {e}{r2}")

    input("\n** Pressione qualquer tecla para sair **")

if __name__ == "__main__":
    banner()
    token = input("Token: ").strip()
    channel_id = input("ID do Canal: ").strip()
    
    if not token or not channel_id:
        print(f"{red}Token ou ID do canal não podem estar vazios!{r2}")
        sys.exit(1)
    
    clear_messages(token, channel_id)
