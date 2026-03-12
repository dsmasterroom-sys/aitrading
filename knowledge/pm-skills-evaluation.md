# PM Skills Marketplace 검토 보고서

**검토일:** 2026-03-07  
**검토자:** 자비스  
**프로젝트:** https://github.com/phuryn/pm-skills.git

---

## 📌 프로젝트 개요

**PM Skills Marketplace** - Claude Code/Cowork용 PM 업무 자동화 스킬 모음
- 65개 스킬 + 36개 워크플로우 (8개 플러그인)
- Teresa Torres, Marty Cagan, Alberto Savoia 등 PM 대가들의 프레임워크 기반
- MIT 라이선스, 활발한 커뮤니티

### 플러그인 구성 (8개)

1. **pm-product-discovery** (13 skills, 5 commands)
   - 아이디어 브레인스토밍, 가설 검증, OST, 인터뷰, 메트릭 대시보드

2. **pm-product-strategy** (12 skills, 5 commands)
   - 비전, 비즈니스 모델, 가격 전략, 경쟁 분석

3. **pm-execution** (15 skills, 10 commands)
   - PRD, OKRs, 로드맵, 스프린트, 회고, 릴리스 노트

4. **pm-market-research** (7 skills, 3 commands)
   - 페르소나, 세그멘테이션, 고객 여정 맵, 시장 규모

5. **pm-data-analytics** (3 skills, 3 commands)
   - SQL 생성, 코호트 분석, A/B 테스트 분석

6. **pm-go-to-market** (6 skills, 3 commands)
   - 비치헤드 세그먼트, ICP, 메시징, 성장 루프, GTM 전략

7. **pm-marketing-growth** (5 skills, 2 commands)
   - 마케팅 아이디어, 포지셔닝, 밸류 프롭, 네이밍, North Star 메트릭

8. **pm-toolkit** (4 skills, 5 commands)
   - 이력서 리뷰, NDA 작성, 프라이버시 정책, 교정

---

## ✅ 강점

1. **검증된 PM 프레임워크 체계화**
   - Opportunity Solution Tree (Teresa Torres)
   - Lean Canvas / Business Model Canvas
   - Jobs-to-be-Done (JTBD)
   - OKRs, PRD 템플릿 등

2. **즉시 실무 적용 가능한 워크플로우**
   - `/discover` → `/strategy` → `/write-prd` → `/plan-launch`
   - 단계별 연결된 커맨드 체인

3. **OpenClaw 호환 가능**
   - SKILL.md 포맷 준수
   - 다른 AI 도구들도 사용 가능

---

## ⚠️ 우리 상황 적합도 분석

### 현재 우선순위 (2026 Q1)
- ✅ **인스타 자동화** (genarchive.kr, gena_feed)
- ✅ **AI 팀 구축 및 자동화 워크플로우**
- ✅ **채널 운영 최적화 (재고 판매 연계)**
- ⚪ IT 프로덕트 개발 (계획 중)

### 적합도 평가
- ❌ 인스타 자동화 - 직접 관련 없음
- ❌ AI 워크플로우 구축 - 직접 관련 없음
- ⚪ IT Product 개발 - **도움 될 수 있음** (전략 수립 단계)

### 기술적 고려사항
- 65개 스킬 전체 로드 시 컨텍스트 오버헤드 발생
- Claude Code/Cowork 중심 설계 (slash 커맨드)
- 우리는 이미 자체 스킬 운영 중 (bkit-lite-codex-v1 등)
- 토큰 효율 최우선 정책과 상충 가능성

---

## 💡 도입 권장사항

### 지금 당장: ❌ **도입 안 함**
**이유:**
- 현 단계 최우선 과제와 직접 연관 없음
- 컨텍스트/토큰 효율 최우선 정책
- 당장 필요한 스킬 아님

### IT 프로덕트 본격 개발 시: ✅ **선택적 도입 고려**

**우선 도입 대상 (3개 플러그인만):**
1. **pm-product-strategy** - 제품 전략, 비즈니스 모델, 가격 전략
2. **pm-execution** - PRD, OKRs, 로드맵 작성
3. **pm-go-to-market** - GTM 전략, ICP, 성장 루프

**테스트 방식:**
- Planner agent 전용으로 설치
- 필요할 때만 로드하는 lazy loading 방식
- 효과 측정 후 확대 여부 결정

---

## 📥 설치 방법 (나중을 위해)

### Claude Code CLI
```bash
# 마켓플레이스 추가
claude plugin marketplace add phuryn/pm-skills

# 선택적 플러그인 설치 (추천: 아래 3개만)
claude plugin install pm-product-strategy@pm-skills
claude plugin install pm-execution@pm-skills
claude plugin install pm-go-to-market@pm-skills
```

### OpenClaw/Codex/Gemini CLI (스킬만)
```bash
# 전체 복사
git clone https://github.com/phuryn/pm-skills.git
cd pm-skills

# OpenClaw workspace에 선택적 복사
cp -r pm-product-strategy/skills/* ~/.openclaw/workspace/skills/
cp -r pm-execution/skills/* ~/.openclaw/workspace/skills/
cp -r pm-go-to-market/skills/* ~/.openclaw/workspace/skills/
```

---

## 🔖 참고 링크

- **GitHub:** https://github.com/phuryn/pm-skills
- **Curator:** Paweł Huryn (The Product Compass Newsletter)
- **License:** MIT
- **기반 서적:**
  - Teresa Torres - Continuous Discovery Habits
  - Marty Cagan - INSPIRED, TRANSFORMED
  - Alberto Savoia - The Right It
  - Dan Olsen - The Lean Product Playbook

---

## 📝 결론 및 넥스트 스텝

**현재 판단:** 좋은 리소스지만 지금 단계에서는 불필요.

**재검토 시점:**
- IT 프로덕트 기획 본격 시작할 때
- PAI 서비스 전략 수립 필요할 때
- 새 프로덕트 PRD/GTM 작성해야 할 때

**보관 위치:** `knowledge/pm-skills-evaluation.md`

---
*검토 완료: 2026-03-07 by 자비스 🤵‍♂️*
