import time
from search import dfs, Estado

def medir_tempo_dfs(estado_inicial):
    """
    Measure the time it takes to solve the game 10 times using DFS.
    """
    total_time = 0

    print("Iniciando o teste de desempenho do DFS...")

    for i in range(10):  # Run DFS 10 times
        start_time = time.time()  # Record the start time
        solucao = dfs(estado_inicial)  # Solve the game using DFS
        end_time = time.time()  # Record the end time

        if solucao:
            print(f"Solução encontrada na execução {i + 1}")
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

# Measure DFS execution time
medir_tempo_dfs(estado_inicial)