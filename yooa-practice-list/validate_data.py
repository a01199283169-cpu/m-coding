#!/usr/bin/env python3
"""
교육실습생 데이터 검증 도구
학번, 연락처 형식 등을 자동으로 검증합니다.
"""

import re
import sys
from pathlib import Path
from hwpx_parser import HwpxParser


class DataValidator:
    """데이터 검증 클래스"""

    @staticmethod
    def validate_student_number(student_number: str) -> bool:
        """학번 형식 검증: 8자리 숫자"""
        return bool(re.match(r'^\d{8}$', student_number))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """전화번호 형식 검증: 010-####-#### 또는 010########"""
        if not phone:
            return True  # 빈 값은 허용
        return bool(re.match(r'^010-?\d{4}-?\d{4}$', phone))

    @staticmethod
    def validate_name(name: str) -> bool:
        """이름 검증: 한글 2-4자"""
        if not name:
            return False
        return bool(re.match(r'^[가-힣]{2,4}$', name))

    @staticmethod
    def validate_year(year: str) -> bool:
        """연도 검증: 2020-2030"""
        try:
            y = int(year)
            return 2020 <= y <= 2030
        except ValueError:
            return False


def validate_file(file_path: str, strict: bool = False):
    """hwpx 파일의 데이터 검증"""
    print(f"\n{'='*60}")
    print(f"📋 데이터 검증: {Path(file_path).name}")
    print(f"{'='*60}\n")

    try:
        parser = HwpxParser(file_path)
        schools = parser.parse_student_list()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
        return False

    validator = DataValidator()
    errors = []
    warnings = []
    total_students = 0

    for school_idx, school in enumerate(schools, 1):
        school_name = school.get('name', f'학교{school_idx}')

        # 기간 검증
        period = school.get('period', {})
        if period:
            year = period.get('year', '')
            if not validator.validate_year(year):
                errors.append(f"⚠️ [{school_name}] 잘못된 연도: {year}")

        # 학생 데이터 검증
        students = school.get('students', [])
        total_students += len(students)

        for student in students:
            name = student.get('성명', '')
            student_num = student.get('학번', '')
            phone = student.get('연락처', '')

            # 이름 검증
            if not validator.validate_name(name):
                errors.append(
                    f"❌ [{school_name}] 잘못된 이름 형식: '{name}'"
                )

            # 학번 검증
            if not validator.validate_student_number(student_num):
                errors.append(
                    f"❌ [{school_name}] {name} - 잘못된 학번: {student_num} "
                    f"(8자리 숫자 필요)"
                )

            # 연락처 검증
            if not validator.validate_phone(phone):
                errors.append(
                    f"❌ [{school_name}] {name} - 잘못된 연락처: {phone} "
                    f"(010-####-#### 형식 필요)"
                )

            # 경고: 빈 연락처
            if not phone and strict:
                warnings.append(
                    f"⚠️ [{school_name}] {name} - 연락처 누락"
                )

            # 경고: 비고 확인
            note = student.get('비고', '')
            if note:
                warnings.append(
                    f"ℹ️ [{school_name}] {name} - 비고: {note}"
                )

    # 결과 출력
    print(f"📊 검증 통계:")
    print(f"   총 기관: {len(schools)}개")
    print(f"   총 실습생: {total_students}명\n")

    if errors:
        print(f"❌ 오류 {len(errors)}건:")
        for error in errors:
            print(f"   {error}")
        print()

    if warnings:
        print(f"⚠️ 경고 {len(warnings)}건:")
        for warning in warnings:
            print(f"   {warning}")
        print()

    if not errors and not warnings:
        print("✅ 모든 데이터가 올바릅니다!")
        return True
    elif not errors:
        print("✅ 오류는 없습니다 (경고만 있음)")
        return True
    else:
        print(f"❌ {len(errors)}개의 오류를 수정해야 합니다")
        return False


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='교육실습생 데이터 검증 도구'
    )
    parser.add_argument('hwpx_file', help='검증할 hwpx 파일')
    parser.add_argument(
        '--strict',
        action='store_true',
        help='엄격 모드 (경고도 표시)'
    )

    args = parser.parse_args()

    # 파일 존재 확인
    if not Path(args.hwpx_file).exists():
        print(f"❌ 파일을 찾을 수 없습니다: {args.hwpx_file}")
        return 1

    # 검증 실행
    success = validate_file(args.hwpx_file, strict=args.strict)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
