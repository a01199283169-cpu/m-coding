#!/usr/bin/env python3
"""
hwpx 양식 파일 파서
교육실습생 명단 등 hwpx 파일을 읽고 JSON/CSV로 변환
"""

import zipfile
import json
import re
import csv
from pathlib import Path
from typing import List, Dict, Optional


class HwpxParser:
    """hwpx 파일 파서 클래스"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    def read_text(self) -> Optional[str]:
        """hwpx 파일에서 텍스트 추출"""
        try:
            with zipfile.ZipFile(self.file_path) as z:
                if 'Preview/PrvText.txt' in z.namelist():
                    with z.open('Preview/PrvText.txt') as f:
                        return f.read().decode('utf-8', errors='ignore')
        except zipfile.BadZipFile:
            print(f"오류: {self.file_path}는 유효한 hwpx 파일이 아닙니다")
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
        return None

    def parse_student_list(self) -> List[Dict]:
        """교육실습생 명단 파싱"""
        text = self.read_text()
        if not text:
            return []

        schools = []

        # 유치원별로 분리
        sections = re.split(r'가\. 교육실습기간:', text)
        sections = [s for s in sections if s.strip()]  # 빈 섹션 제거

        for section in sections:
            school_data = {}

            # 기간 추출
            period_match = re.search(
                r'(\d{4})학년도\s+(\d+)월\s+(\d+)일.*?~\s+(\d+)월\s+(\d+)일.*?총\s+(\d+)주.*?(\d+)시간',
                section
            )
            if period_match:
                year, sm, sd, em, ed, weeks, hours = period_match.groups()
                school_data['period'] = {
                    'year': year,
                    'start_date': f"{year}-{sm.zfill(2)}-{sd.zfill(2)}",
                    'end_date': f"{year}-{em.zfill(2)}-{ed.zfill(2)}",
                    'weeks': int(weeks),
                    'hours': int(hours),
                    'display': f"{year}년 {sm}월 {sd}일 ~ {em}월 {ed}일 (총 {weeks}주, {hours}시간)"
                }

            # 유치원명 추출
            name_match = re.search(r'나\. 교육실습생 명단\((.+?)\)', section)
            if name_match:
                school_data['name'] = name_match.group(1).strip()

            # 학생 데이터 추출
            students = []
            student_pattern = r'<(\d+)><([^>]+)><([^>]+)><([^>]+)><([^>]*)>'

            for match in re.finditer(student_pattern, section):
                name = match.group(2).strip()
                if name and name != '성 명':  # 헤더 제외, 빈 이름 제외
                    students.append({
                        '순번': int(match.group(1)) if match.group(1).isdigit() else match.group(1),
                        '성명': name,
                        '학번': match.group(3).strip(),
                        '연락처': match.group(4).strip(),
                        '비고': match.group(5).strip()
                    })

            if students:
                school_data['students'] = students

            if school_data.get('name') or students:
                schools.append(school_data)

        return schools

    def to_json(self, output_file: Optional[str] = None, indent: int = 2) -> str:
        """JSON 형식으로 변환"""
        data = {
            'source_file': str(self.file_path),
            'schools': self.parse_student_list()
        }

        json_str = json.dumps(data, ensure_ascii=False, indent=indent)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"✅ JSON 파일 생성: {output_file}")

        return json_str

    def to_csv(self, output_file: str = 'students.csv') -> None:
        """CSV 형식으로 변환"""
        schools = self.parse_student_list()

        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['유치원명', '순번', '성명', '학번', '연락처', '비고', '실습기간'])

            for school in schools:
                period_str = school.get('period', {}).get('display', '')

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

        print(f"✅ CSV 파일 생성: {output_file}")

    def to_excel(self, output_file: str = 'students.xlsx') -> None:
        """Excel 형식으로 변환 (pandas 필요)"""
        try:
            import pandas as pd
        except ImportError:
            print("❌ Excel 변환을 위해 pandas를 설치해주세요: pip install pandas openpyxl")
            return

        schools = self.parse_student_list()
        rows = []

        for school in schools:
            period_str = school.get('period', {}).get('display', '')

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
        print(f"✅ Excel 파일 생성: {output_file}")

    def print_summary(self) -> None:
        """요약 정보 출력"""
        schools = self.parse_student_list()

        print(f"\n{'='*60}")
        print(f"📄 파일: {self.file_path.name}")
        print(f"{'='*60}\n")

        total_students = 0

        for i, school in enumerate(schools, 1):
            print(f"[{i}] {school.get('name', '이름 없음')}")

            if 'period' in school:
                print(f"    📅 {school['period']['display']}")

            students = school.get('students', [])
            print(f"    👥 실습생: {len(students)}명\n")

            for student in students:
                print(f"       {student['순번']:2}. {student['성명']:6} | "
                      f"학번: {student['학번']:10} | "
                      f"연락처: {student['연락처']:15} | "
                      f"비고: {student['비고']}")

            total_students += len(students)
            print()

        print(f"{'='*60}")
        print(f"총 {len(schools)}개 기관, {total_students}명의 실습생")
        print(f"{'='*60}\n")


def main():
    """메인 함수 - CLI 인터페이스"""
    import argparse

    parser = argparse.ArgumentParser(
        description='hwpx 양식 파일 파서 - 교육실습생 명단 추출'
    )
    parser.add_argument('hwpx_file', help='hwpx 파일 경로')
    parser.add_argument('-j', '--json', metavar='FILE', help='JSON 파일로 저장')
    parser.add_argument('-c', '--csv', metavar='FILE', help='CSV 파일로 저장')
    parser.add_argument('-x', '--excel', metavar='FILE', help='Excel 파일로 저장')
    parser.add_argument('-s', '--summary', action='store_true', help='요약 정보만 출력')
    parser.add_argument('--raw', action='store_true', help='원본 텍스트 출력')

    args = parser.parse_args()

    try:
        parser_obj = HwpxParser(args.hwpx_file)

        if args.raw:
            # 원본 텍스트 출력
            text = parser_obj.read_text()
            if text:
                print(text)
        elif args.summary:
            # 요약만 출력
            parser_obj.print_summary()
        else:
            # 기본: 요약 출력 + 파일 변환
            parser_obj.print_summary()

            if args.json:
                parser_obj.to_json(args.json)

            if args.csv:
                parser_obj.to_csv(args.csv)

            if args.excel:
                parser_obj.to_excel(args.excel)

            # 옵션 없으면 JSON만 출력
            if not (args.json or args.csv or args.excel):
                print(parser_obj.to_json())

    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
