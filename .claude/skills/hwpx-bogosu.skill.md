# hwpx-bogosu

한글 문서(hwpx) 보고서 자동 생성 스킬

## Description

Python 스크립트를 사용하여 한글(hwpx) 문서를 자동으로 생성합니다.
두 가지 표준 양식을 지원합니다.

## Trigger Keywords

hwpx, 한글 문서, 보고서 양식, 한컴 문서, 보고서 작성, hwp, 문서 생성

## Usage

### 양식 선택

**양식1 - 정식 보고서 (공식 문서용)**
```bash
cd hwpx-Bogosu
python3 hwpx_generator.py -t 1 --title "제목" --department "부서" --author "작성자"
```

**양식2 - 요약 보고서 (신사업/내부 보고서용)**
```bash
cd hwpx-Bogosu
python3 hwpx_generator.py -t 2 --title "제목" --department "부서" --author "작성자" \
    --overview "개요" \
    --approaches "방안1" "방안2" "방안3" \
    --budget "항목1:금액1" "항목2:금액2"
```

## Examples

### 예시 1: 클라우드 전환 제안서 (양식1)
```bash
cd hwpx-Bogosu
python3 hwpx_generator.py \
    -t 1 \
    --title "2027년 클라우드 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희 팀장" \
    --recipient "기술혁신센터"
```

### 예시 2: AI 챗봇 보고서 (양식2)
```bash
cd hwpx-Bogosu
python3 hwpx_generator.py \
    -t 2 \
    --title "AI 챗봇 시스템 도입 보고서" \
    --department "IT혁신부서" \
    --author "김철수 부장" \
    --overview "최신 AI 기술을 활용한 고객 서비스 혁신" \
    --approaches "AI 모델 선정" "시스템 구축" "테스트 및 배포" \
    --budget "AI모델:10억원" "개발:30억원" "운영:5억원"
```

### 예시 일괄 실행
```bash
cd hwpx-Bogosu
./examples.sh
```

## Options

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

## Output

생성된 파일 위치:
```
hwpx-Bogosu/output/{제목}_{날짜}.hwpx
```

Windows 경로:
```
\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\hwpx-Bogosu\output\
```

## Implementation Steps

사용자가 hwpx 문서 생성을 요청하면:

1. **요구사항 확인**
   - 양식 타입 선택 (1: 정식, 2: 요약)
   - 제목, 부서, 작성자 확인
   - 양식2의 경우 추가 정보 확인

2. **명령어 구성**
   - 필수 옵션 추가
   - 사용자 정보에 맞게 옵션 구성
   - 특수문자가 있으면 따옴표로 감싸기

3. **실행**
   ```bash
   cd hwpx-Bogosu
   python3 hwpx_generator.py [옵션...]
   ```

4. **결과 확인**
   - 생성된 파일 경로 출력
   - Windows 경로 제공
   - 한컴오피스로 열기 안내

## Quick Templates

### 신사업 제안
```bash
python3 hwpx_generator.py -t 2 --title "{{사업명}}" \
    --department "{{부서}}" --author "{{작성자}}" \
    --overview "{{개요}}" \
    --approaches "기획" "개발" "운영"
```

### 분기 보고서
```bash
python3 hwpx_generator.py -t 2 --title "{{연도}} {{분기}} 실적 보고" \
    --department "{{부서}}" --author "{{작성자}}" \
    --overview "{{분기}} 주요 사업 추진 현황 및 성과"
```

### 공식 제안서
```bash
python3 hwpx_generator.py -t 1 --title "{{제안서명}}" \
    --department "{{부서}}" --author "{{작성자}}" \
    --recipient "{{수신처}}"
```

## Files Location

- 스크립트: `hwpx-Bogosu/hwpx_generator.py`
- 템플릿: `hwpx-Bogosu/assets/`
- 출력: `hwpx-Bogosu/output/`
- 문서: `hwpx-Bogosu/README.md`
- 상세 문서: `hwpx-Bogosu/hwpx-bogosu.skill.md`

## Requirements

- Python 3.6+
- 한컴오피스 2014+ (파일 열기용)

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

3. **빠른 테스트**: examples.sh 실행
   ```bash
   cd hwpx-Bogosu && ./examples.sh
   ```

## Related

- `/pdca`: PDCA 보고서를 hwpx로 출력
- `/code-review`: 코드 리뷰 결과를 hwpx로 출력
