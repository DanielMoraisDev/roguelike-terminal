import os
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_painel(titulo, conteudo, cor=Fore.WHITE):
    largura = 60
    print(cor + "┌" + "─" * (largura-2) + "┐")
    print(cor + f"│ {titulo.center(largura-4)} │")
    print(cor + "├" + "─" * (largura-2) + "┤")
    for linha in conteudo:
        print(cor + f"│ {str(linha).ljust(largura-4)} │")
    print(cor + "└" + "─" * (largura-2) + "┘")
