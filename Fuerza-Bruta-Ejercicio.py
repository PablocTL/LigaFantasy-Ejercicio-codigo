from itertools import combinations
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


def fuerza_bruta():
    por_pos = {p: [] for p in POSICIONES}
    for nombre, pos, precio, puntos in JUGADORES:
        por_pos[pos].append((nombre, precio, puntos))

    mejor_equipo = None
    mejores_puntos = -1
    total = 0
    factibles = 0

    for por in combinations(por_pos["POR"], 1):
        for defs in combinations(por_pos["DEF"], 4):
            for meds in combinations(por_pos["MED"], 4):
                for dels in combinations(por_pos["DEL"], 2):
                    total += 1
                    equipo = por + defs + meds + dels
                    coste = sum(p for _, p, _ in equipo)
                    if coste > PRESUPUESTO:
                        continue
                    factibles += 1
                    puntos = sum(pts for _, _, pts in equipo)
                    if puntos > mejores_puntos:
                        mejores_puntos = puntos
                        mejor_equipo = equipo

    return mejor_equipo, mejores_puntos, total, factibles


if __name__ == "__main__":
    t0 = timeit.default_timer()
    eq_bf, pt_bf, total, fact = fuerza_bruta()
    t_bf = timeit.default_timer() - t0

    print("FUERZA BRUTA")
    print("combinaciones con cupos:", total)
    print("factibles:", fact)
    print("equipo:", [j[0] for j in eq_bf])
    print("puntos:", pt_bf)
    print("coste:", sum(j[1] for j in eq_bf), "M")
    print("tiempo:", round(t_bf, 4), "s")