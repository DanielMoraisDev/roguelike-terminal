import random
from colorama import Fore
from data import carregar_dados
from ui import exibir_painel, limpar_tela
from combat import combate

class Roguelike:
    def __init__(self):
        self.dados = carregar_dados()
        self.andar = 1
        self.player = None
        self.ouro = 0
        self.exp = 0
        self.nivel = 1

    def selecionar_personagem(self):
        limpar_tela()
        opcoes = [f"{i+1}. {c['type']} (HP: {c['hp']} | ATK: {c['atk']} | DEF: {c['def']} | CRIT: {c['crit_chance']*100}%)" 
                  for i, c in enumerate(self.dados['characters'])]
        exibir_painel("SELECIONE SEU CAMPEÃO", opcoes, Fore.CYAN)
        
        try:
            idx = int(input(f"{Fore.GREEN}>> ")) - 1
            if 0 <= idx < len(self.dados['characters']):
                self.player = self.dados['characters'][idx].copy()
                self.player['nome'] = input(f"{Fore.GREEN}Nome do herói: ").upper()
                self.player['stamina'] = self.player['max_stamina']
            else:
                self.selecionar_personagem()
        except: 
            self.selecionar_personagem()

    def iniciar(self):
        limpar_tela()
        print(Fore.MAGENTA + """
        ╔═══════════════════════════════════════════════╗
        ║       BEM-VINDO AO ROGUELIKE INFINITO         ║
        ║   Explore masmorras, derroте inimigos e       ║
        ║      torne-se a lenda da sua jornada          ║
        ╚═══════════════════════════════════════════════╝
        """)
        input("Pressione Enter para continuar...")
        
        self.selecionar_personagem()
        limpar_tela()
        
        while self.player['hp'] > 0:
            eh_boss = any(b['andar'] == self.andar for b in self.dados['bosses'])
            
            if eh_boss:
                boss = next(b for b in self.dados['bosses'] if b['andar'] == self.andar)
                print(Fore.RED + f"\n╔═════════════════════════════════════════════╗")
                print(Fore.RED + f"║  CHEFE DO ANDAR {self.andar}: {boss['name'].center(25)} ║")
                print(Fore.RED + f"║  {boss['desc'].center(45)} ║")
                print(Fore.RED + f"╚═════════════════════════════════════════════╝")
                input("\nPressione Enter para iniciar o combate...")
                
                inimigos = [boss.copy()]
                inimigos[0]['max_hp'] = inimigos[0]['hp']
                inimigos[0]['atordoado'] = False
            else:
                andar_key = f'andar_{self.andar}'
                if andar_key not in self.dados['enemies']:
                    andares_disponiveis = [int(k.split('_')[1]) for k in self.dados['enemies'].keys() if k.startswith('andar_')]
                    andar_mais_proximo = max([a for a in andares_disponiveis if a <= self.andar], default=max(andares_disponiveis))
                    andar_key = f'andar_{andar_mais_proximo}'
                
                pool = self.dados['enemies'][andar_key]
                quantidade = random.randint(1, 2)
                inimigos = []
                for _ in range(quantidade):
                    inimigo = random.choice(pool).copy()
                    inimigo['max_hp'] = inimigo['hp']
                    inimigo['atordoado'] = False
                    inimigos.append(inimigo)
            
            resultado = combate(self.player, inimigos, False, self.dados)
            
            if resultado == "fuga":
                self.andar = max(1, self.andar - 1)
            elif resultado:
                if eh_boss:
                    boss = next(b for b in self.dados['bosses'] if b['andar'] == self.andar)
                    print(Fore.CYAN + f"\n[!] Você derrotou {boss['name']}!")
                    print(Fore.YELLOW + f"[!] Obteve: {boss['drop_especial']}!")
                    self.player['items'].append(boss['drop_especial'])
                
                exp_ganho = 50 * self.andar
                self.exp += exp_ganho
                print(f"{Fore.YELLOW}\n[!] Você ganhou {exp_ganho} EXP!")
                
                ouro_ganho = random.randint(20 * self.andar, 50 * self.andar)
                self.ouro += ouro_ganho
                print(f"{Fore.YELLOW}[!] Você ganhou {ouro_ganho} moedas de ouro!")
                
                self.andar += 1
                
                if random.random() < 0.4:
                    loot = random.choice(self.dados['loot_tables']['comum'])
                elif random.random() < 0.25:
                    loot = random.choice(self.dados['loot_tables']['raro'])
                else:
                    loot = random.choice(self.dados['loot_tables']['epico'])
                
                self.player['items'].append(loot)
                print(f"{Fore.YELLOW}[!] Você encontrou: {loot}!")
                input("Avançando para o próximo andar...")
            else:
                limpar_tela()
                exibir_painel("FIM DE JOGO", [
                    f"Você chegou ao andar {self.andar}",
                    f"Nível: {self.nivel}",
                    f"Experiência Total: {self.exp}",
                    f"Ouro Coletado: {self.ouro}"
                ], Fore.RED)
                break

if __name__ == "__main__":
    Roguelike().iniciar()