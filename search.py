from collections import deque

# Definir um estado de jogo
class Estado:
    def __init__(self, jogo, movimento=None, custo=0, heuristica=0):
        self.jogo = jogo
        self.movimento = movimento
        self.custo = custo
        self.heuristica = heuristica

    def __lt__(self, other):
        # Comparar os estados para ordenação em busca A*
        return (self.custo + self.heuristica) < (other.custo + other.heuristica)
    # Definir um estado final correto (por exemplo, todos os galhos ordenados por cor)
estado_final = [
    ["amarelo", "amarelo", "amarelo", "amarelo"],
    ["azul", "azul", "azul", "azul"],
    ["verde", "verde", "verde", "verde"],
    ["vermelho", "vermelho", "vermelho", "vermelho"],
    ["marrom", "marrom", "marrom", "marrom"],
    []
]


# Função de Heurística (exemplo simples)
def heuristica(estado):
    # Exemplo de heurística: número de pássaros fora de lugar
    return sum(1 for galho in estado for passaro in galho if passaro != sorted(galho)[0])

# BFS - Busca em Largura
def bfs(inicio):
    fila = deque([inicio])
    visitados = set()
    while fila:
        estado_atual = fila.popleft()
        if estado_atual.jogo == estado_final:  # Verificar se encontrou a solução
            return estado_atual
        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                fila.append(proximo_estado)
                visitados.add(proximo_estado)
    return None

# Função para gerar os próximos estados possíveis (ações)
def gerar_proximos_estados(estado_atual):
    proximos_estados = []
    
    # Percorre todos os galhos para tentar mover um pássaro para outro galho
    for i, galho_origem in enumerate(estado_atual.jogo):
        if not galho_origem:
            continue  # Pula se o galho estiver vazio
        
        passaro = galho_origem[-1]  # Pega o último pássaro do galho
        
        for j, galho_destino in enumerate(estado_atual.jogo):
            if i != j and (len(galho_destino) < 4 and (not galho_destino or galho_destino[-1] == passaro)):
                # Cria uma cópia do estado atual
                novo_estado = [list(g) for g in estado_atual.jogo]
                novo_estado[i].pop()  # Remove o pássaro do galho de origem
                novo_estado[j].append(passaro)  # Adiciona ao galho de destino
                
                proximos_estados.append(Estado(novo_estado, (i, j), estado_atual.custo + 1, heuristica(novo_estado)))

    return proximos_estados


import heapq

def custo_uniforme(inicio):
    fila = []
    heapq.heappush(fila, inicio)
    visitados = set()
    while fila:
        estado_atual = heapq.heappop(fila)
        if estado_atual.jogo == estado_final:
            return estado_atual
        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                heapq.heappush(fila, proximo_estado)
                visitados.add(proximo_estado)
    return None


# Busca Gulosa
def gulosa(inicio):
    fila = []
    heapq.heappush(fila, (inicio.heuristica, inicio))  # Fila com a heurística
    visitados = set()
    while fila:
        _, estado_atual = heapq.heappop(fila)
        if estado_atual.jogo == estado_final:
            return estado_atual
        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                heapq.heappush(fila, (proximo_estado.heuristica, proximo_estado))
                visitados.add(proximo_estado)
    return None

# A* (A Estrela)
def a_star(inicio):
    fila = []
    heapq.heappush(fila, inicio)
    visitados = set()
    while fila:
        estado_atual = heapq.heappop(fila)
        if estado_atual.jogo == estado_final:
            return estado_atual
        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                heapq.heappush(fila, proximo_estado)
                visitados.add(proximo_estado)
    return None
