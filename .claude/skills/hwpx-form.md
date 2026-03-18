# hwpx-form: 한글 양식 파일 처리 스킬

**교육실습생 명단 등 hwpx 양식 파일을 읽고, 분석하고, 데이터를 추출하는 스킬입니다.**

Use proactively when user mentions hwpx files, 한글 양식, 교육실습, or form processing.

Triggers: hwpx, 한글 양식, 교육실습생, form processing, 실습명단, 양식 읽기,
hwpxファイル, ハングル様式, フォーム処理, hwpx文件, 表格处理,
archivo hwpx, formulario, fichier hwpx, formulaire,
hwpx-Datei, Formular, file hwpx, modulo

---

## 📋 주요 기능

### 1. hwpx 파일 분석
- hwpx 파일 구조 읽기 (ZIP 기반)
- 텍스트 내용 추출 (Preview/PrvText.txt)
- XML 메타데이터 분석 (Contents/header.xml, Contents/section0.xml)

### 2. 교육실습생 명단 양식 처리
- 교육실습기간 추출
- 유치원/기관명 추출
- 실습생 명단 테이블 파싱:
  - 순번
  - 성명
  - 학번
  - 연락처
  - 비고

### 3. 데이터 변환
- hwpx → JSON 변환
- hwpx → CSV 변환
- hwpx → Python dict 변환
- JSON/CSV → hwpx 생성 (템플릿 기반)

---

## 🚀 사용 예시

### 예시 1: hwpx 파일 읽기
```
"assets/yuasifsubnane.hwpx 파일 읽어줘"
```

**동작:**
1. Python zipfile로 hwpx 파일 열기
2. Preview/PrvText.txt 추출
3. 구조화된 데이터로 파싱
4. 결과를 보기 좋게 표시

### 예시 2: JSON으로 변환
```
"hwpx 파일을 JSON으로 변환해줘"
```

**출력 형식:**
```json
{
  "schools": [
    {
      "name": "이루니유치원",
      "period": {
        "start": "2025-04-07",
        "end": "2025-05-02",
        "duration": "4주 (160시간 이상)"
      },
      "students": [
        {
          "순번": 1,
          "성명": "김00",
          "학번": "20220036",
          "연락처": "010-6618-1051",
          "비고": ""
        }
      ]
    }
  ]
}
```

### 예시 3: CSV 추출
```
"교육실습생 명단을 CSV로 추출해줘"
```

**출력:**
```csv
유치원명,순번,성명,학번,연락처,비고,실습기간
이루니유치원,1,김00,20220036,010-6618-1051,,2025-04-07~2025-05-02
이루니유치원,2,정00,20220046,010-0000-0000,,2025-04-07~2025-05-02
```

### 예시 4: 새 양식 생성
```
"빈 교육실습생 명단 양식 만들어줘"
```

**동작:**
1. 기존 hwpx 템플릿 로드
2. 데이터 부분만 초기화
3. 새 hwpx 파일 생성

---

## 🔧 구현 가이드

### hwpx 파일 구조
```
yuasifsubnane.hwpx (ZIP file)
├── mimetype
├── version.xml
├── Contents/
│   ├── header.xml          # 문서 헤더
│   ├── section0.xml        # 본문 내용
│   └── content.hpf         # 바이너리 콘텐츠
├── Preview/
│   ├── PrvText.txt         # 텍스트 미리보기 (★ 가장 쉽게 읽을 수 있음)
│   └── PrvImage.png        # 이미지 미리보기
├── META-INF/
│   ├── container.xml
│   ├── container.rdf
│   └── manifest.xml
└── settings.xml
```

### Python 코드 템플릿

