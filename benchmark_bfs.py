import time
from search import bfs, Estado  # Ensure bfs and Estado are correctly imported from search.py

def medir_tempo_bfs(estado_inicial):
    """
    Measure the time it takes to solve the game 10 times using BFS.
    This function runs independently of the game loop.
    """
    total_time = 0

    print("Iniciando o teste de desempenho do BFS...")

    for i in range(10):  # Run BFS 10 times
        start_time = time.time()  # Record the start time
        solucao = bfs(estado_inicial)  # Solve the game using BFS
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

# Measure BFS execution time
medir_tempo_bfs(estado_inicial)