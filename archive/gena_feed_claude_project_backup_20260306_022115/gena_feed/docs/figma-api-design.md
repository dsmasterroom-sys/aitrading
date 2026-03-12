# Figma API Integration Design
# GenArchive 캐러셀 자동 생성 API 설계

## 📋 개요

본 문서는 Figma 템플릿을 활용한 캐러셀 자동 생성 시스템의 API 연동 설계를 정의합니다.
`weekly/copy.md` 콘텐츠 데이터를 Figma 템플릿에 동적 삽입하여 PNG 이미지로 Export하는 워크플로우를 구축합니다.

**핵심 기능:**
- Figma API 인증 및 파일 접근
- 동적 데이터 삽입 (Text, Image, Color)
- PNG Export 자동화
- CLI 인터페이스
- Fallback 메커니즘 (Figma 실패 시 HTML 방식)

---

## 🏗️ 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                    GenArchive 캐러셀 생성 파이프라인              │
└──────────────────────────────────────────────────────────────┘

[1] 콘텐츠 준비
    └─→ weekly/copy.md (Markdown 소스)
         └─→ Parser (YAML frontmatter + sections)

[2] 데이터 매핑
    └─→ Content → Template Mapping
         └─→ H-1, I-2, CTA-1 등 패턴 선택

[3] Figma API 연동
    └─→ Figma Template Update
         ├─→ Text nodes update
         ├─→ Image fills update
         └─→ Color fills update

[4] PNG Export
    └─→ Figma Image API
         └─→ PNG files (1080×1920px, @2x)

[5] 후처리 (Optional)
    └─→ 이미지 최적화, 메타데이터 삽입

[Fallback] HTML 방식
    └─→ compose_carousel.py (기존 방식)
```

---

## 🔐 A. Figma API 인증

### 환경 변수 설정

**`.env` 파일:**
```bash
# Figma API Configuration
FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
FIGMA_FILE_ID=aBcDeFgHiJkLmNoPqRsTuVwXyZ
FIGMA_TEAM_ID=123456789  # Optional, for team libraries

# Export Configuration
FIGMA_EXPORT_SCALE=2     # @2x for Retina displays
FIGMA_EXPORT_FORMAT=png  # png, jpg, svg, pdf

# Fallback Configuration
USE_HTML_FALLBACK=true   # true/false
```

### 인증 클래스 설계

```python
# figma_client.py

import os
import requests
from typing import Optional
from dotenv import load_dotenv

