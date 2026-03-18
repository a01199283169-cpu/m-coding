# hwpx-bogosu - 간단 버전

## CLAUDE.md에 추가 (간단 버전)

---

### hwpx-bogosu

한글(hwpx) 보고서 자동 생성기

**위치**: `.claude/skills/hwpx-bogosu/`

**사용법**:
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t [1|2] --title "제목" --department "부서" --author "작성자"
```

**양식**:
- `1`: 정식 보고서 (공식 문서)
- `2`: 요약 보고서 (신사업/내부)

**예시**:
```bash
# 간단 사용
python3 hwpx_generator.py -t 2 --title "1분기 보고" --department "영업팀" --author "홍길동"

# 상세 사용 (양식2)
python3 hwpx_generator.py -t 2 --title "AI 프로젝트 보고" \
    --department "IT팀" --author "김철수" \
    --overview "AI 도입으로 업무 효율화" \
    --approaches "분석" "구축" "테스트" \
    --budget "개발:10억" "운영:5억"
```

**출력**: `output/{제목}_{날짜}.hwpx`

**문서**: `README.md`, `hwpx-bogosu.skill.md`

---
