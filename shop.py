from colorama import Fore
from ui import exibir_painel, limpar_tela

def abrir_loja(player, ouro, dados):
    """Abre a loja de itens, retorna ouro restante após compras"""
    while True:
        limpar_tela()
        
        loja_items = dados['loja']['items_venda']
        opcoes = [f"{i+1}. {item['item']} - {item['preco']} ouro" 
                  for i, item in enumerate(loja_items)]
        opcoes.append("0. Sair da loja")
        
        exibir_painel(f"LOJA DO VIAJANTE | Ouro: {ouro}", opcoes, Fore.YELLOW)
        
        try:
            escolha = input(f"{Fore.GREEN}>> ")
            
            if escolha == '0' or not escolha:
                return ouro
            
            idx = int(escolha) - 1
            if 0 <= idx < len(loja_items):
                item_data = loja_items[idx]
                nome_item = item_data['item']
                preco = item_data['preco']
                
                if ouro >= preco:
                    ouro -= preco
                    player['items'].append(nome_item)
                    print(Fore.GREEN + f"\n[!] Você comprou {nome_item}!")
                    input("Pressione Enter...")
                else:
                    print(Fore.RED + f"\n[!] Você não tem ouro suficiente! (Custa {preco}, você tem {ouro})")
                    input("Pressione Enter...")
            else:
                continue
        except:
            continue
    
    return ouro
