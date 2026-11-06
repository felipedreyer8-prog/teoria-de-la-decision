"""Corta un audio del narrador con varias frases en un archivo por cue, usando las pausas.

Uso: python3 -I dividir.py <build> <audio_junto.mp3> <id1> <id2> ...
"""
import os, re, subprocess, sys
import numpy as np
B, src, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path.insert(0, B)
import guion
SR = 44100
CUE = {c["id"]: c for c in guion.CUES}
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
# unidades = oraciones; cada cue tiene 1 o más
units = []
for i in ids:
    sents = [s for s in re.split(r"(?<=[.?!])\s+", CUE[i]["text"].strip()) if s]
    units += [(i, s) for s in sents]
fr = int(0.01 * SR); n = len(x) // fr
e = np.sqrt(np.mean(x[: n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
db = 20 * np.log10(e / e.max())
quiet = db < -40
gaps, i = [], 0
while i < n:
    if quiet[i]:
        j = i
        while j < n and quiet[j]: j += 1
        if i > 0 and j < n: gaps.append((i * 0.01, j * 0.01))
        i = j
    else:
        i += 1
k = len(units) - 1
best = sorted(sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[:k])
cuts = [0.0] + [(a + b) / 2 for a, b in best] + [len(x) / SR]
lens = [len(s) for _, s in units]
print("pausas elegidas:", [f"{a:.2f}-{b:.2f} ({b - a:.2f}s)" for a, b in best])
ok = True
segs = {}
for u, (cid, s) in enumerate(units):
    d = cuts[u + 1] - cuts[u]
    rate = len(s) / d
    print(f"  {cid}: {d:5.2f}s  {rate:5.1f} car/s  «{s[:50]}»")
    if not 9 <= rate <= 24: ok = False
    segs.setdefault(cid, [cuts[u], cuts[u + 1]])[1] = cuts[u + 1]
if not ok:
    sys.exit("REVISAR: alguna frase tiene una velocidad rara; el corte puede estar mal")
for cid, (a, b) in segs.items():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-c:a", "libmp3lame", "-q:a", "2",
                    os.path.join(B, "audio", "cues", cid + ".mp3")], check=True)
print("ok:", ", ".join(segs))
