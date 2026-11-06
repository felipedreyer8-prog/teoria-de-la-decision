"""Música de fondo suave (5:00), sintetizada: piano + pad + bajo, con reverb.

Secciones alineadas con las escenas: E1 calma, E2 tensa y escasa, E3 reflexiva,
E4-E6 cálida y resolutiva. Registro medio-grave para no competir con las voces.
"""
import sys, wave
import numpy as np

SR = 44100
DUR = 300.0
N = int(SR * DUR)
rng = np.random.default_rng(7)

def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)

def env_adsr(n, a, r, sus=1.0):
    e = np.ones(n) * sus
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, sus, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e

def piano(f0, dur, vel):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    B = 0.00035
    for k in range(1, 9):
        fk = k * f0 * np.sqrt(1 + B * k * k)
        if fk > 6000: break
        amp = vel / k ** 1.4
        tau = 2.6 / (1 + 0.55 * (k - 1)) * (220 / max(f0, 110)) ** 0.35
        out += amp * np.exp(-t / tau) * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.28))
    att = np.minimum(1, t / 0.006)
    rel = np.ones(n); nr = int(0.25 * SR); rel[-nr:] = np.linspace(1, 0, nr)
    # golpe del martillo: ruido corto y suave
    nz = rng.standard_normal(n) * np.exp(-t / 0.008) * 0.02 * vel
    nz = np.convolve(nz, np.ones(24) / 24, mode="same")
    return (out * att * rel + nz)

def pad(freqs, dur, level):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for i, f in enumerate(freqs):
        for det, pan in ((-0.004, 0.25), (0.004, 0.75)):
            ff = f * (1 + det)
            vib = 1 + 0.0015 * np.sin(2 * np.pi * (0.18 + 0.03 * i) * t)
            ph = 2 * np.pi * np.cumsum(ff * vib) / SR
            w = np.zeros(n)
            for k in range(1, 7):
                w += np.sin(k * ph) / k ** 1.8
            out[:, 0] += w * (1 - pan)
            out[:, 1] += w * pan
    return out * level * env_adsr(n, 1.8, 2.2)[:, None] / len(freqs)

def sine_bass(f, dur, level):
    n = int(dur * SR); t = np.arange(n) / SR
    return level * np.sin(2 * np.pi * f * t) * env_adsr(n, 0.6, 1.2)

# Acordes (notas MIDI). Re mayor / Re menor.
CH = {
    "D":  [50, 57, 62, 66], "Bm": [47, 54, 59, 62], "G":  [43, 55, 59, 62], "A":  [45, 57, 61, 64],
    "Dm": [50, 57, 62, 65], "Bb": [46, 53, 58, 62], "Gm": [43, 55, 58, 62], "A7": [45, 55, 61, 64],
    "Em": [40, 55, 59, 62], "F#m": [42, 54, 57, 61], "Dadd9": [50, 57, 64, 66],
}
# Secciones: (inicio, fin, progresión, segundos por acorde, estilo)
SEC = [
    (0.0,   35.5,  ["D", "Bm", "G", "A"], 4.0, "calma"),
    (33.3,  85.0,  ["Dm", "Bb", "Gm", "A7"], 5.0, "tension"),
    (83.3, 143.5,  ["Bm", "G", "D", "A"], 4.5, "reflexiva"),
    (141.7, 218.5, ["D", "A", "Bm", "G"], 4.0, "calida"),
    (216.7, 268.5, ["G", "D", "Em", "A"], 4.0, "calida"),
    (266.7, 300.0, ["G", "A", "D", "Dadd9"], 4.2, "final"),
]

L = np.zeros((N, 2))

def add(sig, start, gain=1.0, pan=0.5):
    i = int(start * SR)
    if i >= N: return
    if sig.ndim == 1:
        sig = np.stack([sig * (1 - pan) * 1.4, sig * pan * 1.4], axis=1)
    j = min(N, i + len(sig))
    L[i:j] += sig[: j - i] * gain

