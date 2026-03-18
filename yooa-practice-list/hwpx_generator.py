#!/usr/bin/env python3
"""
hwpx 양식 파일 생성기
교육실습생 명단 hwpx 파일을 생성합니다.
"""

import zipfile
import json
import sys
from pathlib import Path
from datetime import datetime


class HwpxGenerator:
    """hwpx 파일 생성 클래스"""

    TEMPLATE = """
  가. 교육실습기간: {year}학년도 {start_month}월 {start_day}일({start_weekday}) ~ {end_month}월 {end_day}일({end_weekday}) / 총 {weeks}주({hours}시간 이상)
  나. 교육실습생 명단({school_name})
<순 번><성 명><학 번><연락처><비 고>
{student_rows}
"""

    def __init__(self, template_file=None):
        """생성기 초기화"""
        if template_file:
            self.template_file = Path(template_file)
        else:
            # 기본 템플릿 사용
            self.template_file = Path(__file__).parent / "assets" / "yuasifsubnane.hwpx"

    def generate_text(self, data):
        """데이터로부터 텍스트 내용 생성"""
        sections = []

        for school in data.get('schools', []):
            # 학생 행 생성
            student_rows = []
            for student in school.get('students', []):
                row = f"<{student.get('no', '')}><{student.get('name', '')}><{student.get('id', '')}><{student.get('phone', '')}><{student.get('note', '')}>"
                student_rows.append(row)

            student_text = '\n'.join(student_rows)

            # 섹션 생성
            section = self.TEMPLATE.format(
                year=data.get('year', '2025'),
                start_month=data.get('start_month', '4'),
                start_day=data.get('start_day', '7'),
                start_weekday=data.get('start_weekday', '월'),
                end_month=data.get('end_month', '5'),
                end_day=data.get('end_day', '2'),
                end_weekday=data.get('end_weekday', '금'),
                weeks=data.get('weeks', 4),
                hours=data.get('hours', 160),
                school_name=school.get('name', ''),
                student_rows=student_text
            )
            sections.append(section)

        return '\n'.join(sections)

    def create_hwpx(self, data, output_file):
        """hwpx 파일 생성"""
        # 템플릿 파일 복사
        if not self.template_file.exists():
            print(f"❌ 템플릿 파일 없음: {self.template_file}")
            return False

        # 텍스트 내용 생성
        text_content = self.generate_text(data)

        # 템플릿 복사 및 수정
        with zipfile.ZipFile(self.template_file, 'r') as template_zip:
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                # 기존 파일 복사 (PrvText.txt 제외)
                for item in template_zip.filelist:
                    if item.filename != 'Preview/PrvText.txt':
                        data_bytes = template_zip.read(item.filename)
                        new_zip.writestr(item, data_bytes)

                # 새 텍스트 내용 추가
                new_zip.writestr('Preview/PrvText.txt', text_content.encode('utf-8'))

        return True


def load_json(json_file):
    """JSON 파일 로드"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def interactive_mode():
    """대화형 모드"""
    print("\n교육실습생 명단 hwpx 생성기")
    print("="*50)

    data = {
        'year': input("학년도 (예: 2025): ").strip() or "2025",
        'start_month': input("시작 월 (예: 4): ").strip() or "4",
        'start_day': input("시작 일 (예: 7): ").strip() or "7",
        'start_weekday': input("시작 요일 (예: 월): ").strip() or "월",
        'end_month': input("종료 월 (예: 5): ").strip() or "5",
        'end_day': input("종료 일 (예: 2): ").strip() or "2",
        'end_weekday': input("종료 요일 (예: 금): ").strip() or "금",
        'weeks': int(input("총 주 수 (예: 4): ").strip() or "4"),
        'hours': int(input("총 시간 (예: 160): ").strip() or "160"),
        'schools': []
    }

    num_schools = int(input("\n유치원 개수: ").strip() or "1")

    for i in range(num_schools):
        print(f"\n[{i+1}번째 유치원]")
        school_name = input("  유치원 이름: ").strip()

        num_students = int(input("  실습생 수: ").strip() or "0")

        students = []
        for j in range(num_students):
            print(f"  [{j+1}번째 실습생]")
            student = {
                'no': j + 1,
                'name': input("    이름: ").strip(),
                'id': input("    학번 (8자리): ").strip(),
                'phone': input("    연락처 (010-####-####): ").strip(),
                'note': input("    비고 (없으면 Enter): ").strip()
            }
            students.append(student)

        data['schools'].append({
            'name': school_name,
            'students': students
        })

    return data


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='hwpx 양식 파일 생성기')
    parser.add_argument('-j', '--json', help='입력 JSON 파일')
    parser.add_argument('-o', '--output', default='명단.hwpx', help='출력 hwpx 파일명')
    parser.add_argument('-i', '--interactive', action='store_true', help='대화형 모드')
    parser.add_argument('-t', '--template', help='템플릿 hwpx 파일')

    args = parser.parse_args()

    # 데이터 준비
    if args.interactive:
        data = interactive_mode()
    elif args.json:
        data = load_json(args.json)
    else:
        print("❌ 오류: --json 또는 --interactive 옵션이 필요합니다")
        parser.print_help()
        return 1

    # 생성기 초기화
    generator = HwpxGenerator(template_file=args.template)

    # hwpx 생성
    print(f"\n{'='*50}")
    print(f"📝 hwpx 파일 생성 중...")
    print(f"{'='*50}\n")

    if generator.create_hwpx(data, args.output):
        print(f"✅ 생성 완료: {args.output}\n")

        # 요약 정보
        total_schools = len(data.get('schools', []))
        total_students = sum(len(s.get('students', [])) for s in data.get('schools', []))

        print(f"📊 요약:")
        print(f"   - 유치원: {total_schools}개")
        print(f"   - 실습생: {total_students}명")
        print(f"   - 기간: {data.get('year')}학년도 {data.get('start_month')}월 {data.get('start_day')}일 ~ {data.get('end_month')}월 {data.get('end_day')}일")
        print()

        return 0
    else:
        print(f"❌ 생성 실패\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
