# hwpx-bogosu

> 한글(hwpx) 보고서 자동 생성 스킬

## Description

Python 스크립트를 사용하여 한글(hwpx) 문서를 자동으로 생성합니다.
두 가지 표준 양식(정식 보고서, 요약 보고서)을 지원합니다.

## Triggers

hwpx, 한글 문서, 보고서 생성, 한컴 문서, hwp, 문서 만들기, 보고서 작성,
report generation, hancom document, create document

## Actions

| Action | Description | Example |
|--------|-------------|---------|
| `create` | hwpx 문서 생성 | `/hwpx-bogosu create 양식1 "제목"` |
| `template1` | 정식 보고서 생성 | `/hwpx-bogosu template1` |
| `template2` | 요약 보고서 생성 | `/hwpx-bogosu template2` |

## Usage

### 기본 사용법

사용자가 다음과 같이 요청하면:

```
"2026년 1분기 실적 보고서를 hwpx로 만들어줘.
부서는 영업팀이고 작성자는 홍길동이야."
```

Claude가 자동으로:

1. 요구사항 분석 (양식, 제목, 부서, 작성자)
2. 적절한 명령어 구성
3. Python 스크립트 실행
4. 생성된 파일 경로 제공

### 양식 선택

**양식1 - 정식 보고서 (공식 문서용)**
- 용도: 공식 제안서, 10+ 페이지 보고서
- 명령어:
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 1 \
    --title "제목" \
    --department "부서" \
    --author "작성자"
```

**양식2 - 요약 보고서 (신사업/내부 보고서용)**
- 용도: 1-2 페이지 요약, 신사업 보고서
- 명령어:
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 2 \
    --title "제목" \
    --department "부서" \
    --author "작성자" \
    --overview "개요" \
    --approaches "방안1" "방안2" "방안3" \
    --budget "항목:금액" "항목:금액"
```

## Examples

### 예시 1: 신사업 보고서

**사용자 요청:**
```
"AI 챗봇 시스템 도입 보고서를 만들어줘.
IT혁신부서, 김철수 부장이 작성.
개요는 '최신 AI 기술을 활용한 고객 서비스 혁신'이야."
```

**Claude 실행:**
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 2 \
    --title "AI 챗봇 시스템 도입 보고서" \
    --department "IT혁신부서" \
    --author "김철수 부장" \
    --overview "최신 AI 기술을 활용한 고객 서비스 혁신" \
    --approaches "AI 모델 선정" "시스템 구축" "테스트" \
    --budget "AI모델:10억" "개발:30억"
```

### 예시 2: 분기 보고서

**사용자 요청:**
```
"2026년 1분기 실적 보고서, 영업팀, 홍길동"
```

**Claude 실행:**
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 2 \
    --title "2026년 1분기 실적 보고서" \
    --department "영업팀" \
    --author "홍길동" \
    --overview "2026년 1분기 주요 사업 추진 현황 및 성과"
```

### 예시 3: 정식 제안서

**사용자 요청:**
```
"클라우드 전환 사업 제안서 만들어줘. 디지털혁신부, 이영희 팀장"
```

**Claude 실행:**
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 1 \
    --title "2027년 클라우드 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희 팀장"
```

## Output

생성된 파일 위치:
```
/home/snowwon5/m-coding/.claude/skills/hwpx-bogosu/output/{제목}_{날짜}.hwpx
```

Windows에서 접근:
```
\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\.claude\skills\hwpx-bogosu\output\
```

## Options Reference

### 필수 옵션
- `-t, --template`: 템플릿 타입 (1=정식, 2=요약)
- `--title`: 문서 제목

### 공통 옵션
- `--department`: 소속 부서 (기본값: OOOO부서)
- `--author`: 작성자 (기본값: 작성자)
- `--date`: 작성일 YYYY.MM.DD (기본값: 오늘)

### 양식1 전용
- `--recipient`: 수신처

### 양식2 전용
- `--overview`: 개요/목적
- `--approaches`: 추진방안 (3개 이상)
- `--budget`: 예산 "항목:금액" 형식
- `--notes`: 기타사항 (3개 이상)

## Implementation Rules

When user requests hwpx document generation:

1. **Analyze Requirements**
   - Determine template type (1 or 2)
   - Extract: title, department, author
   - For template 2: extract overview, approaches, budget

2. **Build Command**
   - Use required options
   - Add user-specific information
   - Quote strings with special characters

3. **Execute**
   ```bash
   cd .claude/skills/hwpx-bogosu
   python3 hwpx_generator.py [options...]
   ```

4. **Report Results**
   - Show generated file path
   - Provide Windows path if needed
   - Remind to open with HancomOffice

## Technical Details

- **Format**: hwpx (ZIP-based XML, HancomOffice format)
- **Requirements**: Python 3.6+, HancomOffice 2014+ (for opening files)
- **Script Location**: `.claude/skills/hwpx-bogosu/hwpx_generator.py`
- **Template Location**: `.claude/skills/hwpx-bogosu/assets/`
- **Output Directory**: `.claude/skills/hwpx-bogosu/output/`

## Quick Templates

### 신사업 제안
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 2 --title "{{사업명}}" \
    --department "{{부서}}" --author "{{작성자}}" \
    --overview "{{개요}}" \
    --approaches "기획" "개발" "운영"
```

### 분기 보고서
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 2 --title "{{연도}} {{분기}} 실적 보고" \
    --department "{{부서}}" --author "{{작성자}}" \
    --overview "{{분기}} 주요 사업 추진 현황 및 성과"
```

### 공식 제안서
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 1 --title "{{제안서명}}" \
    --department "{{부서}}" --author "{{작성자}}" \
    --recipient "{{수신처}}"
```

## Related Skills

- `/pdca`: PDCA 보고서를 hwpx로 출력
- `/code-review`: 코드 리뷰 결과를 hwpx로 출력

## Tips

1. **제목에 특수문자**: 따옴표로 감싸기
   ```bash
   --title "2026년 \"특별\" 프로젝트"
   ```

2. **긴 내용**: 백슬래시로 줄바꿈
   ```bash
   python3 hwpx_generator.py \
       -t 2 \
       --title "제목" \
       --overview "긴 내용..."
   ```

3. **자동 생성**: 자연어로 요청하면 Claude가 자동 처리
   ```
   "영업팀 1분기 보고서 만들어줘" → 자동으로 적절한 명령어 구성
   ```
