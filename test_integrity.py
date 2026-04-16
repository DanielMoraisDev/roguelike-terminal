import sys
import traceback

print("=" * 60)
print("TESTE DE INTEGRIDADE - ROGUELIKE INFINITO".center(60))
print("=" * 60)

testes_passados = []
testes_falhados = []

# Teste 1: Módulo Data
try:
    from data import carregar_dados
    dados = carregar_dados()
    assert isinstance(dados, dict), "dados não é um dicionário"
    assert 'characters' in dados, "chave 'characters' não encontrada"
    assert 'enemies' in dados, "chave 'enemies' não encontrada"
    assert 'bosses' in dados, "chave 'bosses' não encontrada"
    assert 'items' in dados, "chave 'items' não encontrada"
    print(f"✓ MÓDULO DATA: OK - dados carregados")
    testes_passados.append("data.py")
except Exception as e:
    print(f"✗ MÓDULO DATA: FALHOU - {str(e)}")
    testes_falhados.append(("data.py", str(e)))

# Teste 2: Módulo UI
try:
    from ui import limpar_tela, exibir_painel
    assert callable(limpar_tela), "limpar_tela não é callable"
    assert callable(exibir_painel), "exibir_painel não é callable"
    print(f"✓ MÓDULO UI: OK - funções disponíveis")
    testes_passados.append("ui.py")
except Exception as e:
    print(f"✗ MÓDULO UI: FALHOU - {str(e)}")
    testes_falhados.append(("ui.py", str(e)))

# Teste 3: Módulo Player
try:
    from player import Estado, Player
    assert isinstance(Estado.NORMAL, Estado), "Estado.NORMAL não é um Estado"
    assert len(Estado) == 5, "Enum Estado não tem 5 estados"
    dados = carregar_dados()
    player = Player(dados['characters'][0].copy())
    assert hasattr(player, 'em_defesa'), "Player não tem atributo 'em_defesa'"
    print(f"✓ MÓDULO PLAYER: OK - Estado e classe Player funcionando")
    testes_passados.append("player.py")
except Exception as e:
    print(f"✗ MÓDULO PLAYER: FALHOU - {str(e)}")
    testes_falhados.append(("player.py", str(e)))

# Teste 4: Módulo Inventory
try:
    from inventory import abrir_inventario, usar_item
    assert callable(abrir_inventario), "abrir_inventario não é callable"
    assert callable(usar_item), "usar_item não é callable"
    print(f"✓ MÓDULO INVENTORY: OK - funções disponíveis")
    testes_passados.append("inventory.py")
except Exception as e:
    print(f"✗ MÓDULO INVENTORY: FALHOU - {str(e)}")
    testes_falhados.append(("inventory.py", str(e)))

# Teste 5: Módulo Skills
try:
    from skills import usar_skill
    assert callable(usar_skill), "usar_skill não é callable"
    print(f"✓ MÓDULO SKILLS: OK - funções disponíveis")
    testes_passados.append("skills.py")
except Exception as e:
    print(f"✗ MÓDULO SKILLS: FALHOU - {str(e)}")
    testes_falhados.append(("skills.py", str(e)))

# Teste 6: Módulo Combat
try:
    from combat import combate
    assert callable(combate), "combate não é callable"
    print(f"✓ MÓDULO COMBAT: OK - funções disponíveis")
    testes_passados.append("combat.py")
except Exception as e:
    print(f"✗ MÓDULO COMBAT: FALHOU - {str(e)}")
    testes_falhados.append(("combat.py", str(e)))

# Teste 7: Módulo Shop
try:
    from shop import abrir_loja
    assert callable(abrir_loja), "abrir_loja não é callable"
    print(f"✓ MÓDULO SHOP: OK - funções disponíveis")
    testes_passados.append("shop.py")
except Exception as e:
    print(f"✗ MÓDULO SHOP: FALHOU - {str(e)}")
    testes_falhados.append(("shop.py", str(e)))

# Teste 8: Módulo Main
try:
    from main import Roguelike
    game = Roguelike()
    assert hasattr(game, 'dados'), "Roguelike não tem atributo 'dados'"
    assert hasattr(game, 'andar'), "Roguelike não tem atributo 'andar'"
    assert hasattr(game, 'player'), "Roguelike não tem atributo 'player'"
    assert callable(game.selecionar_personagem), "selecionar_personagem não é callable"
    assert callable(game.iniciar), "iniciar não é callable"
    print(f"✓ MÓDULO MAIN: OK - classe Roguelike funcionando")
    testes_passados.append("main.py")
except Exception as e:
    print(f"✗ MÓDULO MAIN: FALHOU - {str(e)}")
    testes_falhados.append(("main.py", str(e)))

# Teste 9: Integridade de Dados
try:
    dados = carregar_dados()
    assert len(dados['characters']) > 0, "nenhum personagem carregado"
    assert len(dados['bosses']) > 0, "nenhum chefe carregado"
    assert len(dados['items']) > 0, "nenhum item carregado"
    assert 'loja' in dados, "chave 'loja' não encontrada"
    print(f"✓ INTEGRIDADE DE DADOS: OK")
    print(f"  - {len(dados['characters'])} personagens")
    print(f"  - {sum(len(v) for k,v in dados['enemies'].items())} inimigos")
    print(f"  - {len(dados['bosses'])} chefes")
    print(f"  - {len(dados['items'])} itens")
    print(f"  - Loja com {len(dados['loja']['items_venda'])} itens disponíveis")
    testes_passados.append("dados")
except Exception as e:
    print(f"✗ INTEGRIDADE DE DADOS: FALHOU - {str(e)}")
    testes_falhados.append(("dados", str(e)))

print("\n" + "=" * 60)
print(f"RESULTADOS: {len(testes_passados)} PASSADOS | {len(testes_falhados)} FALHADOS".center(60))
print("=" * 60)

if testes_falhados:
    print("\nMÓDULOS COM FALHA:")
    for modulo, erro in testes_falhados:
        print(f"  ✗ {modulo}: {erro}")
    sys.exit(1)
else:
    print("\n✓ TODOS OS TESTES PASSARAM - SISTEMA FUNCIONANDO!")
    sys.exit(0)
