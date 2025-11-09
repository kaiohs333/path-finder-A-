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
    
    # 1. Executa a Tarefa 1
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