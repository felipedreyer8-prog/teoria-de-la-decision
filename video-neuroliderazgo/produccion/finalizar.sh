#!/usr/bin/env bash
# Une video y audio, genera la versión web (<15 MB) y el póster para la página.
set -euo pipefail
cd "$(dirname "$0")"
WEB="${1:-render}"
ffmpeg -y -loglevel error -i render/video_mudo.mp4 -i audio/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest render/neuroliderazgo_final.mp4
ffmpeg -y -loglevel error -i render/neuroliderazgo_final.mp4 -vf "scale=1280:720:flags=lanczos,hqdn3d=2:2:5:5" -c:v libx264 -preset slow -b:v 520k -pass 1 -passlogfile render/p2 -an -f mp4 /dev/null
ffmpeg -y -loglevel error -i render/neuroliderazgo_final.mp4 -vf "scale=1280:720:flags=lanczos,hqdn3d=2:2:5:5" -c:v libx264 -preset slow -b:v 520k -maxrate 1100k -bufsize 2200k -pass 2 -passlogfile render/p2 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart "$WEB/neuroliderazgo.mp4"
ffmpeg -y -loglevel error -ss 6.5 -i render/neuroliderazgo_final.mp4 -frames:v 1 -vf scale=1280:720 -q:v 3 "$WEB/poster.jpg"
ls -la render/neuroliderazgo_final.mp4 "$WEB/neuroliderazgo.mp4" "$WEB/poster.jpg"
