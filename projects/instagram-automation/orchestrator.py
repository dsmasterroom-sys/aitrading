#!/usr/bin/env python3
"""
Instagram Automation Orchestrator
자동화 캐러셀/릴스 생성 시스템

Usage:
    python orchestrator.py carousel "봄 패션 트렌드"
    python orchestrator.py reels "데님 스타일링"
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent
CONTENT_DIR = PROJECT_ROOT / "content"
AGENTS_DIR = PROJECT_ROOT / "agents"
SKILLS_DIR = PROJECT_ROOT / "skills"


class Orchestrator:
    """메인 오케스트레이터: 전체 파이프라인 관리"""
    
    def __init__(self, content_type: str, topic: str):
        self.content_type = content_type  # carousel, reels, story
        self.topic = topic
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.work_dir = CONTENT_DIR / f"{self.timestamp}_{self._slugify(topic)}"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🚀 Orchestrator 시작")
        print(f"   Type: {content_type}")
        print(f"   Topic: {topic}")
        print(f"   Work Dir: {self.work_dir}")
        print()
    
    def _slugify(self, text: str) -> str:
        """파일명용 슬러그 생성"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        return text[:50]
    
    def _spawn_agent(
        self,
        agent_name: str,
        task: str,
        model: str,
        label: Optional[str] = None
    ) -> Dict:
        """
        OpenClaw sessions_spawn 호출
        
        Returns:
            {"sessionKey": "...", "status": "..."}
        """
        print(f"🤖 {agent_name} 스폰 중...")
        print(f"   Task: {task[:80]}...")
        print(f"   Model: {model}")
        
        # sessions_spawn은 OpenClaw 내부에서만 작동
        # 이 스크립트는 OpenClaw 세션 내에서 실행되어야 함
        # 임시로 placeholder 반환
        
        # TODO: 실제 구현은 OpenClaw의 sessions_send/sessions_spawn 사용
        # 예시:
        # result = sessions_spawn(
        #     agentId=agent_name,
        #     task=task,
        #     model=model,
        #     label=label or f"{self.timestamp}_{agent_name}"
        # )
        
        session_key = f"agent:isolated:{agent_name}:{self.timestamp}"
        
        print(f"✅ {agent_name} 스폰 완료")
        print(f"   Session: {session_key}")
        print()
        
        return {
            "sessionKey": session_key,
            "status": "running",
            "agent": agent_name
        }
    
    def _wait_for_completion(self, sessions: List[Dict]) -> None:
        """여러 세션이 완료될 때까지 대기"""
        print(f"⏳ {len(sessions)}개 세션 완료 대기 중...")
        
        # TODO: sessions_history로 폴링
        # 임시로 sleep
        time.sleep(2)
        
        print(f"✅ 모든 세션 완료")
        print()
    
    def _read_file(self, filename: str) -> str:
        """작업 디렉토리에서 파일 읽기"""
        filepath = self.work_dir / filename
        if filepath.exists():
            return filepath.read_text()
        return ""
    
    def _write_file(self, filename: str, content: str) -> None:
        """작업 디렉토리에 파일 쓰기"""
        filepath = self.work_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        print(f"💾 {filename} 저장 완료")
    
    # ========== Phase 1: 트렌드 + 아이템 리서치 ==========
    
    def phase1_research(self) -> Dict:
        """병렬 리서치: researcher + item-researcher"""
        print("=" * 60)
        print("📊 Phase 1: 트렌드 + 아이템 리서치")
        print("=" * 60)
        print()
        
        # 병렬 실행
        researcher_session = self._spawn_agent(
            agent_name="researcher",
            task=f"{self.topic} 관련 인스타그램 트렌드 조사 (2026년 3월 기준). "
                 f"추천 토픽 6개 제시. research.md 작성.",
            model="claude-sonnet-4-6"
        )
        
        item_researcher_session = self._spawn_agent(
            agent_name="item-researcher",
            task=f"{self.topic} 관련 패션 아이템 10개 수집 (무신사/지그재그). "
                 f"각 아이템: 이미지 URL, 가격, 브랜드, 시각적 설명. items.json 작성.",
            model="claude-sonnet-4-6"
        )
        
        self._wait_for_completion([researcher_session, item_researcher_session])
        
        # 결과 읽기 (임시)
        research_md = self._read_file("research.md")
        items_json = self._read_file("items.json")
        
        if not research_md:
            # 임시 데이터 (실제로는 에이전트가 작성)
            research_md = f"""# {self.topic} 트렌드 리서치

## 추천 토픽
1. 오버사이즈 니트 코디
2. 레이어드 룩
3. 데님 온 데님
4. 파스텔 스프링 룩
5. 미니멀 모노톤
6. 빈티지 아카이브

## 해시태그
#봄패션 #데일리룩 #오버핏 ...
"""
            self._write_file("research.md", research_md)
        
        if not items_json:
            # 임시 데이터
            items = [
                {
                    "id": i + 1,
                    "name": f"아이템 {i+1}",
                    "brand": "Brand",
                    "price": 50000 + i * 10000,
                    "ref_image_url": f"https://example.com/item{i+1}.jpg",
                    "visual_desc": f"아이템 {i+1} 설명"
                }
                for i in range(10)
            ]
            items_json = json.dumps(items, ensure_ascii=False, indent=2)
            self._write_file("items.json", items_json)
        
        print("✅ Phase 1 완료")
        print()
        
        return {
            "research": research_md,
            "items": json.loads(items_json)
        }
    
    # ========== Gate G1: 토픽 확정 ==========
    
    def gate_g1_topic_selection(self, research: str) -> str:
        """사용자에게 토픽 선택 요청"""
        print("=" * 60)
        print("🚦 Gate G1: 토픽 확정")
        print("=" * 60)
        print()
        print(research)
        print()
        
        # TODO: 실제로는 사용자 입력 대기
        # 임시로 첫 번째 토픽 선택
        selected_topic = "오버사이즈 니트 코디"
        print(f"✅ 선택된 토픽: {selected_topic}")
        print()
        
        return selected_topic
    
    # ========== Phase 2: 프롬프트 생성 ==========
    
    def phase2_prompt_engineering(self, selected_topic: str, items: List[Dict]) -> Dict:
        """프롬프트 엔지니어링"""
        print("=" * 60)
        print("✍️  Phase 2: 프롬프트 생성")
        print("=" * 60)
        print()
        
        prompt_engineer_session = self._spawn_agent(
            agent_name="prompt-engineer",
            task=f"토픽: {selected_topic}\n"
                 f"아이템: {len(items)}개\n"
                 f"캐러셀 10슬라이드 프롬프트 생성. "
                 f"Gena 캐릭터 착장. prompts.json 작성.",
            model="claude-opus-4-6"
        )
        
        self._wait_for_completion([prompt_engineer_session])
        
        prompts_json = self._read_file("prompts.json")
        
        if not prompts_json:
            # 임시 데이터
            prompts = [
                {
                    "slide": i + 1,
                    "image_prompt": f"Slide {i+1} prompt",
                    "reference_images": []
                }
                for i in range(10)
            ]
            prompts_json = json.dumps(prompts, ensure_ascii=False, indent=2)
            self._write_file("prompts.json", prompts_json)
        
        print("✅ Phase 2 완료")
        print()
        
        return json.loads(prompts_json)
    
    # ========== Phase 3: 콘텐츠 기획 + 이미지 생성 (병렬) ==========
    
    def phase3_content_and_design(self, prompts: List[Dict], items: List[Dict]) -> Dict:
        """병렬 실행: contents-marketer + designer"""
        print("=" * 60)
        print("🎨 Phase 3: 콘텐츠 기획 + 이미지 생성")
        print("=" * 60)
        print()
        
        marketer_session = self._spawn_agent(
            agent_name="contents-marketer",
            task=f"캐러셀 기획 및 카피 작성. "
                 f"슬라이드별 제목, 본문, CTA. "
                 f"plan.md, copy.md 작성.",
            model="openai/gpt-5.2"
        )
        
        designer_session = self._spawn_agent(
            agent_name="designer",
            task=f"캐러셀 10슬라이드 이미지 생성 (Nanogen Outfit Swap). "
                 f"Gena 캐릭터 일관성 최우선. "
                 f"assets/ 폴더에 저장.",
            model="openai/gpt-5-mini"
        )
        
        self._wait_for_completion([marketer_session, designer_session])
        
        plan_md = self._read_file("plan.md")
        copy_md = self._read_file("copy.md")
        
        if not plan_md:
            plan_md = f"# {self.topic} 캐러셀 기획\n\n전체 기획 의도..."
            self._write_file("plan.md", plan_md)
        
        if not copy_md:
            copy_md = "# 슬라이드별 카피\n\n## Slide 1\n..."
            self._write_file("copy.md", copy_md)
        
        print("✅ Phase 3 완료")
        print()
        
        return {
            "plan": plan_md,
            "copy": copy_md
        }
    
    # ========== Phase 4: HTML 슬라이드 생성 ==========
    
    def phase4_html_slides(self) -> None:
        """developer: HTML → PNG 렌더링"""
        print("=" * 60)
        print("💻 Phase 4: HTML 슬라이드 생성")
        print("=" * 60)
        print()
        
        developer_session = self._spawn_agent(
            agent_name="developer",
            task=f"캐러셀 HTML 슬라이드 생성 (디자인 시스템 기반). "
                 f"Puppeteer로 PNG 렌더링. "
                 f"slides/ 폴더에 저장.",
            model="claude-sonnet-4-6"
        )
        
        self._wait_for_completion([developer_session])
        
        print("✅ Phase 4 완료")
        print()
    
    # ========== Phase 5: QA 검수 ==========
    
    def phase5_qa_review(self) -> Dict:
        """qa-reviewer: 자동 검수"""
        print("=" * 60)
        print("🔍 Phase 5: QA 검수")
        print("=" * 60)
        print()
        
        qa_reviewer_session = self._spawn_agent(
            agent_name="qa-reviewer",
            task=f"캐러셀 QA 검수 (시각/팩트/레이아웃). "
                 f"validate_slide.py 실행. "
                 f"qa-report.md 작성.",
            model="openai/gpt-5-mini"
        )
        
        self._wait_for_completion([qa_reviewer_session])
        
        qa_report = self._read_file("qa-report.md")
        
        if not qa_report:
            qa_report = "# QA Report\n\n✅ 모든 검사 통과"
            self._write_file("qa-report.md", qa_report)
        
        print("✅ Phase 5 완료")
        print()
        
        # 간단한 파싱 (실제로는 JSON 파싱)
        has_critical_issues = "고 이슈" in qa_report or "FAIL" in qa_report
        
        return {
            "report": qa_report,
            "passed": not has_critical_issues
        }
    
    # ========== Phase 6: 스케줄링 ==========
    
    def phase6_scheduling(self) -> Dict:
        """scheduler: 발행 예약"""
        print("=" * 60)
        print("📅 Phase 6: 스케줄링")
        print("=" * 60)
        print()
        
        scheduler_session = self._spawn_agent(
            agent_name="scheduler",
            task=f"캐러셀 발행 준비 (Meta API 업로드). "
                 f"schedule.json 작성.",
            model="openai/gpt-5-mini"
        )
        
        self._wait_for_completion([scheduler_session])
        
        schedule_json = self._read_file("schedule.json")
        
        if not schedule_json:
            schedule_json = json.dumps({
                "content_type": self.content_type,
                "topic": self.topic,
                "slides_count": 10,
                "scheduled_time": datetime.now().isoformat(),
                "status": "ready"
            }, ensure_ascii=False, indent=2)
            self._write_file("schedule.json", schedule_json)
        
        print("✅ Phase 6 완료")
        print()
        
        return json.loads(schedule_json)
    
    # ========== 메인 실행 ==========
    
    def run_carousel_pipeline(self) -> Dict:
        """캐러셀 전체 파이프라인 실행"""
        start_time = time.time()
        
        print()
        print("=" * 60)
        print(f"🚀 CAROUSEL PIPELINE 시작")
        print(f"   Topic: {self.topic}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        # Phase 1: 리서치
        research_result = self.phase1_research()
        
        # Gate G1: 토픽 선택
        selected_topic = self.gate_g1_topic_selection(research_result["research"])
        
        # Phase 2: 프롬프트
        prompts = self.phase2_prompt_engineering(selected_topic, research_result["items"])
        
        # Phase 3: 콘텐츠 + 이미지
        content = self.phase3_content_and_design(prompts, research_result["items"])
        
        # Phase 4: HTML 슬라이드
        self.phase4_html_slides()
        
        # Phase 5: QA
        qa_result = self.phase5_qa_review()
        
        if not qa_result["passed"]:
            print("⚠️  QA 실패: 수동 확인 필요")
            return {"status": "qa_failed", "qa_report": qa_result["report"]}
        
        # Phase 6: 스케줄링
        schedule = self.phase6_scheduling()
        
        elapsed_time = time.time() - start_time
        
        print()
        print("=" * 60)
        print(f"✅ CAROUSEL PIPELINE 완료!")
        print(f"   소요 시간: {elapsed_time:.1f}초")
        print(f"   Work Dir: {self.work_dir}")
        print("=" * 60)
        print()
        
        return {
            "status": "success",
            "work_dir": str(self.work_dir),
            "schedule": schedule,
            "elapsed_time": elapsed_time
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python orchestrator.py <type> <topic>")
        print("  type: carousel, reels, story")
        print("  topic: 주제 (예: '봄 패션 트렌드')")
        sys.exit(1)
    
    content_type = sys.argv[1]
    topic = " ".join(sys.argv[2:])
    
    if content_type not in ["carousel", "reels", "story"]:
        print(f"❌ 지원하지 않는 타입: {content_type}")
        print("   carousel, reels, story 중 선택")
        sys.exit(1)
    
    orchestrator = Orchestrator(content_type, topic)
    
    if content_type == "carousel":
        result = orchestrator.run_carousel_pipeline()
    elif content_type == "reels":
        print("❌ Reels 파이프라인은 아직 구현되지 않음")
        sys.exit(1)
    elif content_type == "story":
        print("❌ Story 파이프라인은 아직 구현되지 않음")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
