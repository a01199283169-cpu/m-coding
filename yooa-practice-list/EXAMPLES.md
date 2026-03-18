# 사용 예시 모음

실제 사용 사례별로 정리한 예시 모음입니다.

## 📝 시나리오별 예시

### 1. 단일 파일 빠르게 확인

**상황:** 담당자가 hwpx 파일을 보내왔고, 내용을 빠르게 확인하고 싶음

```bash
# 요약 보기
python3 hwpx_parser.py received_file.hwpx --summary

# 원본 텍스트 보기
python3 hwpx_parser.py received_file.hwpx --raw
```

---

### 2. CSV로 변환하여 Excel에서 편집

**상황:** 실습생 명단을 Excel에서 열어서 추가 정보 입력

```bash
# CSV 변환
python3 hwpx_parser.py assets/명단.hwpx -c 편집용명단.csv

# Excel에서 열기
# Windows: start 편집용명단.csv
# Mac: open 편집용명단.csv
# Linux: libreoffice 편집용명단.csv
```

---

### 3. 여러 기관 명단 통합

**상황:** 5개 유치원의 명단을 하나로 합치기

```bash
# 방법 1: 일괄 CSV 변환 후 수동 병합
./batch_convert.sh

# 방법 2: Python으로 자동 통합
python3 << 'PYTHON'
import glob
import pandas as pd

all_data = []
for csv_file in glob.glob('output/*.csv'):
    df = pd.read_csv(csv_file)
    all_data.append(df)

merged = pd.concat(all_data, ignore_index=True)
merged.to_excel('output/전체명단_통합.xlsx', index=False)
print(f"✅ 총 {len(merged)}명 통합 완료")
PYTHON
```

---

### 4. 특정 유치원만 추출

**상황:** 전체 명단에서 "이루니유치원"만 따로 추출

```python
from hwpx_parser import HwpxParser
import json

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

# 이루니유치원만 필터링
iruni = [s for s in schools if '이루니' in s.get('name', '')]

# JSON으로 저장
with open('output/이루니유치원_only.json', 'w', encoding='utf-8') as f:
    json.dump(iruni, f, ensure_ascii=False, indent=2)

print(f"✅ {iruni[0]['name']} 학생 {len(iruni[0]['students'])}명 추출 완료")
```

---

### 5. 실습생 연락처 목록만 추출

**상황:** 문자 발송을 위한 전화번호 목록 생성

```python
from hwpx_parser import HwpxParser

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

# 모든 연락처 추출
contacts = []
for school in schools:
    for student in school.get('students', []):
        phone = student.get('연락처', '').strip()
        if phone and phone != '010-0000-0000':  # 더미 번호 제외
            contacts.append({
                '이름': student.get('성명'),
                '연락처': phone,
                '유치원': school.get('name')
            })

# 텍스트 파일로 저장 (한 줄에 하나씩)
with open('output/연락처목록.txt', 'w', encoding='utf-8') as f:
    for contact in contacts:
        f.write(f"{contact['연락처']}\n")

print(f"✅ {len(contacts)}개 연락처 추출 완료")
```

---

### 6. 학번 중복 체크

**상황:** 동일한 학번이 중복 등록되었는지 확인

```python
from hwpx_parser import HwpxParser
from collections import Counter

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

# 모든 학번 수집
student_numbers = []
for school in schools:
    for student in school.get('students', []):
        student_numbers.append(student.get('학번'))

# 중복 찾기
duplicates = [num for num, count in Counter(student_numbers).items() if count > 1]

if duplicates:
    print(f"❌ 중복된 학번 발견: {duplicates}")
else:
    print("✅ 중복 없음")
```

---

### 7. 실습 기간별 그룹화

**상황:** 실습 기간이 다른 기관들을 기간별로 분류

```python
from hwpx_parser import HwpxParser
from collections import defaultdict

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

# 기간별 그룹화
by_period = defaultdict(list)
for school in schools:
    period_str = school.get('period', {}).get('display', '미정')
    by_period[period_str].append(school.get('name'))

# 결과 출력
for period, school_names in by_period.items():
    print(f"\n📅 {period}")
    for name in school_names:
        print(f"   - {name}")
```

