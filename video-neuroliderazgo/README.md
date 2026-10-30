# Video: Neuroliderazgo, el contexto decide

Video final de 3:00 (1920×1080, 25 fps) para Teoría de la Decisión, basado en el ensayo sobre neuroliderazgo (Dra. Marina Santucci).

## Estructura

| # | Tiempo | Escena | Plano | Voz |
|---|---|---|---|---|
| 1 | 0:00 | Gancho | Avatar con lip-sync en pantalla flotante, travelling de retroceso | Ignacio |
| 2 | 0:08 | Neuroliderazgo | Órbita sobre un cerebro de partículas que se ordena en organigrama | Tipografía |
| 3 | 0:25 | El caso | Dolly a ras de piso y grúa sobre el árbol de decisión (■ decisión, ● azar, ▲ resultado) | Ignacio |
| 4 | 0:43 | Reunión A | Cenital, dolly zoom sobre el líder y órbita | Tipografía |
| 5 | 1:08 | Reunión B y matriz | Rebobinado real de la escena anterior, órbita a la altura de los ojos, matriz de decisión | Ignacio |
| 6 | 1:34 | Modelo SCARF | Órbita entre cinco anillos que pasan de amenaza a recompensa | Tipografía |
| 7 | 1:55 | Marco teórico | Travelling lateral por tres columnas (Simon, Tversky y Kahneman, Galton) | Tipografía |
| 8 | 2:18 | Límites éticos | Push-in sobre un ojo de vigilancia que se cierra | Tipografía |
| 9 | 2:33 | Cierre | Grúa de revelación y firma del avatar | Ignacio |

## Producción

- **Avatar:** un clip de 4 s con lip-sync generado en Higgsfield (Wan 2.7, 720p) con los 6 créditos disponibles: `produccion/avatar/wan_avatar.mp4`.
- **Voz:** Ignacio (ElevenLabs, rioplatense). Se generaron 4 tramos (`produccion/vo/`); ElevenLabs bloqueó el plan gratuito antes de completar el resto, por eso las escenas 2, 4, 6, 7 y 8 se cuentan con tipografía.
- **Motor 3D:** `produccion/motor.html` (three.js). Todo está en función del tiempo, así que se puede renderizar cuadro por cuadro.
- **Música:** `produccion/musica.py`, sintetizada y sincronizada con las escenas.

## Volver a renderizar

```bash
cd video-neuroliderazgo/produccion
python3 -m http.server 8765 --bind 127.0.0.1 &
ffmpeg -i avatar/wan_avatar.mp4 -vf "fps=25,scale=1280:720" -q:v 3 avatar/f_%03d.jpg
./run_render.sh          # 4.500 cuadros en render/video_mudo.mp4
python3 musica.py        # audio/musica.wav
```

La pista de voz (`audio/vo.wav`), la mezcla (`audio/mezcla.wav`) y el video final se arman con los comandos de ffmpeg descritos en `produccion/mezcla.sh`.