#### 1. hwpx 읽기
```python
import zipfile
import json
import re

def read_hwpx(file_path):
    """hwpx 파일 읽고 텍스트 추출"""
    with zipfile.ZipFile(file_path) as z:
        # 미리보기 텍스트 읽기 (가장 간단)
        if 'Preview/PrvText.txt' in z.namelist():
            with z.open('Preview/PrvText.txt') as f:
                return f.read().decode('utf-8', errors='ignore')
    return None

def parse_student_list(text):
    """교육실습생 명단 파싱"""
    schools = []

    # 유치원별로 분리
    sections = re.split(r'가\. 교육실습기간:', text)[1:]  # 첫 번째는 빈 문자열

    for section in sections:
        school_data = {}

        # 기간 추출
        period_match = re.search(r'(\d{4})학년도\s+(\d+)월\s+(\d+)일.*?~\s+(\d+)월\s+(\d+)일.*?총\s+(\d+)주.*?(\d+)시간', section)
        if period_match:
            school_data['period'] = {
                'year': period_match.group(1),
                'start_month': period_match.group(2),
                'start_day': period_match.group(3),
                'end_month': period_match.group(4),
                'end_day': period_match.group(5),
                'weeks': period_match.group(6),
                'hours': period_match.group(7)
            }

        # 유치원명 추출
        name_match = re.search(r'나\. 교육실습생 명단\((.+?)\)', section)
        if name_match:
            school_data['name'] = name_match.group(1)

        # 학생 데이터 추출
        students = []
        student_pattern = r'<(\d+)><([^>]+)><([^>]+)><([^>]+)><([^>]*)>'
        for match in re.finditer(student_pattern, section):
            if match.group(2).strip():  # 이름이 있는 경우만
                students.append({
                    '순번': int(match.group(1)),
                    '성명': match.group(2),
                    '학번': match.group(3),
                    '연락처': match.group(4),
                    '비고': match.group(5)
                })

        if students:
            school_data['students'] = students
            schools.append(school_data)

    return schools

# 사용 예시
text = read_hwpx('assets/yuasifsubnane.hwpx')
data = parse_student_list(text)
print(json.dumps(data, ensure_ascii=False, indent=2))
```

#### 2. CSV 변환
```python
import csv

def to_csv(schools, output_file='students.csv'):
    """JSON 데이터를 CSV로 변환"""
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['유치원명', '순번', '성명', '학번', '연락처', '비고', '실습기간'])

        for school in schools:
            period = school.get('period', {})
            period_str = f"{period.get('year', '')}년 {period.get('start_month', '')}월 {period.get('start_day', '')}일~{period.get('end_month', '')}월 {period.get('end_day', '')}일"

            for student in school.get('students', []):
                writer.writerow([
                    school.get('name', ''),
                    student.get('순번', ''),
                    student.get('성명', ''),
                    student.get('학번', ''),
                    student.get('연락처', ''),
                    student.get('비고', ''),
                    period_str
                ])

    print(f"CSV 파일 생성 완료: {output_file}")
```

#### 3. Excel 변환 (선택사항)
```python
import pandas as pd

def to_excel(schools, output_file='students.xlsx'):
    """JSON 데이터를 Excel로 변환"""
    rows = []

    for school in schools:
        period = school.get('period', {})
        period_str = f"{period.get('year', '')}년 {period.get('start_month', '')}월 {period.get('start_day', '')}일~{period.get('end_month', '')}월 {period.get('end_day', '')}일"

        for student in school.get('students', []):
            rows.append({
                '유치원명': school.get('name', ''),
                '순번': student.get('순번', ''),
                '성명': student.get('성명', ''),
                '학번': student.get('학번', ''),
                '연락처': student.get('연락처', ''),
                '비고': student.get('비고', ''),
                '실습기간': period_str
            })

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)
    print(f"Excel 파일 생성 완료: {output_file}")
```

---

## 📝 양식 템플릿

### 교육실습생 명단 양식 구조
```
가. 교육실습기간: {year}학년도 {start_month}월 {start_day}일(월) ~ {end_month}월 {end_day}일(금) / 총 {weeks}주({hours}시간 이상)

나. 교육실습생 명단({school_name})
<순 번><성 명><학 번><연락처><비 고>
<1><홍길동><20220001><010-0000-0000><>
<2><김철수><20220002><010-1111-1111><>
...
```

