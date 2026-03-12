const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ASSETS_DIR = path.join(__dirname, '../assets');
const SLIDES_DIR = __dirname;
const OUTPUT_WIDTH = 1080;
const OUTPUT_HEIGHT = 1440;

// 이미지를 base64로 변환
function imageToBase64(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  return `data:image/png;base64,${imageBuffer.toString('base64')}`;
}

// 슬라이드 데이터 정의
const slides = [
  {
    num: 1,
    imageFile: 'carousel_slide_01.png',
    layout: 'hero',
    content: {
      title: '봄 가방 고민 끝 🌸',
      subtitle: '가볍고 예쁜 미니멀 크로스백 10선'
    }
  },
  {
    num: 2,
    imageFile: 'carousel_slide_02.png',
    layout: 'text-heavy',
    content: {
      title: '출근길 어깨 괴롭히는 토트백 🥲',
      body: [
        '한쪽 어깨만 아프고',
        '양손은 자유 없고',
        '퇴근 땐 목까지 뻐근하고...'
      ],
      subtitle: '이거 나만 힘든 거 아니지?'
    }
  },
  {
    num: 3,
    imageFile: 'carousel_slide_03.png',
    layout: 'checklist',
    content: {
      title: '양손 자유 + 어깨 편한 크로스백으로 바꿈 ✨',
      items: [
        '✓ 200g 이하 초경량',
        '✓ 무게 양쪽 어깨 분산',
        '✓ 봄 트렌드 컬러까지'
      ],
      subtitle: '출근이 이렇게 가벼울 수 있어?'
    }
  },
  {
    num: 4,
    imageFile: 'carousel_slide_04.png',
    layout: 'product',
    content: {
      title: '봄 트렌드 1위 컬러 라벤더 💜',
      specs: [
        '무신사 스탠다드',
        '39,000원',
        '180g 초경량'
      ],
      details: [
        '경량 나일론 | 플랩 여밈',
        '앞면 지퍼 포켓 | 스트랩 조절 가능'
      ]
    }
  },
  {
    num: 5,
    imageFile: 'carousel_slide_05.png',
    layout: 'product',
    content: {
      title: '뉴트럴 컬러의 정석 🤎',
      specs: [
        '마르헨제이',
        '68,000원',
        '카드슬롯 3개 내장'
      ],
      details: [
        '부드러운 인조가죽 | 메탈 버클 디테일',
        '넓은 스트랩 | 220g'
      ]
    }
  },
  {
    num: 6,
    imageFile: 'carousel_slide_06.png',
    layout: 'product',
    content: {
      title: '봄 데이트룩 완성템 💕',
      specs: [
        '디어베이지',
        '54,000원',
        '체인 스트랩 포인트'
      ],
      details: [
        '퀼팅 패턴 나일론 | 골드 메탈 디테일',
        '플랩 여밈 | 내부 지퍼 포켓 | 210g'
      ]
    }
  },
  {
    num: 7,
    imageFile: 'carousel_slide_07.png',
    layout: 'product',
    content: {
      title: '3만원대 가성비 끝판왕 🤍',
      specs: [
        '무신사 스탠다드',
        '35,000원',
        '160g 최경량'
      ],
      details: [
        '경량 폴리에스터 | 지퍼 여밈',
        '미니멀 디자인 | 내부 칸막이 2개'
      ]
    }
  },
  {
    num: 8,
    imageFile: 'carousel_slide_08.png',
    layout: 'product',
    content: {
      title: '지구도 생각하는 에코 소재 🌿',
      specs: [
        '러브이즈트루',
        '46,000원',
        '145g 초초경량'
      ],
      details: [
        '재활용 나일론 | 플랩+자석 여밈',
        '패딩 스트랩 | 외부 슬립 포켓'
      ]
    }
  },
  {
    num: 9,
    imageFile: 'carousel_slide_09.png',
    layout: 'grid',
    content: {
      title: '봄 컬러 총집합 🎨',
      colors: [
        '라벤더', '민트', '베이비핑크',
        '크림베이지', '아이보리', '그레이지'
      ],
      priceRange: '35,000원 ~ 98,000원',
      subtitle: '나에게 맞는 컬러는?'
    }
  },
  {
    num: 10,
    imageFile: 'carousel_slide_10.png',
    layout: 'cta',
    content: {
      title: '마음에 드는 가방 있으면 저장 📌',
      subtitle: '더 많은 봄 아이템은\n팔로우하고 확인해요 →',
      cta: '👉 프로필 링크에서 바로 구매'
    }
  }
];

