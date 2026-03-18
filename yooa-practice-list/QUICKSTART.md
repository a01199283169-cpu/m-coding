# 빠른 시작 가이드 (Quick Start)

yooa-practice-list 프로젝트를 5분 안에 시작하는 방법입니다.

## 1️⃣ 기본 사용 (의존성 설치 불필요)

### hwpx 파일 내용 확인
```bash
python3 hwpx_parser.py assets/yuasifsubnane.hwpx --summary
```

**출력 예시:**
```
============================================================
📄 파일: yuasifsubnane.hwpx
============================================================

[1] 이루니유치원
    📅 2025년 4월 7일 ~ 5월 2일 (총 4주, 160시간)
    👥 실습생: 2명

        1. 김00    | 학번: 20220036   | 연락처: 010-6618-1051
        2. 정00    | 학번: 20220046   | 연락처: 010-0000-0000
```

### JSON 변환
```bash
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -j data.json
cat data.json  # 결과 확인
```

### CSV 변환
```bash
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -c data.csv
cat data.csv  # 결과 확인
```

---

## 2️⃣ 데이터 검증

```bash
# 기본 검증
python3 validate_data.py assets/yuasifsubnane.hwpx

# 엄격 모드 (경고도 표시)
python3 validate_data.py assets/yuasifsubnane.hwpx --strict
```

---

## 3️⃣ 여러 파일 일괄 처리

```bash
# 1. assets/ 폴더에 여러 hwpx 파일 배치
cp ~/Downloads/*.hwpx assets/

# 2. 일괄 변환
./batch_convert.sh

# 3. 결과 확인
ls -lh output/
```

---

## 4️⃣ Excel 변환 (선택사항)

```bash
# pandas 설치
pip install pandas openpyxl

# Excel 변환
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -x data.xlsx
```

---

## 5️⃣ Python 코드에서 사용

```python
from hwpx_parser import HwpxParser

# 파서 생성
parser = HwpxParser('assets/yuasifsubnane.hwpx')

# 데이터 가져오기
schools = parser.parse_student_list()

# 첫 번째 기관 정보
print(schools[0]['name'])        # 이루니유치원
print(len(schools[0]['students']))  # 2

# 모든 실습생 이름
for school in schools:
    for student in school.get('students', []):
        print(student['성명'], student['학번'])
```

---

## 6️⃣ 일반적인 작업 흐름

```bash
# 1. 새 hwpx 파일 받기
cp ~/Downloads/2025-신규명단.hwpx assets/

# 2. 먼저 확인
python3 hwpx_parser.py assets/2025-신규명단.hwpx --summary

# 3. 검증
python3 validate_data.py assets/2025-신규명단.hwpx

# 4. 변환
python3 hwpx_parser.py assets/2025-신규명단.hwpx -c output/2025-신규명단.csv

# 5. CSV를 Excel에서 열기
# 또는
python3 hwpx_parser.py assets/2025-신규명단.hwpx -x output/2025-신규명단.xlsx
```

---

## 🆘 문제 해결

### 문제: "파일을 찾을 수 없습니다"
```bash
# 해결: 절대 경로 사용
python3 hwpx_parser.py /full/path/to/file.hwpx
```

### 문제: "No such file or directory: 'hwpx_parser.py'"
```bash
# 해결: yooa-practice-list 디렉토리로 이동
cd /path/to/yooa-practice-list
python3 hwpx_parser.py assets/yuasifsubnane.hwpx
```

### 문제: CSV 한글 깨짐
```bash
# 해결: UTF-8 BOM으로 저장되므로 Excel에서 자동 인식됨
# 메모장/VS Code에서 열 때는 UTF-8 인코딩 선택
```

---

## 📚 더 자세한 정보

- 전체 기능: `README.md`
- 스킬 가이드: `SKILL.md`
- 도움말: `python3 hwpx_parser.py --help`

---

**Tip:** Claude Code 스킬을 사용하면 자연어로 요청 가능합니다:
```
"hwpx 파일 읽어줘"
"교육실습생 명단을 CSV로 변환해줘"
```
