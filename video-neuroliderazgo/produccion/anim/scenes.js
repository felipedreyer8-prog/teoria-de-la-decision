// Escenarios (oficina, sala de reuniones, mesa de equipo) y su comportamiento en el tiempo global t.
let TL = null;
function cue(id) { return TL.cues[id]; }
function envAt(id, t) {
  const c = TL.cues[id]; if (!c || t < c.a || t >= c.b) return 0;
  const e = TL.env[id]; const i = Math.floor((t - c.a) * TL.fps);
  return e[Math.min(i, e.length - 1)] || 0;
}
function talk(voz, t) {
  let m = 0;
  for (const id in TL.cues) { const c = TL.cues[id]; if (c.voz === voz && t >= c.a && t < c.b) m = Math.max(m, envAt(id, t)); }
  return m;
}
const R = (t, t0, d) => ease((t - t0) / d);            // rampa 0→1
const mix = (a, b, p) => Array.isArray(a) ? a.map((v, i) => typeof v === 'number' ? lerp(v, b[i], p) : (p < .5 ? v : b[i])) : lerp(a, b, p);
function mixArms(A, B, p) { return [mix(A[0], B[0], p), mix(A[1], B[1], p)]; }
function blend(sa, sb, p) { const o = Object.assign({}, sa); for (const k in sb) { if (k === 'arms') o.arms = mixArms(sa.arms, sb.arms, p); else if (typeof sb[k] === 'number' && typeof sa[k] === 'number') o[k] = lerp(sa[k], sb[k], p); else if (p >= .5) o[k] = sb[k]; } return o; }

