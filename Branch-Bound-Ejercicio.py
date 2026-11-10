import heapq
import timeit

JUGADORES = [
    ("Ortega", "POR", 9, 5.8),
    ("Lunin", "POR", 6, 4.6),
    ("Remiro", "POR", 4, 3.9),
    ("Koundé", "DEF", 12, 6.4),
    ("Mingueza", "DEF", 7, 5.1),
    ("Vivian", "DEF", 5, 4.2),
    ("Huijsen", "DEF", 9, 5.4),
    ("Cucurella", "DEF", 11, 5.9),
    ("Lejeune", "DEF", 3, 3.1),
    ("Mosquera", "DEF", 6, 4.5),
    ("Pedri", "MED", 18, 8.1),
    ("Baena", "MED", 13, 6.9),
    ("Sučić", "MED", 8, 5.2),
    ("Barrios", "MED", 10, 5.9),
    ("Fermín", "MED", 11, 6.2),
    ("Gaya", "MED", 4, 3.3),
    ("Arambarri", "MED", 6, 4.4),
    ("Mbappé", "DEL", 24, 9.6),
    ("Budimir", "DEL", 9, 6.0),
    ("Oyarzabal", "DEL", 14, 7.2),
    ("Iglesias", "DEL", 7, 4.8),
]

PRESUPUESTO = 100
CUPOS = {"POR": 1, "DEF": 4, "MED": 4, "DEL": 2}
POSICIONES = ["POR", "DEF", "MED", "DEL"]


def branch_and_bound():
    jugadores_ord = sorted(JUGADORES, key=lambda x: x[3] / x[2], reverse=True)
    n = len(jugadores_ord)
    idx_pos = {p: i for i, p in enumerate(POSICIONES)}

    def cota(level, precio, puntos, counts):
        B = PRESUPUESTO - precio
        if B < 0:
            return -1

        for p in POSICIONES:
            i = idx_pos[p]
            rem = CUPOS[p] - counts[i]
            if rem < 0:
                return -1
            disponibles = sum(1 for k in range(level, n)
                              if jugadores_ord[k][1] == p)
            if disponibles < rem:
                return -1

        val = puntos
        for k in range(level, n):
            _, _, w, v = jugadores_ord[k]
            if w <= B:
                B -= w
                val += v
            else:
                val += v * (B / w)
                break
        return val

    counts_raiz = tuple(0 for _ in POSICIONES)
    cota_raiz = cota(0, 0, 0, counts_raiz)
    heap = [(-cota_raiz, 0, 0, 0, counts_raiz, ())]

    mejores_puntos = -1
    mejor_equipo = None
    nodos_abiertos = 0

    while heap:
        neg_c, level, precio, puntos, counts, seleccionados = heapq.heappop(heap)
        c = -neg_c
        nodos_abiertos += 1

        if c <= mejores_puntos:
            continue

        if level == n:
            if all(counts[idx_pos[p]] == CUPOS[p] for p in POSICIONES):
                if puntos > mejores_puntos:
                    mejores_puntos = puntos
                    mejor_equipo = seleccionados
            continue

        nombre, pos, w, v = jugadores_ord[level]
        pi = idx_pos[pos]

        if counts[pi] < CUPOS[pos] and precio + w <= PRESUPUESTO:
            nc = list(counts)
            nc[pi] += 1
            nc = tuple(nc)
            np_ = precio + w
            npt = puntos + v
            nb = cota(level + 1, np_, npt, nc)
            if nb > mejores_puntos:
                heapq.heappush(
                    heap,
                    (-nb, level + 1, np_, npt, nc, seleccionados + (nombre,))
                )

        nb = cota(level + 1, precio, puntos, counts)
        if nb > mejores_puntos:
            heapq.heappush(
                heap,
                (-nb, level + 1, precio, puntos, counts, seleccionados)
            )

    return mejor_equipo, mejores_puntos, nodos_abiertos


if __name__ == "__main__":
    t0 = timeit.default_timer()
    eq_bnb, pt_bnb, nodos = branch_and_bound()
    t_bnb = timeit.default_timer() - t0

    print("BRANCH AND BOUND")
    print("equipo:", list(eq_bnb))
    print("puntos:", pt_bnb)
    print("nodos abiertos:", nodos)
    print("tiempo:", round(t_bnb, 4), "s")