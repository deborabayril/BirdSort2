# Solucionador do Bird Sort

Este projeto implementa diversos algoritmos de busca para resolver o jogo **Bird Sort**. Os algoritmos disponíveis incluem:
- **Busca em Largura (BFS)**;
- **Busca Limitada em Profundidade (DLS)**;
- **Busca em Profundidade Iterativa (IDS)**;
- **Busca Gulosa**;
- **Busca A***;
- **Busca A* Ponderada (Weighted A*)**.

O programa também permite realizar benchmarks para comparar o desempenho dos algoritmos com diferentes heurísticas.

---

## Pré-requisitos

Para executar este programa, você precisará de:
- **Python 3.8+** instalado no seu sistema.
- As bibliotecas padrão do Python, como `time` e `heapq`.

---

## Estrutura de Arquivos

- `search.py`: Contém a implementação dos algoritmos de busca e das heurísticas.
- `benchmark_bfs.py`: Realiza benchmarks para o algoritmo BFS.
- `benchmark_depthlimited.py`: Realiza benchmarks para a Busca Limitada em Profundidade.
- `benchmark_iterdeep.py`: Realiza benchmarks para a Busca em Profundidade Iterativa.
- `benchmark_greedy.py`: Realiza benchmarks para a Busca Gulosa.
- `benchmark_astar.py`: Realiza benchmarks para a Busca A*.
- `benchmark_weightastar.py`: Realiza benchmarks para a Busca A* Ponderada.

---

## Como Compilar e Executar

### 1. Clone o Repositório
Clone o projeto para sua máquina local:
```bash
git clone <url-do-repositorio>
cd BirdSortSolver
```

### 2. Instale as Dependências
Certifique-se de que todas as bibliotecas necessárias estão instaladas:
```bash
pip install -r requirements.txt
```

If no `requirements.txt` file exists, list the libraries explicitly:
```bash
pip install time heapq
```

### 3. Execute os Scripts de Benchmark
Para executar os benchmarks, use os seguintes comandos:

- **Busca em Largura (BFS)**:
  ```bash
  python benchmark_bfs.py
  ```

### 4. Personalize o Estado Inicial
O estado inicial do jogo pode ser alterado diretamente nos scripts de benchmark. Por exemplo, no arquivo `benchmark_astar.py`:

```python
estado_inicial = Estado([
    ["vermelho", "marrom", "azul", "verde"],
    ["azul", "verde", "marrom", "vermelho"],
    ["vermelho", "verde", "amarelo"],
    ["azul", "amarelo", "marrom"],
    ["amarelo"],
    []
])
```

Substitua as cores e a configuração dos galhos conforme necessário.

### 5. Escolha o Algoritmo e a Heurística
Cada script de benchmark é projetado para testar um algoritmo específico. Por exemplo:
- `benchmark_greedy.py` testa o algoritmo de Busca Gulosa.
- `benchmark_astar.py` testa o algoritmo de Busca A* com diferentes heurísticas.

No caso do Weighted A*, você pode ajustar o peso:
```python
w = 1.5  # Ajuste o peso conforme necessário
```

E também alternar entre as heurísticas:
```python
medir_tempo_weighted_a_star(estado_inicial, w, heuristica)
medir_tempo_weighted_a_star(estado_inicial, w, heuristica_jogadas_restantes)
```

### 6. Solução de Problemas

#### Problema: O programa não encontra uma solução
- Certifique-se de que o estado inicial é solucionável.
- Verifique se o limite de profundidade (para IDS ou DLS) é suficiente.

#### Problema: Erro de biblioteca ausente
- Instale as bibliotecas necessárias com:
  ```bash
  pip install time heapq
  ```

#### Problema: O programa entra em loop infinito
- Verifique a implementação das funções `verificar_vitoria` e `gerar_proximos_estados` no arquivo `search.py`.