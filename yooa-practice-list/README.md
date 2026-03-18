# hwpx 양식 파서 (hwpx Form Parser)

교육실습생 명단 등 hwpx 양식 파일을 읽고 JSON/CSV/Excel로 변환하는 도구입니다.

## 📋 기능

- ✅ hwpx 파일 자동 파싱
- ✅ 교육실습생 명단 데이터 추출
- ✅ JSON 변환
- ✅ CSV 변환
- ✅ Excel 변환 (pandas 설치 시)
- ✅ 요약 정보 출력

## 🚀 빠른 시작

### 1. 요약 정보 보기
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

        1. 김00    | 학번: 20220036   | 연락처: 010-6618-1051   | 비고:
        2. 정00    | 학번: 20220046   | 연락처: 010-0000-0000   | 비고:

============================================================
총 4개 기관, 4명의 실습생
============================================================
```

### 2. JSON으로 변환
```bash
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -j output.json
```

### 3. CSV로 변환
```bash
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -c output.csv
```

### 4. Excel로 변환
```bash
pip install pandas openpyxl  # 먼저 설치 필요
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -x output.xlsx
```

### 5. 모든 형식으로 한번에 변환
```bash
python3 hwpx_parser.py assets/yuasifsubnane.hwpx -j data.json -c data.csv -x data.xlsx
```

## 📖 사용법

```
usage: hwpx_parser.py [-h] [-j FILE] [-c FILE] [-x FILE] [-s] [--raw] hwpx_file

positional arguments:
  hwpx_file             hwpx 파일 경로

options:
  -h, --help            도움말 표시
  -j FILE, --json FILE  JSON 파일로 저장
  -c FILE, --csv FILE   CSV 파일로 저장
  -x FILE, --excel FILE Excel 파일로 저장
  -s, --summary         요약 정보만 출력
  --raw                 원본 텍스트 출력
```

## 📊 출력 형식

### JSON 형식
```json
{
  "source_file": "assets/yuasifsubnane.hwpx",
  "schools": [
    {
      "period": {
        "year": "2025",
        "start_date": "2025-04-07",
        "end_date": "2025-05-02",
        "weeks": 4,
        "hours": 160,
        "display": "2025년 4월 7일 ~ 5월 2일 (총 4주, 160시간)"
      },
      "name": "이루니유치원",
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

### CSV 형식
```csv
유치원명,순번,성명,학번,연락처,비고,실습기간
이루니유치원,1,김00,20220036,010-6618-1051,,2025년 4월 7일 ~ 5월 2일 (총 4주, 160시간)
이루니유치원,2,정00,20220046,010-0000-0000,,2025년 4월 7일 ~ 5월 2일 (총 4주, 160시간)
```

## 🐍 Python 코드에서 사용

```python
from hwpx_parser import HwpxParser

# 파서 생성
parser = HwpxParser('assets/yuasifsubnane.hwpx')

# 데이터 파싱
schools = parser.parse_student_list()

# JSON 변환
json_str = parser.to_json('output.json')

# CSV 변환
parser.to_csv('output.csv')

# Excel 변환 (pandas 필요)
parser.to_excel('output.xlsx')

# 요약 출력
parser.print_summary()
```

## 🔧 고급 사용법

### 원본 텍스트만 추출
```python
from hwpx_parser import HwpxParser

parser = HwpxParser('file.hwpx')
text = parser.read_text()
print(text)
```

### 커스텀 파싱
```python
from hwpx_parser import HwpxParser
import json

parser = HwpxParser('file.hwpx')
schools = parser.parse_student_list()

# 특정 유치원만 필터링
filtered = [s for s in schools if '이루니' in s.get('name', '')]

# 학생 수 집계
total = sum(len(s.get('students', [])) for s in schools)

print(f"총 {total}명의 실습생")
```

## 📦 의존성

### 필수
- Python 3.6+
- zipfile (내장)
- re (내장)
- json (내장)
- csv (내장)

### 선택사항
- pandas: Excel 변환 지원
- openpyxl: Excel 파일 쓰기

```bash
pip install pandas openpyxl
```

## 🗂️ hwpx 파일 구조

hwpx는 ZIP 압축된 XML 기반 문서 형식입니다:

```
yuasifsubnane.hwpx
├── mimetype
├── version.xml
├── Contents/
│   ├── header.xml          # 문서 헤더
│   ├── section0.xml        # 본문 내용 (XML)
│   └── content.hpf         # 바이너리 콘텐츠
├── Preview/
│   ├── PrvText.txt         # ⭐ 텍스트 미리보기 (가장 쉽게 파싱 가능)
│   └── PrvImage.png        # 이미지 미리보기
└── META-INF/
    ├── container.xml
    └── manifest.xml
```

이 파서는 `Preview/PrvText.txt`를 사용하여 빠르고 정확하게 데이터를 추출합니다.

## 🎯 활용 사례

### 1. 데이터베이스 마이그레이션
```bash
# hwpx → JSON
python3 hwpx_parser.py data.hwpx -j data.json

# JSON을 데이터베이스에 삽입 (예: MongoDB)
mongoimport --db school --collection students --file data.json
```

### 2. 여러 파일 일괄 처리
```bash
#!/bin/bash
for file in assets/*.hwpx; do
    basename="${file%.hwpx}"
    python3 hwpx_parser.py "$file" -j "${basename}.json" -c "${basename}.csv"
done
```

### 3. 웹 API 서버
```python
from flask import Flask, request, jsonify
from hwpx_parser import HwpxParser

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_hwpx():
    file = request.files['hwpx']
    file.save('temp.hwpx')

    parser = HwpxParser('temp.hwpx')
    schools = parser.parse_student_list()

    return jsonify({'schools': schools})

if __name__ == '__main__':
    app.run(debug=True)
```

## ⚠️ 알려진 제약사항

1. **텍스트 기반 파싱**: Preview/PrvText.txt를 사용하므로 복잡한 서식 정보는 손실됩니다
2. **표 구조 한정**: 현재는 교육실습생 명단 양식만 지원합니다
3. **빈 데이터**: 빈 칸이 많은 양식도 파싱되지만 유효 데이터만 추출됩니다

## 🔍 문제 해결

### 파일을 찾을 수 없습니다
```bash
# 절대 경로 사용
python3 hwpx_parser.py /full/path/to/file.hwpx
```

### Excel 변환 실패
```bash
# pandas와 openpyxl 설치
pip install pandas openpyxl
```

### 한글 깨짐 (CSV)
- UTF-8 BOM으로 저장되므로 Excel에서도 정상 표시됩니다
- 메모장이나 VS Code로 열 때는 UTF-8 인코딩 선택

## 📝 라이선스

MIT License

## 👤 개발자

Claude Code (AI Assistant)

## 📞 지원

문제가 발생하면 이슈를 등록해주세요.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-10
