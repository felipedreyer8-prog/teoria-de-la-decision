#!/usr/bin/env bash
# Une video y audio: entrega en 1080p (~100 MB), versión web (<15 MB) y póster.
set -euo pipefail
cd "$(dirname "$0")"
WEB="${1:-render}"
VF="hqdn3d=1:1:3:3"
ffmpeg -y -loglevel error -i render/video_mudo.mp4 -vf "$VF" -c:v libx264 -preset slow -b:v 4200k -pass 1 -passlogfile render/p1 -an -f mp4 /dev/null
ffmpeg -y -loglevel error -i render/video_mudo.mp4 -i audio/mezcla.wav -map 0:v -map 1:a -vf "$VF" -c:v libx264 -preset slow -b:v 4200k -maxrate 6500k -bufsize 13000k -pass 2 -passlogfile render/p1 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest render/neuroliderazgo_final.mp4
WVF="scale=1280:720:flags=lanczos,hqdn3d=2:2:5:5"
ffmpeg -y -loglevel error -i render/video_mudo.mp4 -vf "$WVF" -c:v libx264 -preset slow -b:v 520k -pass 1 -passlogfile render/p2 -an -f mp4 /dev/null
ffmpeg -y -loglevel error -i render/video_mudo.mp4 -i audio/mezcla.wav -map 0:v -map 1:a -vf "$WVF" -c:v libx264 -preset slow -b:v 520k -maxrate 1100k -bufsize 2200k -pass 2 -passlogfile render/p2 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart -shortest "$WEB/neuroliderazgo.mp4"
ffmpeg -y -loglevel error -ss 6.5 -i render/video_mudo.mp4 -frames:v 1 -vf scale=1280:720 -q:v 3 "$WEB/poster.jpg"
ls -la render/neuroliderazgo_final.mp4 "$WEB/neuroliderazgo.mp4" "$WEB/poster.jpg"
