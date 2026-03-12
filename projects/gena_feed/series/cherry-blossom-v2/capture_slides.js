const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 1,
  });

  const baseUrl = 'http://localhost:8888/series/cherry-blossom-v2/slides';
  const outDir = path.join(__dirname, 'output');
  const fs = require('fs');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  for (let i = 1; i <= 10; i++) {
    const num = String(i).padStart(2, '0');
    const page = await context.newPage();
    const url = `${baseUrl}/slide_${num}.html`;
    console.log(`Capturing slide_${num}...`);

    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    // Wait for fonts to load
    await page.waitForTimeout(2000);

    const outPath = path.join(outDir, `slide_${num}.png`);
    await page.screenshot({ path: outPath, type: 'png' });
    const size = fs.statSync(outPath).size;
    console.log(`  -> ${outPath} (${Math.round(size/1024)}KB)`);
    await page.close();
  }

  await browser.close();
  console.log('\nAll 10 slides captured!');
})();
