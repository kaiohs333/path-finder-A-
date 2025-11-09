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
