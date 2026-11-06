// Composición: dos capas (para fundidos), gráficos superpuestos, destello y fundido final.
const W = 1920, H = 1080;
let layers = [], OVS = [], flash, black;
function makeLayer() {
  const div = document.createElement('div'); div.className = 'layer'; document.getElementById('stage').appendChild(div);
  const mk = Cls => { const svg = S('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}` }); div.appendChild(svg); return { svg, sc: new Cls(svg) }; };
  return { div, scenes: { office: mk(Office), meeting: mk(Meeting), team: mk(Team) } };
}
function init(tl) {
  TL = tl;
  layers = [makeLayer(), makeLayer()];
  const st = document.getElementById('stage');
  for (const o of TL.overlays) {
    const img = document.createElement('img'); img.className = 'ov'; img.src = '../gfx/' + o.name + '.png'; st.appendChild(img);
    OVS.push(Object.assign({ img }, o));
  }
  flash = document.createElement('div'); flash.id = 'flash'; st.appendChild(flash);
  black = document.createElement('div'); black.id = 'black'; st.appendChild(black);
}
const camT = c => `translate(${W / 2},${H / 2}) scale(${c[2]}) translate(${-c[0]},${-c[1]})`;
function renderAt(t) {
  let act = TL.shots.filter(s => s.a <= t && t < s.b);
  if (!act.length) act = [TL.shots[TL.shots.length - 1]];
  layers.forEach(L => L.div.style.display = 'none');
  act.slice(0, 2).forEach((sh, i) => {
    const L = layers[i]; L.div.style.display = 'block';
    for (const k in L.scenes) L.scenes[k].svg.style.display = k === sh.scene ? 'block' : 'none';
    const sc = L.scenes[sh.scene].sc;
    sc.update(sh.freezeAt != null ? sh.freezeAt : t);
    const p = clamp((t - sh.cut) / Math.max(1e-3, sh.end - sh.cut), 0, 1);
    let q = p, filter = '', tr = '';
    if (sh.fx === 'rewind') q = 1 - Math.pow(1 - clamp((t - sh.cut) / 0.8, 0, 1), 3);
    const cam = [0, 1, 2].map(k => lerp(sh.cam0[k], sh.cam1[k], q));
    if (sh.fx === 'freeze') filter = 'saturate(.25) brightness(.8) blur(5px)';
    else if (sh.fx === 'dim') filter = 'saturate(.35) brightness(.9)';
    else if (sh.fx === 'rewind') { filter = `saturate(${.3 + .3 * q}) brightness(.85) blur(${(1 - q) * 7 + 2}px)`; tr = `translateX(${Math.sin(t * 90) * 10 * (1 - q)}px)`; }
    else if (sh.fx === 'cool') filter = 'saturate(.86) hue-rotate(-6deg) brightness(.98)';
    else if (sh.fx === 'warm') filter = 'sepia(.06) saturate(1.06)';
    sc.cam.setAttribute('transform', camT(cam));
    L.div.style.filter = filter; L.div.style.transform = tr;
    L.div.style.opacity = i === 1 ? clamp((t - sh.a) / Math.max(1e-3, act[0].b - sh.a), 0, 1) : 1;
    L.div.style.zIndex = i + 1;
  });
  for (const o of OVS) {
    let al = 0;
    if (o.a <= t && t < o.b) { al = 1; if (o.fi > 0) al = Math.min(al, (t - o.a) / o.fi); if (o.fo > 0) al = Math.min(al, (o.b - t) / o.fo); }
    o.img.style.opacity = al; o.img.style.display = al > 0 ? 'block' : 'none';
  }
  const dt = t - TL.esc.E3[0];
  flash.style.opacity = dt >= 0 && dt < .5 ? .22 * (1 - dt / .5) : 0;
  black.style.opacity = t > TL.dur - 1 ? clamp(t - (TL.dur - 1), 0, 1) : 0;
}
