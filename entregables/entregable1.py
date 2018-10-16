import sys
# import time
from typing import Tuple

from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

# from utils.labyrinthviewer import LabyrinthViewer

rows, cols = 0, 0


def load_labyrinth(file: str) -> UndirectedGraph:
    """
    @param file: Fichero que contiene un laberinto.
    @return: Devuelve un UndirectedGraph equivalente al laberinto del fichero.
    """
    f = open(file, "r")
    lines = f.readlines()
    f.close()

    corridors = []
    global cols
    global rows

    rows = len(lines)
    for r in range(rows):
        cells = lines[r].rstrip('\n').split(',')
        if r == 0:
            cols = len(cells)
        for c in range(cols):
            if 's' not in cells[c] and r + 1 < rows:
                corridors.append(((r, c), (r + 1, c)))
            if 'e' not in cells[c] and c + 1 < cols:
                corridors.append(((r, c), (r, c + 1)))

    return UndirectedGraph(E=corridors)


def distance_matrix(g: "UndirectedGraph"):
    """
    @param g: Grafo que contiene un laberinto.
    @return: Devuelve 2 matrices de enteros. La primera contiene la distancia desde todos los vertices hasta el vertice
    origen (0,0) y la segunda la distancia desde todos los vertices hasta el vertice target (rows-1, cols-1).
    """

    def edges_withd_path(graph: "UndirectedGraph", initial_v: Tuple[int, int], ma):
        queue = Fifo()
        seen = set()
        queue.push((initial_v, initial_v))
        seen.add(initial_v)
        ma[initial_v[0]][initial_v[1]] = -1
        while len(queue) > 0:
            u, v = queue.pop()
            ma[v[0]][v[1]] = ma[u[0]][u[1]] + 1
            for suc in graph.succs(v):
                if suc not in seen:
                    seen.add(suc)
                    queue.push((v, suc))
        return ma

    m1 = []
    n = []
    for r in range(rows):
        m1.append([[-1]] * cols)
        n.append([[-1]] * cols)

    m1 = edges_withd_path(g, (0, 0), m1)
    n = edges_withd_path(g, (rows - 1, cols - 1), n)

    return m1, n


def wall_to_break(matrixi, matrixf) -> list:
    """
    @param matrixi: Matriz que contiene la distancia desde todos los vertices hasta el vertice origen.
    @param matrixf: Matriz que contiene la distancia desde todos los vertices has el vertice target.
    @return: Lista que contiene en pos 0 una tupla con los vertices que comparten la pared que hay que tirar,
             en pos 1 la distancia desde origen hasta target sin tirar la pared y en pos 2 la distancia tirando la pared
    """
    total = 0
    listaux = []
    tuplaux = (0, 0)
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0 or j + 1 < cols and total > matrixi[i][j] + matrixf[i][j + 1] + 1:
                total = matrixi[i][j] + matrixf[i][j + 1] + 1
                tuplaux = ((i, j), (i, j + 1))
            if i + 1 < rows and total > matrixi[i][j] + matrixf[i + 1][j] + 1:
                total = matrixi[i][j] + matrixf[i + 1][j] + 1
                tuplaux = ((i, j), (i + 1, j))
    listaux.append(tuplaux)
    listaux.append(matrixf[0][0])
    listaux.append(total)
    return listaux


if __name__ == "__main__":
    # tiempoInicio = time.time()

    graphLab = load_labyrinth(sys.argv[1])

    # print('Carga completa en: ', time.time() - tiempoInicio)
    # tiempoPared = time.time()

    inicio, final = distance_matrix(graphLab)
    lista = wall_to_break(inicio, final)

    # print('Tiempo que ha tardado en encontrar la pared: ', time.time() - tiempoPared)

    print(lista[0][0][0], lista[0][0][1], lista[0][1][0], lista[0][1][1])
    print(lista[1])
    print(lista[2])

    # print('Tiempo que ha tardado en ejecutarse el programa: ', time.time() - tiempoInicio)
    # print('Fin de programa')