// ---------- utilidades de dibujo
function plantMonstera(g, x, y, s = 1) {
  const p = S('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  const leaves = [[-70, -250, -35], [40, -290, 20], [-10, -330, -5], [85, -200, 45], [-95, -170, -60], [10, -210, 8]];
  for (const [lx, ly, r] of leaves) {
    S('line', { x1: 0, y1: -40, x2: lx * .7, y2: ly * .7, stroke: '#2F6B47', 'stroke-width': 5 }, p);
    const lg = S('g', { transform: `translate(${lx},${ly}) rotate(${r})` }, p);
    S('ellipse', { cx: 0, cy: 0, rx: 52, ry: 40, fill: '#3A8A5B' }, lg);
    S('path', { d: 'M-52,0 L52,0', stroke: '#2C6E48', 'stroke-width': 3 }, lg);
    for (const k of [-30, -8, 14, 34]) S('path', { d: `M${k},-6 L${k + 6},-34 M${k},6 L${k + 6},34`, stroke: '#EEF1F3', 'stroke-width': 4 }, lg);
  }
  S('path', { d: 'M-60,-40 L60,-40 L48,40 L-48,40 Z', fill: '#FBFBFA' }, p);
  S('path', { d: 'M20,-40 L60,-40 L48,40 L30,40 Z', fill: '#000', opacity: .06 }, p);
}
function plantFig(g, x, y, s = 1) {
  const p = S('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  S('path', { d: 'M0,-40 C-6,-160 8,-260 0,-380', stroke: '#6B4E37', 'stroke-width': 9, fill: 'none' }, p);
  const lv = [[-40, -120, -40], [36, -150, 35], [-34, -200, -30], [40, -240, 30], [-26, -290, -20], [28, -330, 20], [0, -380, 0], [-44, -250, -50]];
  for (const [lx, ly, r] of lv) S('ellipse', { cx: lx, cy: ly, rx: 24, ry: 38, fill: lx < 0 ? '#2F7A4E' : '#3B8C5C', transform: `rotate(${r},${lx},${ly})` }, p);
  S('path', { d: 'M-46,-40 L46,-40 L38,36 L-38,36 Z', fill: '#C86F4A' }, p);
}
function officeBack(g, opts = {}) {
  S('rect', { x: -400, y: -200, width: 2720, height: 980, fill: '#EDF0F2' }, g);
  S('rect', { x: -400, y: -200, width: 2720, height: 236, fill: '#E2E6E9' }, g);
  // ventanales
  const w = S('g', {}, g);
  const sky = S('linearGradient', { id: 'sky' + (opts.id || ''), x1: 0, y1: 0, x2: 0, y2: 1 }, S('defs', {}, g));
  S('stop', { offset: 0, 'stop-color': '#BFDDEF' }, sky); S('stop', { offset: 1, 'stop-color': '#EAF4FA' }, sky);
  S('rect', { x: 40, y: 110, width: 600, height: 560, fill: `url(#sky${opts.id || ''})` }, w);
  for (const [bx, bw, bh] of [[60, 90, 230], [160, 70, 300], [240, 110, 200], [360, 80, 340], [450, 120, 260], [580, 60, 190]])
    S('rect', { x: bx, y: 670 - bh, width: bw, height: bh, fill: '#C3D5E1' }, w);
  for (const [bx, bw, bh] of [[100, 60, 150], [300, 90, 170], [520, 70, 130]])
    S('rect', { x: bx, y: 670 - bh, width: bw, height: bh, fill: '#B3C8D6' }, w);
  S('rect', { x: 40, y: 110, width: 600, height: 560, fill: 'none', stroke: '#AEBCC6', 'stroke-width': 10 }, w);
  for (const x of [240, 440]) S('rect', { x: x - 4, y: 110, width: 8, height: 560, fill: '#AEBCC6' }, w);
  S('rect', { x: 40, y: 386, width: 600, height: 8, fill: '#AEBCC6' }, w);
  // paneles de madera
  S('rect', { x: 1330, y: 96, width: 590, height: 684, fill: '#CFA87F' }, g);
  for (let x = 1338; x < 1920; x += 26) S('rect', { x, y: 96, width: 11, height: 684, fill: '#BB9168' }, g);
  // lámparas colgantes
  for (const x of [470, 960, 1450]) {
    S('line', { x1: x, y1: 36, x2: x, y2: 150, stroke: '#3A3F46', 'stroke-width': 2 }, g);
    S('path', { d: `M${x - 46},196 L${x - 22},150 L${x + 22},150 L${x + 46},196 Z`, fill: '#2F343B' }, g);
    S('ellipse', { cx: x, cy: 200, rx: 70, ry: 14, fill: '#FFF2CF', opacity: .55 }, g);
  }
  // piso
  S('rect', { x: -400, y: 780, width: 2720, height: 500, fill: '#D6DADE' }, g);
  S('rect', { x: -400, y: 776, width: 2720, height: 8, fill: '#C2C8CD' }, g);
}
function deskSmall(g, x, floorY, s) { // escritorio del fondo con monitor de espaldas
  const d = S('g', { transform: `translate(${x},${floorY}) scale(${s})` }, g);
  S('rect', { x: -200, y: -287, width: 400, height: 20, fill: '#FFFFFF' }, d);
  S('rect', { x: -186, y: -267, width: 14, height: 267, fill: '#C9CED3' }, d);
  S('rect', { x: 172, y: -267, width: 14, height: 267, fill: '#C9CED3' }, d);
  S('rect', { x: -170, y: -267, width: 340, height: 150, fill: '#EEF0F2' }, d);
  return d;
}
function monitorBack(g, x, floorY, s) {
  const d = S('g', { transform: `translate(${x},${floorY}) scale(${s})` }, g);
  S('rect', { x: -14, y: -330, width: 28, height: 45, fill: '#3B4047' }, d);
  S('rect', { x: -120, y: -450, width: 240, height: 140, rx: 8, fill: '#3B4047' }, d);
  S('ellipse', { cx: 0, cy: -289, rx: 50, ry: 6, fill: '#2E3238' }, d);
}
function chairBack(g, x, y, s = 1, h = 220) {
  S('rect', { x: x - 82 * s, y: y - 30 * s, width: 164 * s, height: h * s, rx: 30 * s, fill: '#3A3F47' }, g);
}

// ---------- monitor con la presentación (gráfico de barras)
class Slide {
  constructor(g, x, y, w, h) {
    this.g = S('g', { transform: `translate(${x},${y})` }, g);
    S('rect', { x: 0, y: 0, width: w, height: h, fill: '#FFFFFF' }, this.g);
    S('rect', { x: 18, y: 16, width: w * .5, height: 14, rx: 3, fill: '#4E9890' }, this.g);
    S('rect', { x: 18, y: 38, width: w * .32, height: 7, rx: 3, fill: '#C9D3DA' }, this.g);
    const bx = 30, by = h - 22, bw = (w - 90) / 4;
    S('line', { x1: bx - 8, y1: by, x2: w - 26, y2: by, stroke: '#9AA6AF', 'stroke-width': 2 }, this.g);
    this.vals = [0.45, 0.72, 0.30, 0.58]; this.h = h - 80;
    this.bars = this.vals.map((v, i) => S('rect', { x: bx + i * (bw + 10), y: by - v * this.h, width: bw, height: v * this.h, rx: 3, fill: '#8DB9D8' }, this.g));
    this.bx = bx; this.by = by; this.bw = bw;
    this.ring = S('ellipse', { cx: bx + 2 * (bw + 10) + bw / 2, cy: by - .3 * this.h / 2 - 10, rx: bw * .9, ry: this.h * .32, fill: 'none', stroke: '#E0453A', 'stroke-width': 5, opacity: 0 }, this.g);
    this.check = S('path', { d: `M${w - 64},40 l14,14 l28,-30`, stroke: '#2FA57A', 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', opacity: 0 }, this.g);
  }
  set(err, fix, ring) { // err: 0..1 resalta la barra con error; fix: 0..1 corrección
    const v = lerp(0.30, 0.66, fix);
    const b = this.bars[2];
    b.setAttribute('y', this.by - v * this.h); b.setAttribute('height', v * this.h);
    const red = err * (1 - fix);
    b.setAttribute('fill', red > .5 ? '#E0453A' : fix > .5 ? '#4E9890' : '#8DB9D8');
    this.ring.setAttribute('opacity', ring);
    this.ring.setAttribute('cy', this.by - v * this.h / 2);
    this.check.setAttribute('opacity', clamp((fix - .6) / .4, 0, 1));
  }
}

// ======================================================= OFICINA
class Office {
  constructor(svg) {
    this.cam = S('g', {}, svg);
    const g = this.cam;
    officeBack(g, { id: 'o' + Math.random().toString(36).slice(2, 6) });
    plantMonstera(g, 110, 1010, 1.15);
    plantFig(g, 1868, 1010, 1.2);
    // compañeros al fondo
    const s2 = 0.72, f2 = 890;
    this.cowA = new Person(g, 'cowA'); deskSmall(g, 300, f2, s2); monitorBack(g, 300, f2, s2);
    this.cowB = new Person(g, 'cowB'); deskSmall(g, 1665, f2, s2); monitorBack(g, 1665, f2, s2);
    this.cA = { x: 300, y: f2 - 372 * s2, sc: s2 }; this.cB = { x: 1665, y: f2 - 372 * s2, sc: s2 };
    // jefe (detrás del escritorio principal)
    this.jefe = new Person(g, 'jefe');
    // Lucía + silla + escritorio + monitor
    chairBack(g, 720, 690);
    this.lucia = new Person(g, 'lucia');
    S('rect', { x: 560, y: 753, width: 800, height: 24, fill: '#FFFFFF' }, g);
    S('rect', { x: 560, y: 775, width: 800, height: 6, fill: '#E1E5E8' }, g);
    S('rect', { x: 600, y: 781, width: 720, height: 170, fill: '#EEF0F2' }, g);
    S('rect', { x: 576, y: 781, width: 18, height: 260, fill: '#C9CED3' }, g);
    S('rect', { x: 1326, y: 781, width: 18, height: 260, fill: '#C9CED3' }, g);
    // monitor
    S('ellipse', { cx: 1050, cy: 752, rx: 80, ry: 9, fill: '#2B2F36' }, g);
    S('rect', { x: 1038, y: 700, width: 24, height: 54, fill: '#3A3F46' }, g);
    S('rect', { x: 830, y: 470, width: 440, height: 240, rx: 10, fill: '#2B2F36' }, g);
    this.slide = new Slide(g, 842, 482, 416, 216);
    // teclado, mouse, taza
    S('rect', { x: 840, y: 741, width: 170, height: 13, rx: 4, fill: '#D5DADF' }, g);
    S('ellipse', { cx: 1150, cy: 748, rx: 15, ry: 7, fill: '#D5DADF' }, g);
    S('rect', { x: 640, y: 712, width: 34, height: 42, rx: 6, fill: '#E6ECF0' }, g);
    S('path', { d: 'M674,722 q16,0 16,12 q0,12 -16,12', stroke: '#E6ECF0', 'stroke-width': 6, fill: 'none' }, g);
  }
  update(t) {
    const E = TL.esc, J1 = cue('J1'), L1 = cue('L1'), J2 = cue('J2'), m = TL.marks;
    const late = t >= E.E4[0];          // escena 5c: Lucía corrige sola
    // ---- jefe
    let jx = 2350, walking = false, ph = 0;
    if (!late) {
      if (t >= m.walk0 && t < m.walk1) { const p = (t - m.walk0) / (m.walk1 - m.walk0); jx = lerp(2350, 1410, p); walking = true; ph = (t - m.walk0) * 6.0; }
      else if (t >= m.walk1) jx = 1410;
    }
    const relaxed = [[-8, 4, 'fist'], [8, -4, 'fist']];
    const crossed = [[-24, 74, 'fist'], [24, -74, 'fist']];
    const point = [[-80, -84, 'point'], [8, -4, 'fist']];
    const dismiss = [[-22, -172, 'open'], [8, -4, 'fist']];
    let js = { x: jx, y: 540, standing: true, walking, walk: ph, turn: -0.35, gx: -0.6, gy: 0.2, browIn: 0, smile: 0.05, arms: relaxed };
    if (walking) { const sw = Math.sin(ph); js.arms = [[-8 - sw * 14, 4, 'fist'], [8 - sw * 14, -4, 'fist']]; js.lift = Math.abs(Math.cos(ph)) * 4; }
    const angry = { browIn: -1, smile: -0.6, turn: -0.55, gx: -1, gy: 0.5 };
    if (t >= J1.a - 0.4) {
      js = blend(js, Object.assign({}, angry, { arms: point }), R(t, J1.a - 0.4, 0.35));
      if (t >= J1.b) js = blend(js, Object.assign({}, angry, { arms: crossed, gy: 0.9 }), R(t, J1.b, 0.4));
      if (t >= J2.a - 0.2) js = blend(js, Object.assign({}, angry, { arms: dismiss, browIn: -1.2 }), R(t, J2.a - 0.2, 0.3));
      if (t >= J2.b + 0.2) js = blend(js, Object.assign({}, angry, { arms: crossed, browIn: -0.8, smile: -0.5 }), R(t, J2.b + 0.2, 0.45));
    }
    js.open = talk('jefe', t); js.blink = blinkAt(t, 3);
    if (js.open > 0) js.nod = Math.sin(t * 7) * 1.5 * js.open;
    this.jefe.set(js);
    // ---- Lucía
    const typing = Math.sin(t * 11) * 4, typing2 = Math.sin(t * 9 + 1.3) * 4;
    const desk = [[30, 100 + typing, 'fist'], [40, 115 + typing2, 'fist']];
    const still = [[30, 100, 'fist'], [40, 115, 'fist']];
    let ls = { x: 720, y: 668, turn: 0.55, gx: 1, gy: 0.25, smile: 0.15, browIn: 0, arms: desk };
    if (!late && t >= m.walk1 - 0.8) ls = blend(ls, { turn: 0.85, gx: 1, gy: -0.9, browIn: 0.3, smile: 0.1, arms: still }, R(t, m.walk1 - 0.8, 0.5));
    if (!late && t >= J1.a) ls = blend(ls, { browIn: 1, smile: -0.35, lift: 5, gy: -1 }, R(t, J1.a, 0.4));
    if (!late && t >= L1.a - 0.2) ls = blend(ls, { browIn: 0.85, arms: [[-50, -160, 'open'], [40, 115, 'fist']] }, R(t, L1.a - 0.2, 0.3));
    if (!late && t >= L1.b + 0.1) ls = blend(ls, { arms: still }, R(t, L1.b + 0.1, 0.35));
    if (!late && t >= J2.a) ls = blend(ls, { browIn: 1.25, smile: -0.5, tilt: -4 }, R(t, J2.a, 0.3));
    if (!late && t >= J2.b + 0.6) ls = blend(ls, { gy: 1, gx: 0.3, turn: 0.3, tilt: -5, browIn: 0.9, smile: -0.4, lift: 4 }, R(t, J2.b + 0.6, 0.8));
    if (late) ls = { x: 720, y: 668, turn: 0.55, gx: 1, gy: 0.25, smile: 0.35, browIn: 0, arms: desk };
    ls.open = talk('lucia', t); ls.blink = blinkAt(t, 7);
    this.lucia.set(ls);
    // ---- compañeros
    const look = !late && t >= J1.a - 0.2 ? R(t, J1.a - 0.2, 0.5) : 0;
    this.cowA.set(Object.assign({}, this.cA, { turn: lerp(0, 0.8, look), gx: lerp(0, 1, look), gy: lerp(0.8, 0.1, look), browIn: 0.5 * look, smile: 0.05, blink: blinkAt(t, 11), arms: [[-10, 30, 'fist'], [10, -30, 'fist']] }));
    this.cowB.set(Object.assign({}, this.cB, { turn: lerp(0, -0.8, look), gx: lerp(0, -1, look), gy: lerp(0.8, 0.1, look), browIn: 0.5 * look, smile: 0.05, blink: blinkAt(t, 5), arms: [[-10, 30, 'fist'], [10, -30, 'fist']] }));
    // ---- pantalla
    const err = !late && t >= J1.a - 0.4 ? R(t, J1.a - 0.4, 0.3) : 0;
    const ring = err * (0.75 + 0.25 * Math.sin(t * 6));
    const fix = late ? R(t, m.fix0, 1.6) : 0;
    this.slide.set(late ? 1 : err, fix, late ? 0 : ring);
  }
}

// ======================================================= SALA DE REUNIONES
class Meeting {
  constructor(svg) {
    this.cam = S('g', {}, svg);
    const g = this.cam;
    S('rect', { x: -400, y: -200, width: 2720, height: 1000, fill: '#E8EFF3' }, g);
    // oficina vista a través del vidrio (suave)
    const bgo = S('g', { opacity: .5 }, g);
    for (const [x, w] of [[120, 300], [560, 260], [1180, 320], [1600, 260]]) {
      S('rect', { x, y: 600, width: w, height: 16, fill: '#FFFFFF' }, bgo);
      S('rect', { x: x + 20, y: 616, width: 12, height: 170, fill: '#C3CAD0' }, bgo);
      S('rect', { x: x + w - 32, y: 616, width: 12, height: 170, fill: '#C3CAD0' }, bgo);
      S('rect', { x: x + w / 2 - 60, y: 520, width: 120, height: 78, rx: 6, fill: '#9FAAB3' }, bgo);
    }
    for (const x of [450, 1080, 1520]) { S('ellipse', { cx: x, cy: 560, rx: 42, ry: 74, fill: '#7FB08E' }, bgo); S('rect', { x: x - 24, y: 620, width: 48, height: 56, fill: '#F4F4F2' }, bgo); }
    S('rect', { x: -400, y: -200, width: 2720, height: 1000, fill: '#FFFFFF', opacity: .35 }, g);
    for (let x = 0; x <= 1920; x += 384) S('rect', { x: x - 6, y: 60, width: 12, height: 740, fill: '#AEBAC3' }, g);
    S('rect', { x: -400, y: 54, width: 2720, height: 12, fill: '#AEBAC3' }, g);
    for (const x of [200, 900, 1500]) S('path', { d: `M${x},70 L${x + 140},70 L${x - 60},790 L${x - 200},790 Z`, fill: '#FFFFFF', opacity: .18 }, g);
    S('rect', { x: -400, y: 790, width: 2720, height: 500, fill: '#D3D8DC' }, g);
    S('rect', { x: -400, y: 786, width: 2720, height: 8, fill: '#BFC6CC' }, g);
    plantFig(g, 1810, 1010, 1.1);
    chairBack(g, 690, 690, 1, 120); chairBack(g, 1230, 690, 1, 120);
    this.jefe = new Person(g, 'jefe');
    this.lucia = new Person(g, 'lucia');
    // mesa redonda
    S('ellipse', { cx: 960, cy: 800, rx: 310, ry: 40, fill: '#FFFFFF' }, g);
    S('path', { d: 'M650,800 a310,40 0 0 0 620,0 l0,12 a310,40 0 0 1 -620,0 Z', fill: '#DDE2E6' }, g);
    S('rect', { x: 942, y: 850, width: 36, height: 160, fill: '#C3C9CF' }, g);
    S('ellipse', { cx: 960, cy: 1012, rx: 120, ry: 13, fill: '#B5BCC2' }, g);
    // laptop
    S('rect', { x: 880, y: 778, width: 160, height: 12, rx: 3, fill: '#C9CED3' }, g);
    S('rect', { x: 892, y: 680, width: 136, height: 100, rx: 6, fill: '#2B2F36' }, g);
    this.slide = new Slide(g, 900, 688, 120, 84);
    S('rect', { x: 720, y: 786, width: 90, height: 10, fill: '#F7F7F5', transform: 'rotate(-4,765,790)' }, g);
  }
  update(t) {
    const ids = ['J3', 'L2', 'J4', 'L3', 'J5'], c = {}; ids.forEach(i => c[i] = cue(i));
    const E = TL.esc;
    const rest = [[-20, 60, 'fist'], [20, -60, 'fist']];
    let js = { x: 690, y: 668, turn: 0.5, gx: 1, gy: 0.1, smile: 0.2, browIn: 0.1, arms: rest };
    let ls = { x: 1230, y: 668, turn: -0.5, gx: -1, gy: 0.1, smile: 0.15, browIn: 0.15, arms: rest };
    const palm = [[-20, 60, 'fist'], [62, 140, 'open']];
    const lPalm = [[-62, -140, 'open'], [20, -60, 'fist']];
    if (t >= c.J3.a - .3) js = blend(js, { arms: palm, smile: 0.25 }, R(t, c.J3.a - .3, .4));
    if (t >= c.J3.b) js = blend(js, { arms: rest }, R(t, c.J3.b, .4));
    if (t >= c.L2.a - .2) ls = blend(ls, { arms: lPalm, browIn: 0.3 }, R(t, c.L2.a - .2, .4));
    if (t >= c.L2.b) ls = blend(ls, { arms: rest, browIn: 0.1 }, R(t, c.L2.b, .4));
    if (t >= c.J4.a - .2) js = blend(js, { arms: [[-20, 60, 'fist'], [55, 128, 'open']], smile: 0.35 }, R(t, c.J4.a - .2, .4));
    if (t >= c.J4.b) js = blend(js, { arms: rest }, R(t, c.J4.b, .4));
    if (t >= c.L3.a - .2) ls = blend(ls, { arms: [[-58, -120, 'open'], [20, -60, 'fist']], smile: 0.35, browIn: 0 }, R(t, c.L3.a - .2, .4));
    if (t >= c.L3.b) ls = blend(ls, { arms: rest, smile: 0.45 }, R(t, c.L3.b, .4));
    if (t >= c.J5.a - .2) js = blend(js, { arms: [[-20, 60, 'fist'], [50, 150, 'open']], smile: 0.5 }, R(t, c.J5.a - .2, .4));
    if (t >= c.J5.b + .3) { js = blend(js, { arms: rest, turn: 0.3, gx: 0.8, gy: 0.9, smile: 0.4 }, R(t, c.J5.b + .3, .6)); ls = blend(ls, { turn: -0.3, gx: -0.8, gy: 0.9, smile: 0.4, arms: [[-35, -95, 'fist'], [20, -60, 'fist']] }, R(t, c.J5.b + .3, .6)); }
    // escena 5: el jefe escucha; revisan juntos
    if (t >= E.E5[0]) {
      js = { x: 690, y: 668, turn: 0.5, gx: 1, gy: 0.1, smile: 0.25, browIn: 0.2, arms: rest, nod: Math.sin(t * 2.2) * 3 };
      ls = { x: 1230, y: 668, turn: -0.5, gx: -1, gy: 0, smile: 0.3, arms: [[-55 + Math.sin(t * 2) * 8, -135, 'open'], [20, -60, 'fist']] };
      if (t >= TL.marks.review) {
        const p = R(t, TL.marks.review, .6);
        js = blend(js, { turn: 0.35, gx: 0.9, gy: 1, lean: 3, nod: 0 }, p);
        ls = blend(ls, { turn: -0.35, gx: -0.9, gy: 1, arms: [[-62, -100, 'point'], [20, -60, 'fist']] }, p);
      }
    }
    // asentir al escuchar
    const jt = talk('jefe', t), lt = talk('lucia', t);
    js.open = jt; ls.open = lt;
    if (lt > 0 && t < E.E5[0]) js.nod = Math.sin(t * 3) * 2.5;
    if (jt > 0) { ls.nod = Math.sin(t * 2.6) * 2; js.nod = (js.nod || 0) + Math.sin(t * 7) * 1.4 * jt; }
    if (lt > 0) ls.nod = (ls.nod || 0) + Math.sin(t * 7.5) * 1.4 * lt;
    js.blink = blinkAt(t, 3); ls.blink = blinkAt(t, 7);
    this.jefe.set(js); this.lucia.set(ls);
    this.slide.set(0, 0, 0);
  }
}

// ======================================================= MESA DE EQUIPO
class Team {
  constructor(svg) {
    this.cam = S('g', {}, svg);
    const g = this.cam;
    officeBack(g, { id: 't' + Math.random().toString(36).slice(2, 6) });
    plantMonstera(g, 110, 1010, 1.1);
    plantFig(g, 1830, 1010, 1.15);
    for (const x of [520, 820, 1110, 1410]) chairBack(g, x, 670, 1, 140);
    this.p = [new Person(g, 'cowA'), new Person(g, 'lucia'), new Person(g, 'jefe'), new Person(g, 'cowB')];
    S('rect', { x: 300, y: 790, width: 1320, height: 22, fill: '#FFFFFF' }, g);
    S('rect', { x: 300, y: 810, width: 1320, height: 6, fill: '#E1E5E8' }, g);
    S('rect', { x: 330, y: 816, width: 1260, height: 150, fill: '#EEF0F2' }, g);
    S('rect', { x: 316, y: 816, width: 18, height: 224, fill: '#C9CED3' }, g);
    S('rect', { x: 1586, y: 816, width: 18, height: 224, fill: '#C9CED3' }, g);
    S('rect', { x: 890, y: 780, width: 160, height: 12, rx: 3, fill: '#C9CED3' }, g);
    S('rect', { x: 902, y: 682, width: 136, height: 100, rx: 6, fill: '#2B2F36' }, g);
    this.slide = new Slide(g, 910, 690, 120, 84);
    for (const [x, r] of [[560, -6], [700, 5], [1240, -4], [1370, 7]]) {
      const pg = S('g', { transform: `rotate(${r},${x + 45},786)` }, g);
      S('rect', { x, y: 778, width: 90, height: 14, fill: '#FAFAF8' }, pg);
    }
  }
  update(t) {
    const xs = [520, 820, 1110, 1410];
    const base = [
      { turn: 0.5, gx: 1, smile: 0.45, arms: [[-20, 60, 'fist'], [30, -40, 'fist']] },
      { turn: 0.4, gx: 1, gy: 0.6, smile: 0.5, arms: [[-20, 60, 'fist'], [58, 112, 'point']] },
      { turn: -0.4, gx: -1, gy: 0.6, smile: 0.5, arms: [[-30, 70, 'fist'], [20, -60, 'fist']] },
      { turn: -0.5, gx: -1, smile: 0.45, arms: [[-30, 40, 'fist'], [20, -60, 'fist']] },
    ];
    this.p.forEach((pp, i) => {
      const s = Object.assign({ x: xs[i], y: 650, browIn: 0.1 }, base[i]);
      s.nod = Math.sin(t * (1.6 + i * .3) + i) * 2.2;
      s.blink = blinkAt(t, 2 + i * 3);
      if (i === 1) s.arms[1][1] = 112 + Math.sin(t * 1.5) * 6;
      pp.set(s);
    });
    this.slide.set(1, 1, 0);
  }
}
