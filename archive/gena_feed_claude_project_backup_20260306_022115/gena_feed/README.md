# gena_feed - Figma Template Export

Figma 템플릿 기반 캐러셀 Export 파이프라인입니다.

## 구현 범위

- `gena_feed/figma_client.py`: Figma REST API 클라이언트
- `gena_feed/figma_updater.py`: 템플릿 업데이트 페이로드 생성 + Plugin bridge
- `gena_feed/figma_exporter.py`: PNG Export/다운로드/최적화
- `gena_feed/models.py`: `SlideData`, `NodeMapping`, `TemplatePattern`
- `gena_feed/fallback_handler.py`: Figma 실패 시 HTML fallback 실행
- `scripts/figma_export.py`: 통합 CLI

## 사전 준비

1. `.env.example`을 `.env`로 복사 후 값 설정
2. Python 3.11+
3. 의존성 설치

```bash
pip install requests python-dotenv
# optimize 옵션 사용 시
pip install pillow
# markdown/yaml 데이터 파싱 시 (권장)
pip install pyyaml
```

## CLI 사용법

```bash
python scripts/figma_export.py --all
python scripts/figma_export.py --slide 1,3,7
python scripts/figma_export.py --all --update --data weekly/copy.md
python scripts/figma_export.py --all --optimize
python scripts/figma_export.py --all --fallback
python scripts/figma_export.py --test
```

### 주요 옵션

- `--all`: 전체 슬라이드 Export
- `--slide 1,3,7`: 특정 슬라이드 Export
- `--update --data <file>`: Figma Plugin 업데이트 요청 JSON 생성 후 대기
- `--optimize`: Export 후 PNG 최적화(Pillow)
- `--fallback`: Figma 실패 시 `scripts/compose_carousel.py` 실행
- `--dry-run`: 실제 Export 없이 매핑/타겟 검증
- `--mapping-file`: 매핑 JSON 직접 지정 (기본 탐색: `figma_mappings.json`, `figma-node-mapping.json`)

## 매핑 파일

- 권장: `figma_mappings.json`
- 호환: `figma-node-mapping.json` (이 경우 텍스트/이미지/컬러 노드 매핑은 비어 있을 수 있음)

## 백업

기존 스크립트 백업:

- `scripts/backup/figma_export.py.bak`
- `scripts/backup/figma_node_mapper.py.bak`
