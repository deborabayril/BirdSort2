from collections import deque

# Definir um estado de jogo
class Estado:
    def __init__(self, jogo, movimento=None, custo=0, profundidade=0, heuristica=0):
        self.jogo = jogo
        self.movimento = movimento
        self.custo = custo
        self.profundidade = profundidade
        self.heuristica = heuristica  # Valor heurístico do estado

    def __eq__(self, other):
        return self.jogo == other.jogo

    def __hash__(self):
        return hash(str(self.jogo))

    def __lt__(self, other):
        return self.heuristica < other.heuristica

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
    """
    Exemplo de heurística: número de pássaros fora de lugar.
    """
    return sum(1 for galho in estado.jogo for passaro in galho if passaro != galho[0])

# Função para verificar se o estado atual é uma vitória
def verificar_vitoria(jogo):
    """
    Verifica se o estado atual do jogo é uma vitória.
    """
    cores_em_galhos = {}  # Dicionário para rastrear em quais galhos cada cor aparece

    for i, galho in enumerate(jogo):
        if len(galho) > 0:  # Ignora galhos vazios
            if len(set(galho)) > 1:  # Mais de uma cor no mesmo galho
                return False
            cor = galho[0]  # A cor dominante do galho
            if cor not in cores_em_galhos:
                cores_em_galhos[cor] = set()
            cores_em_galhos[cor].add(i)  # Adiciona o índice do galho onde a cor aparece

    # Verifica se cada cor está presente em apenas um galho
    for galhos in cores_em_galhos.values():
        if len(galhos) > 1:  # A cor aparece em mais de um galho
            return False

    # Verifica se todas as cores possíveis estão agrupadas
    num_cores, _ = obter_dados_do_estado_inicial(jogo)
    todas_cores = set(cores_em_galhos.keys())
    return len(todas_cores) == num_cores

# BFS - Busca em Largura
def bfs(inicio):
    """
    Implementação da busca em largura (BFS) para encontrar a solução do jogo.
    """
    from collections import deque

    fila = deque([inicio])  # Fila para BFS
    visitados = set()  # Conjunto para rastrear estados visitados

    while fila:
        estado_atual = fila.popleft()  # Pega o próximo estado

        if verificar_vitoria(estado_atual.jogo):  # Verifica se é um estado vencedor
            return estado_atual  # Retorna o estado vencedor

        visitados.add(estado_atual)  # Marca o estado como visitado

        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                fila.append(proximo_estado)  # Adiciona o próximo estado à fila

    return None  # Retorna None se nenhuma solução for encontrada

# Função para gerar os próximos estados possíveis (ações)
def gerar_proximos_estados(estado_atual):
    proximos_estados = []
    jogo_atual = estado_atual.jogo

    for i, galho_origem in enumerate(jogo_atual):
        if not galho_origem:
            continue  # Pula galhos vazios
        passaro = galho_origem[-1]  # Pega o último pássaro do galho
        for j, galho_destino in enumerate(jogo_atual):
            if i != j and (len(galho_destino) < 4 and (not galho_destino or galho_destino[-1] == passaro)):
                novo_jogo = [list(g) for g in jogo_atual]  # Cópia profunda do estado atual
                novo_jogo[i].pop()  # Remove o pássaro do galho de origem
                novo_jogo[j].append(passaro)  # Adiciona o pássaro ao galho de destino
                estado_novo = Estado(novo_jogo, movimento=(i, j), custo=estado_atual.custo + 1, profundidade=estado_atual.profundidade + 1)
                proximos_estados.append(estado_novo)
    return proximos_estados


import heapq

def custo_uniforme(inicio):
    """
    Implementação da busca de custo uniforme para encontrar a solução do jogo.
    """
    fila = []
    heapq.heappush(fila, inicio)  # Adiciona o estado inicial à fila de prioridade
    visitados = set()  # Conjunto para rastrear estados visitados

    while fila:
        estado_atual = heapq.heappop(fila)  # Pega o estado com menor custo

        if verificar_vitoria(estado_atual.jogo):  # Verifica se é um estado vencedor
            return estado_atual  # Retorna o estado vencedor

        visitados.add(estado_atual)  # Marca o estado como visitado

        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                heapq.heappush(fila, proximo_estado)  # Adiciona o próximo estado à fila
                visitados.add(proximo_estado)

    return None  # Retorna None se nenhuma solução for encontrada


# Busca Gulosa
def gulosa(inicio):
    """
    Implementação da busca gulosa para encontrar a solução do jogo.
    """
    fila = []
    inicio.heuristica = heuristica(inicio)  # Calcula a heurística para o estado inicial
    heapq.heappush(fila, (inicio.heuristica, inicio))  # Adiciona o estado inicial à fila com a heurística
    visitados = set()

    while fila:
        _, estado_atual = heapq.heappop(fila)  # Pega o estado com menor valor heurístico

        if verificar_vitoria(estado_atual.jogo):  # Verifica se é um estado vencedor
            return estado_atual  # Retorna o estado vencedor

        visitados.add(estado_atual)  # Marca o estado como visitado

        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                proximo_estado.heuristica = heuristica(proximo_estado)  # Calcula a heurística para o próximo estado
                heapq.heappush(fila, (proximo_estado.heuristica, proximo_estado))  # Adiciona à fila

    return None  # Retorna None se nenhuma solução for encontrada

