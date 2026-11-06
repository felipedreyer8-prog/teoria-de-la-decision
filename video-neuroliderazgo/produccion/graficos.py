"""Genera los gráficos superpuestos (PNG 1920x1080 con transparencia) como HTML."""
import json, pathlib, sys

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;background:transparent;overflow:hidden}
body{font-family:'Inter','Inter Display',sans-serif;color:#F7F9FC;-webkit-font-smoothing:antialiased}
.accent{color:#5FD3C6}
"""

def page(body, extra=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{body}</body></html>"

# --- íconos (trazo simple, estilo lineal) ---
def svg(paths, size=92, stroke="#5FD3C6"):
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 48 48' fill='none' stroke='{stroke}' "
            f"stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'>{paths}</svg>")

ICONOS = {
    # podio: posición frente a los demás
    "S": "<rect x='5' y='26' width='12' height='16' rx='1.5'/><rect x='18' y='16' width='12' height='26' rx='1.5'/><rect x='31' y='31' width='12' height='11' rx='1.5'/><path d='M24 4l2.2 4.4 4.8.7-3.5 3.4.8 4.8L24 15l-4.3 2.3.8-4.8L17 9.1l4.8-.7z'/>",
    # brújula: saber qué esperar
    "C": "<circle cx='24' cy='24' r='18'/><path d='M30.5 17.5l-4 9-9 4 4-9z'/><circle cx='24' cy='24' r='1.2' fill='#5FD3C6'/>",
    # bifurcación: margen de decisión
    "A": "<path d='M24 44V26'/><path d='M24 26L12 12'/><path d='M24 26l12-14'/><path d='M12 12h0M7 13l5-5 5 5' /><path d='M31 13l5-5 5 5'/>",
    # dos personas: confianza y pertenencia
    "R": "<circle cx='17' cy='15' r='6'/><circle cx='32' cy='17' r='5'/><path d='M5 40c0-7 5.4-12 12-12s12 5 12 12'/><path d='M27 29.5c1.5-.9 3.2-1.5 5-1.5 6 0 11 4.5 11 11'/>",
    # balanza: trato justo
    "F": "<path d='M24 6v36'/><path d='M14 42h20'/><path d='M8 13h32'/><path d='M24 6l-1 0'/><path d='M8 13l-5 13h10z'/><path d='M40 13l-5 13h10z'/><path d='M3 26a5 3.2 0 0 0 10 0'/><path d='M35 26a5 3.2 0 0 0 10 0'/>",
}
SCARF = [
    ("S", "Estatus", "Posición frente a los demás"),
    ("C", "Certidumbre", "Saber qué esperar"),
    ("A", "Autonomía", "Margen de decisión"),
    ("R", "Relación", "Confianza y pertenencia"),
    ("F", "Equidad", "Trato justo"),
]

pages = {}

# 1) Título de apertura
pages["titulo"] = page("""
<div class='veil'></div>
<div class='box'>
  <div class='bar'></div>
  <h1>Neuroliderazgo</h1>
  <h2>en el ámbito laboral</h2>
</div>""", """
.veil{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,14,26,.78) 0%,rgba(8,14,26,.55) 45%,rgba(8,14,26,0) 80%)}
.box{position:absolute;left:140px;top:360px}
.bar{width:120px;height:8px;border-radius:4px;background:#5FD3C6;margin-bottom:34px}
h1{font-family:'Inter Display','Inter';font-weight:700;font-size:132px;letter-spacing:-2px;line-height:1}
h2{font-weight:300;font-size:70px;margin-top:18px;color:rgba(247,249,252,.92)}
""")

# 2) SCARF progresivo: k = tarjetas reveladas (0..5); la última revelada queda resaltada
for k in range(0, 6):
    cards = []
    for i, (letra, palabra, desc) in enumerate(SCARF):
        if i < k:
            cls = "card on" + (" cur" if i == k - 1 else "")
            cards.append(f"<div class='{cls}'>{svg(ICONOS[letra])}<div class='l'>{letra}</div>"
                         f"<div class='w'>{palabra}</div><div class='d'>{desc}</div></div>")
        else:
            cards.append(f"<div class='card ghost'><div class='gl'>{letra}</div></div>")
    pages[f"scarf_{k}"] = page(f"""
<div class='veil'></div>
<div class='head'>
  <h1>Modelo <span class='accent'>SCARF</span></h1>
  <div class='sub'>David Rock (2008)</div>
  <div class='legend'><span class='dot t'></span>Amenaza<span class='arrow'>⟷</span><span class='dot r'></span>Recompensa</div>
</div>
<div class='row'>{''.join(cards)}</div>""", """
.veil{position:absolute;inset:0;background:rgba(8,14,26,.62)}
.head{position:absolute;top:96px;left:0;right:0;text-align:center}
h1{font-family:'Inter Display','Inter';font-weight:700;font-size:84px;letter-spacing:-1px}
.sub{font-size:32px;color:rgba(247,249,252,.75);margin-top:10px}
.legend{display:inline-flex;align-items:center;gap:14px;margin-top:22px;font-size:28px;color:rgba(247,249,252,.85);
  padding:10px 26px;border-radius:40px;background:rgba(255,255,255,.07)}
.dot{width:16px;height:16px;border-radius:50%;display:inline-block}.dot.t{background:#FF7A6B}.dot.r{background:#F6C667}
.arrow{opacity:.7;margin:0 6px}
.row{position:absolute;top:388px;left:0;right:0;display:flex;justify-content:center;gap:30px}
.card{width:318px;height:372px;border-radius:26px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px}
.card.on{background:rgba(16,28,48,.88);border:2px solid rgba(95,211,198,.35)}
.card.cur{border:3px solid #5FD3C6;box-shadow:0 0 44px rgba(95,211,198,.45);transform:translateY(-10px)}
.card.ghost{border:2px dashed rgba(247,249,252,.28);background:rgba(16,28,48,.35)}
.gl{font-family:'Inter Display','Inter';font-weight:700;font-size:96px;color:rgba(247,249,252,.30)}
.l{font-family:'Inter Display','Inter';font-weight:700;font-size:60px;color:#5FD3C6;margin-top:14px;line-height:1}
.w{font-weight:700;font-size:40px;margin-top:10px}
.d{font-size:27px;color:rgba(247,249,252,.78);margin-top:12px;line-height:1.25}
""")

# 3) Amenazas en la situación (sobre la escena congelada)
AMEN = ["Exposición pública", "Instrucciones confusas", "Control excesivo"]
for k in range(1, 4):
    tags = "".join(f"<div class='tag'><span class='ic'>!</span>{t}</div>" for t in AMEN[:k])
    pages[f"amenazas_{k}"] = page(f"""
<div class='veil'></div>
<div class='col'><div class='h'>Posibles amenazas</div>{tags}</div>""", """
.veil{position:absolute;inset:0;background:linear-gradient(270deg,rgba(8,14,26,.80) 0%,rgba(8,14,26,.45) 40%,rgba(8,14,26,0) 70%)}
.col{position:absolute;right:120px;top:250px;display:flex;flex-direction:column;align-items:flex-end;gap:26px}
.h{font-size:34px;font-weight:600;color:rgba(247,249,252,.85);letter-spacing:.5px;margin-bottom:6px}
.tag{display:flex;align-items:center;gap:20px;font-size:46px;font-weight:700;padding:22px 34px;border-radius:20px;
  background:rgba(40,16,18,.80);border:3px solid #FF7A6B;box-shadow:0 0 34px rgba(255,122,107,.35)}
.ic{width:52px;height:52px;border-radius:50%;background:#FF7A6B;color:#1b0d0d;font-size:36px;font-weight:800;
  display:flex;align-items:center;justify-content:center}
""")

# 4) Transición "Volvamos a intentarlo"
pages["volvamos"] = page(f"""
<div class='veil'></div>
<div class='c'>{svg("<path d='M8 24a16 16 0 1 0 5-11.6'/><path d='M8 6v8h8'/>", size=150)}
<div class='t'>Volvamos a intentarlo</div></div>""", """
.veil{position:absolute;inset:0;background:rgba(8,14,26,.80)}
.c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px}
.t{font-family:'Inter Display','Inter';font-weight:700;font-size:104px;letter-spacing:-1px}
""")

# 5) Palabras de la escena 5 (se acumulan)
PAL = ["Atención", "Percepción", "Regulación emocional"]
for k in range(1, 4):
    items = "".join(f"<div class='p{' cur' if i == k-1 else ''}'>{w}</div>" for i, w in enumerate(PAL[:k]))
    pages[f"palabras_{k}"] = page(f"<div class='veil'></div><div class='col'>{items}</div>", """
.veil{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,14,26,.62) 0%,rgba(8,14,26,.25) 32%,rgba(8,14,26,0) 55%)}
.col{position:absolute;left:110px;top:120px;display:flex;flex-direction:column;gap:24px;align-items:flex-start}
.p{font-weight:700;font-size:52px;padding:18px 34px 18px 30px;border-radius:18px;background:rgba(12,22,38,.80);
  border-left:10px solid rgba(95,211,198,.55);color:rgba(247,249,252,.82)}
.p.cur{border-left-color:#5FD3C6;color:#F7F9FC;box-shadow:0 0 36px rgba(95,211,198,.35)}
""")

# 6) Cierre: título + placa de referencias
pages["cierre"] = page("""
<div class='veil'></div>
<div class='c'>
  <div class='bar'></div>
  <h1>Neuroliderazgo</h1>
  <h2>en el ámbito laboral</h2>
  <div class='ref'>Referencias: Rock, 2008; Simon, 1955; Tversky y Kahneman, 1974; Gross, 1998; Edmondson, 1999</div>
</div>""", """
.veil{position:absolute;inset:0;background:rgba(8,14,26,.74)}
.c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.bar{width:120px;height:8px;border-radius:4px;background:#5FD3C6;margin-bottom:34px}
h1{font-family:'Inter Display','Inter';font-weight:700;font-size:124px;letter-spacing:-2px;line-height:1}
h2{font-weight:300;font-size:66px;margin-top:16px;color:rgba(247,249,252,.92)}
.ref{margin-top:84px;font-size:31px;color:rgba(247,249,252,.88);padding:22px 40px;border-radius:16px;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16)}
""")

(OUT / "pages.json").write_text(json.dumps(pages, ensure_ascii=False))
print(len(pages), "páginas")
