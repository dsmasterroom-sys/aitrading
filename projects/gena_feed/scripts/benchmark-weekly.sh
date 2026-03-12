#!/bin/bash
# 벤치마크 주간 분석 자동 실행

set -e  # 오류 발생 시 중단

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TODAY=$(date +%Y-%m-%d)
REPORT_PATH="$PROJECT_DIR/docs/benchmarks/weekly-$TODAY.md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 벤치마크 주간 분석 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📅 분석 일자: $TODAY"
echo "📁 리포트 경로: $REPORT_PATH"
echo ""

# 1. 벤치마크 디렉토리 생성 (없을 경우)
mkdir -p "$PROJECT_DIR/docs/benchmarks"

# 2. Researcher 에이전트 실행
echo "🤖 Step 1/3: Researcher 에이전트 실행 중..."
echo ""

# 주의: 실제 환경에 맞게 claude 또는 sessions_spawn 명령 조정 필요
# 아래는 예시 명령입니다.

# Option A: Claude CLI 직접 호출 (로컬 환경)
# claude --agent researcher \
#   --task "벤치마크 계정 5개 분석: @1ldk_shop, @oncuration, @eun_noo, @theopen_product, @nobordersshop (최근 7일)" \
#   --context "$PROJECT_DIR/workflows/benchmark-analysis.md" \
#   --output "$REPORT_PATH"

# Option B: OpenClaw sessions_spawn (권장)
# openclaw sessions spawn \
#   --runtime subagent \
#   --agent researcher \
#   --task "벤치마크 계정 5개 분석: @1ldk_shop, @oncuration, @eun_noo, @theopen_product, @nobordersshop (최근 7일). workflows/benchmark-analysis.md를 참조하여 주간 리포트 작성." \
#   --mode run \
#   --cleanup delete \
#   --cwd "$PROJECT_DIR"

# 임시: 수동 실행 안내 (자동화 완성 전까지)
echo "⚠️  자동 에이전트 호출은 아직 구현되지 않았습니다."
echo "    수동으로 researcher 에이전트를 실행해주세요:"
echo ""
echo "    1. OpenClaw에서 researcher 에이전트 spawn"
echo "    2. Task: \"벤치마크 계정 5개 분석 (최근 7일)\""
echo "    3. 결과를 $REPORT_PATH에 저장"
echo ""
echo "    또는 Jarvis에게 다음과 같이 요청:"
echo "    \"벤치마크 주간 분석 실행해줘\""
echo ""

# 3. 리포트 생성 확인
if [ ! -f "$REPORT_PATH" ]; then
    echo "❌ 리포트 파일이 생성되지 않았습니다: $REPORT_PATH"
    echo "   researcher 에이전트를 수동으로 실행한 후 다시 시도하세요."
    exit 1
fi

echo "✅ Step 1/3 완료: 벤치마크 리포트 생성됨"
echo ""

# 4. Contents-Marketer 에이전트 실행 (인사이트 추출)
echo "🤖 Step 2/3: Contents-Marketer 인사이트 추출 중..."
echo ""

# 실제 환경에 맞게 명령 조정
# openclaw sessions spawn \
#   --runtime subagent \
#   --agent contents-marketer \
#   --task "벤치마크 리포트($REPORT_PATH)에서 인사이트 추출 및 @gena_feed 적용 액션 생성. workflows/benchmark-analysis.md 참조." \
#   --mode run \
#   --cleanup delete \
#   --cwd "$PROJECT_DIR"

echo "⚠️  인사이트 추출은 아직 자동화되지 않았습니다."
echo "    리포트 확인 후 수동으로 적용 액션을 정리하세요."
echo ""

echo "✅ Step 2/3 완료 (수동 확인 필요)"
echo ""

# 5. 누적 인사이트 업데이트 (Python 스크립트)
echo "🤖 Step 3/3: 누적 인사이트 업데이트 중..."
echo ""

# Python 스크립트 호출 (아직 미구현)
# if [ -f "$SCRIPT_DIR/update_insights_summary.py" ]; then
#     python3 "$SCRIPT_DIR/update_insights_summary.py" "$REPORT_PATH"
# else
#     echo "⚠️  update_insights_summary.py가 없습니다. 수동으로 insights-summary.md를 업데이트하세요."
# fi

echo "⚠️  자동 업데이트 스크립트는 아직 구현되지 않았습니다."
echo "    docs/benchmarks/insights-summary.md를 수동으로 업데이트하세요."
echo ""

echo "✅ Step 3/3 완료 (수동 확인 필요)"
echo ""

# 6. 완료 메시지
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 벤치마크 주간 분석 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 생성된 리포트: $REPORT_PATH"
echo "📊 누적 인사이트: $PROJECT_DIR/docs/benchmarks/insights-summary.md"
echo ""
echo "다음 단계:"
echo "  1. 리포트 검토"
echo "  2. 적용 액션 확인 (HIGH 우선순위 항목)"
echo "  3. 다음 시리즈 기획 시 자동 반영됩니다."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
