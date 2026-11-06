# Teoría de la Decisión

Apuntes, ejemplos y herramientas en Python para la asignatura de **Teoría de la Decisión**.

## Contenido

| Carpeta | Descripción |
|---|---|
| [`apuntes/`](apuntes/) | Resúmenes teóricos por tema |
| [`src/decision/`](src/decision/) | Implementación de criterios de decisión |
| [`ejemplos/`](ejemplos/) | Problemas resueltos |
| [`tests/`](tests/) | Pruebas automáticas |
| [`video-neuroliderazgo/`](video-neuroliderazgo/) | Video final "Neuroliderazgo en el ámbito laboral" (3:45), subtítulos y archivos de producción |

## Temas

1. [Introducción y elementos de un problema de decisión](apuntes/01-introduccion.md)
2. [Decisión bajo incertidumbre](apuntes/02-incertidumbre.md) — Wald (maximin), maximax, Hurwicz, Savage (minimax regret), Laplace
3. [Decisión bajo riesgo](apuntes/03-riesgo.md) — valor esperado, pérdida de oportunidad esperada, VEIP
4. [Árboles de decisión](apuntes/04-arboles.md)
5. [Teoría de la utilidad](apuntes/05-utilidad.md)

## Uso rápido

```bash
python -m pip install -e .
python ejemplos/inversion.py
python -m pytest
```

```python
from decision import maximin, hurwicz, savage, valor_esperado

pagos = [
    [200, 50, -20],   # Alternativa A
    [150, 100, 30],   # Alternativa B
    [80, 80, 80],     # Alternativa C
]
print(maximin(pagos))              # (2, 80)
print(hurwicz(pagos, alfa=0.6))
print(valor_esperado(pagos, [0.3, 0.5, 0.2]))
```

## Licencia

MIT
