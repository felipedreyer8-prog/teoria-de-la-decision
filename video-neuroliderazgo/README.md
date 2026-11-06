# Video: Neuroliderazgo en el ámbito laboral

**[Neuroliderazgo_en_el_ambito_laboral.mp4](Neuroliderazgo_en_el_ambito_laboral.mp4)**: 3:45 min · 1920×1080 (16:9) · español con acento rioplatense · subtítulos incluidos en la imagen y también en [`.srt`](Neuroliderazgo_en_el_ambito_laboral.srt).

La primera versión duraba 5:00 y está en el historial del repo. A pedido del grupo se aceleró a 3:45, con pausas más cortas entre las voces.

Basado en el *Trabajo Final de Teoría de la Decisión* (Dra. Marina Santucci, Universidad Austral). Los personajes son siempre los mismos en todas las escenas: el jefe y Lucía, más dos compañeros de equipo.

## Escenas

| Escena | Tiempo | Qué se ve |
|---|---|---|
| 1. Introducción | 0:00 – 0:26 | Título. Lucía trabaja en una presentación y el jefe se acerca. |
| 2. Una respuesta que genera amenaza | 0:26 – 1:01 | El jefe señala el error delante de los compañeros. Lucía queda incómoda. |
| 3. ¿Qué está pasando? | 1:01 – 1:45 | La escena se congela. Aparecen las cinco dimensiones de SCARF y las amenazas de la situación. |
| 4. La misma situación, otra forma de liderar | 1:45 – 2:39 | Placa "Volvamos a intentarlo" y conversación en privado, con tono tranquilo. |
| 5. Relación con la toma de decisiones | 2:39 – 3:13 | El jefe escucha, revisan juntos y Lucía corrige la presentación. Aparecen las palabras Atención, Percepción y Regulación emocional. |
| 6. Cierre | 3:13 – 3:45 | El equipo trabaja en conjunto. Título y placa de referencias. |

La duración de cada escena sale de lo que se dice en ella, con pausas naturales: unos 0,6 s entre diálogos y alrededor de 1 s entre frases del narrador. El aire extra va al título, la placa de transición, las apariciones de SCARF y el cierre. No se agregó contenido: la narración y los diálogos son exactamente los del prompt.

## Cómo se hizo

- **Voces:** ElevenLabs (`eleven_v4`), con voces rioplatenses de su biblioteca. Narrador: *Carlos – Argentinian Narrator*. Jefe: *Franco – Argentina*. Lucía: *Malena – Conversacional*. Los nombres de los personajes y las indicaciones visuales no se leen en voz alta.
- **Imagen:** animación 2D vectorial generada por código. Los personajes se dibujaron a partir de dos retratos de referencia y mueven la boca al ritmo de su voz. El estilo es animado y no fotorrealista porque el plan gratuito de ElevenLabs solo permitió generar 2 imágenes en el día.
- **Música:** pista suave sintetizada por código, sin derechos de terceros. Baja automáticamente cuando hay voces.
- **Gráficos y subtítulos:** título, modelo SCARF con íconos, amenazas, palabras clave y placa de referencias, generados por código.

## Archivos de producción (`produccion/`)

| Archivo | Para qué sirve |
|---|---|
| `guion.py` | Textos exactos de cada voz, escenas y tiempos |
| `timeline.py` | Arma la línea de tiempo, la mezcla de audio y los subtítulos |
| `anim/` | Escenarios, personajes y render cuadro por cuadro (Playwright + Chromium) |
| `musica.py` | Genera la música de fondo |
| `graficos.py`, `render_graficos.js` | Generan los gráficos superpuestos |
| `dividir.py` | Corta la narración generada por escena en una frase por archivo |

Los audios de las voces no están en el repo. Para rehacer el video hay que volver a generarlos en `audio/cues/<id>.mp3`, usando los IDs de `guion.py`.