// HTML 템플릿 생성
function generateHTML(slide) {
  const imageBase64 = imageToBase64(path.join(ASSETS_DIR, slide.imageFile));
  
  let contentHTML = '';
  
  switch(slide.layout) {
    case 'hero':
      contentHTML = `
        <h1>${slide.content.title}</h1>
        <p class="subtitle">${slide.content.subtitle}</p>
      `;
      break;
    
    case 'text-heavy':
      contentHTML = `
        <h1>${slide.content.title}</h1>
        <div class="body-text">
          ${slide.content.body.map(line => `<p>${line}</p>`).join('')}
        </div>
        <p class="subtitle">${slide.content.subtitle}</p>
      `;
      break;
    
    case 'checklist':
      contentHTML = `
        <h1>${slide.content.title}</h1>
        <div class="checklist">
          ${slide.content.items.map(item => `<p>${item}</p>`).join('')}
        </div>
        <p class="subtitle">${slide.content.subtitle}</p>
      `;
      break;
    
    case 'product':
      contentHTML = `
        <h1>${slide.content.title}</h1>
        <div class="specs">
          ${slide.content.specs.map(spec => `<p>${spec}</p>`).join('')}
        </div>
        <div class="details">
          ${slide.content.details.map(detail => `<p>${detail}</p>`).join('')}
        </div>
      `;
      break;
    
    case 'grid':
      contentHTML = `
        <h1>${slide.content.title}</h1>
        <div class="color-grid">
          ${slide.content.colors.map(color => `<span class="color-tag">${color}</span>`).join('')}
        </div>
        <p class="price-range">${slide.content.priceRange}</p>
        <p class="subtitle">${slide.content.subtitle}</p>
      `;
      break;
    
    case 'cta':
      contentHTML = `
        <h1>${slide.content.title}</h1>
        <p class="subtitle">${slide.content.subtitle}</p>
        <p class="cta">${slide.content.cta}</p>
      `;
      break;
  }

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide ${slide.num}</title>
  <style>
    * { 
      margin: 0; 
      padding: 0; 
      box-sizing: border-box; 
    }
    
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
    
    body { 
      font-family: 'Pretendard Variable', -apple-system, sans-serif;
      margin: 0;
      padding: 0;
    }
    
    .canvas { 
      width: ${OUTPUT_WIDTH}px; 
      height: ${OUTPUT_HEIGHT}px; 
      position: relative; 
      overflow: hidden;
      background: #000;
    }
    
    .bg-image { 
      width: 100%; 
      height: 100%; 
      object-fit: cover;
    }
    
    .overlay { 
      position: absolute; 
      top: 0; 
      left: 0; 
      width: 100%; 
      height: 100%; 
      background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.75) 60%, rgba(0,0,0,0.9) 100%);
      display: flex; 
      flex-direction: column; 
      justify-content: flex-end; 
      padding: 64px 48px; 
      gap: 24px;
    }
    
    h1 { 
      font-size: 48px; 
      font-weight: 800; 
      color: #FFFFFF; 
      line-height: 1.3; 
      text-shadow: 4px 4px 0 #000000;
      word-wrap: break-word;
    }
    
    .subtitle { 
      font-size: 28px; 
      font-weight: 600; 
      color: #FFFFFF; 
      opacity: 0.95;
      line-height: 1.4;
      white-space: pre-line;
    }
    
    .body-text p,
    .checklist p { 
      font-size: 32px; 
      font-weight: 500; 
      color: #FFFFFF; 
      line-height: 1.5;
      margin-bottom: 12px;
    }
    
    .specs {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(20px);
      padding: 24px 32px;
      border-radius: 12px;
      border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .specs p { 
      font-size: 28px; 
      font-weight: 700; 
      color: #FFFFFF; 
      line-height: 1.5;
    }
    
    .details {
      margin-top: 12px;
    }
    
    .details p { 
      font-size: 22px; 
      font-weight: 400; 
      color: #FFFFFF; 
      line-height: 1.6;
      opacity: 0.9;
    }
    
    .color-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin: 24px 0;
    }
    
    .color-tag {
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      padding: 16px 20px;
      border-radius: 8px;
      font-size: 24px;
      font-weight: 600;
      color: #FFFFFF;
      text-align: center;
      border: 2px solid rgba(255, 255, 255, 0.4);
    }
    
    .price-range {
      font-size: 32px;
      font-weight: 700;
      color: #FFE600;
      text-shadow: 2px 2px 0 #000000;
    }
    
    .cta {
      font-size: 36px;
      font-weight: 800;
      color: #00FF41;
      text-shadow: 3px 3px 0 #000000;
      margin-top: 16px;
    }
  </style>
</head>
<body>
  <div class="canvas">
    <img class="bg-image" src="${imageBase64}" alt="Slide ${slide.num}">
    <div class="overlay">
      ${contentHTML}
    </div>
  </div>
</body>
</html>`;
}

// PNG 렌더링
async function renderToPNG(htmlPath, outputPath) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setViewport({
    width: OUTPUT_WIDTH,
    height: OUTPUT_HEIGHT,
    deviceScaleFactor: 2
  });
  
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
  
  await page.screenshot({
    path: outputPath,
    type: 'png',
    fullPage: false
  });
  
  await browser.close();
  console.log(`✓ Rendered: ${path.basename(outputPath)}`);
}

// 메인 실행
async function main() {
  console.log('🚀 Starting slide generation...\n');
  
  for (const slide of slides) {
    const slideNum = String(slide.num).padStart(2, '0');
    const htmlPath = path.join(SLIDES_DIR, `slide_${slideNum}.html`);
    const pngPath = path.join(SLIDES_DIR, `slide_${slideNum}.png`);
    
    // HTML 생성
    const html = generateHTML(slide);
    fs.writeFileSync(htmlPath, html, 'utf-8');
    console.log(`✓ Generated: slide_${slideNum}.html`);
    
    // PNG 렌더링
    await renderToPNG(htmlPath, pngPath);
  }
  
  console.log('\n✨ All slides completed!');
}

main().catch(console.error);
