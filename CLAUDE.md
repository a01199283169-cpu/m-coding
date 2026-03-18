# Project Guide for Claude

## Available Custom Tools

### hwpx-bogosu: 한글 문서 자동 생성기

**위치**: `.claude/skills/hwpx-bogosu/`

**기능**: 한글(hwpx) 보고서를 자동으로 생성합니다.

**사용법**:
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t [1|2] --title "제목" --department "부서" --author "작성자"
```

**양식 타입**:
- `1`: 정식 보고서 (공식 문서, 제안서용)
- `2`: 요약 보고서 (신사업, 내부 보고서용)

**양식2 추가 옵션**:
```bash
--overview "개요/목적"
--approaches "방안1" "방안2" "방안3"
--budget "항목1:금액1" "항목2:금액2"
--notes "사항1" "사항2" "사항3"
```

**예시**:
```bash
# 신사업 보고서
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py \
    -t 2 \
    --title "AI 챗봇 시스템 도입 보고서" \
    --department "IT혁신부서" \
    --author "김철수 부장" \
    --overview "최신 AI 기술을 활용한 고객 서비스 혁신" \
    --approaches "AI 모델 선정" "시스템 구축" "테스트 및 배포" \
    --budget "AI모델:10억원" "개발:30억원" "운영:5억원"

# 정식 제안서
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py \
    -t 1 \
    --title "2027년 클라우드 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희 팀장"
```

**출력 위치**:
```
.claude/skills/hwpx-bogosu/output/{제목}_{날짜}.hwpx
```

**Windows 경로**:
```
\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\.claude\skills\hwpx-bogosu\output\
```

**문서**:
- 사용 설명서: `.claude/skills/hwpx-bogosu/README.md`
- 기술 문서: `.claude/skills/hwpx-bogosu/hwpx-bogosu.skill.md`
- 예시 스크립트: `.claude/skills/hwpx-bogosu/examples.sh`

---

### hello: 간단한 인사 스킬 (예제)

**위치**: `.claude/skills/hello.skill.md`

**기능**: 시간대에 맞는 인사를 합니다.

**트리거**: "안녕", "hello", "인사"

**동작**:
- 아침(6-12시): "좋은 아침입니다 ☀️"
- 점심(12-18시): "좋은 오후입니다 🌤️"
- 저녁(18-22시): "좋은 저녁입니다 🌙"
- 밤(22-6시): "늦은 시간이네요 🌃"

---

## How to Use

When user requests hwpx document generation:

1. **확인**: 양식 타입(1 또는 2), 제목, 부서, 작성자
2. **명령 구성**: 위 사용법 참고하여 명령어 작성
3. **실행**:
   ```bash
   cd .claude/skills/hwpx-bogosu
   python3 hwpx_generator.py [옵션...]
   ```
4. **결과**: 생성된 파일 경로와 Windows 경로 제공

**Important**:
- 양식1: 공식 문서, 10+ 페이지
- 양식2: 신사업/내부 보고서, 1-2 페이지
- 특수문자 있으면 따옴표로 감싸기
- 생성 후 한컴오피스 2014 이상에서 열기
