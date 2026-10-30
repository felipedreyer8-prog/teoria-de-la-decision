#!/usr/bin/env bash
# Arma la pista de voz, la mezcla con la música y une todo con el video renderizado.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p audio

# Voz: cada tramo en su lugar de la línea de tiempo (milisegundos).
ffmpeg -y -loglevel error -f lavfi -t 180 -i anullsrc=r=48000:cl=mono \
  -i vo/hook_4s.wav -i vo/s3.mp3 -i vo/s5.mp3 -i vo/s9.mp3 -filter_complex \
  "[1:a]aresample=48000,aformat=channel_layouts=mono,adelay=300[a1];\
   [2:a]aresample=48000,aformat=channel_layouts=mono,adelay=25800[a2];\
   [3:a]aresample=48000,aformat=channel_layouts=mono,adelay=70200[a3];\
   [4:a]aresample=48000,aformat=channel_layouts=mono,adelay=154000[a4];\
   [0:a][a1][a2][a3][a4]amix=inputs=5:normalize=0:duration=first[out]" \
  -map "[out]" -c:a pcm_s16le audio/vo.wav

# Mezcla: la música baja sola cuando habla la voz (sidechain), luego -14 LUFS.
ffmpeg -y -loglevel error -i audio/vo.wav -i audio/musica.wav -filter_complex \
  "[0:a]volume=5.4dB,alimiter=limit=0.84:attack=5:release=60:level=false,aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][sc];\
   [1:a]volume=-3.5dB[mus];[mus][sc]sidechaincompress=threshold=0.015:ratio=8:attack=25:release=500[duck];\
   [vo][duck]amix=inputs=2:normalize=0[out]" -map "[out]" -ar 48000 -c:a pcm_s24le audio/premezcla.wav
I=$(ffmpeg -hide_banner -nostats -i audio/premezcla.wav -af loudnorm=print_format=json -f null - 2>&1 | grep '"input_i"' | sed 's/[^0-9.-]//g')
G=$(python3 -c "print(round(-14-($I),2))")
ffmpeg -y -loglevel error -i audio/premezcla.wav -af "volume=${G}dB,alimiter=limit=0.84:attack=3:release=80:level=false" -ar 48000 -c:a pcm_s16le audio/mezcla.wav

# Video final.
ffmpeg -y -loglevel error -i render/video_mudo.mp4 -i audio/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest render/neuroliderazgo_final.mp4
echo "listo: render/neuroliderazgo_final.mp4"
