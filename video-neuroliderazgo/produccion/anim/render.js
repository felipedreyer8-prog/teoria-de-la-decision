// Renderiza un tramo de cuadros: node render.js <build> <f0> <f1> <salida.mp4>
// o capturas sueltas: node render.js <build> --stills t1,t2,... <carpeta>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
(async () => {
  const [, , B, a1, a2, a3] = process.argv;
  const tl = JSON.parse(fs.readFileSync(path.join(B, 'out', 'timeline.json'), 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => { console.error('ERROR en página:', e.message); process.exit(1); });
  await page.goto('file://' + path.join(B, 'anim', 'index.html'));
  await page.evaluate(tl => init(tl), tl);
  await page.waitForFunction(() => Array.from(document.images).every(i => i.complete));
  await page.evaluate(() => document.fonts.ready);
  if (a1 === '--stills') {
    fs.mkdirSync(a3, { recursive: true });
    for (const ts of a2.split(',')) {
      await page.evaluate(t => renderAt(t), +ts);
      await page.screenshot({ path: path.join(a3, `t_${(+ts).toFixed(1).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 88 });
    }
  } else {
    const f0 = +a1, f1 = +a2, fps = tl.fps;
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-g', '60', a3], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = f0; f < f1; f++) {
      await page.evaluate(t => renderAt(t), f / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
