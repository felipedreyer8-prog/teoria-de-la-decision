// Renderiza cada página HTML a PNG transparente 1920x1080.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = process.argv[2];
  const pages = JSON.parse(fs.readFileSync(path.join(dir, 'pages.json'), 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const [name, html] of Object.entries(pages)) {
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(dir, name + '.png'), omitBackground: true });
  }
  await browser.close();
  console.log('ok', Object.keys(pages).length);
})();
