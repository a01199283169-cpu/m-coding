#!/bin/bash
# 신한대학교 기자재 관리 시스템 종료 스크립트

echo "🛑 기자재 관리 시스템 종료 중..."
pkill -f "streamlit run app.py"

sleep 2
if ps aux | grep -v grep | grep "streamlit run app.py" > /dev/null; then
    echo "⚠️ 프로세스가 아직 실행 중입니다. 강제 종료합니다..."
    pkill -9 -f "streamlit run app.py"
    sleep 1
fi

if ps aux | grep -v grep | grep "streamlit run app.py" > /dev/null; then
    echo "❌ 종료 실패"
else
    echo "✅ 서버가 종료되었습니다."
fi
