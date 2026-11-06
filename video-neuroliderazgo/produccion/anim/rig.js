// Personajes vectoriales (vista frontal, estilo plano) con rig simple.
const NS = 'http://www.w3.org/2000/svg';
function S(tag, attrs = {}, parent = null) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
const D2R = Math.PI / 180;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, p) => a + (b - a) * p;
const ease = p => p < 0 ? 0 : p > 1 ? 1 : p * p * (3 - 2 * p);
function shade(hex, f) { // f<1 oscurece, f>1 aclara
  const n = parseInt(hex.slice(1), 16);
  let r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  if (f < 1) { r *= f; g *= f; b *= f; } else { r += (255 - r) * (f - 1); g += (255 - g) * (f - 1); b += (255 - b) * (f - 1); }
  return '#' + [r, g, b].map(v => Math.round(clamp(v, 0, 255)).toString(16).padStart(2, '0')).join('');
}

const PEOPLE = {
  lucia: { skin: '#D6A07A', hair: '#33241D', shirt: '#4E9890', pants: '#2E3540', style: 'blouse', hairStyle: 'long', earrings: true, sleeve: 'three' },
  jefe: { skin: '#DDAA88', hair: '#4A3B32', grey: '#A39C96', shirt: '#AFC8E4', pants: '#4A4F57', style: 'dress', hairStyle: 'short', beard: '#8D847D', watch: true, sleeve: 'rolled' },
  cowA: { skin: '#C08A66', hair: '#1D1D22', shirt: '#8D9298', pants: '#3A3F47', style: 'sweater', hairStyle: 'shortBlack', glasses: true, sleeve: 'long' },
  cowB: { skin: '#EDC2A2', hair: '#9C4E2C', shirt: '#2C3D66', pants: '#2C2F36', style: 'cardigan', hairStyle: 'curly', sleeve: 'long' },
};

