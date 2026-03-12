#!/usr/bin/env node
/**
 * HTML → PNG 렌더링 (Puppeteer)
 * 
 * 사용법:
 *   node scripts/html_to_png.js slides/slide_01.html slides/slide_01.png
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function htmlToPng(htmlPath, outputPath) {
  console.log('🎨 HTML → PNG 렌더링 시작...');
  console.log(`  입력: ${htmlPath}`);
  console.log(`  출력: ${outputPath}`);
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    
    // 뷰포트 설정 (1080×1440px, 3:4)
    await page.setViewport({
      width: 1080,
      height: 1440,
      deviceScaleFactor: 2 // Retina
    });
    
    // HTML 파일 로드
    const htmlFullPath = path.resolve(htmlPath);
    await page.goto(`file://${htmlFullPath}`, {
      waitUntil: 'networkidle0'
    });
    
    // 스크린샷 캡처
    await page.screenshot({
      path: outputPath,
      type: 'png',
      fullPage: false
    });
    
    const stats = fs.statSync(outputPath);
    console.log(`✅ 렌더링 완료!`);
    console.log(`📊 파일 크기: ${(stats.size / 1024).toFixed(1)} KB`);
    
  } catch (error) {
    console.error('❌ 렌더링 실패:', error.message);
    throw error;
  } finally {
    await browser.close();
  }
}

// CLI 실행
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('사용법: node html_to_png.js <input.html> <output.png>');
    process.exit(1);
  }
  
  const [htmlPath, outputPath] = args;
  
  htmlToPng(htmlPath, outputPath)
    .then(() => {
      console.log('✅ SUCCESS');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ FAILED:', error.message);
      process.exit(1);
    });
}

module.exports = { htmlToPng };
