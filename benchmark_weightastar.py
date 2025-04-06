import time
from search import weighted_a_star, Estado

def medir_tempo_weighted_a_star(estado_inicial, w):
    """
    Measure the time it takes to solve the game 10 times using Weighted A* Search.
    """
    total_time = 0

    print(f"Iniciando o teste de desempenho da Busca A* Ponderada com peso {w}...")

    for i in range(10):  # Run Weighted A* Search 10 times
        start_time = time.time()  # Record the start time
        solucao = weighted_a_star(estado_inicial, w)  # Solve the game using Weighted A* Search
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

# Define the weight factor
w = 9  # Adjust the weight factor as needed

# Measure Weighted A* Search execution time
medir_tempo_weighted_a_star(estado_inicial, w)