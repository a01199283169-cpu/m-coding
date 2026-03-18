#!/bin/bash
# 여러 hwpx 파일을 일괄 변환하는 스크립트

set -e  # 에러 발생 시 중단

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "======================================"
echo "hwpx 파일 일괄 변환 시작"
echo "======================================"

# output 디렉토리 생성
mkdir -p output

# 변환할 파일 카운트
file_count=$(find assets -name "*.hwpx" | wc -l)
echo -e "${YELLOW}변환할 파일: ${file_count}개${NC}\n"

if [ $file_count -eq 0 ]; then
    echo -e "${RED}❌ assets/ 폴더에 hwpx 파일이 없습니다${NC}"
    exit 1
fi

# 각 hwpx 파일 처리
current=0
for file in assets/*.hwpx; do
    current=$((current + 1))
    basename="${file##*/}"
    basename="${basename%.hwpx}"

    echo -e "${GREEN}[$current/$file_count]${NC} 처리 중: $basename"

    # JSON, CSV 변환
    python3 hwpx_parser.py "$file" \
        -j "output/${basename}.json" \
        -c "output/${basename}.csv" 2>&1 | grep -E "✅|❌|오류" || true

    echo ""
done

echo "======================================"
echo -e "${GREEN}✅ 일괄 변환 완료${NC}"
echo "======================================"
echo ""
echo "생성된 파일 목록:"
ls -lh output/ | tail -n +2 | awk '{print "  " $9 " (" $5 ")"}'
echo ""

# 요약 통계
json_count=$(find output -name "*.json" | wc -l)
csv_count=$(find output -name "*.csv" | wc -l)

echo "요약:"
echo "  JSON 파일: ${json_count}개"
echo "  CSV 파일: ${csv_count}개"
echo ""
