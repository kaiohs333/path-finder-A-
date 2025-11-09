import heapq
import math

def find_start_and_end(maze):
    """
    Encontra as coordenadas (linha, coluna) dos pontos de início 'S' e fim 'E'.
    
    Argumentos:
        maze (list[list]): A matriz 2D do labirinto.

    Retorna:
        tuple: (start, end) onde start e end são tuplas (linha, coluna)
               Retorna (None, None) se 'S' ou 'E' não forem encontrados.
    """
    start = None
    end = None
    
    # Itera por cada célula da matriz
    for r_idx, row in enumerate(maze):
        for c_idx, cell in enumerate(row):
            if cell == 'S':
                start = (r_idx, c_idx)
            elif cell == 'E':
                end = (r_idx, c_idx)
            
            if start and end:
                return start, end
                
    return start, end

#-- Definição da heuristica --
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

#-- Implementação do algoritimo A* --
def get_neighbors(maze, node):
    """
    Encontra vizinhos válidos (8 direções) de um nó e o custo do MOVIMENTO.
    
    Retorna:
        list: Uma lista de tuplas (vizinho, custo_movimento)
              onde vizinho é (linha, coluna) e custo_movimento é 1 ou sqrt(2).
    """
    neighbors = []
    (r, c) = node
    num_rows = len(maze)
    num_cols = len(maze[0])
    
    # Movimentos possíveis (reto, diagonal) e seus custos
    # (dr, dc, custo_movimento)
    moves = [
        (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),  # Retos
        (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),  # Diagonais
        (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))
    ]
    
    for dr, dc, move_cost in moves:
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            if maze[nr][nc] != 1:  # 1 ainda é o único obstáculo
                neighbors.append(((nr, nc), move_cost))
                
    return neighbors

def get_terrain_cost(cell_value):
    """
    Retorna o custo de um terreno com base no valor da célula.
    'S', 'E' e 0 (livre) têm custo 1 (terreno normal).
    Outros números (ex: 5) são terrenos difíceis.
    """
    if cell_value in ('S', 'E', 0):
        return 1  # Custo de terreno normal
    if isinstance(cell_value, int):
        return cell_value  # Custo do terreno (ex: 5)
    return float('inf') # Caso inesperado



def a_star_search(maze, start, end):
    """
    Executa o algoritmo A* para encontrar o menor caminho.
    """
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
            # Caminho encontrado! Retorna os dados para reconstrução
            return came_from, current 

        # iteramos sobre vizinhos E o custo do movimento
        for neighbor, move_cost in get_neighbors(maze, current):
            
            # Pega o custo do terreno do vizinho
            terrain_cost = get_terrain_cost(maze[neighbor[0]][neighbor[1]])
            
            # O custo total do passo é o custo do movimento * peso do terreno
            # (Se o terreno for 5 e o movimento for diagonal, o custo é 5 * sqrt(2))
            step_cost = move_cost * terrain_cost
            
            tentative_g_score = g_score[current] + step_cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    # Sem solução
    return None, None

# Exibição dos resultados
def reconstruct_path(came_from, current):
    """
    Reconstrói o caminho do fim para o início usando o dicionário came_from.
    
    Argumentos:
        came_from (dict): Dicionário {nó: nó_anterior}
        current (tuple): O nó final ('E')
        
    Retorna:
        list: A lista de coordenadas [(linha, coluna), ...] do início ao fim.
    """
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
        if current is None: # Chegamos ao início
            break
            
    # O caminho está de trás para frente (Fim -> Início), então invertemos
    return path[::-1]

def display_maze_with_path(maze, path, start, end):
    """
    Exibe o labirinto com o caminho destacado ('*').
    
    Argumentos:
        maze (list[list]): O labirinto original.
        path (list): A lista de coordenadas do caminho.
        start (tuple): Coordenadas de 'S'.
        end (tuple): Coordenadas de 'E'.
    """
    # Cria uma cópia do labirinto para não modificar o original
    # Converte tudo para string para facilitar a impressão
    display_maze = [list(map(str, row)) for row in maze]
    
    # Itera pelo caminho e marca com '*'
    for (r, c) in path:
        # Não sobrescreve 'S' e 'E'
        if (r, c) != start and (r, c) != end:
            display_maze[r][c] = '*'
            
    print("\nLabirinto com o caminho destacado:")
    for row in display_maze:
        print(" ".join(row))

# --- Execução Principal (para testar a Etapa 1) ---
if __name__ == "__main__":
    
    #Labirinto com terreno difícil (5)
    labirinto_exemplo = [
        ['S', 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 5, 5, 5, 0], # Terreno difícil (custo 5)
        [1, 0, 0, 'E', 1]
    ]

    print("--- PathFinder A* ---")
    print("Labirinto de Entrada:")
    for row in labirinto_exemplo:
        print(" ".join(map(str, row)))
    
    # 1. Executa a leitura do labirinto e encontra 'S' e 'E'
    start_node, end_node = find_start_and_end(labirinto_exemplo)

    if not start_node or not end_node:
        print("\nErro: Ponto inicial 'S' ou final 'E' não encontrado.")
    else:
        print(f"\nInício 'S' encontrado em: {start_node}")
        print(f"Fim 'E' encontrado em: {end_node}")
        
    # 2. Testando a heurística
    print("\nPath Finder A* - Testando a Heurística de Manhattan")
    distanciaEstimada = heuristic(start_node, end_node)
    print(f"Distância estimada (heurística) entre 'S' e 'E': {distanciaEstimada}")
    
    # Teste com outros pontos
    ponto1 = (1,5)
    ponto2 = (3,7)
    distanciaTeste = heuristic(ponto1, ponto2)
    print(f"Distancia de Manhattan entre {ponto1} e {ponto2}: {distanciaTeste}")
    
    # 3. Testando o algoritmo A*
    print("\nPath Finder A* - Testando o Algoritmo A*")
    print("Executando A*...")
    
    path_data, end_point = a_star_search(labirinto_exemplo, start_node, end_node)
    
    if path_data:
        print("Resultado do A*: Sucesso!!")
    else: print("Resultado do A*: Falha :(")
    
    # 4. Executa a Tarefa 4 (NOVO)
    if path_data:
        print("Caminho encontrado!")
            
        # Reconstrói e exibe a lista de coordenadas
        caminho_final = reconstruct_path(path_data, end_point)
        print("\nMenor caminho (em coordenadas):")
        print(caminho_final)
            
        # Exibe o labirinto destacado
        display_maze_with_path(labirinto_exemplo, caminho_final, start_node, end_node)
    else:
        print(f"\nSem solução: Não foi possível encontrar um caminho de 'S' para 'E'.")   