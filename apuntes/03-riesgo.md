# 3. Decisión bajo riesgo

Se conocen las probabilidades $p_j$ de cada estado, con $\sum_j p_j = 1$.

## Valor esperado (VE)
$$VE_i = \sum_j p_j\, x_{ij}, \qquad a^* = \arg\max_i VE_i$$

## Pérdida de oportunidad esperada (POE)
$$POE_i = \sum_j p_j\, r_{ij}$$
Minimizar la POE lleva siempre a la misma decisión que maximizar el VE.

## Valor esperado con información perfecta (VECIP)
$$VECIP = \sum_j p_j \max_i x_{ij}$$

## Valor esperado de la información perfecta (VEIP)
$$VEIP = VECIP - \max_i VE_i = \min_i POE_i$$
Es lo máximo que convendría pagar por saber con certeza qué estado ocurrirá.
