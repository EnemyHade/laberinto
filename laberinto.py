from collections import deque
import heapq
import networkx as nx

laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, "S", 0, 0, 0, 1, "P", "P", 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, "C1", 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, "C2", 1, 0, 1],
    [1, 0, 0, "P", 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, "P", 0, 0, 0, "C1", 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, "M", 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#valores
COSTOS = {
    0: 1.0,  # Camino normal
    "S": 1.0,  # Inicio
    "M": 1.0,  # Meta
    "P": 0.5,  # Premio
    "C1": 3.0,  # Penalización leve
    "C2": 5.0,  # Penalización alta
}

#matriz
def construir_grafo(matriz):
    G = nx.Graph()
    filas = len(matriz)
    columnas = len(matriz[0])
    inicio, meta = None, None

    for r in range(filas):
        for c in range(columnas):
            val = matriz[r][c]
            if val != 1:  
                G.add_node((r, c), tipo=str(val))
                if val == "S":
                    inicio = (r, c)
                elif val == "M":
                    meta = (r, c)

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izq, Der[cite: 1]
    for u in G.nodes():
        r, c = u
        for dr, dc in movimientos:
            v = (r + dr, c + dc)
            if v in G:
                tipo_destino = G.nodes[v]["tipo"]
                peso = COSTOS.get(tipo_destino, 1.0)
                G.add_edge(u, v, weight=peso)

    return G, inicio, meta

def dfs_propio(G, inicio, meta):
    stack = [(inicio, [inicio])]
    visitados = set()
    orden_exploracion = []

    while stack:
        actual, camino = stack.pop()
        if actual not in visitados:
            visitados.add(actual)
            orden_exploracion.append(actual)

            if actual == meta:
                return camino, orden_exploracion

            for vecino in G.neighbors(actual):
                if vecino not in visitados:
                    stack.append((vecino, camino + [vecino]))

    return None, orden_exploracion


def bfs_propio(G, inicio, meta):
    queue = deque([(inicio, [inicio])])
    visitados = {inicio}
    orden_exploracion = []

    while queue:
        actual, camino = queue.popleft()
        orden_exploracion.append(actual)

        if actual == meta:
            return camino, orden_exploracion

        for vecino in G.neighbors(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append((vecino, camino + [vecino]))

    return None, orden_exploracion


def dijkstra_propio(G, inicio, meta):
    pq = [(0, inicio, [inicio])]
    distancias = {nodo: float("inf") for nodo in G.nodes()}
    distancias[inicio] = 0
    orden_exploracion = []
    visitados = set()

    while pq:
        costo_actual, actual, camino = heapq.heappop(pq)

        if actual in visitados:
            continue
        visitados.add(actual)
        orden_exploracion.append(actual)

        if actual == meta:
            return camino, orden_exploracion, costo_actual

        for vecino in G.neighbors(actual):
            peso = G[actual][vecino]["weight"]
            nuevo_costo = costo_actual + peso

            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                heapq.heappush(pq, (nuevo_costo, vecino, camino + [vecino]))

    return None, orden_exploracion, float("inf")


def calcular_costo_camino(G, camino):
    return sum(G[camino[i]][camino[i + 1]]["weight"] for i in range(len(camino) - 1))


if __name__ == "__main__":
    G, inicio, meta = construir_grafo(laberinto)

    camino_dfs, exp_dfs = dfs_propio(G, inicio, meta)
    costo_dfs = calcular_costo_camino(G, camino_dfs)

    camino_bfs, exp_bfs = bfs_propio(G, inicio, meta)
    costo_bfs = calcular_costo_camino(G, camino_bfs)

    camino_dijkstra, exp_dijkstra, costo_dijkstra = dijkstra_propio(G, inicio, meta)

    resultados = {
        "DFS": (exp_dfs, camino_dfs, costo_dfs),
        "BFS": (exp_bfs, camino_bfs, costo_bfs),
        "Dijkstra": (exp_dijkstra, camino_dijkstra, costo_dijkstra),
    }

    for algo, (exp, camino, costo) in resultados.items():
        print(f"\nAlgoritmo: {algo}")
        print(f"Nodos explorados: {len(exp)}")
        print(f"Número de movimientos: {len(camino) - 1}")
        print(f"Costo total: {costo}")
        print("Camino: " + " -> ".join(map(str, camino)))