class Person {
  constructor(parent, who) {
    this.who = who; this.p = PEOPLE[who];
    const p = this.p;
    this.root = S('g', {}, parent);
    this.legsG = S('g', {}, this.root);
    this.hairBackG = S('g', {}, this.root);
    this.armBack = [S('g', {}, this.root), S('g', {}, this.root)];
    this.torsoG = S('g', {}, this.root);
    this.headG = S('g', {}, this.root);
    this.armFront = [S('g', {}, this.root), S('g', {}, this.root)];
    // piernas (solo de pie)
    this.legs = [0, 1].map(i => {
      const g = S('g', {}, this.legsG);
      S('path', { d: 'M-24,0 L24,0 L20,290 L-20,290 Z', fill: p.pants }, g);
      S('ellipse', { cx: i ? 12 : -12, cy: 300, rx: 34, ry: 14, fill: '#2A2A2E' }, g);
      return g;
    });
    // pelo de atrás
    if (p.hairStyle === 'long') {
      S('path', { d: 'M-92,-120 C-112,-40 -104,10 -88,58 C-72,96 -40,92 -30,70 L30,70 C40,92 72,96 88,58 C104,10 112,-40 92,-120 C80,-200 -80,-200 -92,-120 Z', fill: p.hair }, this.hairBackG);
      S('path', { d: 'M-80,-60 C-92,0 -84,40 -70,70', stroke: shade(p.hair, 1.25), 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round', opacity: .6 }, this.hairBackG);
      S('path', { d: 'M80,-60 C92,0 84,40 70,70', stroke: shade(p.hair, 1.25), 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round', opacity: .6 }, this.hairBackG);
    }
    if (p.hairStyle === 'curly') {
      for (const [x, y, r] of [[-62, -150, 30], [-30, -178, 32], [8, -184, 33], [44, -170, 31], [66, -140, 28], [-74, -110, 26], [76, -106, 25], [-70, -74, 22], [72, -72, 21]])
        S('circle', { cx: x, cy: y, r, fill: p.hair }, this.hairBackG);
    }
    // torso
    S('path', { d: 'M-76,18 C-76,4 -60,-4 -40,-6 L40,-6 C60,-4 76,4 76,18 L66,200 L-66,200 Z', fill: p.shirt }, this.torsoG);
    S('path', { d: 'M20,-6 L40,-6 C60,-4 76,4 76,18 L66,200 L34,200 Z', fill: '#000', opacity: .07 }, this.torsoG);
    S('rect', { x: -19, y: -46, width: 38, height: 48, rx: 10, fill: shade(p.skin, .93) }, this.torsoG);
    if (p.style === 'dress') {
      S('path', { d: 'M-22,-8 L0,22 L22,-8 L14,-14 L0,6 L-14,-14 Z', fill: shade(p.shirt, 1.18) }, this.torsoG);
      S('line', { x1: 0, y1: 22, x2: 0, y2: 198, stroke: shade(p.shirt, .86), 'stroke-width': 2 }, this.torsoG);
      for (const y of [52, 96, 140, 184]) S('circle', { cx: 0, cy: y, r: 3, fill: '#F4F7FA' }, this.torsoG);
      S('rect', { x: -66, y: 186, width: 132, height: 14, fill: '#2B2B30' }, this.torsoG);
    } else if (p.style === 'blouse') {
      S('path', { d: 'M-26,-6 Q0,26 26,-6 Z', fill: shade(p.skin, .97) }, this.torsoG);
      S('path', { d: 'M-27,-6 Q0,28 27,-6', stroke: shade(p.shirt, .82), 'stroke-width': 3, fill: 'none' }, this.torsoG);
    } else if (p.style === 'sweater') {
      S('path', { d: 'M-24,-6 Q0,16 24,-6', stroke: shade(p.shirt, .8), 'stroke-width': 7, fill: 'none' }, this.torsoG);
      S('rect', { x: -66, y: 186, width: 132, height: 14, fill: shade(p.shirt, .85) }, this.torsoG);
    } else if (p.style === 'cardigan') {
      S('path', { d: 'M-24,-6 L0,60 L24,-6 Z', fill: '#F2F2EE' }, this.torsoG);
      S('path', { d: 'M-24,-6 L0,60 L0,200 M24,-6 L0,60', stroke: shade(p.shirt, .7), 'stroke-width': 3, fill: 'none' }, this.torsoG);
      for (const y of [92, 130, 168]) S('circle', { cx: -7, cy: y, r: 3.4, fill: shade(p.shirt, 1.5) }, this.torsoG);
    }
    // cabeza
    const H = this.headG;
    this.headInner = S('g', {}, H);
    const hi = this.headInner;
    S('ellipse', { cx: -57, cy: -98, rx: 11, ry: 16, fill: shade(p.skin, .95) }, hi);
    S('ellipse', { cx: 57, cy: -98, rx: 11, ry: 16, fill: shade(p.skin, .95) }, hi);
    if (p.earrings) { S('circle', { cx: -58, cy: -82, r: 4.2, fill: '#E2B649' }, hi); S('circle', { cx: 58, cy: -82, r: 4.2, fill: '#E2B649' }, hi); }
    this.face = S('ellipse', { cx: 0, cy: -100, rx: 57, ry: 69, fill: p.skin }, hi);
    S('path', { d: 'M18,-160 C52,-150 62,-110 54,-70 C46,-44 26,-32 6,-31 C34,-50 42,-100 18,-160 Z', fill: '#000', opacity: .05 }, hi);
    // rasgos (se desplazan para simular giro de cabeza)
    this.feat = S('g', {}, hi);
    const F = this.feat;
    this.cheeks = [S('ellipse', { cx: -30, cy: -78, rx: 12, ry: 7, fill: '#E57C6B', opacity: .14 }, F), S('ellipse', { cx: 30, cy: -78, rx: 12, ry: 7, fill: '#E57C6B', opacity: .14 }, F)];
    this.eyes = [-22, 22].map(x => {
      const g = S('g', { transform: `translate(${x},-104)` }, F);
      const e = S('ellipse', { cx: 0, cy: 0, rx: 6.5, ry: 8.5, fill: '#2A211D' }, g);
      const hl = S('circle', { cx: 2.2, cy: -3, r: 2.1, fill: '#fff', opacity: .9 }, g);
      const lid = S('rect', { x: -10, y: -12, width: 20, height: 0, fill: p.skin }, g);
      return { g, e, hl, lid, x };
    });
    this.brows = [-22, 22].map(x => S('path', { d: '', stroke: p.hairStyle === 'curly' ? shade(p.hair, .7) : shade(p.hair, .9), 'stroke-width': 5.5, 'stroke-linecap': 'round', fill: 'none' }, F));
    S('path', { d: 'M0,-96 Q6,-80 -2,-76', stroke: shade(p.skin, .78), 'stroke-width': 3, fill: 'none', 'stroke-linecap': 'round' }, F);
    if (p.beard) {
      this.beard = S('path', { d: 'M-54,-96 C-54,-40 -30,-26 0,-26 C30,-26 54,-40 54,-96 C50,-74 40,-60 26,-58 C16,-66 -16,-66 -26,-58 C-40,-60 -50,-74 -54,-96 Z', fill: p.beard, opacity: .93 }, F);
      S('path', { d: 'M-20,-71 C-10,-78 10,-78 20,-71 C12,-68 -12,-68 -20,-71 Z', fill: shade(p.beard, .85) }, F);
    }
    this.mouthG = S('g', { transform: 'translate(0,-61)' }, F);
    this.mouthOpen = S('path', { d: '', fill: '#6A2A2A' }, this.mouthG);
    this.teeth = S('path', { d: '', fill: '#F7F4EE' }, this.mouthG);
    this.mouthLine = S('path', { d: '', stroke: '#7A3B32', 'stroke-width': 3.6, fill: 'none', 'stroke-linecap': 'round' }, this.mouthG);
    if (p.glasses) {
      const gl = S('g', { fill: 'none', stroke: '#1E1E22', 'stroke-width': 3.5 }, F);
      S('rect', { x: -38, y: -116, width: 30, height: 24, rx: 7 }, gl); S('rect', { x: 8, y: -116, width: 30, height: 24, rx: 7 }, gl);
      S('path', { d: 'M-8,-106 Q0,-111 8,-106' }, gl);
    }
    // pelo de adelante
    if (p.hairStyle === 'long') {
      S('path', { d: 'M-60,-108 C-66,-160 -30,-182 6,-178 C44,-176 68,-150 62,-104 C54,-126 40,-140 18,-146 C-4,-140 -30,-130 -44,-112 C-50,-96 -58,-84 -60,-108 Z', fill: p.hair }, hi);
      S('path', { d: 'M-46,-150 C-20,-166 18,-168 40,-150', stroke: shade(p.hair, 1.35), 'stroke-width': 4, fill: 'none', opacity: .5, 'stroke-linecap': 'round' }, hi);
    } else if (p.hairStyle === 'short') {
      S('path', { d: 'M-58,-104 C-64,-160 -26,-184 4,-182 C40,-182 66,-158 58,-104 C54,-128 42,-140 22,-144 C0,-148 -24,-146 -40,-138 C-52,-130 -56,-118 -58,-104 Z', fill: p.hair }, hi);
      S('path', { d: 'M-58,-104 C-60,-120 -58,-130 -54,-136 L-48,-112 Z', fill: p.grey }, hi);
      S('path', { d: 'M58,-104 C60,-120 58,-130 54,-136 L48,-112 Z', fill: p.grey }, hi);
      S('path', { d: 'M-30,-170 C-10,-178 14,-178 34,-168', stroke: p.grey, 'stroke-width': 4, fill: 'none', opacity: .55, 'stroke-linecap': 'round' }, hi);
    } else if (p.hairStyle === 'shortBlack') {
      S('path', { d: 'M-58,-100 C-62,-160 -24,-180 4,-178 C38,-178 64,-156 58,-100 C52,-130 30,-144 4,-146 C-24,-144 -50,-130 -58,-100 Z', fill: p.hair }, hi);
    } else if (p.hairStyle === 'curly') {
      for (const [x, y, r] of [[-40, -156, 20], [-12, -166, 21], [18, -164, 21], [44, -150, 19], [-56, -128, 16], [58, -124, 16]])
        S('circle', { cx: x, cy: y, r, fill: p.hair }, hi);
    }
    // brazos
    this.arms = [0, 1].map(i => {
      const side = i ? 1 : -1;
      const g = this.armFront[i];
      const upper = S('path', { d: '', stroke: p.shirt, 'stroke-width': 31, 'stroke-linecap': 'round', fill: 'none' }, g);
      const fore = S('path', { d: '', stroke: p.sleeve === 'long' ? p.shirt : p.skin, 'stroke-width': 26, 'stroke-linecap': 'round', fill: 'none' }, g);
      const cuff = S('path', { d: '', stroke: p.sleeve === 'rolled' ? shade(p.shirt, .9) : p.shirt, 'stroke-width': 30, 'stroke-linecap': 'butt', fill: 'none' }, g);
      const hand = S('circle', { r: 15, fill: p.skin }, g);
      const palm = S('ellipse', { rx: 13, ry: 19, fill: p.skin }, g);
      const finger = S('path', { d: '', stroke: p.skin, 'stroke-width': 9, 'stroke-linecap': 'round', fill: 'none' }, g);
      const watch = p.watch && i === 0 ? S('path', { d: '', stroke: '#1B1B1F', 'stroke-width': 28, fill: 'none' }, g) : null;
      return { side, g, upper, fore, cuff, hand, palm, finger, watch };
    });
    this.state = {};
  }

  set(st) {
    const p = this.p;
    const s = Object.assign({ x: 0, y: 0, sc: 1, turn: 0, gx: 0, gy: 0, browIn: 0, browOut: 0, open: 0, smile: 0, blink: 0, tilt: 0, nod: 0,
      lean: 0, standing: false, walk: 0, lift: 0, arms: [[-12, 40, 'fist'], [12, -40, 'fist']], blur: 0 }, st);
    this.root.setAttribute('transform', `translate(${s.x},${s.y}) scale(${s.sc}) rotate(${s.lean})`);
    this.legsG.style.display = s.standing ? '' : 'none';
    if (s.standing) {
      const sw = Math.sin(s.walk) * 16 * (s.walking ? 1 : 0);
      this.legs[0].setAttribute('transform', `translate(-28,200) rotate(${sw})`);
      this.legs[1].setAttribute('transform', `translate(28,200) rotate(${-sw})`);
    }
    const bob = s.lift;
    this.torsoG.setAttribute('transform', `translate(0,${-bob})`);
    this.hairBackG.setAttribute('transform', `translate(${s.turn * 4},${-bob + s.nod * 0.6}) rotate(${s.tilt},0,-100)`);
    this.headG.setAttribute('transform', `translate(${s.turn * 6},${-bob + s.nod}) rotate(${s.tilt},0,-40)`);
    this.feat.setAttribute('transform', `translate(${s.turn * 14},${s.gy * 0.4})`);
    // ojos
    for (const e of this.eyes) {
      e.e.setAttribute('cx', s.gx * 3.2); e.e.setAttribute('cy', s.gy * 2.6);
      e.hl.setAttribute('cx', 2.2 + s.gx * 3.2); e.hl.setAttribute('cy', -3 + s.gy * 2.6);
      const h = 24 * clamp(s.blink, 0, 1);
      e.lid.setAttribute('height', h);
      e.hl.style.display = s.blink > .5 ? 'none' : '';
    }
    // cejas: browIn >0 sube la parte interna (preocupación), <0 la baja (enojo)
    this.brows.forEach((b, i) => {
      const side = i ? 1 : -1, x = side * 22;
      const yi = -125 - s.browIn * 7 + (s.blink > .5 ? 2 : 0), yo = -127 - s.browOut * 5;
      b.setAttribute('d', `M${x - side * 11},${yi} Q${x},${(yi + yo) / 2 - 4} ${x + side * 12},${yo}`);
    });
    // boca
    const o = clamp(s.open, 0, 1), sm = clamp(s.smile, -1, 1);
    const w = 15 + sm * 3 - o * 2;
    if (o > 0.06) {
      const h = 3 + o * 17;
      this.mouthOpen.setAttribute('d', `M${-w},0 Q0,${-3 - sm * 2} ${w},0 Q${w * .6},${h} 0,${h + 1} Q${-w * .6},${h} ${-w},0 Z`);
      this.teeth.setAttribute('d', o > .3 ? `M${-w * .7},${-0.5} Q0,${-3} ${w * .7},${-0.5} L${w * .6},${3.5} Q0,${2} ${-w * .6},${3.5} Z` : '');
      this.mouthLine.setAttribute('d', `M${-w},0 Q0,${-3 - sm * 2} ${w},0`);
      this.mouthLine.setAttribute('stroke-width', 2.4);
    } else {
      this.mouthOpen.setAttribute('d', ''); this.teeth.setAttribute('d', '');
      this.mouthLine.setAttribute('d', `M${-w},${-sm * 3} Q0,${sm * 9} ${w},${-sm * 3}`);
      this.mouthLine.setAttribute('stroke-width', 3.6);
    }
    this.cheeks.forEach(c => c.setAttribute('opacity', .12 + Math.max(0, sm) * .1));
    // brazos: [ángulo brazo, ángulo antebrazo, mano] (grados desde la vertical hacia abajo; + hacia la derecha)
    this.arms.forEach((a, i) => {
      const [a1, a2, handType] = s.arms[i];
      const sx = a.side * 66, sy = 26 - bob;
      const ex = sx + Math.sin(a1 * D2R) * 92, ey = sy + Math.cos(a1 * D2R) * 92;
      const hx = ex + Math.sin(a2 * D2R) * 84, hy = ey + Math.cos(a2 * D2R) * 84;
      a.upper.setAttribute('d', `M${sx},${sy} L${ex},${ey}`);
      a.fore.setAttribute('d', `M${ex},${ey} L${hx},${hy}`);
      if (p.sleeve === 'rolled') {
        const cx2 = ex + Math.sin(a2 * D2R) * 12, cy2 = ey + Math.cos(a2 * D2R) * 12;
        a.cuff.setAttribute('d', `M${ex},${ey} L${cx2},${cy2}`);
      } else if (p.sleeve === 'three') {
        const cx2 = ex + Math.sin(a2 * D2R) * 36, cy2 = ey + Math.cos(a2 * D2R) * 36;
        a.cuff.setAttribute('d', `M${ex},${ey} L${cx2},${cy2}`); a.cuff.setAttribute('stroke-width', 28);
      } else a.cuff.setAttribute('d', '');
      if (a.watch) {
        const wx = hx - Math.sin(a2 * D2R) * 20, wy = hy - Math.cos(a2 * D2R) * 20;
        const wx2 = hx - Math.sin(a2 * D2R) * 12, wy2 = hy - Math.cos(a2 * D2R) * 12;
        a.watch.setAttribute('d', `M${wx},${wy} L${wx2},${wy2}`);
      }
      a.hand.setAttribute('cx', hx); a.hand.setAttribute('cy', hy);
      a.hand.style.display = handType === 'open' ? 'none' : '';
      a.palm.style.display = handType === 'open' ? '' : 'none';
      if (handType === 'open') {
        const px = hx + Math.sin(a2 * D2R) * 8, py = hy + Math.cos(a2 * D2R) * 8;
        a.palm.setAttribute('cx', px); a.palm.setAttribute('cy', py);
        a.palm.setAttribute('transform', `rotate(${-a2},${px},${py})`);
      }
      if (handType === 'point') {
        const fx = hx + Math.sin(a2 * D2R) * 26, fy = hy + Math.cos(a2 * D2R) * 26;
        a.finger.setAttribute('d', `M${hx},${hy} L${fx},${fy}`);
      } else if (handType === 'open') {
        const th = a2 + a.side * 55;
        const fx = hx + Math.sin(th * D2R) * 16, fy = hy + Math.cos(th * D2R) * 16;
        a.finger.setAttribute('d', `M${hx},${hy} L${fx},${fy}`);
      } else a.finger.setAttribute('d', '');
    });
    this.root.style.filter = s.blur ? `blur(${s.blur}px)` : '';
  }
}

function blinkAt(t, seed) { // parpadeo cada ~3-5 s
  const period = 3.4 + (seed % 7) * 0.31;
  const ph = ((t + seed * 1.37) % period);
  return ph < 0.13 ? Math.sin(ph / 0.13 * Math.PI) : 0;
}
