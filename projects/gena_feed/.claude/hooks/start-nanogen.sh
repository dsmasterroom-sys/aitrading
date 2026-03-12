#!/bin/bash
# 나노젠 로컬 서버 자동 시작 (이미 실행 중이면 스킵)

NANOGEN_DIR="/Users/master/.openclaw/workspace/nanogen"
VENV_PYTHON="$NANOGEN_DIR/venv/bin/python"
PORT=8000
LOG_FILE="/tmp/nanogen-server.log"

# 이미 실행 중인지 확인
if curl -s -o /dev/null --connect-timeout 2 http://localhost:$PORT 2>/dev/null; then
  echo "nanogen server already running on port $PORT"
  exit 0
fi

# 서버 백그라운드 실행
nohup "$VENV_PYTHON" "$NANOGEN_DIR/manage.py" runserver $PORT > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# 최대 10초 대기
for i in {1..10}; do
  if curl -s -o /dev/null --connect-timeout 1 http://localhost:$PORT 2>/dev/null; then
    echo "nanogen server started (PID: $SERVER_PID, port: $PORT)"
    exit 0
  fi
  sleep 1
done

echo "nanogen server failed to start. log: $LOG_FILE" >&2
exit 0