---

### 8. 통계 리포트 생성

**상황:** 전체 실습 현황 요약 보고서 작성

```python
from hwpx_parser import HwpxParser

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

print("="*60)
print("📊 교육실습 현황 리포트")
print("="*60)

total_schools = len(schools)
total_students = sum(len(s.get('students', [])) for s in schools)

print(f"\n1. 전체 현황")
print(f"   - 총 기관: {total_schools}개")
print(f"   - 총 실습생: {total_students}명")
print(f"   - 기관당 평균: {total_students/total_schools:.1f}명")

print(f"\n2. 기관별 상세")
for idx, school in enumerate(schools, 1):
    print(f"   {idx}. {school.get('name', '이름없음')}: {len(school.get('students', []))}명")

print(f"\n3. 실습 기간")
periods = set()
for school in schools:
    period = school.get('period', {}).get('display', '')
    if period:
        periods.add(period)

for period in sorted(periods):
    print(f"   - {period}")

print("\n" + "="*60)
```

---

### 9. 이메일 주소 추가 (확장)

**상황:** hwpx에는 없지만, 학번 기반으로 이메일 생성

```python
from hwpx_parser import HwpxParser
import pandas as pd

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

students_with_email = []
for school in schools:
    for student in school.get('students', []):
        student_data = {
            '성명': student.get('성명'),
            '학번': student.get('학번'),
            '연락처': student.get('연락처'),
            '이메일': f"{student.get('학번')}@univ.ac.kr",  # 자동 생성
            '유치원': school.get('name')
        }
        students_with_email.append(student_data)

df = pd.DataFrame(students_with_email)
df.to_excel('output/실습생_이메일포함.xlsx', index=False)
print(f"✅ {len(df)}명 이메일 추가 완료")
```

---

### 10. 출석부 양식 생성

**상황:** 각 유치원별 출석부 Excel 파일 생성

```python
from hwpx_parser import HwpxParser
import pandas as pd
from datetime import datetime, timedelta

parser = HwpxParser('assets/yuasifsubnane.hwpx')
schools = parser.parse_student_list()

for school in schools:
    school_name = school.get('name', '학교')
    students = school.get('students', [])

    if not students:
        continue

    # 실습 기간 날짜 생성 (예: 4주 = 20일)
    period = school.get('period', {})
    start_date = datetime.strptime(period.get('start_date', '2025-04-07'), '%Y-%m-%d')

    dates = []
    current = start_date
    for _ in range(20):  # 20일간
        if current.weekday() < 5:  # 월-금만
            dates.append(current.strftime('%m/%d'))
        current += timedelta(days=1)

    # 출석부 데이터프레임 생성
    attendance_data = []
    for student in students:
        row = {
            '순번': student.get('순번'),
            '성명': student.get('성명'),
            '학번': student.get('학번')
        }
        # 날짜별 출석 칸
        for date in dates:
            row[date] = ''

        attendance_data.append(row)

    df = pd.DataFrame(attendance_data)
    filename = f'output/출석부_{school_name}.xlsx'
    df.to_excel(filename, index=False)
    print(f"✅ {school_name} 출석부 생성: {filename}")
```

---

## 🔄 자동화 스크립트

### Cron Job으로 정기 처리

```bash
# crontab -e
# 매일 오전 9시에 새 파일 확인 및 변환
0 9 * * * cd /path/to/yooa-practice-list && ./batch_convert.sh >> logs/cron.log 2>&1
```

### Watch 폴더 모니터링

```bash
#!/bin/bash
# watch_and_convert.sh

WATCH_DIR="./incoming"
OUTPUT_DIR="./output"

inotifywait -m "$WATCH_DIR" -e create |
while read path action file; do
    if [[ "$file" == *.hwpx ]]; then
        echo "새 파일 감지: $file"
        python3 hwpx_parser.py "$WATCH_DIR/$file" -c "$OUTPUT_DIR/${file%.hwpx}.csv"
    fi
done
```

---

**더 많은 예시가 필요하시면 SKILL.md를 참고하세요!**
