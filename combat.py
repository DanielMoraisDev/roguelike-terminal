import random
from colorama import Fore
from ui import exibir_painel, limpar_tela
from inventory import abrir_inventario
from skills import usar_skill

def exibir_status(player, inimigos):
    barra_hp = "█" * (player['hp'] // (player['max_hp'] // 20)) + "░" * (20 - (player['hp'] // (player['max_hp'] // 20)))
    barra_stamina = "▓" * (player['stamina'] // (player['max_stamina'] // 15)) + "░" * (15 - (player['stamina'] // (player['max_stamina'] // 15)))
    
    status_p = [
        f"HERÓI: {player['nome']} | Nv. 1",
        f"HP: [{barra_hp}] {player['hp']}/{player['max_hp']}",
        f"Stamina: [{barra_stamina}] {player['stamina']}/{player['max_stamina']}",
        f"ATK: {player['atk']} | DEF: {player['def']} | CRIT: {player['crit_chance']*100:.0f}%",
    ]
    exibir_painel("STATUS DO JOGADOR", status_p, Fore.GREEN)
    
    status_e = []
    for i, e in enumerate(inimigos):
        vida = f"{e['hp']} HP" if e['hp'] > 0 else "MORTO"
        barra = "█" * (e['hp'] // max(1, e['max_hp'] // 15)) + "░" * (15 - (e['hp'] // max(1, e['max_hp'] // 15)))
        status_e.append(f"[{i+1}] {e['name'].ljust(15)} [{barra}] {vida}")
    exibir_painel("INIMIGOS", status_e, Fore.RED)

def combate(player, inimigos, em_defesa, dados):
    rodada = 1
    pula_ataque = False
    
    while player['hp'] > 0 and any(e['hp'] > 0 for e in inimigos):
        limpar_tela()
        exibir_status(player, inimigos)
        
        print(Fore.YELLOW + f"\n═══ RODADA {rodada} ═══")
        
        print(f"{Fore.CYAN}(A)tacar | (S)kill | (I)nventário | (D)efesa | (R)efúgio")
        acao = input(f"{Fore.GREEN}>> ").upper()
        
        pula_ataque_inimigo = False
        
        if acao == 'A':
            vivos = [i+1 for i, e in enumerate(inimigos) if e['hp'] > 0]
            if vivos:
                print(f"Alvo {vivos}: ", end='')
                try:
                    alvo = int(input()) - 1
                    if 0 <= alvo < len(inimigos) and inimigos[alvo]['hp'] > 0:
                        crit = random.random() < player['crit_chance']
                        dano_base = player['atk']
                        if em_defesa:
                            dano_base = int(dano_base * 0.7)
                            em_defesa = False
                        dano = int(dano_base * (1.5 if crit else 1))
                        inimigos[alvo]['hp'] -= dano
                        print(Fore.YELLOW + f"\nVocê causou {dano} de dano! {'(CRÍTICO!)' if crit else ''}")
                except:
                    pass
        
        elif acao == 'S':
            print(f"\n{Fore.CYAN}Habilidades disponíveis:")
            for i, s in enumerate(player['skills']):
                stamina_color = Fore.GREEN if player['stamina'] >= s['custo_stamina'] else Fore.RED
                print(f"{stamina_color}{i+1}. {s['name']} (Custo: {s['custo_stamina']} Stamina) - {s['desc']}")
            
            try:
                skill_idx = int(input(f"{Fore.GREEN}Escolha a skill (1-{len(player['skills'])}): ")) - 1
                resultado = usar_skill(skill_idx, player, inimigos, dados)
                if resultado == "defesa":
                    em_defesa = True
                elif resultado == "stun":
                    pula_ataque_inimigo = True
            except:
                pass
        
        elif acao == 'I':
            resultado = abrir_inventario(player, inimigos, dados)
            if not resultado: 
                continue
            if resultado == "stun": 
                pula_ataque_inimigo = True
        
        elif acao == 'D':
            em_defesa = True
            print(Fore.CYAN + "\n[!] Você assumiu uma postura defensiva!")
        
        elif acao == 'R':
            return "fuga"
        
        input("Pressione Enter...")

        # Turno dos Inimigos
        if not pula_ataque_inimigo:
            print(f"\n{Fore.RED}Turno dos inimigos...")
            for e in inimigos:
                if e['hp'] > 0:
                    if e.get('atordoado'):
                        print(f"{Fore.BLUE}{e['name']} está atordoado e não pode atacar!")
                        e['atordoado'] = False
                    else:
                        dano_base = max(1, e['atk'] - (player['def'] // 2))
                        if em_defesa:
                            dano_base = int(dano_base * 0.5)
                        dano_e = dano_base
                        player['hp'] -= dano_e
                        print(f"{Fore.RED}{e['name']} atacou: {dano_e} de dano!")
                        em_defesa = False
            
            # Recuperar stamina
            stamina_recovery = max(15, int(player['max_stamina'] * 0.25))
            player['stamina'] = min(player['max_stamina'], player['stamina'] + stamina_recovery)
            
            rodada += 1
            input("\nFim do turno... [Enter]")

    return player['hp'] > 0
