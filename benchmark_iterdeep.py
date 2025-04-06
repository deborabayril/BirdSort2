import time
from search import iterative_deepening_search, Estado

def medir_tempo_iterative_deepening(estado_inicial, limite_maximo):
    """
    Measure the time it takes to solve the game 3 times using Iterative Deepening Search.
    """
    total_time = 0

    print(f"Iniciando o teste de desempenho da Busca em Profundidade Iterativa com limite máximo {limite_maximo}...")

    for i in range(10):  # Run Iterative Deepening Search 3 times
        start_time = time.time()  # Record the start time
        solucao = iterative_deepening_search(estado_inicial, limite_maximo)  # Solve the game using IDS
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

    average_time = total_time / 3
    print(f"Tempo total para 3 execuções: {total_time:.4f} segundos")
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

# Define the maximum depth limit
limite_maximo = 15  # Reduce the depth limit for testing

# Measure Iterative Deepening Search execution time
medir_tempo_iterative_deepening(estado_inicial, limite_maximo)