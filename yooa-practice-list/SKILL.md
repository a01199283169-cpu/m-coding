---
name: yooa-practice-list
description: "유아교육과 교육실습생 명단 hwpx 양식 파일을 생성하고 관리하는 스킬"
version: "1.0.0"
author: "Claude Code"
triggers:
  - 교육실습
  - 실습생 명단
  - 유아교육
  - hwpx 양식
  - 실습명단 만들기
---

# yooa-practice-list

유아교육과 교육실습생 명단 hwpx 양식 파일을 생성합니다.

## 양식 구조

```
가. 교육실습기간: 2025학년도 4월 7일(월) ~ 5월 2일(금) / 총 4주(160시간 이상)

나. 교육실습생 명단(이루니유치원)
<순 번><성 명><학 번><연락처><비 고>
<1><김철수><20220036><010-1234-5678><>
<2><이영희><20220046><010-2345-6789><>
```

## 사용 예시

### 1. 새 명단 생성

사용자: "신규 유치원 3곳에 실습생 각 5명씩 배치한 명단 만들어줘"

**생성 절차:**
1. 실습기간 확인 (학년도, 시작일, 종료일, 주수, 시간)
2. 유치원 이름 입력받기
3. 각 유치원별 실습생 정보 입력
4. hwpx 양식 생성

### 2. 기존 명단 수정

사용자: "이루니유치원 명단에 실습생 2명 추가해줘"

**수정 절차:**
1. 기존 hwpx 파일 파싱
2. 해당 유치원 찾기
3. 순번 자동 증가하여 학생 추가
4. 업데이트된 hwpx 생성

## 핵심 템플릿

```python
# hwpx 생성 템플릿
TEMPLATE = """
가. 교육실습기간: {year}학년도 {start_month}월 {start_day}일(월) ~ {end_month}월 {end_day}일(금) / 총 {weeks}주({hours}시간 이상)

나. 교육실습생 명단({school_name})
<순 번><성 명><학 번><연락처><비 고>
{student_rows}
"""

STUDENT_ROW = "<{no}><{name}><{student_id}><{phone}><{note}>"
```

## 생성 가이드

### Step 1: 데이터 준비
```python
data = {
    "year": "2025",
    "start": "2025-04-07",
    "end": "2025-05-02",
    "weeks": 4,
    "hours": 160,
    "schools": [
        {
            "name": "이루니유치원",
            "students": [
                {"no": 1, "name": "김철수", "id": "20220036", "phone": "010-1234-5678"},
                {"no": 2, "name": "이영희", "id": "20220046", "phone": "010-2345-6789"}
            ]
        }
    ]
}
```

### Step 2: hwpx 파일 생성 (hwpx_generator.py 사용)
```bash
python3 hwpx_generator.py --input data.json --output 실습명단_2025.hwpx
```

## 중요 규칙

1. **학번**: 8자리 숫자 (예: 20220036)
2. **연락처**: 010-####-#### 형식
3. **순번**: 1부터 순차 증가
4. **실습기간**: 총 4주, 160시간 이상
5. **빈 칸**: `<>` 형식으로 표시

## 자동 검증

생성 시 자동으로 다음을 검증:
- 학번 8자리 확인
- 연락처 형식 확인
- 순번 중복 체크
- 필수 필드 누락 확인

## 빠른 명령어

```bash
# 템플릿 기반 생성
python3 hwpx_generator.py --template basic --schools 3 --students 5

# JSON에서 생성
python3 hwpx_generator.py --json data.json

# 대화형 생성
python3 hwpx_generator.py --interactive
```

## 참고

- 샘플 파일: `assets/yuasifsubnane.hwpx`
- 파싱 도구: `hwpx_parser.py`
- 검증 도구: `validate_data.py`
