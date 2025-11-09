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
            
            # Otimização: se já encontramos os dois, podemos parar
            if start and end:
                return start, end
                
    # Se o loop terminar e não tivermos encontrado os dois
    return start, end

# --- Execução Principal (para testar a Etapa 1) ---
if __name__ == "__main__":
    
    # A "Entrada" é esta matriz
    labirinto_exemplo = [
        ['S', 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 'E', 1]
    ]

    print("--- PathFinder A* - Etapa 1 ---")
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