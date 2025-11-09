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

Isso permite que o A* explore caminhos que *parecem* promissores (baixo h-score) sem se afastar muito de um caminho que já se provou eficiente (baixo g-score).

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

`Custo de Movimento (get_neighbors)`: O custo para se mover para uma célula vizinha. É 1 para movimentos retos e sqrt(2) para diagonais.

`Custo de Terreno (get_terrain_cost)`: O custo intrínseco de entrar numa célula. Células 'S', 'E' e '0' têm custo 1 (terreno normal). Outros números (como 5 no exemplo) representam terreno difícil.

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

