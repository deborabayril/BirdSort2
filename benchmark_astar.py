import time
from search import a_star, Estado, heuristica, heuristica_jogadas_restantes

def medir_tempo_a_star(estado_inicial, heuristica_func):
    """
    Measure the time it takes to solve the game 10 times using A* Search with a specified heuristic.
    """
    total_time = 0

    print(f"Iniciando o teste de desempenho da Busca A* com a heurística: {heuristica_func.__name__}...")

    for i in range(10):  # Run A* Search 10 times
        start_time = time.time()  # Record the start time
        solucao = a_star(estado_inicial, heuristica_func=heuristica_func)  # Solve the game using A* Search
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

# Measure A* Search execution time with the default heuristic
#medir_tempo_a_star(estado_inicial, heuristica)

# Measure A* Search execution time with the "jogadas restantes" heuristic
medir_tempo_a_star(estado_inicial, heuristica_jogadas_restantes)