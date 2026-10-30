"""Banda sonora del video (180 s), sintetizada y sincronizada con las escenas del motor 3D."""
import wave
import numpy as np

SR = 48000
DUR = 180.0
N = int(SR * DUR)
L = np.zeros(N, np.float64)
R = np.zeros(N, np.float64)
rng = np.random.default_rng(7)
OUT = '/home/user/teoria-de-la-decision/video-neuroliderazgo/produccion/audio/musica.wav'


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    H = np.ones_like(fr)
    if hi:
        H *= 1 / (1 + (fr / hi) ** 4)
    if lo:
        H *= 1 / (1 + (lo / np.maximum(fr, 1e-3)) ** 4)
    return np.fft.irfft(X * H, n=len(x))


def add(s0, l, r):
    n = min(len(l), N - s0)
    if n <= 0:
        return
    L[s0:s0 + n] += l[:n]
    R[s0:s0 + n] += r[:n]


def wavetable(f, n=4096):
    ph = np.arange(n) / n
    w = np.zeros(n)
    for k in range(1, max(1, int(2800 / f)) + 1):
        w += np.sin(2 * np.pi * k * ph) / k ** 1.6
    return w / np.max(np.abs(w))


def pad(t0, t1, freqs, gain=0.10, att=2.2, rel=2.5):
    s0 = int(t0 * SR)
    n = min(N, int((t1 + rel) * SR)) - s0
    t = np.arange(n) / SR
    e = np.ones(n)
    a, r = int(att * SR), int(rel * SR)
    e[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    e[-r:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r))
    trem = 1 + 0.12 * np.sin(2 * np.pi * 0.09 * t + rng.random() * 6)
    l, rr = np.zeros(n), np.zeros(n)
    for i, f in enumerate(freqs):
        tb = wavetable(f)
        for side, det in ((0, -0.0028), (1, 0.0028)):
            idx = (((f * (1 + det)) * t + rng.random()) * 4096 % 4096).astype(np.int64)
            v = tb[idx] * (0.9 if i == 0 else 0.55)
            if side == 0:
                l += v * 0.8; rr += v * 0.35
            else:
                rr += v * 0.8; l += v * 0.35
    sub = np.sin(2 * np.pi * freqs[0] / 2 * t) * 0.6
    l = (l + sub) * e * trem * gain
    rr = (rr + sub) * e * trem * gain
    add(s0, l, rr)


def pluck(t0, f, gain=0.035, decay=1.0, pan=0.0):
    s0 = int(t0 * SR)
    n = int(SR * decay * 4)
    t = np.arange(n) / SR
    env = np.exp(-t / decay) * (1 - np.exp(-t / 0.004))
    v = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t / (decay * 0.5))
         + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t / (decay * 0.3))) * env * gain
    add(s0, v * (1 - pan) * 0.7, v * (1 + pan) * 0.7)


def hit(t0, gain=0.5):
    s0 = int(t0 * SR)
    n = int(SR * 2.4)
    t = np.arange(n) / SR
    f = 34 + 42 * np.exp(-t / 0.22)
    v = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.75) * gain
    nz = fft_filter(rng.standard_normal(n) * np.exp(-t / 0.09), hi=700) * 0.12 * gain
    add(s0, v + nz, v + nz)


def whoosh(t_end, dur=1.3, gain=0.10):
    s0 = int((t_end - dur) * SR)
    n = int(dur * SR) + int(0.35 * SR)
    t = np.arange(n) / SR
    k = np.clip(t / dur, 0, 1)
    env = k ** 2.4 * np.exp(-np.maximum(t - dur, 0) / 0.09)
    nz = fft_filter(rng.standard_normal(n), lo=350, hi=4800) * env
    glide = np.sin(2 * np.pi * np.cumsum(180 + 700 * k ** 2) / SR) * env * 0.15
    v = (nz / (np.max(np.abs(nz)) + 1e-9) + glide) * gain
    add(s0, v * 0.9, v)


def thump(t0, gain):
    s0 = int(t0 * SR)
    n = int(SR * 0.45)
    t = np.arange(n) / SR
    f = 46 + 22 * np.exp(-t / 0.05)
    v = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12) * gain
    add(s0, v, v)


def tick(t0, gain=0.045):
    s0 = int(t0 * SR)
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    v = (np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.025) + rng.standard_normal(n) * np.exp(-t / 0.006) * 0.3) * gain
    add(s0, v, v * 0.9)


# --- armonía por escena ---
Dm9 = [146.83, 220.00, 329.63, 349.23]
Bbmaj7 = [116.54, 174.61, 220.00, 293.66]
Fadd9 = [87.31, 130.81, 220.00, 392.00]
Tension = [73.42, 110.00, 311.13, 349.23]
G6E = [98.00, 146.83, 246.94, 329.63]
Cadd9 = [130.81, 196.00, 293.66, 329.63]
Am7 = [110.00, 164.81, 196.00, 261.63]
Dm7 = [146.83, 174.61, 220.00, 261.63]
Dadd9 = [146.83, 220.00, 369.99, 329.63]

pad(0.0, 8.0, Dm9, gain=0.085, att=2.6)
pad(7.4, 25.0, Bbmaj7)
pad(24.4, 43.0, Fadd9, gain=0.09)
pad(42.6, 67.4, Tension, gain=0.10, rel=0.6)
pad(69.8, 94.0, G6E, att=1.2)
pad(93.4, 115.0, Cadd9)
pad(114.4, 138.0, Am7, gain=0.09)
pad(137.4, 153.0, Dm7, gain=0.09)
pad(152.4, 165.0, Bbmaj7, gain=0.095)
pad(164.0, 176.5, Dadd9, gain=0.11, rel=3.2)

