# hwpx-bogosu

한글 문서(hwpx) 보고서 자동 생성

## 사용법

```bash
# 양식1: 정식 보고서
python3 hwpx_generator.py -t 1 --title "제목" --department "부서" --author "작성자"

# 양식2: 요약 보고서
python3 hwpx_generator.py -t 2 --title "제목" --department "부서" --author "작성자" \
    --overview "개요" --approaches "방안1" "방안2" "방안3"
```

## 출력 위치

```
.claude/skills/hwpx-bogosu/output/
```

자세한 사용법은 부모 디렉토리의 `hwpx-bogosu.skill.md` 참조
