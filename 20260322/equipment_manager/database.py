"""
데이터베이스 초기화 및 테이블 생성
"""
import sqlite3
import bcrypt
from pathlib import Path
from datetime import datetime


def get_db_path():
    """데이터베이스 파일 경로 반환"""
    db_dir = Path(__file__).parent / "data"
    db_dir.mkdir(exist_ok=True)
    return db_dir / "equipment.db"


def get_connection():
    """DB 연결 반환 (멀티스레드 대응)"""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """비밀번호 bcrypt 해싱"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def init_database():
    """데이터베이스 초기화 - 테이블 생성 및 초기 데이터 삽입"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. departments 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_code    TEXT PRIMARY KEY,
            dept_name    TEXT NOT NULL,
            college      TEXT NOT NULL,
            college_code TEXT NOT NULL
        )
    """)

    # 1-1. categories 테이블 (카테고리 관리)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT UNIQUE NOT NULL,
            sort_order  INTEGER DEFAULT 0,
            is_active   INTEGER DEFAULT 1,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 1-2. asset_types 테이블 (자산구분 관리)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_types (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT UNIQUE NOT NULL,
            sort_order  INTEGER DEFAULT 0,
            is_active   INTEGER DEFAULT 1,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 1-3. equipment_items 테이블 (품목 마스터)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment_items (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name    TEXT NOT NULL,
            category     TEXT,
            dept_code    TEXT,
            college_code TEXT,
            is_active    INTEGER DEFAULT 1,
            created_by   TEXT,
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(item_name, dept_code)
        )
    """)

    # 2. users 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password      TEXT NOT NULL,
            college_code  TEXT NOT NULL,
            college_name  TEXT NOT NULL,
            role          TEXT DEFAULT 'college',
            is_active     INTEGER DEFAULT 1,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. equipment 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code       TEXT UNIQUE NOT NULL,
            item_name       TEXT NOT NULL,
            category        TEXT,
            spec            TEXT,
            dept_code       TEXT NOT NULL REFERENCES departments(dept_code),
            college_code    TEXT NOT NULL,
            quantity        INTEGER NOT NULL,
            unit_price      INTEGER NOT NULL,
            total_price     INTEGER NOT NULL,
            purchase_date   DATE NOT NULL,
            arrival_date    DATE NOT NULL,
            vendor          TEXT,
            asset_type      TEXT NOT NULL DEFAULT '교육용기자재',
            location        TEXT,
            useful_life     INTEGER,
            disposal_date   DATE,
            doc_path        TEXT,
            note            TEXT,
            registrant_name TEXT NOT NULL,
            registrant_id   TEXT NOT NULL,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at      DATETIME,
            is_deleted      INTEGER DEFAULT 0
        )
    """)

    # 4. equipment_photos 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment_photos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id  INTEGER NOT NULL REFERENCES equipment(id),
            file_name     TEXT NOT NULL,
            file_path     TEXT NOT NULL,
            original_name TEXT,
            file_size     INTEGER,
            sort_order    INTEGER DEFAULT 1,
            uploaded_by   TEXT NOT NULL,
            uploaded_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 5. equipment_repairs 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment_repairs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id    INTEGER NOT NULL REFERENCES equipment(id),
            repair_type     TEXT NOT NULL CHECK(repair_type IN ('수리','정기점검','부품교체','보증수리','자체수리')),
            repair_date     DATE NOT NULL,
            description     TEXT NOT NULL,
            vendor          TEXT,
            cost            INTEGER DEFAULT 0,
            status          TEXT DEFAULT '완료' CHECK(status IN ('완료','진행중','대기')),
            next_check_date DATE,
            memo            TEXT,
            created_by_name TEXT NOT NULL,
            created_by_id   TEXT NOT NULL,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 초기 데이터 삽입 - equipment_items (교육용 기자재 품목)
    cursor.execute("SELECT COUNT(*) FROM equipment_items")
    if cursor.fetchone()[0] == 0:
        items_data = [
            # 공통 품목 (dept_code = NULL)
            # 컴퓨터 및 주변기기
            ('노트북 컴퓨터', 'IT기기', None, None),
            ('데스크탑 컴퓨터', 'IT기기', None, None),
            ('태블릿 PC', 'IT기기', None, None),
            ('모니터', 'IT기기', None, None),
            # 영상/음향 기기
            ('프로젝터', '영상음향', None, None),
            ('스크린', '영상음향', None, None),
            ('스피커', '영상음향', None, None),
            # 출력 기기
            ('프린터', '출력기기', None, None),
            ('복합기', '출력기기', None, None),
            # 가구
            ('책상', '가구', None, None),
            ('의자', '가구', None, None),
            ('화이트보드', '교육기자재', None, None),
            # 기타
            ('기타(직접입력)', '기타', None, None)
        ]
        cursor.executemany(
            "INSERT INTO equipment_items (item_name, category, dept_code, college_code) VALUES (?, ?, ?, ?)",
            items_data
        )
        print(f"✓ {len(items_data)}개 품목 데이터 삽입 완료")

    # 초기 데이터 삽입 - departments (37개 학과)
    cursor.execute("SELECT COUNT(*) FROM departments")
    if cursor.fetchone()[0] == 0:
        departments_data = [
            # 공과대학 (7개)
            ('EV','미래자동차공학과','공과대학','ENG'),
            ('ME','기계공학과','공과대학','ENG'),
            ('SW','소프트웨어융합학과','공과대학','ENG'),
            ('EE','전자공학과','공과대학','ENG'),
            ('EN','에너지공학과','공과대학','ENG'),
            ('MS','첨단소재공학과','공과대학','ENG'),
            ('CD','사이버드론봇군사학과','공과대학','ENG'),
            # 보건대학 (7개)
            ('FN','식품영양학과','보건대학','HLT'),
            ('BF','바이오식품외식산업학과','보건대학','HLT'),
            ('DH','치위생학과','보건대학','HLT'),
            ('DT','치기공학과','보건대학','HLT'),
            ('OT','안경광학과','보건대학','HLT'),
            ('CP','임상병리학과','보건대학','HLT'),
            ('RS','방사선학과','보건대학','HLT'),
            # 디자인예술대학 (7개)
            ('PA','공연예술학과','디자인예술대학','ART'),
            ('KP','K-POP학과','디자인예술대학','ART'),
            ('MC','모델콘텐츠학과','디자인예술대학','ART'),
            ('KB','K-뷰티학과','디자인예술대학','ART'),
            ('ID','산업디자인학과','디자인예술대학','ART'),
            ('FD','패션디자인학과','디자인예술대학','ART'),
            ('ND','실내디자인학과','디자인예술대학','ART'),
            # 경영대학 (6개)
            ('BD','빅데이터경영학과','경영대학','BIZ'),
            ('GT','글로벌무역학과','경영대학','BIZ'),
            ('MV','미디어영상학과','경영대학','BIZ'),
            ('IC','국제개발협력학과','경영대학','BIZ'),
            ('TM','글로벌관광경영학과','경영대학','BIZ'),
            ('BZ','경영대학 자율전공','경영대학','BIZ'),
            # 사회과학대학 (7개)
            ('LA','토지행정학과','사회과학대학','SOC'),
            ('PB','행정학과','사회과학대학','SOC'),
            ('PC','경찰행정학과','사회과학대학','SOC'),
            ('CS','상담심리학과','사회과학대학','SOC'),
            ('WF','사회복지학과','사회과학대학','SOC'),
            ('EC','유아교육과','사회과학대학','SOC'),
            ('SF','사회과학대학 자율전공','사회과학대학','SOC'),
            # 태권도ㆍ체육대학 (3개)
            ('TK','태권도학부','태권도ㆍ체육대학','SPT'),
            ('FS','미래스포츠융합학과','태권도ㆍ체육대학','SPT'),
            ('SM','스포츠의학과','태권도ㆍ체육대학','SPT')
        ]
        cursor.executemany(
            "INSERT INTO departments VALUES (?, ?, ?, ?)",
            departments_data
        )
        print("✓ 37개 학과 데이터 삽입 완료")

    # 초기 데이터 삽입 - users (초기 계정)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users_data = [
            ('admin', hash_password('admin1234'), 'ALL', '전체', 'admin', 1),
            ('eng_1', hash_password('eng1234'), 'ENG', '공과대학', 'college', 1),
            ('hlt_1', hash_password('hlt1234'), 'HLT', '보건대학', 'college', 1),
            ('art_1', hash_password('art1234'), 'ART', '디자인예술대학', 'college', 1),
            ('biz_1', hash_password('biz1234'), 'BIZ', '경영대학', 'college', 1),
            ('soc_1', hash_password('soc1234'), 'SOC', '사회과학대학', 'college', 1),
            ('spt_1', hash_password('spt1234'), 'SPT', '태권도ㆍ체육대학', 'college', 1)
        ]
        cursor.executemany(
            "INSERT INTO users (username, password, college_code, college_name, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            users_data
        )
        print("✓ 초기 계정 7개 생성 완료")

    # 자산구분 초기 데이터
    cursor.execute("SELECT COUNT(*) FROM asset_types")
    if cursor.fetchone()[0] == 0:
        asset_types_data = [
            ('교육용기자재', 1)
        ]
        cursor.executemany(
            "INSERT INTO asset_types (name, sort_order) VALUES (?, ?)",
            asset_types_data
        )
        print("✓ 초기 자산구분 1개 생성 완료")

    # 카테고리 초기 데이터
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories_data = [
            ('실험기구', 1),
            ('전자기기', 2),
            ('의료기기', 3),
            ('공구/장비', 4),
            ('소모품', 5),
            ('도서/교재', 6),
            ('기타', 99)
        ]
        cursor.executemany(
            "INSERT INTO categories (name, sort_order) VALUES (?, ?)",
            categories_data
        )
        print("✓ 초기 카테고리 7개 생성 완료")

    conn.commit()
    conn.close()
    print("✓ 데이터베이스 초기화 완료")


if __name__ == "__main__":
    init_database()
