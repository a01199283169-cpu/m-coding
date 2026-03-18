#!/usr/bin/env python3
"""
Claude Code 스킬 패키징 도구
프로젝트 디렉토리를 스킬 패키지로 변환합니다.
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


def package_skill(skill_dir: str, output_dir: str = "dist"):
    """
    스킬 디렉토리를 패키징합니다.

    Args:
        skill_dir: 패키징할 스킬 디렉토리
        output_dir: 출력 디렉토리
    """
    skill_path = Path(skill_dir).resolve()

    if not skill_path.exists():
        print(f"❌ 오류: 디렉토리를 찾을 수 없습니다: {skill_dir}")
        return 1

    skill_name = skill_path.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print(f"\n{'='*60}")
    print(f"📦 스킬 패키징: {skill_name}")
    print(f"{'='*60}\n")

    # 1. SKILL.md 확인
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"⚠️  경고: SKILL.md 파일이 없습니다")
        print(f"   자동으로 README.md를 SKILL.md로 사용합니다\n")

        readme = skill_path / "README.md"
        if readme.exists():
            skill_md = readme
        else:
            print(f"❌ 오류: SKILL.md 또는 README.md가 필요합니다")
            return 1

    # 2. .claude/skills/ 디렉토리에 복사
    claude_skills_dir = Path.home() / ".claude" / "skills"
    claude_skills_dir.mkdir(parents=True, exist_ok=True)

    skill_file_name = f"{skill_name}.md"
    target_skill = claude_skills_dir / skill_file_name

    print(f"📝 1. 스킬 파일 설치")
    shutil.copy2(skill_md, target_skill)
    print(f"   ✅ {target_skill}")

    # 3. 필수 파일 수집
    essential_files = [
        "SKILL.md",
        "README.md",
        "QUICKSTART.md",
        "EXAMPLES.md",
        "requirements.txt",
        ".gitignore"
    ]

    python_files = list(skill_path.glob("*.py"))
    shell_files = list(skill_path.glob("*.sh"))

    # 4. ZIP 아카이브 생성
    zip_name = f"{skill_name}_{timestamp}.zip"
    zip_path = output_path / zip_name

    print(f"\n📦 2. 아카이브 생성")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0

        # 문서 파일
        for filename in essential_files:
            file_path = skill_path / filename
            if file_path.exists():
                arcname = f"{skill_name}/{filename}"
                zipf.write(file_path, arcname)
                print(f"   ✅ {filename}")
                file_count += 1

        # Python 파일
        for py_file in python_files:
            arcname = f"{skill_name}/{py_file.name}"
            zipf.write(py_file, arcname)
            print(f"   ✅ {py_file.name}")
            file_count += 1

        # Shell 스크립트
        for sh_file in shell_files:
            arcname = f"{skill_name}/{sh_file.name}"
            zipf.write(sh_file, arcname)
            print(f"   ✅ {sh_file.name}")
            file_count += 1

        # assets 디렉토리 (샘플 파일)
        assets_dir = skill_path / "assets"
        if assets_dir.exists():
            for asset_file in assets_dir.rglob("*"):
                if asset_file.is_file():
                    rel_path = asset_file.relative_to(skill_path)
                    arcname = f"{skill_name}/{rel_path}"
                    zipf.write(asset_file, arcname)
                    file_count += 1

    print(f"\n   총 {file_count}개 파일 포함")

    # 5. 배포 패키지 정보 생성
    info_file = output_path / f"{skill_name}_info.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"스킬 패키지 정보\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"스킬 이름: {skill_name}\n")
        f.write(f"패키징 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"아카이브: {zip_name}\n")
        f.write(f"크기: {zip_path.stat().st_size / 1024:.1f} KB\n")
        f.write(f"파일 수: {file_count}\n\n")

        f.write(f"설치 방법:\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"1. ZIP 파일 압축 해제:\n")
        f.write(f"   unzip {zip_name}\n\n")
        f.write(f"2. 디렉토리 이동:\n")
        f.write(f"   cd {skill_name}\n\n")
        f.write(f"3. 의존성 설치:\n")
        f.write(f"   pip install -r requirements.txt\n\n")
        f.write(f"4. 빠른 시작:\n")
        f.write(f"   cat QUICKSTART.md\n\n")

    # 6. 요약 출력
    print(f"\n{'='*60}")
    print(f"✅ 패키징 완료!")
    print(f"{'='*60}\n")

    print(f"📁 출력 파일:")
    print(f"   • {zip_path.name} ({zip_path.stat().st_size / 1024:.1f} KB)")
    print(f"   • {info_file.name}")
    print(f"\n📍 위치: {output_path.absolute()}\n")

    print(f"🔧 Claude Code 스킬 설치됨:")
    print(f"   • ~/.claude/skills/{skill_file_name}\n")

    print(f"🚀 사용법:")
    print(f"   Claude Code에서 다음 키워드 사용:")
    print(f"   - {skill_name}")
    print(f"   - 관련 키워드 (SKILL.md의 Triggers 참고)\n")

    print(f"📦 배포:")
    print(f"   {zip_name}를 다른 사용자와 공유 가능\n")

    return 0


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python -m scripts.package_skill <skill_directory> [output_directory]")
        print("\n예시:")
        print("  python -m scripts.package_skill yooa-practice-list/")
        print("  python -m scripts.package_skill yooa-practice-list/ dist/")
        return 1

    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "dist"

    return package_skill(skill_dir, output_dir)


if __name__ == "__main__":
    sys.exit(main())