---

## ⚠️ 주의사항

### hwpx 파일 처리 제약
1. **바이너리 콘텐츠**: content.hpf는 바이너리 형식이므로 파싱 어려움
2. **XML 복잡도**: section0.xml은 복잡한 구조, Preview/PrvText.txt 사용 권장
3. **버전 호환성**: 한글 버전에 따라 XML 스키마 다를 수 있음

### 데이터 추출 한계
1. **표 구조**: 복잡한 중첩 표는 정확도 떨어질 수 있음
2. **서식 정보**: 글꼴, 색상 등 서식 정보는 손실됨
3. **이미지**: 이미지는 별도 추출 필요

---

## 🔍 활용 시나리오

### 1. 데이터 마이그레이션
```
문제: 교육실습생 명단이 hwpx 파일로만 관리됨
해결: hwpx → JSON → 데이터베이스 저장
```

### 2. 자동화 시스템 연동
```
문제: 수기로 hwpx 파일 열어서 데이터 입력
해결: Python 스크립트로 자동 파싱 → API 전송
```

### 3. 통계 분석
```
문제: 여러 기관의 실습생 현황 파악 어려움
해결: 모든 hwpx 파일 파싱 → CSV 통합 → 데이터 분석
```

### 4. 양식 표준화
```
문제: 각 기관마다 다른 양식 사용
해결: 표준 JSON 스키마 정의 → hwpx 템플릿 생성
```

---

## 📚 확장 가능성

### 추가 기능 아이디어
1. **웹 인터페이스**: Flask/FastAPI로 hwpx 업로드 → 데이터 표시
2. **자동 검증**: 학번 형식, 연락처 형식 자동 체크
3. **병합 기능**: 여러 hwpx 파일을 하나의 Excel/CSV로 병합
4. **템플릿 편집기**: 웹에서 양식 편집 → hwpx 생성
5. **OCR 통합**: 스캔 이미지 → hwpx 자동 생성

---

## 🎯 사용 권장 사항

### 언제 이 스킬을 사용하나요?
- ✅ hwpx 파일 데이터를 프로그래밍 방식으로 읽어야 할 때
- ✅ 교육실습생 명단을 데이터베이스에 저장해야 할 때
- ✅ 여러 hwpx 파일을 통합 분석해야 할 때
- ✅ hwpx → JSON/CSV 변환이 필요할 때

### 언제 이 스킬을 사용하지 않나요?
- ❌ 한글 워드프로세서로 직접 편집하는 것이 더 빠를 때
- ❌ 복잡한 서식/레이아웃을 유지해야 할 때
- ❌ 일회성 데이터 확인만 필요할 때

---

## 🛠️ 의존성

### 필수
- Python 3.6+
- zipfile (내장 모듈)

### 선택사항
- pandas: Excel 변환
- openpyxl: Excel 파일 쓰기
- lxml: XML 파싱 (고급 기능)

### 설치
```bash
pip install pandas openpyxl
```

---

## 💡 팁

### 빠른 데이터 확인
```python
# 1줄로 hwpx 텍스트 읽기
import zipfile
text = zipfile.ZipFile('file.hwpx').open('Preview/PrvText.txt').read().decode('utf-8')
print(text)
```

### 에러 처리
```python
def safe_read_hwpx(file_path):
    try:
        with zipfile.ZipFile(file_path) as z:
            if 'Preview/PrvText.txt' in z.namelist():
                with z.open('Preview/PrvText.txt') as f:
                    return f.read().decode('utf-8', errors='ignore')
    except zipfile.BadZipFile:
        print(f"Error: {file_path} is not a valid hwpx file")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None
```

---

## 📞 지원

이 스킬은 교육실습생 명단 양식을 기준으로 작성되었습니다.
다른 hwpx 양식을 처리하려면 파싱 로직을 수정해야 할 수 있습니다.

---

**Version:** 1.0.0
**Author:** Claude Code
**Last Updated:** 2026-03-10
