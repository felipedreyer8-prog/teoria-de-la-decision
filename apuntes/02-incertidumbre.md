# 2. Decisión bajo incertidumbre

No se conocen las probabilidades de los estados. (Para matrices de **beneficios**; si son costos, invertir max/min.)

## Criterio de Wald (maximin, pesimista)
$$a^* = \arg\max_i \min_j x_{ij}$$

## Criterio maximax (optimista)
$$a^* = \arg\max_i \max_j x_{ij}$$

## Criterio de Hurwicz (coeficiente de optimismo $\alpha \in [0,1]$)
$$H_i = \alpha \max_j x_{ij} + (1-\alpha)\min_j x_{ij}$$
Con $\alpha = 0$ coincide con Wald; con $\alpha = 1$, con maximax.

## Criterio de Savage (minimax arrepentimiento)
Matriz de arrepentimiento: $r_{ij} = \max_k x_{kj} - x_{ij}$
$$a^* = \arg\min_i \max_j r_{ij}$$

## Criterio de Laplace (razón insuficiente)
Todos los estados equiprobables:
$$L_i = \frac{1}{n}\sum_j x_{ij}$$
