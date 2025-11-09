import heapq


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
    """ Calcula a distância de Manhattan entre dois pontos (r1, c1) e (r2, c2).
    h(n) = |x_atual - x_final| + |y_atual - y_final|
    
    Argumentos:
        a (tuple): O primeiro ponto (linha1, coluna1).
        b (tuple): O segundo ponto (linha2, coluna2).
        
    Retorna:
        int: A distância de Manhattan. """
        
    (r1, c1) = a
    (r2, c2) = b
    return abs(r1 - r2) + abs(c1 - c2)

#-- Implementação do algoritimo A* --
def get_neighbors(maze, node):
    """ Econtra os vizinhos validos (cima, baixo, esquerda, direita) de um nó.
    
    Argumentos:
        maze (list[list]): A matriz 2D do labirinto.
        node (tuple): O nó atual (linha, coluna).
        
        Retorna:
            list: Uma lista de nós vizinhos válidos (linha, coluna). """
            
    neighbors = []
    (r, c) = node
    num_rows = len(maze)
    num_cols = len(maze[0])
    
    # movimentos possiveis
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita
    
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        # Verifica se o vizinho está dentro dos limites
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            # Verifica se o vizinho não é uma parede (1)
            if maze[nr][nc] != 1:
                neighbors.append((nr, nc))
    
    return neighbors

def a_star_search(maze, start, end):
    """ Executa o algoritimo A* para encontrar o menor caminho do ponto start ao ponto end.
    
    Argumentos:
        maze (list[list]): A matriz 2D do labirinto.
        start (tuple): O ponto inicial (linha, coluna).
        end (tuple): O ponto final (linha, coluna).
        
        Retorna: 
        dict: o dicionario 'come-from' que reconstroi o caminho, ou None se não houver caminho."""
    
    # fila de prioridade (open_set): armazena (f_score, node)
    # heapq faz com que sempre o nó com menor f_score seja extraído primeiro
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}  # dicionario para reconstruir o caminho
    
    #g_score: custo do caminho do start até o node atual
    g_score = {start: 0}
    # os outros nodes sao inicialmente infinitos
    
    # f_score é o custo total estimado (g_score + heuristica)
    f_score = {start: heuristic(start, end)}
    
    #setamos os nodes da fila de prioridade
    open_set_hash = {start}
    
    while open_set:
        # Pega o nó na fila de prioridade com o menor f_score
        current = heapq.heappop(open_set)[1] # Pegamos o [1] pois o [0] é o f_score
        open_set_hash.remove(current)
        
        # Verifica se chegamos ao fim
        if current == end:
            print("Caminho encontrado!")
            return came_from, current

        # Explora os vizinhos
        for neighbor in get_neighbors(maze, current):
            # custo do move é 1
            tentative_g_score = g_score[current] + 1
            
            # Se este caminho para o vizinho é melhor do que qualquer outro já visto
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                # Atualiza o caminho e os scores
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                # Se o vizinho não está na fila, adiciona
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    # Se o loop terminar e não encontramos o fim
    print("Sem solução: Não foi possível encontrar um caminho.")
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
    
    # A "Entrada" é esta matriz
    labirinto_exemplo = [
        ['S', 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0],
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