---
name: hwpx-bogosu
description: "한글(hwpx) 보고서 자동 생성 스킬 - 정식 보고서와 요약 보고서 양식 지원"
version: "1.0.0"
author: "Claude Code"
triggers:
  - hwpx
  - 한글 문서
  - 보고서 생성
  - 한컴 문서
  - hwp
  - 문서 만들기
  - 보고서 작성
  - report
  - hancom
---

# hwpx-bogosu

한글(hwpx) 보고서를 자동으로 생성하는 스킬입니다.
두 가지 표준 양식(정식 보고서, 요약 보고서)을 지원합니다.

## 양식 타입

### 양식1 - 정식 보고서
- **용도**: 공식 문서, 제안서
- **분량**: 10+ 페이지
- **특징**: 상세한 내용 전개

### 양식2 - 요약 보고서
- **용도**: 신사업, 내부 보고서
- **분량**: 1-2 페이지
- **특징**: 핵심 요약 중심

## 사용 예시

### 1. 분기 보고서

**사용자:** "2026년 1분기 실적 보고서 만들어줘. 영업팀, 작성자 홍길동"

**생성 절차:**
1. 양식 선택 (자동: 양식2)
2. 필수 정보 추출 (제목, 부서, 작성자)
3. 개요 자동 생성
4. hwpx 파일 생성

### 2. 신사업 제안서

**사용자:** "AI 챗봇 시스템 도입 보고서 만들어줘. IT혁신부서, 김철수 부장, 개요는 최신 AI 기술 활용"

**생성 절차:**
1. 양식 선택 (자동: 양식2)
2. 필수 정보 + 개요 추출
3. 추진방안 기본값 설정
4. hwpx 파일 생성

### 3. 공식 제안서

**사용자:** "클라우드 전환 사업 제안서 만들어줘. 디지털혁신부, 이영희 팀장"

**생성 절차:**
1. 양식 선택 (명시 또는 자동: 양식1)
2. 필수 정보 추출
3. 수신처 확인 (선택사항)
4. hwpx 파일 생성

## 핵심 옵션

### 필수 옵션
```bash
-t, --template      # 양식 타입 (1=정식, 2=요약)
--title            # 문서 제목
```

### 공통 옵션
```bash
--department       # 소속 부서 (기본값: OOOO부서)
--author          # 작성자 (기본값: 작성자)
--date            # 작성일 YYYY.MM.DD (기본값: 오늘)
```

### 양식1 전용
```bash
--recipient       # 수신처
```

### 양식2 전용
```bash
--overview        # 개요/목적
--approaches      # 추진방안 (공백으로 구분, 3개 권장)
--budget          # 예산 "항목:금액" 형식 (공백으로 구분)
--notes           # 기타사항 (공백으로 구분, 3개 권장)
```

## 명령어 템플릿

### 양식1 (정식 보고서)
```bash
python3 hwpx_generator.py -t 1 \
    --title "제안서 제목" \
    --department "부서명" \
    --author "작성자명"
```

### 양식2 (요약 보고서)
```bash
python3 hwpx_generator.py -t 2 \
    --title "보고서 제목" \
    --department "부서명" \
    --author "작성자명" \
    --overview "사업 개요 및 목적" \
    --approaches "1단계" "2단계" "3단계" \
    --budget "개발비:10억" "운영비:5억"
```

## 출력

### 생성 위치
```
hwpx-bogosu-skill/output/{제목}_{날짜}.hwpx
```

### Windows 경로
```
\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\hwpx-bogosu-skill\output\
```

## 자동 검증

생성 시 자동으로 다음을 확인:
- ✅ 템플릿 파일 존재 확인
- ✅ 필수 필드 입력 확인
- ✅ ZIP 구조 검증 (mimetype 첫 번째 + uncompressed)
- ✅ 파일 순서 보존
- ✅ 압축 타입 매핑 유지

## 빠른 명령어

```bash
# 기본 보고서
python3 hwpx_generator.py -t 2 --title "실적 보고" --department "영업팀" --author "홍길동"

# 상세 보고서
python3 hwpx_generator.py -t 2 \
    --title "AI 프로젝트 보고서" \
    --department "IT팀" \
    --author "김철수" \
    --overview "AI 도입으로 업무 효율화" \
    --approaches "분석" "구축" "테스트" \
    --budget "개발:10억" "운영:5억"

# 공식 제안서
python3 hwpx_generator.py -t 1 --title "클라우드 전환 제안서" --department "디지털혁신부" --author "이영희"
```

## 중요 규칙

1. **mimetype 파일**: 반드시 첫 번째 + uncompressed (ZIP_STORED)
2. **파일 순서**: 원본 템플릿과 동일하게 유지
3. **압축 타입**: 각 파일의 원본 압축 방식 보존
4. **특수문자**: 따옴표로 감싸기
5. **한컴오피스**: 2014 이상 버전에서 열기

## 참고

- **템플릿**: `assets/(샘플양식1).hwpx`, `assets/(샘플양식2).hwpx`
- **생성기**: `hwpx_generator.py`
- **상세 문서**: `README.md`
- **빠른 시작**: `QUICKSTART.md`
- **예시 모음**: `EXAMPLES.md`
