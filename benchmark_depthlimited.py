import time
from search import depth_limited_search, Estado

def medir_tempo_depth_limited(estado_inicial, limite):
    """
    Measure the time it takes to solve the game 10 times using Depth-Limited Search.
    """
    total_time = 0

    print(f"Iniciando o teste de desempenho da Busca Limitada em Profundidade com limite {limite}...")

    for i in range(10):  # Run Depth-Limited Search 10 times
        start_time = time.time()  # Record the start time
        solucao = depth_limited_search(estado_inicial, limite)  # Solve the game using Depth-Limited Search
        end_time = time.time()  # Record the end time

        if solucao:
            print(f"Solução encontrada na execução {i + 1}")
            print("Estado final:")
            for galho in solucao.jogo:
                print(galho)  # Print the final solution state
        else:
            print(f"Não foi possível resolver o jogo na execução {i + 1}")

        execution_time = end_time - start_time
        total_time += execution_time
        print(f"Tempo para a execução {i + 1}: {execution_time:.4f} segundos")

    average_time = total_time / 10
    print(f"Tempo total para 10 execuções: {total_time:.4f} segundos")
    print(f"Tempo médio por execução: {average_time:.4f} segundos")

# Define the initial game state
estado_inicial = Estado([
    ["vermelho", "marrom", "azul", "verde"],
    ["azul", "verde", "marrom", "vermelho"],
    ["vermelho", "verde", "amarelo"],
    ["azul", "amarelo", "marrom"],
    ["amarelo"],
    []
])

# Define the depth limit
limite = 15  # Increase the depth limit

# Measure Depth-Limited Search execution time
medir_tempo_depth_limited(estado_inicial, limite)