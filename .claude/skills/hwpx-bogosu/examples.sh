#!/bin/bash
# hwpx-bogosu 사용 예시 스크립트

echo "🚀 hwpx-bogosu 예시 실행"
echo "========================================"

# 예시 1: 양식1 - 정식 보고서
echo ""
echo "📋 예시 1: 정식 보고서 (양식1)"
python3 hwpx_generator.py \
    --template 1 \
    --title "2027년 클라우드 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희 팀장" \
    --recipient "기술혁신센터"

# 예시 2: 양식2 - 신사업 보고서
echo ""
echo "📋 예시 2: 신사업 보고서 (양식2)"
python3 hwpx_generator.py \
    --template 2 \
    --title "AI 챗봇 시스템 도입 보고서" \
    --department "IT혁신부서" \
    --author "김철수 부장" \
    --overview "최신 AI 기술을 활용한 고객 서비스 혁신 및 업무 효율화" \
    --approaches "AI 모델 선정 및 검증" "시스템 아키텍처 설계 및 구축" "테스트 및 배포 전략 수립" \
    --budget "AI모델구매:10억원" "시스템개발:30억원" "운영및유지보수:5억원" \
    --notes "AI팀과 협업 필요" "보안 검토 필수" "2026년 12월 오픈 목표"

# 예시 3: 양식2 - 1분기 실적 보고
echo ""
echo "📋 예시 3: 1분기 실적 보고서 (양식2)"
python3 hwpx_generator.py \
    --template 2 \
    --title "2026년 1분기 사업 실적 보고" \
    --department "경영관리팀" \
    --author "박영수 차장" \
    --overview "2026년 1분기 주요 사업 추진 현황 및 성과 보고" \
    --approaches "매출 목표 달성 현황" "신규 고객 확보 현황" "프로젝트 진행 현황"

echo ""
echo "========================================"
echo "✅ 모든 예시 실행 완료!"
echo "📂 output/ 폴더에서 생성된 파일을 확인하세요."