class FigmaClient:
    """
    Figma API 클라이언트
    
    환경변수:
        FIGMA_ACCESS_TOKEN: Figma Personal Access Token
        FIGMA_FILE_ID: Figma 파일 ID (URL에서 추출)
    """
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self):
        load_dotenv()
        self.access_token = os.getenv("FIGMA_ACCESS_TOKEN")
        self.file_id = os.getenv("FIGMA_FILE_ID")
        
        if not self.access_token:
            raise ValueError("FIGMA_ACCESS_TOKEN not found in environment")
        if not self.file_id:
            raise ValueError("FIGMA_FILE_ID not found in environment")
        
        self.headers = {
            "X-Figma-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Figma API 요청 헬퍼
        
        Args:
            method: HTTP 메서드 (GET, POST, etc.)
            endpoint: API 엔드포인트 (예: /files/{file_id})
            **kwargs: requests 라이브러리 파라미터
        
        Returns:
            API 응답 JSON
        
        Raises:
            requests.HTTPError: API 오류 시
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_file(self, file_id: Optional[str] = None) -> dict:
        """
        Figma 파일 전체 구조 가져오기
        
        Args:
            file_id: Figma 파일 ID (기본값: 환경변수)
        
        Returns:
            파일 구조 JSON
        """
        fid = file_id or self.file_id
        return self._request("GET", f"/files/{fid}")
    
    def get_file_nodes(self, node_ids: list[str], file_id: Optional[str] = None) -> dict:
        """
        특정 노드만 가져오기 (성능 최적화)
        
        Args:
            node_ids: 노드 ID 리스트
            file_id: Figma 파일 ID
        
        Returns:
            노드 데이터 JSON
        """
        fid = file_id or self.file_id
        ids_param = ",".join(node_ids)
        return self._request("GET", f"/files/{fid}/nodes?ids={ids_param}")
    
    def get_images(self, node_ids: list[str], scale: float = 2.0, 
                   format: str = "png", file_id: Optional[str] = None) -> dict:
        """
        노드를 이미지로 Export
        
        Args:
            node_ids: Export할 노드 ID 리스트
            scale: Export 배율 (1.0, 2.0, 3.0)
            format: 이미지 포맷 (png, jpg, svg, pdf)
            file_id: Figma 파일 ID
        
        Returns:
            {
                "err": null,
                "images": {
                    "node_id": "https://s3-alpha-sig.figma.com/..."
                }
            }
        """
        fid = file_id or self.file_id
        ids_param = ",".join(node_ids)
        params = {
            "ids": ids_param,
            "scale": scale,
            "format": format
        }
        return self._request("GET", f"/images/{fid}", params=params)
    
    def test_connection(self) -> bool:
        """
        API 연결 테스트
        
        Returns:
            연결 성공 여부
        """
        try:
            response = self._request("GET", "/me")
            print(f"✓ Connected as: {response.get('email', 'Unknown')}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
```

### Access Token 발급 방법

1. Figma 로그인 → Settings → Personal Access Tokens
2. "Generate new token" 클릭
3. Token name: `GenArchive Carousel Generator`
4. Scopes: `File content (Read only)` 선택
5. 생성된 토큰을 `.env`에 저장 (한 번만 표시됨)

**Security Note:** `.gitignore`에 `.env` 추가 필수!

---

## 🔄 B. 동적 데이터 삽입

### 데이터 구조 정의

```python
# models.py

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum

class TemplatePattern(Enum):
    """17개 레이아웃 패턴"""
    H1 = "H-1"  # Hero Statement
    H2 = "H-2"  # Visual Impact
    H3 = "H-3"  # Split Hero
    I1 = "I-1"  # Data Grid
    I2 = "I-2"  # Timeline
    I3 = "I-3"  # Stat Comparison
    I4 = "I-4"  # Feature List
    I5 = "I-5"  # Quote + Source
    P1 = "P-1"  # Step-by-Step
    P2 = "P-2"  # Before/After
    P3 = "P-3"  # Process Flow
    C1 = "C-1"  # Side-by-Side
    C2 = "C-2"  # Pros/Cons
    M1 = "M-1"  # Product Showcase
    M2 = "M-2"  # Collection Grid
    CTA1 = "CTA-1"  # Primary CTA
    CTA2 = "CTA-2"  # Urgency CTA

@dataclass
class SlideData:
    """
    슬라이드 콘텐츠 데이터
    """
    slide_number: int
    template: TemplatePattern
    variables: Dict[str, Any]  # 템플릿별 동적 변수
    
    # Metadata
    title: Optional[str] = None
    description: Optional[str] = None

@dataclass
class NodeMapping:
    """
    Figma 노드 매핑 정보
    """
    frame_id: str              # 슬라이드 프레임 ID
    template: TemplatePattern
    text_nodes: Dict[str, str]  # {"variable_name": "node_id"}
    image_nodes: Dict[str, str]
    color_nodes: Dict[str, str]

# 예시 데이터
slide_data_example = SlideData(
    slide_number=1,
    template=TemplatePattern.H1,
    variables={
        "hero_number": "2,500+",
        "hero_headline": "GenArchive에서 만난 아카이브",
        "hero_subtext": "국내 최대 아카이브 커뮤니티",
        "bg_gradient_start": "#4A4A6A",
        "bg_gradient_end": "#1A1A2E"
    },
    title="Hero Slide",
    description="메인 강조 슬라이드"
)
```

### 템플릿 업데이트 함수

```python
# figma_updater.py

from typing import Dict, Any, Optional
import requests
from .figma_client import FigmaClient
from .models import SlideData, NodeMapping, TemplatePattern

class FigmaTemplateUpdater:
    """
    Figma 템플릿 동적 업데이트
    """
    
    def __init__(self, client: FigmaClient):
        self.client = client
        self.node_mappings: Dict[str, NodeMapping] = {}
    
    def load_node_mappings(self, mapping_file: str = "figma_mappings.json"):
        """
        노드 매핑 JSON 파일 로드
        
        파일 예시:
        {
            "slide_01": {
                "frame_id": "123:456",
                "template": "H-1",
                "text_nodes": {
                    "hero_number": "123:457",
                    "hero_headline": "123:458"
                },
                "image_nodes": {},
                "color_nodes": {
                    "bg_gradient_start": "123:459"
                }
            }
        }
        """
        import json
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for slide_key, mapping_data in data.items():
            self.node_mappings[slide_key] = NodeMapping(
                frame_id=mapping_data["frame_id"],
                template=TemplatePattern(mapping_data["template"]),
                text_nodes=mapping_data["text_nodes"],
                image_nodes=mapping_data.get("image_nodes", {}),
                color_nodes=mapping_data.get("color_nodes", {})
            )
    
    def update_text_node(self, node_id: str, text: str, file_id: Optional[str] = None):
        """
        텍스트 노드 업데이트
        
        주의: Figma REST API는 현재 직접적인 node update를 지원하지 않습니다.
        대안:
        1. Figma Plugin API 사용 (Plugin 개발 필요)
        2. Variables API 사용 (Beta 기능)
        3. 템플릿 복제 + 수동 업데이트 후 Export
        
        **권장 방식:** Figma Variables + Figma Plugin
        
        Args:
            node_id: 텍스트 노드 ID
            text: 새로운 텍스트
            file_id: Figma 파일 ID
        """
        # Note: 실제 구현은 Figma Plugin 또는 Variables API 사용
        # 이 설계서에서는 인터페이스만 정의
        raise NotImplementedError(
            "Figma REST API does not support direct node updates. "
            "Use Figma Plugin API or Variables feature."
        )
    
    def update_image_fill(self, node_id: str, image_url: str, file_id: Optional[str] = None):
        """
        이미지 Fill 업데이트
        
        주의: REST API 한계로 인해 Figma Plugin 필요
        
        Args:
            node_id: 이미지 노드 ID
            image_url: 새로운 이미지 URL
            file_id: Figma 파일 ID
        """
        raise NotImplementedError(
            "Figma REST API does not support direct image fill updates. "
            "Use Figma Plugin API."
        )
    
    def prepare_slide_data(self, slide: SlideData) -> Dict[str, Any]:
        """
        슬라이드 데이터를 Figma 업데이트용 구조로 변환
        
        Args:
            slide: 슬라이드 콘텐츠 데이터
        
        Returns:
            Figma Plugin으로 전달할 데이터 구조
        """
        slide_key = f"slide_{slide.slide_number:02d}"
        
        if slide_key not in self.node_mappings:
            raise ValueError(f"No mapping found for {slide_key}")
        
        mapping = self.node_mappings[slide_key]
        
        # 템플릿 검증
        if mapping.template != slide.template:
            raise ValueError(
                f"Template mismatch: mapping has {mapping.template}, "
                f"slide has {slide.template}"
            )
        
        # 업데이트 데이터 구조 생성
        update_data = {
            "frameId": mapping.frame_id,
            "template": slide.template.value,
            "updates": {
                "text": {},
                "images": {},
                "colors": {}
            }
        }
        
        # Text nodes
        for var_name, node_id in mapping.text_nodes.items():
            if var_name in slide.variables:
                update_data["updates"]["text"][node_id] = slide.variables[var_name]
        
        # Image nodes
        for var_name, node_id in mapping.image_nodes.items():
            if var_name in slide.variables:
                update_data["updates"]["images"][node_id] = slide.variables[var_name]
        
        # Color nodes
        for var_name, node_id in mapping.color_nodes.items():
            if var_name in slide.variables:
                update_data["updates"]["colors"][node_id] = slide.variables[var_name]
        
        return update_data

# Figma Plugin API를 통한 업데이트 (대안 방식)
class FigmaPluginBridge:
    """
    Figma Plugin과의 브릿지
    
    워크플로우:
    1. Python → JSON 파일 생성 (업데이트 데이터)
    2. Figma Plugin → JSON 읽기
    3. Plugin → Figma 노드 업데이트
    4. Plugin → 완료 신호
    5. Python → Export 진행
    """
    
    def __init__(self, bridge_dir: str = "./figma_bridge"):
        self.bridge_dir = bridge_dir
        os.makedirs(bridge_dir, exist_ok=True)
    
    def write_update_request(self, slide_updates: List[Dict[str, Any]]) -> str:
        """
        업데이트 요청을 JSON 파일로 저장
        
        Args:
            slide_updates: prepare_slide_data() 결과 리스트
        
        Returns:
            생성된 JSON 파일 경로
        """
        import json
        import time
        
        timestamp = int(time.time())
        filename = f"update_request_{timestamp}.json"
        filepath = os.path.join(self.bridge_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "slides": slide_updates
            }, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def wait_for_completion(self, request_file: str, timeout: int = 300) -> bool:
        """
        Plugin 처리 완료 대기
        
        Plugin은 완료 시 {request_file}.done 파일 생성
        
        Args:
            request_file: 요청 파일 경로
            timeout: 최대 대기 시간 (초)
        
        Returns:
            완료 여부
        """
        import time
        
        done_file = f"{request_file}.done"
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(done_file):
                # 완료 파일 확인
                with open(done_file, 'r') as f:
                    result = json.load(f)
                
                if result.get("status") == "success":
                    print("✓ Figma Plugin update completed")
                    return True
                else:
                    print(f"✗ Plugin update failed: {result.get('error')}")
                    return False
            
            time.sleep(2)  # 2초마다 체크
        
        print(f"✗ Timeout waiting for Figma Plugin ({timeout}s)")
        return False
```

### Figma Plugin 스크립트 설계 (TypeScript)

```typescript
// figma_plugin/code.ts
// Figma Plugin이 실행할 스크립트 (별도 개발 필요)

interface UpdateRequest {
  timestamp: number;
  slides: SlideUpdate[];
}

interface SlideUpdate {
  frameId: string;
  template: string;
  updates: {
    text: { [nodeId: string]: string };
    images: { [nodeId: string]: string };
    colors: { [nodeId: string]: string };
  };
}

async function processUpdateRequest(requestPath: string) {
  // 1. JSON 파일 읽기 (Figma Plugin은 로컬 파일 접근 불가, 
  //    따라서 UI에서 파일 내용을 전달받아야 함)
  const request: UpdateRequest = await loadRequestFromUI();
  
  for (const slide of request.slides) {
    const frame = figma.getNodeById(slide.frameId) as FrameNode;
    
    if (!frame) {
      console.error(`Frame not found: ${slide.frameId}`);
      continue;
    }
    
    // Text updates
    for (const [nodeId, text] of Object.entries(slide.updates.text)) {
      const node = figma.getNodeById(nodeId) as TextNode;
      if (node && node.type === 'TEXT') {
        await figma.loadFontAsync(node.fontName as FontName);
        node.characters = text;
      }
    }
    
    // Image updates
    for (const [nodeId, imageUrl] of Object.entries(slide.updates.images)) {
      const node = figma.getNodeById(nodeId);
      if (node && 'fills' in node) {
        const image = await loadImageFromUrl(imageUrl);
        node.fills = [{
          type: 'IMAGE',
          imageHash: image.hash,
          scaleMode: 'FILL'
        }];
      }
    }
    
    // Color updates
    for (const [nodeId, color] of Object.entries(slide.updates.colors)) {
      const node = figma.getNodeById(nodeId);
      if (node && 'fills' in node) {
        const rgb = hexToRgb(color);
        node.fills = [{
          type: 'SOLID',
          color: { r: rgb.r / 255, g: rgb.g / 255, b: rgb.b / 255 }
        }];
      }
    }
  }
  
  // 완료 신호
  figma.ui.postMessage({ status: 'success' });
}

// Helper functions...
```

**중요:** Figma Plugin 개발은 별도 프로젝트로 진행 필요.
본 설계서는 인터페이스와 데이터 구조만 정의합니다.

---

## 📤 C. PNG Export

### Export 함수

```python
# figma_exporter.py

import os
import requests
from typing import List, Optional
from .figma_client import FigmaClient

class FigmaExporter:
    """
    Figma 노드를 PNG 이미지로 Export
    """
    
    def __init__(self, client: FigmaClient, output_dir: str = "./output"):
        self.client = client
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_slide(self, node_id: str, output_filename: str, 
                     scale: float = 2.0, file_id: Optional[str] = None) -> str:
        """
        단일 슬라이드 Export
        
        Args:
            node_id: Export할 프레임 노드 ID
            output_filename: 출력 파일명 (예: "slide_01.png")
            scale: Export 배율 (@2x = 2.0)
            file_id: Figma 파일 ID
        
        Returns:
            저장된 파일 경로
        """
        # 1. Figma API로 이미지 URL 요청
        response = self.client.get_images(
            node_ids=[node_id],
            scale=scale,
            format="png",
            file_id=file_id
        )
        
        if response.get("err"):
            raise Exception(f"Figma API error: {response['err']}")
        
        image_url = response["images"].get(node_id)
        
        if not image_url:
            raise Exception(f"No image URL returned for node {node_id}")
        
        # 2. 이미지 다운로드
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        
        # 3. 파일 저장
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'wb') as f:
            f.write(img_response.content)
        
        print(f"✓ Exported: {output_path} ({len(img_response.content)} bytes)")
        
        return output_path
    
    def export_all_slides(self, node_mappings: dict, scale: float = 2.0) -> List[str]:
        """
        모든 슬라이드 일괄 Export
        
        Args:
            node_mappings: {slide_key: NodeMapping} 딕셔너리
            scale: Export 배율
        
        Returns:
            저장된 파일 경로 리스트
        """
        node_ids = [mapping.frame_id for mapping in node_mappings.values()]
        
        # 1. 한 번에 모든 이미지 URL 요청 (API 효율성)
        response = self.client.get_images(
            node_ids=node_ids,
            scale=scale,
            format="png"
        )
        
        if response.get("err"):
            raise Exception(f"Figma API error: {response['err']}")
        
        # 2. 각 이미지 다운로드 및 저장
        output_paths = []
        
        for slide_key, mapping in node_mappings.items():
            image_url = response["images"].get(mapping.frame_id)
            
            if not image_url:
                print(f"⚠ No image URL for {slide_key}, skipping...")
                continue
            
            # 파일명: slide_01.png, slide_02.png, ...
            filename = f"{slide_key}.png"
            output_path = os.path.join(self.output_dir, filename)
            
            # 다운로드
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            # 저장
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✓ Exported: {output_path}")
            output_paths.append(output_path)
        
        return output_paths
    
    def export_with_optimization(self, node_id: str, output_filename: str, 
                                  optimize: bool = True) -> str:
        """
        최적화된 PNG Export
        
        Args:
            node_id: Export할 노드 ID
            output_filename: 출력 파일명
            optimize: PNG 최적화 활성화
        
        Returns:
            저장된 파일 경로
        """
        # 1. 기본 Export
        output_path = self.export_slide(node_id, output_filename)
        
        if not optimize:
            return output_path
        
        # 2. PNG 최적화 (pngquant 사용)
        try:
            from PIL import Image
            
            img = Image.open(output_path)
            
            # EXIF 메타데이터 추가
            from PIL import PngImagePlugin
            meta = PngImagePlugin.PngInfo()
            meta.add_text("Author", "GenArchive Carousel Generator")
            meta.add_text("Software", "Figma API + Python")
            
            # 재저장 (최적화)
            img.save(output_path, "PNG", optimize=True, pnginfo=meta)
            
            print(f"✓ Optimized: {output_path}")
            
        except ImportError:
            print("⚠ PIL not installed, skipping optimization")
        except Exception as e:
            print(f"⚠ Optimization failed: {e}")
        
        return output_path
```

---

## 🖥️ D. CLI 인터페이스

### 메인 스크립트

```python
# scripts/figma_export.py

import argparse
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from gena_feed.figma_client import FigmaClient
from gena_feed.figma_updater import FigmaTemplateUpdater, FigmaPluginBridge
from gena_feed.figma_exporter import FigmaExporter
from gena_feed.models import SlideData, TemplatePattern

def main():
    parser = argparse.ArgumentParser(
        description="GenArchive Carousel - Figma Export Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export all slides
  python scripts/figma_export.py --all
  
  # Export specific slides
  python scripts/figma_export.py --slide 1,3,7
  
  # Dry run (no actual export)
  python scripts/figma_export.py --all --dry-run
  
  # Update templates and export
  python scripts/figma_export.py --all --update --data weekly/copy.md
  
  # Test Figma connection
  python scripts/figma_export.py --test
        """
    )
    
    # Arguments
    parser.add_argument(
        "--all",
        action="store_true",
        help="Export all slides"
    )
    
    parser.add_argument(
        "--slide",
        type=str,
        help="Export specific slides (comma-separated, e.g., '1,3,7')"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode (no actual export)"
    )
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update Figma templates before export"
    )
    
    parser.add_argument(
        "--data",
        type=str,
        help="Content data file (e.g., weekly/copy.md)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="Output directory for PNG files (default: ./output)"
    )
    
    parser.add_argument(
        "--scale",
        type=float,
        default=2.0,
        help="Export scale (@2x = 2.0, default: 2.0)"
    )
    
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Optimize PNG files after export"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test Figma API connection and exit"
    )
    
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="Use HTML fallback if Figma fails"
    )
    
    args = parser.parse_args()
    
    # Initialize Figma client
    try:
        client = FigmaClient()
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("Please set FIGMA_ACCESS_TOKEN and FIGMA_FILE_ID in .env")
        sys.exit(1)
    
    # Test mode
    if args.test:
        if client.test_connection():
            print("✓ Figma API connection successful")
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Validate arguments
    if not args.all and not args.slide:
        parser.error("Must specify either --all or --slide")
    
    if args.update and not args.data:
        parser.error("--update requires --data argument")
    
    # Initialize components
    updater = FigmaTemplateUpdater(client)
    exporter = FigmaExporter(client, output_dir=args.output)
    
    # Load node mappings
    try:
        updater.load_node_mappings("figma_mappings.json")
    except FileNotFoundError:
        print("✗ figma_mappings.json not found")
        print("Please create node mappings file first")
        sys.exit(1)
    
    # Determine which slides to export
    if args.all:
        slide_keys = list(updater.node_mappings.keys())
    else:
        slide_numbers = [int(n.strip()) for n in args.slide.split(",")]
        slide_keys = [f"slide_{n:02d}" for n in slide_numbers]
    
    print(f"📋 Exporting {len(slide_keys)} slides...")
    
    # Update templates if requested
    if args.update:
        print("🔄 Updating Figma templates...")
        
        # Parse content data
        from gena_feed.content_parser import parse_content_file
        slides_data = parse_content_file(args.data)
        
        # Prepare updates
        updates = []
        for slide_data in slides_data:
            slide_key = f"slide_{slide_data.slide_number:02d}"
            if slide_key in slide_keys:
                update = updater.prepare_slide_data(slide_data)
                updates.append(update)
        
        # Send to Figma Plugin
        bridge = FigmaPluginBridge()
        request_file = bridge.write_update_request(updates)
        
        print(f"📝 Update request written: {request_file}")
        print("👉 Please run Figma Plugin to apply updates, then press Enter...")
        
        if not args.dry_run:
            input()  # Wait for user
            
            if not bridge.wait_for_completion(request_file):
                print("✗ Figma update failed")
                
                if args.fallback:
                    print("🔄 Falling back to HTML method...")
                    # Call existing compose_carousel.py
                    os.system(f"python scripts/compose_carousel.py --input {args.data}")
                    sys.exit(0)
                else:
                    sys.exit(1)
    
    # Export
    if args.dry_run:
        print("🔍 Dry run mode - skipping actual export")
        for slide_key in slide_keys:
            mapping = updater.node_mappings[slide_key]
            print(f"  Would export: {slide_key} (node: {mapping.frame_id})")
    else:
        print("📤 Exporting slides...")
        
        try:
            exported_files = []
            
            for slide_key in slide_keys:
                mapping = updater.node_mappings[slide_key]
                filename = f"{slide_key}.png"
                
                if args.optimize:
                    path = exporter.export_with_optimization(
                        mapping.frame_id,
                        filename
                    )
                else:
                    path = exporter.export_slide(
                        mapping.frame_id,
                        filename,
                        scale=args.scale
                    )
                
                exported_files.append(path)
            
            print(f"\n✓ Successfully exported {len(exported_files)} slides")
            print(f"📁 Output directory: {args.output}")
            
        except Exception as e:
            print(f"\n✗ Export failed: {e}")
            
            if args.fallback:
                print("🔄 Falling back to HTML method...")
                os.system(f"python scripts/compose_carousel.py")
                sys.exit(0)
            else:
                sys.exit(1)

if __name__ == "__main__":
    main()
```

### CLI 사용 예시

```bash
# 1. 환경 설정
cp .env.example .env
# .env 파일에 FIGMA_ACCESS_TOKEN, FIGMA_FILE_ID 입력

# 2. 연결 테스트
python scripts/figma_export.py --test

# 3. 전체 슬라이드 Export (업데이트 없이)
python scripts/figma_export.py --all

# 4. 특정 슬라이드만 Export
python scripts/figma_export.py --slide 1,3,5,7

# 5. 콘텐츠 업데이트 + Export
python scripts/figma_export.py --all --update --data weekly/copy.md

# 6. Dry run (시뮬레이션)
python scripts/figma_export.py --all --dry-run

# 7. 최적화 + Fallback
python scripts/figma_export.py --all --optimize --fallback
```

---

## 🔄 E. Fallback 메커니즘

### HTML 방식 자동 전환

```python
# fallback_handler.py

import os
import subprocess
from typing import Optional

class FallbackHandler:
    """
    Figma 실패 시 HTML 방식으로 자동 전환
    """
    
    def __init__(self, html_script: str = "scripts/compose_carousel.py"):
        self.html_script = html_script
    
    def trigger_html_fallback(self, input_data: Optional[str] = None) -> bool:
        """
        HTML 방식 실행
        
        Args:
            input_data: 입력 데이터 파일 경로
        
        Returns:
            성공 여부
        """
        try:
            cmd = ["python", self.html_script]
            
            if input_data:
                cmd.extend(["--input", input_data])
            
            print("🔄 Triggering HTML fallback...")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print(result.stdout)
            print("✓ HTML fallback completed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ HTML fallback failed: {e}")
            print(e.stderr)
            return False
    
    def should_use_fallback(self, figma_error: Exception) -> bool:
        """
        Fallback 사용 여부 판단
        
        Args:
            figma_error: Figma 에러
        
        Returns:
            Fallback 사용 여부
        """
        # 환경 변수 체크
        use_fallback = os.getenv("USE_HTML_FALLBACK", "true").lower() == "true"
        
        if not use_fallback:
            return False
        
        # 에러 타입별 판단
        error_str = str(figma_error).lower()
        
        # API 인증 실패 → Fallback 사용
        if "401" in error_str or "403" in error_str:
            print("⚠ Figma authentication failed")
            return True
        
        # Rate limit → Fallback 사용
        if "429" in error_str or "rate limit" in error_str:
            print("⚠ Figma API rate limit exceeded")
            return True
        
        # Timeout → Fallback 사용
        if "timeout" in error_str:
            print("⚠ Figma API timeout")
            return True
        
        # 기타 에러 → Fallback 사용 안 함 (재시도 가능)
        return False
```

### 통합 워크플로우

```python
# workflow.py

from .figma_client import FigmaClient
from .figma_exporter import FigmaExporter
from .fallback_handler import FallbackHandler

def execute_carousel_generation(input_data: str, use_figma: bool = True):
    """
    캐러셀 생성 통합 워크플로우
    
    Args:
        input_data: 콘텐츠 데이터 파일
        use_figma: Figma 사용 여부
    """
    fallback = FallbackHandler()
    
    if not use_figma:
        # 직접 HTML 방식 사용
        fallback.trigger_html_fallback(input_data)
        return
    
    try:
        # Figma 방식 시도
        client = FigmaClient()
        exporter = FigmaExporter(client)
        
        # ... (Export 로직)
        
    except Exception as e:
        print(f"✗ Figma generation failed: {e}")
        
        # Fallback 판단
        if fallback.should_use_fallback(e):
            fallback.trigger_html_fallback(input_data)
        else:
            raise
```

---

## 📊 F. 성능 최적화

### 배치 처리

```python
# Figma API 호출 최소화
# 나쁜 예: 슬라이드별로 개별 호출
for slide in slides:
    export_slide(slide.id)  # API 호출 10회

# 좋은 예: 한 번에 일괄 호출
node_ids = [slide.id for slide in slides]
export_all_slides(node_ids)  # API 호출 1회
```

### 캐싱

```python
# figma_cache.py

import json
import time
from pathlib import Path

class FigmaCache:
    """
    Figma API 응답 캐싱
    """
    
    def __init__(self, cache_dir: str = "./.figma_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cached_image_url(self, node_id: str, max_age: int = 3600) -> Optional[str]:
        """
        캐시된 이미지 URL 가져오기
        
        Args:
            node_id: 노드 ID
            max_age: 최대 캐시 시간 (초)
        
        Returns:
            캐시된 URL 또는 None
        """
        cache_file = self.cache_dir / f"{node_id}.json"
        
        if not cache_file.exists():
            return None
        
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        # 캐시 만료 체크
        if time.time() - data["timestamp"] > max_age:
            return None
        
        return data["url"]
    
    def set_cached_image_url(self, node_id: str, url: str):
        """
        이미지 URL 캐싱
        """
        cache_file = self.cache_dir / f"{node_id}.json"
        
        with open(cache_file, 'w') as f:
            json.dump({
                "timestamp": time.time(),
                "node_id": node_id,
                "url": url
            }, f)
```

---

## 🧪 G. 테스트

### 단위 테스트

```python
# tests/test_figma_client.py

import pytest
from gena_feed.figma_client import FigmaClient

def test_figma_connection():
    """Figma API 연결 테스트"""
    client = FigmaClient()
    assert client.test_connection() == True

def test_get_file():
    """파일 정보 가져오기 테스트"""
    client = FigmaClient()
    file_data = client.get_file()
    
    assert "name" in file_data
    assert "document" in file_data

@pytest.mark.skipif(not os.getenv("FIGMA_ACCESS_TOKEN"), reason="No Figma token")
def test_export_image():
    """이미지 Export 테스트"""
    from gena_feed.figma_exporter import FigmaExporter
    
    client = FigmaClient()
    exporter = FigmaExporter(client, output_dir="./test_output")
    
    # 테스트용 노드 ID (실제 파일에 맞게 수정)
    test_node_id = "123:456"
    
    output_path = exporter.export_slide(test_node_id, "test_slide.png")
    
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
```

---

## 📝 H. 환경 변수 템플릿

```bash
# .env.example

# ============================================
# Figma API Configuration
# ============================================

# Figma Personal Access Token
# Get it from: https://www.figma.com/settings (Personal Access Tokens)
FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Figma File ID
# Extract from URL: https://www.figma.com/file/{FILE_ID}/...
FIGMA_FILE_ID=aBcDeFgHiJkLmNoPqRsTuVwXyZ

# Figma Team ID (Optional, for team libraries)
# FIGMA_TEAM_ID=123456789

# ============================================
# Export Configuration
# ============================================

# Export scale (1.0 = @1x, 2.0 = @2x, 3.0 = @3x)
FIGMA_EXPORT_SCALE=2

# Export format (png, jpg, svg, pdf)
FIGMA_EXPORT_FORMAT=png

# Output directory
FIGMA_OUTPUT_DIR=./output

# ============================================
# Fallback Configuration
# ============================================

# Use HTML fallback if Figma fails (true/false)
USE_HTML_FALLBACK=true

# HTML script path
HTML_FALLBACK_SCRIPT=scripts/compose_carousel.py

# ============================================
# Cache Configuration
# ============================================

# Enable API response caching (true/false)
FIGMA_CACHE_ENABLED=true

# Cache directory
FIGMA_CACHE_DIR=./.figma_cache

# Cache max age in seconds (3600 = 1 hour)
FIGMA_CACHE_MAX_AGE=3600
```

---

## 🎯 I. 구현 로드맵

### Phase 1: 기본 연동 (Week 1-2)
- [ ] Figma API 클라이언트 구현
- [ ] 노드 매핑 JSON 생성
- [ ] 이미지 Export 기능
- [ ] CLI 인터페이스

### Phase 2: 동적 업데이트 (Week 3-4)
- [ ] Figma Plugin 개발
- [ ] Plugin Bridge 구현
- [ ] 콘텐츠 파서 (copy.md → SlideData)
- [ ] 템플릿 업데이트 워크플로우

### Phase 3: 고도화 (Week 5-6)
- [ ] Fallback 메커니즘
- [ ] 캐싱 시스템
- [ ] PNG 최적화
- [ ] 에러 핸들링

### Phase 4: 테스트 & 문서화 (Week 7-8)
- [ ] 단위 테스트 작성
- [ ] 통합 테스트
- [ ] 사용자 가이드 작성
- [ ] 성능 튜닝

---

## 📚 참고 자료

- **Figma REST API:** https://www.figma.com/developers/api
- **Figma Plugin API:** https://www.figma.com/plugin-docs/
- **Figma Variables (Beta):** https://help.figma.com/hc/en-us/articles/15339657135383
- **requests Library:** https://docs.python-requests.org/
- **Python dotenv:** https://pypi.org/project/python-dotenv/

---

**문서 버전:** 1.0  
**작성일:** 2026-03-01  
**작성자:** GenArchive Development Team  
**다음 단계:** Figma Plugin 개발 및 통합 테스트