# A* (A Estrela)
def a_star(inicio):
    """
    Implementação da busca A* para encontrar a solução do jogo.
    """
    fila = []
    inicio.heuristica = heuristica(inicio)  # Calcula a heurística para o estado inicial
    heapq.heappush(fila, (inicio.custo + inicio.heuristica, inicio))  # Adiciona o estado inicial à fila com f(n) = g(n) + h(n)
    visitados = set()

    while fila:
        _, estado_atual = heapq.heappop(fila)  # Pega o estado com menor f(n)

        if verificar_vitoria(estado_atual.jogo):  # Verifica se é um estado vencedor
            return estado_atual  # Retorna o estado vencedor

        visitados.add(estado_atual)  # Marca o estado como visitado

        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                proximo_estado.heuristica = heuristica(proximo_estado)  # Calcula a heurística para o próximo estado
                f_n = proximo_estado.custo + proximo_estado.heuristica  # Calcula f(n) = g(n) + h(n)
                heapq.heappush(fila, (f_n, proximo_estado))  # Adiciona o próximo estado à fila

    return None  # Retorna None se nenhuma solução for encontrada

def weighted_a_star(inicio, w=1.5):
    """
    Implementação da busca A* ponderada (Weighted A*) para encontrar a solução do jogo.
    :param inicio: Estado inicial do jogo.
    :param w: Peso aplicado à heurística (w >= 1).
    :return: Estado vencedor ou None se nenhuma solução for encontrada.
    """
    fila = []
    inicio.heuristica = heuristica(inicio)  # Calcula a heurística para o estado inicial
    heapq.heappush(fila, (inicio.custo + w * inicio.heuristica, inicio))  # Adiciona o estado inicial à fila com f(n) = g(n) + w * h(n)
    visitados = set()

    while fila:
        _, estado_atual = heapq.heappop(fila)  # Pega o estado com menor f(n)

        if verificar_vitoria(estado_atual.jogo):  # Verifica se é um estado vencedor
            return estado_atual  # Retorna o estado vencedor

        visitados.add(estado_atual)  # Marca o estado como visitado

        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                proximo_estado.heuristica = heuristica(proximo_estado)  # Calcula a heurística para o próximo estado
                f_n = proximo_estado.custo + w * proximo_estado.heuristica  # Calcula f(n) = g(n) + w * h(n)
                heapq.heappush(fila, (f_n, proximo_estado))  # Adiciona o próximo estado à fila

    return None  # Retorna None se nenhuma solução for encontrada

def dfs(inicio):
    """
    Implementação da busca em profundidade (DFS) para encontrar a solução do jogo.
    """
    pilha = [inicio]  # Pilha para DFS
    visitados = set()  # Conjunto para rastrear estados visitados

    while pilha:
        estado_atual = pilha.pop()  # Pega o próximo estado do topo da pilha

        if verificar_vitoria(estado_atual.jogo):  # Verifica se é um estado vencedor
            return estado_atual  # Retorna o estado vencedor

        visitados.add(estado_atual)  # Marca o estado como visitado

        for proximo_estado in gerar_proximos_estados(estado_atual):
            if proximo_estado not in visitados:
                pilha.append(proximo_estado)  # Adiciona o próximo estado à pilha

    return None  # Retorna None se nenhuma solução for encontrada

def depth_limited_search(inicio, limite):
    visitados = set()

    def dls_recursivo(estado_atual, profundidade):
        if estado_atual in visitados:
            return None

        visitados.add(estado_atual)

        if verificar_vitoria(estado_atual.jogo):
            print(f"Solução encontrada na profundidade: {estado_atual.profundidade}")
            return estado_atual

        if profundidade == 0:
            return None

        for proximo_estado in gerar_proximos_estados(estado_atual):
            resultado = dls_recursivo(proximo_estado, profundidade - 1)
            if resultado is not None:
                return resultado

        return None

    return dls_recursivo(inicio, limite)

def iterative_deepening_search(inicio, limite_maximo):
    """
    Implementação da busca em profundidade iterativa (IDS) para encontrar a solução do jogo.
    :param inicio: Estado inicial do jogo.
    :param limite_maximo: Limite máximo de profundidade para a busca.
    :return: Estado vencedor ou None se nenhuma solução for encontrada.
    """
    for limite in range(1, limite_maximo + 1):  # Incrementa o limite de profundidade
        print(f"Buscando com limite de profundidade: {limite}")
        solucao = depth_limited_search(inicio, limite)  # Chama a busca limitada em profundidade
        if solucao is not None:
            return solucao  # Retorna a solução encontrada
    return None  # Retorna None se nenhuma solução for encontrada dentro do limite máximo

def obter_dados_do_estado_inicial(estado_inicial):
    """
    Determina o número de cores e o número de pássaros por cor no estado inicial.
    """
    contador_cores = {}  # Dicionário para contar o número de pássaros por cor

    for galho in estado_inicial:
        for passaro in galho:
            if passaro not in contador_cores:
                contador_cores[passaro] = 0
            contador_cores[passaro] += 1

    num_cores = len(contador_cores)  # Número de cores distintas
    passaros_por_cor = list(contador_cores.values())[0] if contador_cores else 0  # Número de pássaros por cor (assume que todas as cores têm o mesmo número de pássaros)

    return num_cores, passaros_por_cor


