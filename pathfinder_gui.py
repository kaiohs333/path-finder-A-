import pygame
import heapq
import math
import sys
import time # Para medir o tempo de execução

# --- Constantes do Pygame ---
# Cores (R, G, B)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (200, 200, 200)
VERMELHO = (255, 0, 0)     # Obstáculo (1)
VERDE = (0, 255, 0)       # Ponto Final (E)
AZUL = (0, 0, 255)        # Ponto Inicial (S)
LARANJA = (255, 165, 0)   # Caminho Final (*)
TURQUESA = (64, 224, 208) # Nós no Open Set (explorando)
CINZA_ESCURO = (100, 100, 100) # Nós no Closed Set (já explorado)
MARROM = (139, 69, 19)    # Terreno Difícil (5)
AMARELO = (255, 255, 0)  # Cor para texto

# Tamanho de cada célula do grid em pixels
TAMANHO_CELULA = 40 # Aumentado para melhor visualização
MARGEM = 1 # Margem entre as células
PAINEL_LARGURA = 250 # Largura do painel lateral de informações

# --- Funções do A* (do pathfinder.py) ---
# (Mantidas as mesmas do último commit, corrigido o bug do closed_set)

def find_start_and_end(maze):
    start = None
    end = None
    for r_idx, row in enumerate(maze):
        for c_idx, cell in enumerate(row):
            if cell == 'S':
                start = (r_idx, c_idx)
            elif cell == 'E':
                end = (r_idx, c_idx)
            if start and end:
                return start, end
    return start, end

def heuristic(a, b):
    (r1, c1) = a
    (r2, c2) = b
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    D = 1
    D2 = math.sqrt(2)
    return D * (max(dr, dc) - min(dr, dc)) + D2 * min(dr, dc)

def get_neighbors(maze, node):
    neighbors = []
    (r, c) = node
    num_rows = len(maze)
    num_cols = len(maze[0])
    moves = [
        (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),
        (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
        (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))
    ]
    for dr, dc, move_cost in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < num_rows and 0 <= nc < num_cols:
            if maze[nr][nc] != 1:
                neighbors.append(((nr, nc), move_cost))
    return neighbors

def get_terrain_cost(cell_value):
    if cell_value in ('S', 'E', 0):
        return 1
    if isinstance(cell_value, int):
        return cell_value
    return float('inf')

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
        if current is None:
            break
    return path[::-1]

# --- Função A* como Gerador (Generator) ---
# Retorna mais informações para a GUI
def a_star_search_realtime(maze, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    open_set_hash = {start}
    closed_set_hash = set()
    
    # Adicionando contadores para estatísticas
    nodes_visited_count = 0
    current_node_f = 0
    current_node_g = 0
    
    while open_set:
        # Atualiza informações do nó atual para exibição
        current_f, current = open_set[0] # Pega o próximo a ser processado (sem tirar da heap)
        current_node_f = f_score.get(current, float('inf'))
        current_node_g = g_score.get(current, float('inf'))

        yield {
            "open_set": open_set_hash,
            "closed_set": closed_set_hash,
            "nodes_visited": nodes_visited_count,
            "open_set_size": len(open_set),
            "current_f_score": current_node_f,
            "current_g_score": current_node_g,
            "path": None # Por enquanto o caminho final é None
        }
        
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)
        closed_set_hash.add(current)
        nodes_visited_count += 1
        
        if current == end:
            path = reconstruct_path(came_from, current)
            yield {
                "open_set": open_set_hash,
                "closed_set": closed_set_hash,
                "nodes_visited": nodes_visited_count,
                "open_set_size": len(open_set),
                "current_f_score": f_score.get(current, float('inf')),
                "current_g_score": g_score.get(current, float('inf')),
                "path": path # Caminho final
            }
            return

        for neighbor, move_cost in get_neighbors(maze, current):
            terrain_cost = get_terrain_cost(maze[neighbor[0]][neighbor[1]])
            step_cost = move_cost * terrain_cost
            tentative_g_score = g_score[current] + step_cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    yield {"path": None, "nodes_visited": nodes_visited_count, "open_set_size": len(open_set)}
    return

# --- Funções de Desenho do Pygame ---

def get_color_for_cell(cell_value):
    if cell_value == 'S':
        return AZUL
    if cell_value == 'E':
        return VERDE
    if cell_value == 1:
        return VERMELHO
    if cell_value == 5:
        return MARROM
    return BRANCO

