import random
from colorama import Fore

def usar_skill(skill_idx, player, inimigos, dados):
    skill = player['skills'][skill_idx]
    
    if player['stamina'] < skill['custo_stamina']:
        print(Fore.RED + "\n[!] Stamina insuficiente!")
        return False
    
    player['stamina'] -= skill['custo_stamina']
    
    if skill.get('tipo') == 'defesa':
        print(Fore.CYAN + f"\n[!] {player['nome']} usou {skill['name']}!")
        print(f"Reduzindo {skill['desc']}")
        return "defesa"
    
    elif skill.get('tipo') == 'buff':
        player['atk'] = int(player['atk'] * 1.3)
        print(Fore.YELLOW + f"\n[!] {skill['name']} ativada!")
        print(f"ATK aumentado em 30% por 2 turnos!")
        return True
    
    else:  # Ataque
        vivos = [i+1 for i, e in enumerate(inimigos) if e['hp'] > 0]
        if not vivos:
            return False
        
        print(f"Alvo {vivos}: ", end='')
        try:
            alvo = int(input()) - 1
            if 0 <= alvo < len(inimigos) and inimigos[alvo]['hp'] > 0:
                dano = skill['dano']
                crit_chance = player['crit_chance'] + 0.2
                crit = random.random() < crit_chance
                
                if crit:
                    dano = int(dano * 1.5)
                
                inimigos[alvo]['hp'] -= dano
                print(Fore.YELLOW + f"\n{skill['name']}! {dano} de dano! {'(CRÍTICO!)' if crit else ''}")
                return True
        except:
            return False
