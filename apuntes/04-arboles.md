# 4. Árboles de decisión

Representan decisiones **secuenciales**.

- ▢ **Nodo de decisión**: el decisor elige una rama.
- ◯ **Nodo de azar**: la naturaleza elige una rama según sus probabilidades.
- ◁ **Nodo terminal**: resultado final.

## Resolución (hacia atrás / *rollback*)

1. Empezar por los nodos terminales.
2. En cada nodo de azar: calcular el valor esperado de sus ramas.
3. En cada nodo de decisión: quedarse con la rama de mayor valor (podar las demás `||`).
4. Repetir hasta llegar a la raíz.

## Información muestral y Bayes

Con un estudio de resultado $s$, las probabilidades se actualizan:
$$P(e_j \mid s) = \frac{P(s \mid e_j)\,P(e_j)}{\sum_k P(s \mid e_k)\,P(e_k)}$$

- **VEIM** (valor esperado de la información muestral) = VE con estudio − VE sin estudio.
- **Eficiencia** = VEIM / VEIP.

Ver [`src/decision/arbol.py`](../src/decision/arbol.py).
