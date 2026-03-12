# workflow-reels.md — 릴스 제작 (Nanogen Workflow Studio)

trigger: "릴스 만들어줘" / "영상 제작" / weekly에서 릴스 포맷 확정 시

---

## 사전 확인

- [ ] `weekly/research.md` 확정 주제 존재 여부
- [ ] `assets/gena-base.png` 존재 여부
- [ ] `assets/slant-product.png` 존재 여부
- [ ] Nanogen 서버 응답 확인: `GET http://localhost:8000/`
- [ ] `gena_reels_base` 워크플로 저장 여부 (없으면 AGENT.md 노드 구성 참조)

---

## 실행 흐름

```
STEP 1. spawn: contents-marketer (plan-content)
  스킬: skills/plan-content.md
  입력: weekly/research.md (확정 주제)
  출력: weekly/scene-plan.json (S1~S6 씬 구성)

STEP 2. spawn: contents-marketer (write-copy)
  스킬: skills/write-copy.md + skills/monetize.md
  입력: weekly/scene-plan.json
  출력: weekly/copy.md (씬별 자막 스크립트 S1~S6)

STEP 3. spawn: designer
  스킬: skills/design-visual.md
  입력: weekly/scene-plan.json + weekly/copy.md
  출력: weekly/image-prompts.json (씬별 이미지·동영상 프롬프트)
  → S4·S6 Outfit Swap 여부 확인 포함

STEP 4. [G2 게이팅] 사용자 확인
  전달 내용:
    - 씬 구성 요약 (S1~S6 역할·자막)
    - 씬별 권장 모델:
        S1 kling-v3 pro (훅 — 품질 최우선)
        S2 kling-v2.6 standard (공감 — 속도 가능)
        S3 kling-v2.6 standard (팁 — 속도 가능)
        S4 kling-v3 pro (Outfit Swap — 디테일 중요)
        S5 kling-v3 pro (결론 — 품질 우선)
        S6 kling-v3 pro (CTA — 구매 욕구)
    - monetize 태그 + 광고 표기 방식
  대기: 사용자 모델 선택 + 승인

STEP 5. spawn: developer (Nanogen 실행)
  스킬: skills/build-html.md (TRACK 2)
  실행:
    - Nanogen gena_reels_base 워크플로 로드
    - weekly/scene-plan.json + weekly/image-prompts.json 데이터 교체
    - Nanogen API 호출 (씬별 이미지 생성 → I2V 변환)
    - ffmpeg 클립 합성 + 자막 + BGM
  출력: output/reels/final.mp4
  완료 후: scene-05.png → assets/reels/ 복사

STEP 6. spawn: qa-reviewer
  스킬: skills/qa-check.md (릴스 항목)
  출력: weekly/qa-report.md

STEP 7. QA 루프
  고·중 이슈 존재 시: developer 재수정 → qa-reviewer 재검증
  고·중 이슈 0건까지 반복

STEP 8. [G3 게이팅] 발행 최종 확인
  체크: QA 0건 · slant CTA S6 · 광고 표기 · 재생 15~30초
  통과 후: Buffer/Later 금요일 19:00 예약
```
