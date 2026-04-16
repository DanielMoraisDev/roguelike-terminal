from enum import Enum

class Estado(Enum):
    NORMAL = 0
    DEFESA = 1
    ATORDOADO = 2
    BUFF_ATK = 3
    BUFF_DEF = 4

class Player:
    def __init__(self, dados):
        self.player = dados
        self.em_defesa = False
        self.buff_atk = 0
        self.buff_def = 0
    
    def reset_estado_turno(self):
        self.em_defesa = False
