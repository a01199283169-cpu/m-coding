"""
품목코드 자동생성
형식: [학과코드(2자리)]-[연도(4자리)]-[일련번호(4자리)]
예시: DH-2026-0001
"""
from database import get_connection
from datetime import datetime


def generate_item_code(dept_code: str, year: int = None) -> str:
    """
    품목코드 자동생성

    Args:
        dept_code: 학과 코드 (예: DH, EV)
        year: 연도 (None이면 현재 연도)

    Returns:
        생성된 품목코드 (예: DH-2026-0001)
    """
    if year is None:
        year = datetime.now().year

    conn = get_connection()
    cursor = conn.cursor()

    # 해당 학과+연도의 최대 일련번호 조회
    cursor.execute("""
        SELECT item_code
        FROM equipment
        WHERE dept_code = ? AND item_code LIKE ?
        ORDER BY item_code DESC
        LIMIT 1
    """, (dept_code, f"{dept_code}-{year}-%"))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        # 첫 번째 품목
        serial = 1
    else:
        # 기존 코드에서 일련번호 추출 후 +1
        last_code = result['item_code']
        try:
            serial = int(last_code.split('-')[-1]) + 1
        except (ValueError, IndexError):
            serial = 1

    # 품목코드 생성: DH-2026-0001 형식
    item_code = f"{dept_code}-{year}-{serial:04d}"
    return item_code


def validate_item_code(item_code: str) -> bool:
    """
    품목코드 형식 검증

    Args:
        item_code: 검증할 품목코드

    Returns:
        True if 올바른 형식, False otherwise
    """
    try:
        parts = item_code.split('-')
        if len(parts) != 3:
            return False

        dept_code, year, serial = parts

        # 학과코드: 2자리 영문
        if len(dept_code) != 2 or not dept_code.isalpha():
            return False

        # 연도: 4자리 숫자
        if len(year) != 4 or not year.isdigit():
            return False

        # 일련번호: 4자리 숫자
        if len(serial) != 4 or not serial.isdigit():
            return False

        return True
    except Exception:
        return False


def check_code_exists(item_code: str) -> bool:
    """
    품목코드 중복 체크

    Args:
        item_code: 확인할 품목코드

    Returns:
        True if 이미 존재, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as cnt
        FROM equipment
        WHERE item_code = ?
    """, (item_code,))

    result = cursor.fetchone()
    conn.close()

    return result['cnt'] > 0


if __name__ == "__main__":
    # 테스트
    print("품목코드 생성 테스트:")
    print(f"DH 학과: {generate_item_code('DH')}")
    print(f"EV 학과: {generate_item_code('EV')}")
    print(f"SW 학과 2025년: {generate_item_code('SW', 2025)}")

    print("\n품목코드 검증 테스트:")
    print(f"DH-2026-0001: {validate_item_code('DH-2026-0001')}")
    print(f"DH-2026-001: {validate_item_code('DH-2026-001')}")  # False
    print(f"DH-26-0001: {validate_item_code('DH-26-0001')}")    # False