def draw_grid(screen, maze, offset_x=0, offset_y=0):
    num_rows = len(maze)
    num_cols = len(maze[0])
    
    for r in range(num_rows):
        for c in range(num_cols):
            color = get_color_for_cell(maze[r][c])
            pygame.draw.rect(screen, color,
                             [(MARGEM + TAMANHO_CELULA) * c + MARGEM + offset_x,
                              (MARGEM + TAMANHO_CELULA) * r + MARGEM + offset_y,
                              TAMANHO_CELULA,
                              TAMANHO_CELULA])
            # (NOVO) Desenhar texto da célula se for 0 ou 5
            if maze[r][c] in (0, 5):
                font = pygame.font.SysFont("Arial", 12)
                text_surface = font.render(str(maze[r][c]), True, PRETO)
                text_rect = text_surface.get_rect(center=((MARGEM + TAMANHO_CELULA) * c + MARGEM + offset_x + TAMANHO_CELULA // 2,
                                                          (MARGEM + TAMANHO_CELULA) * r + MARGEM + offset_y + TAMANHO_CELULA // 2))
                screen.blit(text_surface, text_rect)


def draw_state(screen, state_data, start, end, offset_x=0, offset_y=0):
    if "closed_set" in state_data:
        for (r, c) in state_data["closed_set"]:
            if (r, c) != start and (r, c) != end:
                pygame.draw.rect(screen, CINZA_ESCURO,
                                 [(MARGEM + TAMANHO_CELULA) * c + MARGEM + offset_x,
                                  (MARGEM + TAMANHO_CELULA) * r + MARGEM + offset_y,
                                  TAMANHO_CELULA,
                                  TAMANHO_CELULA])

    if "open_set" in state_data:
        for (r, c) in state_data["open_set"]:
            if (r, c) != start:
                pygame.draw.rect(screen, TURQUESA,
                                 [(MARGEM + TAMANHO_CELULA) * c + MARGEM + offset_x,
                                  (MARGEM + TAMANHO_CELULA) * r + MARGEM + offset_y,
                                  TAMANHO_CELULA,
                                  TAMANHO_CELULA])

def draw_final_path(screen, path, start, end, offset_x=0, offset_y=0):
    for (r, c) in path:
        if (r, c) != start and (r, c) != end:
            pygame.draw.rect(screen, LARANJA,
                             [(MARGEM + TAMANHO_CELULA) * c + MARGEM + offset_x,
                              (MARGEM + TAMANHO_CELULA) * r + MARGEM + offset_y,
                              TAMANHO_CELULA,
                              TAMANHO_CELULA])

def draw_info_panel(screen, maze, state_data, start_time, total_time, final_path, font):
    """Desenha o painel lateral com informações."""
    
    # Posição inicial do painel
    panel_x = (len(maze[0]) * (TAMANHO_CELULA + MARGEM) + MARGEM) + 10 # 10 pixels de margem
    y_offset = 10
    
    # Título
    title_surface = font.render("A* PathFinder Info", True, AMARELO)
    screen.blit(title_surface, (panel_x, y_offset))
    y_offset += 30

    # Labirinto (visualização textual)
    maze_text_title = font.render("Maze Matrix:", True, BRANCO)
    screen.blit(maze_text_title, (panel_x, y_offset))
    y_offset += 20
    
    for row in maze:
        row_str = " ".join(map(str, row))
        row_surface = font.render(row_str, True, CINZA)
        screen.blit(row_surface, (panel_x, y_offset))
        y_offset += 18
    y_offset += 10
    
    # Tempo de Execução
    if final_path:
        time_str = f"Time: {total_time:.4f}s"
    else:
        time_str = f"Time: {time.time() - start_time:.4f}s (running)"
    time_surface = font.render(time_str, True, BRANCO)
    screen.blit(time_surface, (panel_x, y_offset))
    y_offset += 30
    
    # Nós Visitados
    nodes_visited_str = f"Nodes Visited: {state_data.get('nodes_visited', 0)}"
    nodes_visited_surface = font.render(nodes_visited_str, True, BRANCO)
    screen.blit(nodes_visited_surface, (panel_x, y_offset))
    y_offset += 25

    # Open Set Size
    open_set_size_str = f"Open Set Size: {state_data.get('open_set_size', 0)}"
    open_set_size_surface = font.render(open_set_size_str, True, BRANCO)
    screen.blit(open_set_size_surface, (panel_x, y_offset))
    y_offset += 25

    # Current Node Scores (se estiver explorando)
    if state_data.get('path') is None: # Se ainda não encontrou o caminho final
        current_f = state_data.get('current_f_score', 0)
        current_g = state_data.get('current_g_score', 0)
        
        f_score_str = f"Current F: {current_f:.2f}"
        g_score_str = f"Current G: {current_g:.2f}"
        
        f_surface = font.render(f_score_str, True, CINZA)
        screen.blit(f_surface, (panel_x, y_offset))
        y_offset += 25
        
        g_surface = font.render(g_score_str, True, CINZA)
        screen.blit(g_surface, (panel_x, y_offset))
        y_offset += 25
    
    # Status
    status_str = "Status: Exploring..."
    if final_path:
        status_str = "Status: Path Found!"
    elif state_data.get('path') is False: # Se o A* indicou explicitamente que não há caminho
        status_str = "Status: No Solution!"
    
    status_surface = font.render(status_str, True, BRANCO)
    screen.blit(status_surface, (panel_x, y_offset))
    y_offset += 30

    # Controles
    controls_title = font.render("Controls:", True, AMARELO)
    screen.blit(controls_title, (panel_x, y_offset))
    y_offset += 25
    
    controls_q = font.render("Q: Quit", True, CINZA)
    screen.blit(controls_q, (panel_x, y_offset))
    y_offset += 20
    
    controls_r = font.render("R: Restart", True, CINZA)
    screen.blit(controls_r, (panel_x, y_offset))
    y_offset += 20
    
    
# --- Função Principal (Main Loop) ---

def main():
    labirinto_exemplo = [
        ['S', 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 5, 5, 5, 0], # Terreno difícil
        [1, 0, 0, 'E', 1],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    num_rows = len(labirinto_exemplo)
    num_cols = len(labirinto_exemplo[0])
    
    start_node, end_node = find_start_and_end(labirinto_exemplo)
    
    if not start_node or not end_node:
        print("Erro: 'S' ou 'E' não encontrado.")
        return

    pygame.init()
    pygame.font.init() # Inicializa o módulo de fontes

    # Define o tamanho da tela (largura do labirinto + largura do painel)
    largura_labirinto = num_cols * (TAMANHO_CELULA + MARGEM) + MARGEM
    altura_total = num_rows * (TAMANHO_CELULA + MARGEM) + MARGEM
    
    largura_total = largura_labirinto + PAINEL_LARGURA
    screen = pygame.display.set_mode((largura_total, altura_total))
    pygame.display.set_caption("A* PathFinder - Visualização Detalhada")
    
    font = pygame.font.SysFont("Arial", 16) # Fonte para o texto do painel

    a_star_generator = a_star_search_realtime(labirinto_exemplo, start_node, end_node)
    
    running = True
    clock = pygame.time.Clock()
    
    final_path = None
    explorando = True
    start_time = time.time() # Inicia o contador de tempo
    total_time = 0
    current_state_data = {} # Para armazenar o último estado do gerador

    # --- Loop Principal ---
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r:
                    main() # Reinicia a simulação
                    return

        # Lógica de atualização
        if explorando:
            try:
                current_state_data = next(a_star_generator)
                
                # Se o gerador retornou um caminho, o algoritmo terminou
                if current_state_data.get("path") is not None:
                    final_path = current_state_data["path"]
                    explorando = False
                    total_time = time.time() - start_time # Finaliza o tempo
                    if final_path is None: # Se "path" é explicitamente None, não há solução
                        print("Sem solução encontrada!")
                    else:
                        print(f"Caminho encontrado em {total_time:.4f} segundos!")

            except StopIteration:
                explorando = False
                total_time = time.time() - start_time
                if final_path is None: # Se o gerador parou e não encontrou caminho
                    print("Sem solução encontrada!")
        
        # Lógica de desenho
        screen.fill(PRETO) # Limpa a tela
        
        # Desenha o labirinto (com offset para o painel de info)
        draw_grid(screen, labirinto_exemplo) 
        
        if explorando:
            draw_state(screen, current_state_data, start_node, end_node)
        
        if final_path:
            draw_final_path(screen, final_path, start_node, end_node)

        # Desenha o painel de informações
        draw_info_panel(screen, labirinto_exemplo, current_state_data, start_time, total_time, final_path, font)

        pygame.display.flip()
        clock.tick(5) # Velocidade da simulação (15 FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":

    main()