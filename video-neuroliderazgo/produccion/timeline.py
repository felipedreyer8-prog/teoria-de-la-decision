"""Línea de tiempo del video animado 'Neuroliderazgo en el ámbito laboral' (1920x1080, 5:00).

Uso: python3 -I timeline.py <build_dir>
Escribe out/timeline.json (tomas, cámaras, envolventes de boca), out/mezcla.wav y subtítulos.
"""
import json, math, os, re, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

B = os.path.abspath(sys.argv[1])
DRAFT = "--draft" in sys.argv
sys.path.insert(0, B)
import guion  # noqa: E402

W, H = 1920, 1080
FPS = 30
DUR = 300.0
SR = 48000
OUT = os.path.join(B, "out"); os.makedirs(OUT, exist_ok=True)
CUE = {c["id"]: c for c in guion.CUES}

# ---------------------------------------------------------------- audio
def decode(path, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def trim(x, sr=SR, thr_db=-42, pad=0.06):
    fr = int(0.01 * sr)
    n = len(x) // fr
    e = np.sqrt(np.mean(x[: n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(e / (e.max() + 1e-12))
    on = np.where(db > thr_db)[0]
    if len(on) == 0:
        return x
    a = max(0, on[0] * fr - int(pad * sr)); b = min(len(x), (on[-1] + 1) * fr + int(pad * sr))
    y = x[a:b].copy()
    f = int(0.008 * sr); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y

def speech_rms_db(x, sr=SR):
    fr = int(0.02 * sr); n = len(x) // fr
    e = np.sqrt(np.mean(x[: n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    act = e[e > e.max() * 0.1]
    return 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-12)

def room(x, sr=SR, rt=0.35, wet=0.10, seed=3):
    rng = np.random.default_rng(seed)
    n = int(rt * sr); t = np.arange(n) / sr
    ir = rng.standard_normal(n) * np.exp(-6.9 * t / rt)
    ir = np.convolve(ir, np.ones(16) / 16, mode="same"); ir /= np.sqrt((ir ** 2).sum())
    y = np.convolve(x, ir)
    out = np.zeros(len(y), dtype=np.float32); out[: len(x)] = x
    return (out * (1 - wet) + y * wet).astype(np.float32)

def gaps(x, sr=SR, min_gap=0.14, thr_db=-38):
    """Silencios internos (inicio, fin) en segundos."""
    fr = int(0.01 * sr); n = len(x) // fr
    e = np.sqrt(np.mean(x[: n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    quiet = 20 * np.log10(e / (e.max() + 1e-12)) < thr_db
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if i > 0 and j < n and (j - i) * 0.01 >= min_gap:
                out.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return out

AUD = {}
for c in guion.CUES:
    x = trim(decode(os.path.join(B, "audio", "cues", c["id"] + ".mp3")))
    x = x * 10 ** ((-20.0 - speech_rms_db(x)) / 20)          # misma sonoridad para las tres voces
    if c["voz"] != "narrador":
        x = room(x)                                          # los diálogos suenan "en la oficina"
    AUD[c["id"]] = x
DURS = {k: len(v) / SR for k, v in AUD.items()}

# ---------------------------------------------------------------- disposición temporal
def P(mn, w, cap=None, label=None, elastic=False):
    return dict(k="pad", min=mn, w=w, cap=cap, label=label, elastic=elastic)
def C(i):
    return dict(k="cue", id=i)

# Pausas naturales (mín., peso para repartir el tiempo extra, tope). La duración de cada escena sale del
# contenido; el total se lleva a OBJETIVO sumando aire sobre todo en título, placa, SCARF y cierre.
OBJETIVO = 225.0   # 3:45
LAYOUT = {
    "E1": [P(4.5, 1.0, 6.0, "title"), C("N1a"), P(.8, .3, 1.2), C("N1b"), P(.9, .3, 1.2), C("N1c"), P(1.2, .5, 2.0)],
    "E2": [P(2.4, .6, 3.2, "arrive"), C("J1"), P(.55, .1, .8), C("L1"), P(.5, .1, .8), C("J2"), P(2.0, .8, 3.0, "silence"),
           C("N2a"), P(.8, .3, 1.2), C("N2b"), P(.8, .3, 1.2), C("N2c"), P(1.5, .5, 2.2)],
    "E3": [P(1.4, .5, 2.2), C("N3a"), P(1.2, .5, 1.8), C("N3b"), P(1.0, .5, 1.6), C("N3c"), P(1.0, .5, 1.6), C("N3d"),
           P(1.0, .5, 1.6), C("N3e"), P(1.0, .5, 1.6), C("N3f"), P(1.6, .6, 2.4, "hold"), C("N3g"), P(1.6, .5, 2.4)],
    "E4": [P(3.6, .8, 4.6, "card"), P(1.2, .5, 2.2, "establish"), C("J3"), P(.6, .1, .8), C("L2"), P(.6, .1, .8), C("J4"),
           P(.6, .1, .8), C("L3"), P(.6, .1, .8), C("J5"), P(1.4, .5, 2.2, "after"), C("N4a"), P(.9, .3, 1.2), C("N4b"),
           P(.9, .3, 1.2), C("N4c"), P(1.3, .5, 2.0)],
    "E5": [P(.8, .4, 1.6), C("N5a"), P(1.0, .3, 1.3), C("N5b"), P(.9, .3, 1.2), C("N5c"), P(1.0, .3, 1.3), C("N5d"),
           P(1.3, .5, 2.0)],
    "E6": [P(.7, .3, 1.2), C("N6a"), P(.7, .2, 1.0), C("N6b"), P(.7, .2, 1.0), C("N6c"), P(.7, .2, 1.0), C("N6d"),
           P(6.5, .8, 7.5, "plate")],
}

pads = [i for items in LAYOUT.values() for i in items if i["k"] == "pad"]
natural = sum(DURS[i["id"]] for items in LAYOUT.values() for i in items if i["k"] == "cue") + sum(p["min"] for p in pads)
extra = {id(p): 0.0 for p in pads}
rest = OBJETIVO - natural
for _ in range(20):                   # reparto por pesos respetando topes
    free = [p for p in pads if p["min"] + extra[id(p)] < p["cap"] - 1e-6]
    if rest < 1e-6 or not free:
        break
    wsum = sum(p["w"] for p in free); used = 0
    for p in free:
        add = min(rest * p["w"] / wsum, p["cap"] - p["min"] - extra[id(p)])
        extra[id(p)] += add; used += add
    rest -= used
print(f"duración natural {natural:.1f}s -> {natural + sum(extra.values()):.1f}s")

T, PADS, E = {}, {}, {}
t = 0.0
for esc, items in LAYOUT.items():
    s0 = t
    for i in items:
        if i["k"] == "cue":
            T[i["id"]] = (t, t + DURS[i["id"]]); t += DURS[i["id"]]
        else:
            d = i["min"] + extra[id(i)]
            if i["label"]:
                PADS[(esc, i["label"])] = (t, t + d)
            t += d
    E[esc] = (s0, t)
DUR = round(t * FPS) / FPS

def st(i): return T[i][0]
def en(i): return T[i][1]

# ---------------------------------------------------------------- tomas (cámara sobre escenarios vectoriales)
SH = []
def shot(scene, cut, tr, cam0, cam1, fx=None, freeze=None):
    SH.append(dict(scene=scene, cut=cut, tr=tr, cam0=cam0, cam1=cam1, fx=fx, freezeAt=freeze))

shot("office", 0.0, 0.0, (960, 540, 1.00), (900, 556, 1.08))                                   # E1a título
shot("office", st("N1b") - .3, 0.0, (860, 600, 1.50), (880, 592, 1.66))                       # E1b Lucía trabaja
shot("office", st("N1c") - .3, 0.0, (1120, 540, 1.12), (1060, 556, 1.22))                     # E1c entra el jefe
shot("office", E["E2"][0], 0.0, (1010, 560, 1.12), (1020, 556, 1.22), fx="cool")              # E2a señala el error
shot("office", st("L1") - .12, 0.0, (735, 585, 2.30), (735, 580, 2.45), fx="cool")           # E2b Lucía responde
shot("office", st("J2") - .12, 0.0, (1405, 505, 2.10), (1405, 500, 2.25), fx="cool")         # E2c jefe impaciente
shot("office", en("J2") + 1.0, 0.0, (740, 590, 2.40), (735, 585, 2.75), fx="cool")            # E2b Lucía en silencio
shot("office", st("N2c") - .3, 0.0, (990, 560, 1.12), (990, 556, 1.20), fx="cool")            # E2a plano general
fz = SH[-1]; tf = E["E3"][0]
shot("office", E["E3"][0], .9, fz["cam1"], (990, 556, 1.24), fx="freeze", freeze=tf)         # E3 congelado + SCARF
shot("office", st("N3g") - .5, .9, (990, 556, 1.24), (990, 556, 1.28), fx="dim", freeze=tf)  # E3 amenazas
shot("office", E["E4"][0], .25, (990, 556, 1.28), (960, 540, 0.96), fx="rewind", freeze=tf)  # rebobinado
card = PADS[("E4", "card")]
shot("meeting", card[1] - .3, .9, (960, 640, 1.30), (960, 640, 1.42), fx="warm")             # E4a en privado
shot("meeting", st("L2") - .12, 0.0, (1180, 630, 2.00), (1185, 628, 2.12), fx="warm")        # E4b Lucía
shot("meeting", st("J4") - .12, 0.0, (740, 630, 2.00), (735, 628, 2.12), fx="warm")          # E4c jefe
shot("meeting", st("L3") - .12, 0.0, (1185, 640, 2.10), (1180, 632, 2.25), fx="warm")        # E4b Lucía
shot("meeting", st("J5") - .12, 0.0, (735, 640, 2.10), (740, 632, 2.25), fx="warm")          # E4c jefe
shot("meeting", en("J5") + 1.0, 0.0, (960, 650, 1.55), (960, 640, 1.32), fx="warm")           # E4a plano general
shot("meeting", E["E5"][0], 0.0, (860, 640, 1.75), (830, 636, 1.90), fx="warm")               # E5a el jefe escucha
shot("meeting", st("N5b") - .3, 0.0, (960, 680, 1.70), (960, 670, 1.95), fx="warm")           # E5b revisan juntos
shot("office", st("N5d") - .3, .8, (870, 600, 1.50), (900, 598, 1.70), fx="warm")            # E5c Lucía corrige
shot("team", E["E6"][0], .8, (960, 600, 1.18), (960, 610, 1.32), fx="warm")                  # E6 equipo
for k, s in enumerate(SH):
    s["end"] = SH[k + 1]["cut"] if k + 1 < len(SH) else DUR
    s["a"] = s["cut"] - s["tr"] / 2
    s["b"] = s["end"] + (SH[k + 1]["tr"] / 2 if k + 1 < len(SH) else 0)

MARKS = dict(walk0=max(st("N1c") + 0.6, E["E2"][0] + 1.2 - 7.5), walk1=E["E2"][0] + 1.2, review=st("N5b") - 0.3, fix0=st("N5d") + 0.6)

# ---------------------------------------------------------------- gráficos superpuestos
OV = []
def ov(name, a, b, fi=.5, fo=.5):
    OV.append(dict(name=name, a=a, b=b, fi=fi, fo=fo))

ov("titulo", .5, st("N1a") - .25, 1.0, .8)
sc = [E["E3"][0] + .7, st("N3b") - .25, st("N3c") - .25, st("N3d") - .25, st("N3e") - .25, st("N3f") - .25, st("N3g") - .5]
for k in range(6):
    ov(f"scarf_{k}", sc[k], sc[k + 1] + (.3 if k < 5 else 0), .3 if k else .7, .3 if k < 5 else .6)
txt = CUE["N3g"]["text"]; d3 = en("N3g") - st("N3g")
marks = [st("N3g") + d3 * txt.index(w) / len(txt) - .15 for w in ("la exposición", "las instrucciones", "el control")]
for k in range(3):
    ov(f"amenazas_{k + 1}", marks[k], (marks[k + 1] + .25) if k < 2 else E["E4"][0] + .2, .25, .25 if k < 2 else .35)
ov("volvamos", E["E4"][0] + .2, card[1], .45, .6)
ov("palabras_1", E["E5"][0] + .6, st("N5b") - .3, .5, .3)
ov("palabras_2", st("N5b") - .3, st("N5d") - .3, .3, .3)
ov("palabras_3", st("N5d") - .3, E["E5"][1] - .3, .3, .6)
plate = PADS[("E6", "plate")]
ov("cierre", plate[0] + .2, DUR, 1.0, 0.0)

# ---------------------------------------------------------------- subtítulos
def split_text(text, maxc=84):
    sents = re.findall(r"[^.?!:]+[.?!:]+|[^.?!:]+$", text)
    out = []
    for s in (x.strip() for x in sents):
        if len(s) <= maxc:
            out.append(s); continue
        parts, cur = [], ""
        for w in re.split(r"(?<=,)\s+", s):
            if cur and len(cur) + 1 + len(w) > maxc:
                parts.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur: parts.append(cur)
        for part in parts:          # frases largas sin comas: cortar cerca del medio, antes de un conector
            while len(part) > maxc:
                ws = part.split(" ")
                best, bscore = None, 1e9
                for i in range(2, len(ws) - 1):
                    left = len(" ".join(ws[:i]))
                    score = abs(left - len(part) / 2) - (12 if ws[i] in ("para", "y", "que", "con", "ni", "pero", "por", "sino", "en") else 0)
                    if score < bscore:
                        best, bscore = i, score
                out.append(" ".join(ws[:best])); part = " ".join(ws[best:])
            out.append(part)
    # unir trozos muy cortos con el siguiente
    merged = []
    for p in out:
        if merged and len(merged[-1]) < 22 and len(merged[-1]) + len(p) + 1 <= maxc:
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged

SUBS = []
for c in guion.CUES:
    a, b = T[c["id"]]; d = b - a
    chunks = split_text(c["text"])
    tot = sum(len(x) for x in chunks)
    est, acc = [], 0
    for x in chunks[:-1]:
        acc += len(x); est.append(d * acc / tot)
    gp = [(g0 + g1) / 2 for g0, g1 in gaps(AUD[c["id"]])]
    bounds = []
    for e_ in est:
        cand = [g for g in gp if g not in bounds and abs(g - e_) < max(0.9, 0.18 * d)]
        bounds.append(min(cand, key=lambda g: abs(g - e_)) if cand else e_)
    bounds = sorted(bounds)
    edges = [0.0] + bounds + [d]
    for k, x in enumerate(chunks):
        SUBS.append(dict(a=a + edges[k], b=a + edges[k + 1] + (0.25 if k == len(chunks) - 1 else 0.0),
                         text=x, narr=c["voz"] == "narrador"))
for i in range(len(SUBS) - 1):     # evitar solapamientos
    SUBS[i]["b"] = min(SUBS[i]["b"], SUBS[i + 1]["a"] - 0.04)

def ts_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
def ts_ass(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

with open(os.path.join(OUT, "subtitulos.srt"), "w", encoding="utf-8") as f:
    for i, s in enumerate(SUBS, 1):
        f.write(f"{i}\n{ts_srt(s['a'])} --> {ts_srt(s['b'])}\n{s['text']}\n\n")
fs = 46 if not DRAFT else 23
ass = [
    "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    f"Style: Dialogo,Inter SemiBold,{fs},&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,0,0,3,{fs*0.28:.0f},0,2,{W//8},{W//8},{H*0.06:.0f},1",
    f"Style: Narrador,Inter SemiBold,{fs},&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,-1,0,0,100,100,0,0,3,{fs*0.28:.0f},0,2,{W//8},{W//8},{H*0.06:.0f},1",
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
for s in SUBS:
    ass.append(f"Dialogue: 0,{ts_ass(s['a'])},{ts_ass(s['b'])},{'Narrador' if s['narr'] else 'Dialogo'},,0,0,0,,{{\\fad(120,120)}}{s['text']}")
with open(os.path.join(OUT, "subtitulos.ass"), "w", encoding="utf-8") as f:
    f.write("\n".join(ass) + "\n")

# ---------------------------------------------------------------- mezcla de audio
n = int(DUR * SR)
voice = np.zeros(n, dtype=np.float32)
for c in guion.CUES:
    i = int(round(st(c["id"]) * SR)); x = AUD[c["id"]]
    j = min(n, i + len(x)); voice[i:j] += x[: j - i]
json.dump(dict(dur=DUR, esc=E), open(os.path.join(OUT, "escenas.json"), "w"))
subprocess.run([sys.executable, "-I", os.path.join(B, "musica.py"), os.path.join(B, "audio", "musica.wav"),
                os.path.join(OUT, "escenas.json")], check=True)
mus = decode(os.path.join(B, "audio", "musica.wav"))
mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]
mus *= 10 ** ((-16.0 - speech_rms_db(mus)) / 20)
# automatización: más baja bajo la voz, sube en las pausas, título y cierre
talk = np.zeros(n, dtype=bool)
for c in guion.CUES:
    a, b = T[c["id"]]; talk[max(0, int((a - .3) * SR)): int((b + .35) * SR)] = True
g_db = np.where(talk, -21.0, -14.5)
g_db[: int(st("N1a") * SR)] = -12.0
g_db[int(plate[0] * SR):] = -12.0
k = int(0.5 * SR)
g = 10 ** (np.convolve(g_db, np.ones(k) / k, mode="same") / 20)
mix = voice + mus * g
fo = int(2.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
mix /= max(1e-6, np.abs(mix).max()) / 0.9
pre = os.path.join(OUT, "mezcla_pre.wav")
with wave.open(pre, "wb") as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes((mix * 32767).astype(np.int16).tobytes())
meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
js = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
# ganancia fija (loudnorm "lineal" pasa a modo dinámico si no puede, y eso subía la música en las pausas)
gain = -16.0 - float(js["input_i"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
                f"volume={gain:.2f}dB,alimiter=limit=0.89:attack=5:release=60:level=disabled,aresample=48000",
                "-ac", "2", os.path.join(OUT, "mezcla.wav")], check=True)


# ---------------------------------------------------------------- envolventes para mover la boca (30 fps)
ENV = {}
for c in guion.CUES:
    x = AUD[c["id"]]; hop = SR // FPS
    n_ = len(x) // hop
    r = np.sqrt(np.mean(x[: n_ * hop].reshape(n_, hop) ** 2, axis=1))
    r = r / (np.percentile(r, 95) + 1e-9)
    r = np.clip((r - 0.12) / 0.88, 0, 1) ** 0.7
    r = np.convolve(r, np.ones(3) / 3, mode="same")
    ENV[c["id"]] = [round(float(v), 2) for v in r]


json.dump(dict(
    dur=DUR, fps=FPS,
    cues={c["id"]: dict(a=T[c["id"]][0], b=T[c["id"]][1], voz=c["voz"]) for c in guion.CUES},
    env=ENV, esc=E, marks=MARKS,
    pads={f"{k[0]}:{k[1]}": v for k, v in PADS.items()},
    shots=[{k: s[k] for k in ("scene", "cut", "end", "a", "b", "cam0", "cam1", "fx", "freezeAt")} for s in SH],
    overlays=OV,
), open(os.path.join(OUT, "timeline.json"), "w"))
print("timeline ok:", len(SH), "tomas,", len(OV), "gráficos,", len(SUBS), "subtítulos")