for (a, b, prog, spc, estilo) in SEC:
    sec = np.zeros_like(L)
    t = a; idx = 0
    while t < b:
        ch = CH[prog[idx % len(prog)]]
        d = min(spc, b - t) + 2.0
        freqs = [midi(n) for n in ch]
        lvl = {"tension": 0.20, "reflexiva": 0.22}.get(estilo, 0.24)
        p = pad(freqs[1:], d, lvl)
        i = int(t * SR); j = min(N, i + len(p)); sec[i:j] += p[: j - i]
        bb = sine_bass(midi(ch[0] - 12 if ch[0] > 45 else ch[0]), d, 0.10 if estilo != "tension" else 0.12)
        i2 = min(N, i + len(bb)); sec[i:i2] += np.stack([bb, bb], 1)[: i2 - i] * 0.7
        beat = spc / 4
        if estilo == "tension":
            pat = [(0, ch[0] + 12, 0.30), (2, ch[2], 0.20)]
        elif estilo == "reflexiva":
            pat = [(0, ch[1] + 12, 0.24), (1.5, ch[2] + 12, 0.17), (3, ch[3], 0.15)]
        elif estilo == "final" and idx == len(prog) - 1:
            pat = [(0, ch[0] + 12, 0.30), (0.02, ch[2] + 12, 0.22), (0.04, ch[3] + 12, 0.2)]
        else:
            notes = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 12]
            pat = [(k * 1.0, notes[k % 4], 0.22 - 0.02 * (k % 2)) for k in range(4)]
            if estilo in ("calida", "final") and idx % 2 == 1:
                pat += [(3.5, ch[3] + 19 if ch[3] + 19 < 86 else ch[3] + 7, 0.12)]
        for off, note, vel in pat:
            st = t + off * beat
            if st >= b: continue
            pn = piano(midi(note), 4.5, vel * rng.uniform(0.9, 1.05))
            pan = 0.35 + 0.3 * ((note % 7) / 6)
            ii = int(st * SR); jj = min(N, ii + len(pn))
            sec[ii:jj, 0] += pn[: jj - ii] * (1 - pan) * 1.4
            sec[ii:jj, 1] += pn[: jj - ii] * pan * 1.4
        t += spc; idx += 1
    # fundido de entrada/salida de cada sección (crossfade de ~2 s)
    ia, ib = int(a * SR), min(N, int(b * SR))
    w = np.zeros(N)
    w[ia:ib] = 1
    fi = int(2.0 * SR)
    if a > 0: w[ia:ia + fi] = np.linspace(0, 1, fi)
    if b < DUR: w[ib - fi:ib] = np.linspace(1, 0, fi)
    L += sec * w[:, None]

# Reverb por convolución (respuesta al impulso sintética, ~2.8 s)
def reverb(x, rt=2.8, mix=0.32):
    n = int(rt * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-6.9 * t / rt)[:, None]
    for c in range(2):  # suavizar agudos de la cola
        ir[:, c] = np.convolve(ir[:, c], np.ones(12) / 12, mode="same")
    ir /= np.sqrt((ir ** 2).sum(0))
    out = np.zeros_like(x)
    blk = 1 << 16
    nfft = 1 << int(np.ceil(np.log2(blk + n)))
    H = np.fft.rfft(ir, nfft, axis=0)
    for s in range(0, len(x), blk):
        seg = x[s:s + blk]
        Y = np.fft.irfft(np.fft.rfft(seg, nfft, axis=0) * H, nfft, axis=0)
        e = min(len(x), s + nfft)
        out[s:e] += Y[: e - s]
    return x * (1 - mix) + out * mix * 2.2

L = reverb(L)
# filtro pasabajos suave (media móvil doble) para dejar espacio a la voz
for _ in range(2):
    for c in range(2):
        L[:, c] = np.convolve(L[:, c], np.ones(5) / 5, mode="same")
# fundido final
fo = int(4.0 * SR); L[-fo:] *= np.linspace(1, 0, fo)[:, None]
fi = int(1.5 * SR); L[:fi] *= np.linspace(0, 1, fi)[:, None]
L /= np.max(np.abs(L)) / 0.85
pcm = (L * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes(pcm.tobytes())
print("ok", len(pcm) / SR, "s")
