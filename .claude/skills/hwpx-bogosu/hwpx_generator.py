#!/usr/bin/env python3
"""
hwpx-bogosu: 한글 문서(hwpx) 보고서 자동 생성기

사용법:
    python hwpx_generator.py --template 1 --title "보고서 제목" --department "부서명"
    python hwpx_generator.py --template 2 --title "신사업 보고서" --author "홍길동"
"""

import argparse
import zipfile
import shutil
import os
import re
from datetime import datetime
from pathlib import Path


class HwpxGenerator:
    """hwpx 보고서 생성기"""

    def __init__(self, template_type: int):
        """
        Args:
            template_type: 1 (정식 보고서) 또는 2 (요약 보고서)
        """
        self.template_type = template_type
        self.base_dir = Path(__file__).parent
        self.template_path = self._get_template_path()
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def _get_template_path(self) -> Path:
        """템플릿 파일 경로 반환"""
        if self.template_type == 1:
            filename = "(샘플양식1) 보고서 기본 양식.hwpx"
        elif self.template_type == 2:
            filename = "(샘플양식2) 보고서 기반 양식(요약).hwpx"
        else:
            raise ValueError("템플릿 타입은 1 또는 2여야 합니다.")

        template_path = self.base_dir / "assets" / filename
        if not template_path.exists():
            raise FileNotFoundError(f"템플릿 파일을 찾을 수 없습니다: {template_path}")

        return template_path

    def generate(self, title: str, **options) -> Path:
        """
        hwpx 보고서 생성

        Args:
            title: 문서 제목
            **options: 추가 옵션
                - department: 소속 부서
                - author: 작성자
                - date: 작성일 (기본값: 오늘)
                - overview: 개요/목적 (양식2 전용)
                - approaches: 추진방안 리스트 (양식2 전용)
                - budget: 예산 딕셔너리 (양식2 전용)

        Returns:
            생성된 hwpx 파일 경로
        """
        # 기본값 설정
        department = options.get('department', 'OOOO부서')
        author = options.get('author', '작성자')
        date_str = options.get('date', datetime.now().strftime('%Y.%m.%d'))

        # 출력 파일명 생성
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        output_filename = f"{safe_title}_{date_str.replace('.', '')}.hwpx"
        output_path = self.output_dir / output_filename

        # 임시 디렉토리 생성
        temp_dir = self.base_dir / "temp_hwpx"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        try:
            # 1. 템플릿 압축 해제
            with zipfile.ZipFile(self.template_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # 2. section0.xml 수정
            section_path = temp_dir / "Contents" / "section0.xml"
            with open(section_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 3. 텍스트 치환
            if self.template_type == 1:
                content = self._replace_template1(content, title, department, author, date_str, options)
            elif self.template_type == 2:
                content = self._replace_template2(content, title, department, author, date_str, options)

            # 4. 수정된 내용 저장
            with open(section_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 5. 미리보기 텍스트 업데이트
            preview_path = temp_dir / "Preview" / "PrvText.txt"
            if preview_path.exists():
                with open(preview_path, 'w', encoding='utf-8') as f:
                    f.write(self._generate_preview_text(title, department, date_str))

            # 6. hwpx 파일 재생성 (원본과 동일한 순서와 압축 방식 유지)
            # 먼저 원본 템플릿의 압축 정보를 읽어옴
            compress_map = {}
            file_order = []
            with zipfile.ZipFile(self.template_path, 'r') as template_zip:
                for info in template_zip.infolist():
                    compress_map[info.filename] = info.compress_type
                    file_order.append(info.filename)

            # 원본과 동일한 순서로 파일 추가
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for arcname in file_order:
                    file_path = temp_dir / arcname
                    if file_path.exists():
                        # 원본과 동일한 압축 방식 사용
                        compress_type = compress_map.get(arcname, zipfile.ZIP_DEFLATED)
                        zip_ref.write(file_path, arcname, compress_type=compress_type)

            print(f"✅ hwpx 파일 생성 완료: {output_path}")
            return output_path

        finally:
            # 임시 디렉토리 정리
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def _replace_template1(self, content: str, title: str, department: str,
                          author: str, date_str: str, options: dict) -> str:
        """양식1 (정식 보고서) 텍스트 치환"""
        # 제목 치환
        content = content.replace(
            '2027년 회계연도  회계감사인 선임 제안 요청서',
            title
        )

        # 날짜 치환
        content = content.replace('2026. 2. 14.', date_str)

        # 부서 치환
        content = content.replace('전 략 실 (전 략 부)', department)

        # 담당자 치환
        content = content.replace('홍길동 팀장', author)

        # 수신처 치환
        if 'recipient' in options:
            content = content.replace('신한대학교', options['recipient'])

        return content

    def _replace_template2(self, content: str, title: str, department: str,
                          author: str, date_str: str, options: dict) -> str:
        """양식2 (요약 보고서) 텍스트 치환"""
        # 제목 치환
        content = content.replace('OOO 신사업 보고서', title)

        # 부서 및 날짜 치환
        content = content.replace('OOOO부서', department)
        content = content.replace('2022.12.31', date_str)

        # 개요/목적 치환
        if 'overview' in options:
            old_overview = '최신 기술을 접목한 OOOO 시스템의 사용자 친화적 UI/UX 개선을 위한 용역사업 추진'
            content = content.replace(old_overview, options['overview'])

        # 추진방안 치환
        if 'approaches' in options:
            approaches = options['approaches']
            if isinstance(approaches, list) and len(approaches) >= 3:
                content = content.replace(
                    '추진방안 1 : 사용자 온라인 수요조사 수행',
                    f'추진방안 1 : {approaches[0]}'
                )
                content = content.replace(
                    '추진방안 2 : 용역 공고를 통한 UI/UX 경험을 가진 전문 업체의 선정',
                    f'추진방안 2 : {approaches[1]}'
                )
                content = content.replace(
                    '추진방안 3 : 2024년도까지 시스템 오픈을 위한 일정 준수',
                    f'추진방안 3 : {approaches[2]}'
                )

        # 예산 치환
        if 'budget' in options:
            budget = options['budget']
            if isinstance(budget, dict):
                items = list(budget.items())
                if len(items) >= 1:
                    content = content.replace('수요조사 : 00억원', f'{items[0][0]} : {items[0][1]}')
                if len(items) >= 2:
                    content = content.replace('시스템개발 : 00억원', f'{items[1][0]} : {items[1][1]}')
                if len(items) >= 3:
                    content = content.replace('시스템 안정화 : 00억원', f'{items[2][0]} : {items[2][1]}')

        # 기타사항 치환
        if 'notes' in options:
            notes = options['notes']
            if isinstance(notes, list) and len(notes) >= 3:
                content = content.replace('OO부서의 협력 필요', notes[0])
                content = content.replace('환율 문제로 인한 리스크 대응 필요', notes[1])
                content = content.replace('서비스 오픈을 위한 일정 준수 필요', notes[2])

        return content

    def _generate_preview_text(self, title: str, department: str, date_str: str) -> str:
        """미리보기 텍스트 생성"""
        return f"{title}\n\n{department}, {date_str}\n"


def main():
    """CLI 메인 함수"""
    parser = argparse.ArgumentParser(
        description='hwpx-bogosu: 한글 문서(hwpx) 보고서 자동 생성기',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 양식1: 정식 보고서
  python hwpx_generator.py -t 1 --title "2027년 클라우드 전환 사업 제안서" \\
      --department "디지털혁신부" --author "이영희 팀장"

  # 양식2: 요약 보고서
  python hwpx_generator.py -t 2 --title "AI 챗봇 시스템 도입 보고서" \\
      --department "IT혁신부서" --author "김철수 부장" \\
      --overview "최신 AI 기술을 활용한 고객 서비스 개선" \\
      --approaches "AI 모델 선정" "시스템 구축" "테스트 및 배포"
        """
    )

    parser.add_argument('-t', '--template', type=int, choices=[1, 2], required=True,
                        help='템플릿 타입: 1=정식 보고서, 2=요약 보고서')
    parser.add_argument('--title', type=str, required=True,
                        help='문서 제목')
    parser.add_argument('--department', type=str, default='OOOO부서',
                        help='소속 부서 (기본값: OOOO부서)')
    parser.add_argument('--author', type=str, default='작성자',
                        help='작성자 (기본값: 작성자)')
    parser.add_argument('--date', type=str,
                        help='작성일 (기본값: 오늘, 형식: YYYY.MM.DD)')
    parser.add_argument('--recipient', type=str,
                        help='수신처 (양식1 전용)')

    # 양식2 전용 옵션
    parser.add_argument('--overview', type=str,
                        help='개요/목적 (양식2 전용)')
    parser.add_argument('--approaches', nargs='+',
                        help='추진방안 목록 (양식2 전용, 최소 3개)')
    parser.add_argument('--budget', nargs='+',
                        help='예산 항목:금액 쌍 (양식2 전용, 형식: "항목:금액")')
    parser.add_argument('--notes', nargs='+',
                        help='기타사항 목록 (양식2 전용, 최소 3개)')

    args = parser.parse_args()

    # 옵션 딕셔너리 구성
    options = {
        'department': args.department,
        'author': args.author,
    }

    if args.date:
        options['date'] = args.date

    if args.recipient:
        options['recipient'] = args.recipient

    if args.overview:
        options['overview'] = args.overview

    if args.approaches:
        options['approaches'] = args.approaches

    if args.budget:
        # "항목:금액" 형식을 딕셔너리로 변환
        budget_dict = {}
        for item in args.budget:
            if ':' in item:
                key, value = item.split(':', 1)
                budget_dict[key] = value
        options['budget'] = budget_dict

    if args.notes:
        options['notes'] = args.notes

    # 생성기 실행
    try:
        generator = HwpxGenerator(template_type=args.template)
        output_path = generator.generate(title=args.title, **options)
        print(f"\n📄 생성된 파일: {output_path.absolute()}")
        print(f"💡 한컴오피스로 열어서 확인하세요!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()
