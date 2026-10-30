"""Ejemplo: elegir una inversión según distintos criterios."""

from decision import (
    Azar, Decision, Terminal,
    hurwicz, laplace, maximax, maximin, savage, valor_esperado, veip,
)

alternativas = ["Acciones", "Bonos", "Plazo fijo"]
estados = ["Expansión", "Estabilidad", "Recesión"]
pagos = [
    [200, 50, -20],
    [150, 100, 30],
    [80, 80, 80],
]
probs = [0.3, 0.5, 0.2]

print("Matriz de pagos")
print(f"{'':12}" + "".join(f"{e:>13}" for e in estados))
for a, fila in zip(alternativas, pagos):
    print(f"{a:12}" + "".join(f"{x:>13}" for x in fila))
print()

for nombre, (i, v) in [
    ("Maximin (Wald)", maximin(pagos)),
    ("Maximax", maximax(pagos)),
    ("Hurwicz (α=0.6)", hurwicz(pagos, 0.6)),
    ("Savage", savage(pagos)),
    ("Laplace", laplace(pagos)),
    ("Valor esperado", valor_esperado(pagos, probs)),
]:
    print(f"{nombre:18} -> {alternativas[i]:11} ({v:.2f})")
print(f"\nVEIP = {veip(pagos, probs):.2f}")

# Árbol: ¿lanzar un producto o no?
arbol = Decision({
    "Lanzar": Azar([(0.6, Terminal(500)), (0.4, Terminal(-300))]),
    "No lanzar": Terminal(0),
})
print(f"\nÁrbol: VE = {arbol.resolver():.2f}, decisión = {arbol.eleccion}")
