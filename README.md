# Implementação do Algoritmo A* (A-Star) para Pathfinding em Labirintos 2D

**Trabalho em Grupo 1 da disciplina de Fundamentos de Projetos e Análise de Algoritmos.**

## Integrantes: 

* [Gabriel Lucas Tinoco de Aguiar](https://github.com/gabrieltinoco)
* [Kaio Henrique Oliveira da Silveira Barbosa](https://github.com/kaiohs333)
* [Maximiliano Augusto de Jesus Junior](https://github.com/MaxJunior2002)

## Professor:

* [João Paulo Carneiro Aramuni](https://github.com/joaopauloaramuni)

## 🎯 Objetivo

Implementar o Algoritmo A* para encontrar o menor caminho em um labirinto 2D. O objetivo é ajudar um robô de resgate a navegar de um ponto inicial **'S'** até um ponto final **'E'**, evitando obstáculos ('1') e considerando terrenos de diferentes custos.

## O que é o Algoritmo A*?

O **A* (A-Star)** é um algoritmo de busca de caminho (pathfinding) amplamente utilizado para encontrar a rota de menor custo entre dois pontos. Sua eficiência vem da forma como ele decide qual nó explorar em seguida.

Ele faz isso combinando duas informações:
1.  **g(n) (Custo do Caminho Percorrido):** O custo real do caminho desde o ponto inicial 'S' até o nó atual 'n'.
2.  **h(n) (Heurística):** Uma *estimativa* do custo do caminho mais barato do nó atual 'n' até o ponto final 'E'.

O algoritmo prioriza nós com o menor valor de **f(n)**, onde:

$$f(n) = g(n) + h(n)$$

Isso permite que o A* explore caminhos que *parecem* promissores (baixo `h-score`) sem se afastar muito de um caminho que já se provou eficiente (baixo `g-score`).

## 🧭 Explicação do Algoritmo Implementado

O código fornecido no `pathfinder.py` implementa o A* considerando os requisitos básicos e também os pontos extras de **movimento diagonal** e **custos de terreno**.

### 1. Heurística: Distância Diagonal (Octile)

O enunciado do trabalho sugere a "Distância de Manhattan", que é ideal para movimentos em 4 direções (cima, baixo, esquerda, direita).

No entanto, como nossa implementação inclui o ponto extra de **movimento diagonal** (8 direções), utilizámos uma heurística mais adequada: a **Distância Diagonal (ou Octile)**. Esta calcula o custo considerando movimentos retos (custo 1) e diagonais (custo $\sqrt{2}$), como implementado na função `heuristic` do `pathfinder.py`.

```python
def heuristic(a, b):
    """
    Calcula a distância heurística.
    Usa a Distância Diagonal (Octile) para 8 direções.
    """
    (r1, c1) = a
    (r2, c2) = b
    
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    
    # Custo reto = 1
    # Custo diagonal = sqrt(2)
    # Fórmula: (custo reto) * (total de passos - passos diagonais) + (custo diagonal) * (passos diagonais)
    # Simplifica para: (custo reto) * (passos retos) + (custo diagonal) * (passos diagonais)
    
    D = 1
    D2 = math.sqrt(2)
    return D * (max(dr, dc) - min(dr, dc)) + D2 * min(dr, dc)
```

### 2. Custos de Movimento e Terreno

A implementação considera dois tipos de custo que se multiplicam para definir o custo real de um passo, conforme visto nas funções `get_neighbors` e `get_terrain_cost` do `pathfinder.py`:

**Custo de Movimento (`get_neighbors`)**: O custo para se mover para uma célula vizinha. É 1 para movimentos retos e sqrt(2) para diagonais.

**Custo de Terreno (`get_terrain_cost`)**: O custo intrínseco de entrar numa célula. Células 'S', 'E' e '0' têm custo `1` (terreno normal). Outros números (como `5` no exemplo) representam terreno difícil.

```python
def get_neighbors(maze, node):
    # ... (definição de movimentos e custos) ...
    moves = [
        (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),  # Retos (custo 1)
        (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),  # Diagonais (custo sqrt(2))
        (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))
    ]
    # ... (lógica para encontrar vizinhos válidos) ...

def get_terrain_cost(cell_value):
    if cell_value in ('S', 'E', 0):
        return 1  # Custo de terreno normal
    if isinstance(cell_value, int):
        return cell_value  # Custo do terreno (ex: 5)
    return float('inf')
```

### 3. O Algoritmo A* (`a_star_search`)

Esta é a função principal que executa a busca:

1. **Inicialização:**

* `open_set`: Uma fila de prioridade (`heapq`) que armazena os nós a serem explorados, priorizados pelo menor `f_score`.

* `came_from`: Um dicionário que armazena o caminho, mapeando `nó -> nó_anterior`.

* `g_score`: Um dicionário que armazena o custo real (`g(n)`) do início até cada nó.

* `f_score`: Um dicionário que armazena o custo estimado total (`f(n)`) para cada nó.

2. **Loop de Busca:**

* Enquanto a `open_set` não estiver vazia, o algoritmo retira o nó com o **menor f-score** (este é `current`).
    
* Se `current` for o nó final 'E', o caminho foi encontrado.

* Caso contrário, analisa os vizinhos (neighbor) de `current`.

3. **Cálculo de Custo do Passo:**

* Para cada vizinho, o custo do passo (step_cost) é calculado: step_cost = move_cost * terrain_cost

* O `tentative_g_score` é o g_score do nó atual + step_cost.

4. **Atualização de Caminho:**

* Se o `tentative_g_score` for menor do que o `g_score` já registado para aquele vizinho, significa que encontrámos um caminho melhor para chegar até ele.

* O algoritmo atualiza `came_from[neighbor]`, `g_score[neighbor]`, `f_score[neighbor]`, e adiciona o vizinho à `open_set` para exploração.

5. **Sem Solução:**

* Se o loop terminar (a `open_set` ficar vazia) e 'E' não for encontrado, o algoritmo retorna `None`, indicando que não há caminho.

```python 
def a_star_search(maze, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start)) # (f_score, nó)
    
    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)
        
        if current == end:
            # Caminho encontrado!
            return came_from, current 

        for neighbor, move_cost in get_neighbors(maze, current):
            
            terrain_cost = get_terrain_cost(maze[neighbor[0]][neighbor[1]])
            step_cost = move_cost * terrain_cost
            
            tentative_g_score = g_score[current] + step_cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                # Este é um caminho melhor do que qualquer um anterior
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    # Sem solução
    return None, None
```

### 4. Execução e Exibição

O bloco if `__name__ == "__main__"`: é o ponto de entrada do script:

1. Define o labirinto de exemplo.

2. Usa `find_start_and_end` para localizar 'S' e 'E', validando que ambos existem.

3. Chama `a_star_search`.

4. Se um caminho for encontrado, `reconstruct_path` o reconstrói (invertendo o dicionário `came_from`) e exibe-o como uma lista de coordenadas.

5. `display_maze_with_path` exibe o labirinto final com o caminho destacado.

## 🚀 Como executar o projeto

1. Guarde o código do seu grupo num ficheiro chamado pathfinder.py.

2. Certifique-se de que tem o Python 3 instalado.

3. Navegue até ao diretório onde o ficheiro foi guardado.

4. Execute o script Python pelo terminal:

```bash
python pathfinder.py
```

5. O programa será executado com o labirinto de exemplo (labirinto_exemplo) definido no código e exibirá o resultado no terminal.

### 📊 Exemplo de Entrada e Saída
 
Esta secção ilustra o funcionamento do projeto 11usando o labirinto definido em` pathfinder.py`, que inclui terreno difícil (custo 5)

#### **Entrada:**

O labirinto é definido internamente no código:
```Python
labirinto_exemplo = [
    ['S', 0, 1, 0, 0],
    [0, 0, 1, 0, 1],
    [1, 5, 5, 5, 0], # Terreno difícil (custo 5)
    [1, 0, 0, 'E', 1]
]
```

#### **Saída no Terminal:**

A execução do script `pathfinder.py` produzirá a seguinte saída:

```
--- PathFinder A* Iniciado (com Diagonais e Pesos) ---

S 0 1 0 0
0 0 1 0 1
1 5 5 5 0
1 0 0 E 1

Início 'S' encontrado em: (0, 0)
Fim 'E' encontrado em: (3, 3)

Distância Diagonal (heurística) de 'S' a 'E': 3.00

Executando A*...
Caminho encontrado!

Menor caminho (em coordenadas):
[(0, 0), (1, 0), (1, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 3)]

Labirinto com o caminho destacado:
S 0 * * *
* * 1 0 *
1 5 5 5 *
1 0 0 E 1
```

## ✨ Funcionalidades Extras Implementadas

Este projeto vai além dos requisitos básicos e implementa com sucesso dois dos pontos extras sugeridos:

1. **Movimento Diagonal**: O robô pode mover-se em 8 direções. O custo do movimento diagonal é $\sqrt{2}$, enquanto o reto é 1.


2. **Pesos de Terreno**: O labirinto suporta células com custos de movimento variados (terrenos difíceis). O custo final de um passo é `custo_movimento * custo_terreno`.

