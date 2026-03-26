#!/bin/bash
# 신한대학교 기자재 관리 시스템 시작 스크립트

# 기존 프로세스 종료
pkill -f "streamlit run app.py"

# 디렉토리 이동
cd /home/snowwon5/m-coding/20260322/equipment_manager

# 서버 시작
echo "🚀 기자재 관리 시스템 시작 중..."
python3 -m streamlit run app.py --server.port 8502 --server.headless true > /tmp/equipment.log 2>&1 &

# 프로세스 확인
sleep 3
if ps aux | grep -v grep | grep "streamlit run app.py" > /dev/null; then
    echo "✅ 서버가 정상적으로 시작되었습니다!"
    echo "📍 접속 주소: http://localhost:8502"
    echo "🌐 네트워크: http://$(hostname -I | awk '{print $1}'):8502"
else
    echo "❌ 서버 시작 실패. 로그를 확인하세요: tail -f /tmp/equipment.log"
fi
