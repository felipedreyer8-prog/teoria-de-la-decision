// Renderiza el motor 3D cuadro por cuadro con Chromium headless.
// Uso:
//   node render.js frames <salida.mp4> <cuadroInicial> <cuadroFinal>
//   node render.js stills <carpeta> <t1,t2,...>
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const URL = 'http://127.0.0.1:8765/motor.html?render=1';

async function open() {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error') console.error('[consola]', m.text()); });
  page.on('pageerror', e => console.error('[error]', e.message));
  await page.goto(URL, { waitUntil: 'load' });
  await page.evaluate(() => window.ENGINE.ready);
  return { browser, page };
}

async function frames(out, f0, f1) {
  const { browser, page } = await open();
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '25', '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '25', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = f0; f < f1; f++) {
    await page.evaluate(t => window.ENGINE.renderAt(t), f / 25);
    const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - f0) % 100 === 99) console.log(`${out}: ${f - f0 + 1}/${f1 - f0} cuadros, ${((Date.now() - t0) / (f - f0 + 1)).toFixed(0)} ms/cuadro`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
}

async function stills(dir, times) {
  fs.mkdirSync(dir, { recursive: true });
  const { browser, page } = await open();
  for (const t of times) {
    const s = Date.now();
    await page.evaluate(x => window.ENGINE.renderAt(x), t);
    await page.screenshot({ type: 'jpeg', quality: 88, path: path.join(dir, `t_${String(t.toFixed(2)).padStart(6, '0')}.jpg`) });
    console.log(`t=${t} ${Date.now() - s} ms`);
  }
  await browser.close();
}

(async () => {
  const [mode, a, b, c] = process.argv.slice(2);
  if (mode === 'frames') await frames(a, +b, +c);
  else await stills(a, b.split(',').map(Number));
})().catch(e => { console.error(e); process.exit(1); });
