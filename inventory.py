from colorama import Fore
from ui import exibir_painel, limpar_tela

def abrir_inventario(player, inimigos, dados):
    while True:
        itens = player['items']
        menu_i = [f"{i+1}. {item} - {dados['items'][item]['desc']}" for i, item in enumerate(itens)]
        menu_i.append("0. Voltar")
        
        limpar_tela()
        exibir_painel("MOCHILA (Escolha para usar)", menu_i, Fore.MAGENTA)
        
        escolha = input(f"{Fore.GREEN}>> ")
        if escolha == '0' or not escolha: 
            return False
        
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(itens):
                nome_item = itens.pop(idx)
                return usar_item(nome_item, player, inimigos, dados)
            else:
                continue
        except: 
            continue

def usar_item(nome_item, player, inimigos, dados):
    item_data = dados['items'][nome_item]
    
    if item_data['tipo'] == "cura":
        player['hp'] = min(player['max_hp'], player['hp'] + item_data['valor'])
        print(Fore.GREEN + f"\n[!] Você usou {nome_item}! HP restaurado.")
    
    elif item_data['tipo'] == "cura_stamina":
        player['hp'] = min(player['max_hp'], player['hp'] + item_data['valor'])
        player['stamina'] = min(player['max_stamina'], player['stamina'] + 50)
        print(Fore.CYAN + f"\n[!] Você usou {nome_item}! HP e Stamina restaurados.")
    
    elif item_data['tipo'] == "dano_area":
        dano_por_inimigo = item_data['valor']
        for e in inimigos:
            e['hp'] -= dano_por_inimigo
        print(Fore.RED + f"\n[!] {nome_item} explodiu no campo! Todos os inimigos sofreram {dano_por_inimigo} de dano!")
    
    elif item_data['tipo'] == "stun":
        print(Fore.BLUE + f"\n[!] {nome_item} ativado! Inimigos atordoados por 1 turno!")
        for e in inimigos:
            e['atordoado'] = True
        return "stun"
    
    elif item_data['tipo'] == "buff":
        player['atk'] = int(player['atk'] * 1.3)
        print(Fore.YELLOW + f"\n[!] {nome_item}! ATK aumentado em 30% por 2 turnos!")
    
    elif item_data['tipo'] == "buff_def":
        player['def'] = int(player['def'] * 1.25)
        print(Fore.YELLOW + f"\n[!] {nome_item}! DEF aumentada em 25% por 2 turnos!")
    
    elif item_data['tipo'] == "ouro":
        print(Fore.YELLOW + f"\n[!] Ganhou {item_data['valor']} moedas de ouro!")
    
    return True
