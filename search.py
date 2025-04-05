from collections import deque

# Definir um estado de jogo
class Estado:
    def __init__(self, jogo, movimento=None, custo=0):
        self.jogo = jogo
        self.movimento = movimento
        self.custo = custo

    def __eq__(self, other):
        return self.jogo == other.jogo

    def __hash__(self):
        return hash(str(self.jogo))

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
    """
    Gera todos os estados possíveis a partir do estado atual,
    movendo o último pássaro de um galho para outro.
    """
    proximos_estados = []
    jogo_atual = estado_atual.jogo  # Estado atual do jogo

    for i, galho_origem in enumerate(jogo_atual):
        if not galho_origem:
            continue  # Pula galhos vazios

        passaro = galho_origem[-1]  # Pega o último pássaro do galho de origem

        for j, galho_destino in enumerate(jogo_atual):
            if i != j:  # Não pode mover para o mesmo galho
                # Verifica se o movimento é válido
                if len(galho_destino) < 4 and (not galho_destino or galho_destino[-1] == passaro):
                    # Cria uma cópia do estado atual
                    novo_jogo = [list(g) for g in jogo_atual]
                    # Move o pássaro
                    novo_jogo[i].pop()  # Remove o pássaro do galho de origem
                    novo_jogo[j].append(passaro)  # Adiciona o pássaro ao galho de destino

                    # Cria um novo estado com o movimento realizado
                    estado_novo = Estado(novo_jogo, movimento=(i, j), custo=estado_atual.custo + 1)
                    proximos_estados.append(estado_novo)

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


