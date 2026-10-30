#!/usr/bin/env bash
# Renderiza los 4500 cuadros (180 s a 25 fps) en 4 tramos paralelos y los une.
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="$(npm root -g)"
mkdir -p render
N=4; TOTAL=4500; STEP=$((TOTAL / N))
for i in $(seq 0 $((N - 1))); do
  a=$((i * STEP)); b=$(( i == N - 1 ? TOTAL : (i + 1) * STEP ))
  node render.js frames "render/seg_$i.mp4" "$a" "$b" > "render/seg_$i.log" 2>&1 &
done
wait
: > render/lista.txt
for i in $(seq 0 $((N - 1))); do echo "file 'seg_$i.mp4'" >> render/lista.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i render/lista.txt -c copy render/video_mudo.mp4
ffprobe -v error -show_entries format=duration:stream=nb_frames -of compact render/video_mudo.mp4
echo "RENDER LISTO"