# --- arpegios y campanas ---
arp = [466.16, 587.33, 698.46, 880.00, 698.46, 587.33]
for i, t0 in enumerate(np.arange(9.0, 24.2, 0.62)):
    pluck(t0, arp[i % len(arp)], gain=0.03, decay=1.1, pan=0.4 if i % 2 else -0.4)
for i, t0 in enumerate(np.arange(26.0, 42.0, 0.652)):
    pluck(t0, [174.61, 261.63][i % 2], gain=0.022, decay=0.35, pan=-0.2 if i % 2 else 0.2)
arpB = [392.00, 493.88, 587.33, 659.25]
for i, t0 in enumerate(np.arange(76.0, 93.6, 0.5)):
    pluck(t0, arpB[i % 4], gain=0.026, decay=0.9, pan=0.35 if i % 2 else -0.35)
arpC = [523.25, 659.25, 783.99, 1174.66]
for i, t0 in enumerate(np.arange(102.0, 114.6, 0.45)):
    pluck(t0, arpC[i % 4], gain=0.02, decay=1.0, pan=0.45 if i % 2 else -0.45)
for t0, f in ((116.6, 523.25), (122.8, 587.33), (129.4, 659.25)):
    pluck(t0, f, gain=0.06, decay=2.4)
for t0 in np.arange(117.0, 137.0, 1.3):
    pluck(t0, 220.0, gain=0.014, decay=0.4)
for t0, f in ((157.0, 587.33), (160.6, 698.46), (165.0, 880.00), (169.9, 739.99)):
    pluck(t0, f, gain=0.045, decay=2.2)

# --- latido en la reunión A ---
for k in np.arange(49.0, 65.5, 0.86):
    p = (k - 49.0) / 16.5
    thump(k, 0.22 + 0.2 * p)
    thump(k + 0.2, 0.13 + 0.12 * p)

# --- golpes, whooshes y ticks ---
for t0, g in ((4.4, 0.45), (8.0, 0.25), (25.0, 0.35), (43.0, 0.45), (70.2, 0.3), (87.6, 0.4), (94.0, 0.35),
              (115.0, 0.3), (138.0, 0.4), (153.0, 0.35), (169.85, 0.4), (175.0, 0.25)):
    hit(t0, g)
for b in (8.0, 25.0, 43.0, 94.0, 115.0, 138.0, 153.0, 169.85):
    whoosh(b)
for t0 in (31.6, 33.4, 35.1, 46.2, 51.2, 55.2, 61.2, 73.6, 76.45, 79.2, 85.1, 85.6, 86.2, 86.8,
           95.4, 95.6, 95.8, 96.0, 96.2, 117.0, 123.2, 129.8, 139.0, 143.2, 146.6, 175.0):
    tick(t0)

# --- rebobinado: la música de la reunión A al revés y acelerada, más un frenado de cinta ---
a, b = int(43.0 * SR), int(67.8 * SR)
seg_l, seg_r = L[a:b][::-1].copy(), R[a:b][::-1].copy()
m = int(1.9 * SR)
x = np.linspace(0, len(seg_l) - 1, m)
rw_l = fft_filter(np.interp(x, np.arange(len(seg_l)), seg_l), hi=4200) * 0.55
rw_r = fft_filter(np.interp(x, np.arange(len(seg_r)), seg_r), hi=4200) * 0.55
s0 = int(66.6 * SR)
n = int(1.4 * SR)
t = np.arange(n) / SR
swell = fft_filter(rng.standard_normal(n), lo=1500) * (t / 1.4) ** 3 * 0.05
add(s0, swell, swell)
L[int(67.4 * SR):int(68.0 * SR)] *= np.linspace(1, 0.15, int(68.0 * SR) - int(67.4 * SR))
R[int(67.4 * SR):int(68.0 * SR)] *= np.linspace(1, 0.15, int(68.0 * SR) - int(67.4 * SR))
s0 = int(68.0 * SR)
n = int(1.0 * SR)
t = np.arange(n) / SR
f = 380 * np.exp(-t * 3.2) + 25
saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
spin = fft_filter(saw * np.exp(-t / 0.6) * 0.16, hi=1500)
add(s0, spin, spin)
add(s0, rw_l, rw_r)

# --- reverb por convolución ---
irn = int(2.6 * SR)
ti = np.arange(irn) / SR
pre = int(0.02 * SR)
wet = []
for ch, x in ((0, L), (1, R)):
    ir = rng.standard_normal(irn) * np.exp(-ti / 0.55)
    ir[:pre] = 0
    ir = fft_filter(ir, hi=6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + irn)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:N]
    wet.append(y)
L = L * 0.8 + wet[0] * 0.38
R = R * 0.8 + wet[1] * 0.38

# --- cierre: fundido final ---
fo = int(178.6 * SR)
L[fo:] *= np.linspace(1, 0, N - fo)
R[fo:] *= np.linspace(1, 0, N - fo)
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
st = (np.stack([L, R], 1) / peak * 0.85 * 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(st.tobytes())
print('musica lista', OUT, 'pico', round(peak, 3))
