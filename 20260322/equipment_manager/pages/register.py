"""
기자재 등록·수정 폼
"""
import streamlit as st
from database import get_connection
from utils.code_gen import generate_item_code, check_code_exists
from datetime import datetime, date, timedelta
from pathlib import Path
import shutil


def get_categories() -> list:
    """카테고리 목록 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM categories
        WHERE is_active = 1
        ORDER BY sort_order, name
    """)
    categories = cursor.fetchall()
    conn.close()
    return [cat['name'] for cat in categories]


def get_asset_types() -> list:
    """자산구분 목록 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM asset_types
        WHERE is_active = 1
        ORDER BY sort_order, name
    """)
    asset_types = cursor.fetchall()
    conn.close()
    return [at['name'] for at in asset_types]


def get_all_colleges() -> list:
    """모든 단과대학 목록 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT college
        FROM departments
        ORDER BY college
    """)
    colleges = cursor.fetchall()
    conn.close()
    return [c['college'] for c in colleges]


def get_depts_by_college(college_name: str) -> list:
    """특정 단과대학의 학과 목록 반환"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dept_code, dept_name
        FROM departments
        WHERE college = ?
        ORDER BY dept_code
    """, (college_name,))
    depts = cursor.fetchall()
    conn.close()
    return [(d['dept_code'], d['dept_name']) for d in depts]


def get_user_depts(college_code: str) -> list:
    """사용자 소속 단과대학의 학과 목록 반환"""
    conn = get_connection()
    cursor = conn.cursor()

    # admin(college_code='ALL')은 전체 학과 조회
    if college_code == 'ALL':
        cursor.execute("""
            SELECT dept_code, dept_name, college
            FROM departments
            ORDER BY college, dept_code
        """)
        depts = cursor.fetchall()
        conn.close()
        # "학과명 (단과대학)" 형식으로 반환
        return [(d['dept_code'], f"{d['dept_name']} ({d['college']})") for d in depts]
    else:
        cursor.execute("""
            SELECT dept_code, dept_name
            FROM departments
            WHERE college_code = ?
            ORDER BY dept_code
        """, (college_code,))
        depts = cursor.fetchall()
        conn.close()
        return [(d['dept_code'], d['dept_name']) for d in depts]


def load_equipment_data(item_id: int) -> dict | None:
    """기존 기자재 데이터 로드 (수정 모드)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM equipment
        WHERE id = ? AND is_deleted = 0
    """, (item_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return dict(result)
    return None


def get_equipment_photos(item_id: int) -> list:
    """기자재 사진 목록 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM equipment_photos
        WHERE equipment_id = ?
        ORDER BY sort_order
    """, (item_id,))

    photos = cursor.fetchall()
    conn.close()

    return [dict(p) for p in photos]


def save_equipment(data: dict, user: dict, is_edit: bool = False, item_id: int = None) -> tuple:
    """
    기자재 저장 (등록 또는 수정)

    Returns:
        (success: bool, message: str, item_id: int)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if is_edit and item_id:
            # 수정 모드
            cursor.execute("""
                UPDATE equipment
                SET asset_code = ?,
                    budget_dept = ?,
                    item_name = ?,
                    category = ?,
                    spec = ?,
                    dept_code = ?,
                    quantity = ?,
                    unit_price = ?,
                    total_price = ?,
                    purchase_date = ?,
                    arrival_date = ?,
                    vendor = ?,
                    asset_type = ?,
                    location = ?,
                    useful_life = ?,
                    disposal_date = ?,
                    note = ?,
                    registrant_name = ?,
                    updated_at = ?
                WHERE id = ?
            """, (
                data.get('asset_code'),
                data.get('budget_dept'),
                data['item_name'],
                data.get('category'),
                data.get('spec'),
                data['dept_code'],
                data['quantity'],
                data['unit_price'],
                data['total_price'],
                data['purchase_date'],
                data['arrival_date'],
                data['vendor'],
                data['asset_type'],
                data['location'],
                data['useful_life'],
                data['disposal_date'],
                data['note'],
                data['registrant_name'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                item_id
            ))
            conn.commit()
            conn.close()
            return True, "수정되었습니다.", item_id

        else:
            # 신규 등록 모드
            # 품목코드 검증
            item_code = data.get('item_code', '').strip()

            if not item_code:
                return False, "품목코드를 입력해주세요. (시설팀 부여 코드)", None

            # 중복 체크
            if check_code_exists(item_code):
                return False, f"품목코드 {item_code}가 이미 존재합니다.", None

            # dept_code로부터 실제 college_code 조회 (admin 대응)
            cursor.execute("""
                SELECT college_code
                FROM departments
                WHERE dept_code = ?
            """, (data['dept_code'],))
            dept_info = cursor.fetchone()
            actual_college_code = dept_info['college_code'] if dept_info else user['college_code']

            cursor.execute("""
                INSERT INTO equipment (
                    item_code, asset_code, budget_dept, item_name, category, spec, dept_code, college_code,
                    quantity, unit_price, total_price,
                    purchase_date, arrival_date, vendor,
                    asset_type, location, useful_life, disposal_date,
                    note, registrant_name, registrant_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_code,
                data.get('asset_code'),
                data.get('budget_dept'),
                data['item_name'],
                data.get('category'),
                data.get('spec'),
                data['dept_code'],
                actual_college_code,
                data['quantity'],
                data['unit_price'],
                data['total_price'],
                data['purchase_date'],
                data['arrival_date'],
                data['vendor'],
                data['asset_type'],
                data['location'],
                data['useful_life'],
                data['disposal_date'],
                data['note'],
                data['registrant_name'],
                user['username']
            ))

            new_item_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return True, f"등록되었습니다. (품목코드: {item_code})", new_item_id

    except Exception as e:
        return False, f"저장 실패: {str(e)}", None


def save_uploaded_photos(files, item_id: int, item_code: str, college_code: str, username: str) -> int:
    """
    업로드된 사진 파일 저장

    Returns:
        저장된 파일 개수
    """
    if not files:
        return 0

    # 저장 디렉토리 생성
    upload_dir = Path(__file__).parent.parent / "uploads" / college_code / item_code
    upload_dir.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # 기존 사진 개수 확인 (sort_order 결정용)
    cursor.execute("""
        SELECT COALESCE(MAX(sort_order), 0) as max_order
        FROM equipment_photos
        WHERE equipment_id = ?
    """, (item_id,))

    max_order = cursor.fetchone()['max_order']

    saved_count = 0

    for idx, file in enumerate(files, start=1):
        # 파일 확장자 추출
        file_ext = Path(file.name).suffix.lower()

        # 파일명 생성: {item_code}_photo_{순번}.jpg
        new_filename = f"{item_code}_photo_{max_order + idx:03d}{file_ext}"
        file_path = upload_dir / new_filename

        # 파일 저장
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        # DB에 메타데이터 저장
        cursor.execute("""
            INSERT INTO equipment_photos (
                equipment_id, file_name, file_path, original_name,
                file_size, sort_order, uploaded_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id,
            new_filename,
            str(file_path),
            file.name,
            file.size,
            max_order + idx,
            username
        ))

        saved_count += 1

    conn.commit()
    conn.close()

    return saved_count


def delete_photo(photo_id: int) -> bool:
    """사진 삭제"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 파일 경로 조회
        cursor.execute("SELECT file_path FROM equipment_photos WHERE id = ?", (photo_id,))
        result = cursor.fetchone()

        if result:
            file_path = Path(result['file_path'])
            # 파일 삭제
            if file_path.exists():
                file_path.unlink()

            # DB에서 삭제
            cursor.execute("DELETE FROM equipment_photos WHERE id = ?", (photo_id,))
            conn.commit()

        conn.close()
        return True
    except Exception as e:
        st.error(f"사진 삭제 실패: {str(e)}")
        return False


def show_register_form(user: dict):
    """기자재 등록·수정 폼"""
    # 수정 모드 체크
    is_edit = st.session_state.get('edit_mode', False)
    item_id = st.session_state.get('edit_item_id', None)

    # 기존 데이터 로드 (수정 모드)
    existing_data = None
    existing_photos = []
    if is_edit and item_id:
        existing_data = load_equipment_data(item_id)
        if existing_data:
            existing_photos = get_equipment_photos(item_id)
        else:
            st.error("해당 기자재를 찾을 수 없습니다.")
            st.stop()

    # 제목
    title = "✏️ 기자재 수정" if is_edit else "➕ 기자재 신규 등록"
    st.title(title)

    # 섹션1: 기본정보
    st.subheader("📝 기본 정보")

    # 관리자인 경우 단과대학 선택 가능
    is_admin = user['college_code'] == 'ALL'

    if is_admin:
        # 모든 단과대학 목록 조회
        all_colleges = get_all_colleges()
        college_options = ['전체'] + all_colleges

        # 세션 상태 초기화
        if 'selected_college_register' not in st.session_state:
            # 수정 모드이고 기존 데이터가 있으면 해당 단과대학으로 초기화
            if existing_data:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT college FROM departments WHERE dept_code = ?",
                             (existing_data['dept_code'],))
                result = cursor.fetchone()
                conn.close()
                if result:
                    st.session_state.selected_college_register = result['college']
                else:
                    st.session_state.selected_college_register = '전체'
            else:
                st.session_state.selected_college_register = '전체'

        col1, col2 = st.columns(2)

        with col1:
            # 단과대학 선택
            default_college_idx = 0
            if st.session_state.selected_college_register in college_options:
                default_college_idx = college_options.index(st.session_state.selected_college_register)

            selected_college = st.selectbox(
                "단과대학 *",
                college_options,
                index=default_college_idx,
                key="college_select"
            )

            # 단과대학 선택이 바뀌면 세션 상태 업데이트
            if selected_college != st.session_state.selected_college_register:
                st.session_state.selected_college_register = selected_college
                st.rerun()

        with col2:
            # 선택된 단과대학에 따라 학과 목록 필터링
            if selected_college == '전체':
                depts = get_user_depts('ALL')
            else:
                depts = get_depts_by_college(selected_college)

            if not depts:
                st.warning(f"⚠️ {selected_college}에 등록된 학과가 없습니다.")
                dept_options = []
                dept_code = ""
            else:
                dept_options = [f"{code} - {name}" for code, name in depts]

                # 기본값 설정
                default_dept_idx = 0
                if existing_data and existing_data['dept_code']:
                    for idx, (code, name) in enumerate(depts):
                        if code == existing_data['dept_code']:
                            default_dept_idx = idx
                            break

                if dept_options:
                    selected_dept = st.selectbox(
                        "학과 *",
                        dept_options,
                        index=default_dept_idx,
                        key="dept_select"
                    )
                    dept_code = selected_dept.split(' - ')[0] if selected_dept else ""
                else:
                    dept_code = ""
    else:
        # 일반 사용자는 소속 단과대학의 학과만 표시
        depts = get_user_depts(user['college_code'])

        if not depts:
            st.error(f"⚠️ {user['college_name']}에 등록된 학과가 없습니다. 관리자에게 문의하세요.")
            st.stop()

        dept_options = [f"{code} - {name}" for code, name in depts]

        # 기본값 설정
        default_dept_idx = 0
        if existing_data and existing_data['dept_code']:
            for idx, (code, name) in enumerate(depts):
                if code == existing_data['dept_code']:
                    default_dept_idx = idx
                    break

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("단과대학", value=user['college_name'], disabled=True)

        with col2:
            selected_dept = st.selectbox(
                "학과 *",
                dept_options,
                index=default_dept_idx,
                key="dept_select"
            )
            dept_code = selected_dept.split(' - ')[0] if selected_dept else ""

    # 품목코드 입력 (시설팀 부여 코드)
    if is_edit and existing_data:
        item_code_input = st.text_input(
            "품목코드 (수정 불가)",
            value=existing_data['item_code'],
            disabled=True,
            help="품목코드는 수정할 수 없습니다",
            key="item_code_edit"
        )
    else:
        item_code_input = st.text_input(
            "품목코드 ⚠️ 시설팀 부여 코드 입력 (필수)",
            value="",
            placeholder="예: EDU-2024-001 또는 시설팀 부여 코드",
            help="⚠️ 중요: 시설팀에서 부여받은 정확한 품목코드를 입력하세요",
            key="item_code_new"
        )

    # 자산코드 입력
    asset_code = st.text_input(
        "자산코드 (선택)",
        value=existing_data.get('asset_code', '') if existing_data else '',
        placeholder="예: ASSET-2024-001",
        help="학교 자산관리 코드 (있는 경우 입력)",
        key="asset_code_input"
    )

    # 예산부서 입력
    budget_dept = st.text_input(
        "예산부서 (선택)",
        value=existing_data.get('budget_dept', '') if existing_data else '',
        placeholder="예: 교무처, 학생처, 총무처 등",
        help="예산을 집행한 부서명",
        key="budget_dept_input"
    )

    # 자산구분 선택 (DB에서 조회)
    asset_type_options = get_asset_types()
    if not asset_type_options:
        asset_type_options = ['교육용기자재']

    # 기존 데이터가 있으면 해당 자산구분을 기본값으로
    if existing_data and existing_data.get('asset_type') in asset_type_options:
        default_asset_type_idx = asset_type_options.index(existing_data['asset_type'])
    else:
        default_asset_type_idx = 0

    asset_type = st.selectbox(
        "자산구분 *",
        asset_type_options,
        index=default_asset_type_idx,
        key="asset_type_select"
    )

    # 카테고리 선택 (DB에서 조회)
    category_options = get_categories()
    if not category_options:
        category_options = ['기타']

    # 기존 데이터가 있으면 해당 카테고리를 기본값으로
    if existing_data and existing_data.get('category') in category_options:
        default_category_idx = category_options.index(existing_data['category'])
    else:
        default_category_idx = 0

    category = st.selectbox(
        "카테고리 *",
        category_options,
        index=default_category_idx,
        key="category_select_main"
    )

    # 품목명 직접 입력
    item_name = st.text_input(
        "품목명 *",
        value=existing_data['item_name'] if existing_data else "",
        placeholder="품목명을 입력하세요",
        key="item_name_input"
    )

    # 규격 입력
    spec = st.text_input(
        "규격",
        value=existing_data.get('spec', '') if existing_data else "",
        placeholder="예: Intel i7, 16GB RAM",
        key="spec"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        quantity = st.number_input(
            "수량 *",
            min_value=1,
            value=existing_data['quantity'] if existing_data else 1,
            key="quantity"
        )

    with col2:
        unit_price = st.number_input(
            "단가 (원) *",
            min_value=0,
            value=existing_data['unit_price'] if existing_data else 0,
            step=1000,
            format="%d",
            key="unit_price",
            help="천원 단위로 입력하세요"
        )

    with col3:
        # 총액 자동계산 및 표시
        total_price = quantity * unit_price
        st.text_input("총액 (원)", value=f"{total_price:,}", disabled=True)

    col1, col2 = st.columns(2)

    with col1:
        vendor = st.text_input(
            "납품업체",
            value=existing_data['vendor'] if existing_data else "",
            key="vendor"
        )

    with col2:
        location = st.text_input(
            "보관위치",
            value=existing_data['location'] if existing_data else "",
            key="location"
        )

    col1, col2 = st.columns(2)

    with col1:
        purchase_date = st.date_input(
            "구매일자 *",
            value=datetime.strptime(existing_data['purchase_date'], '%Y-%m-%d').date() if existing_data and existing_data['purchase_date'] else date.today(),
            key="purchase_date"
        )

    with col2:
        arrival_date = st.date_input(
            "입고일자 *",
            value=datetime.strptime(existing_data['arrival_date'], '%Y-%m-%d').date() if existing_data and existing_data['arrival_date'] else date.today(),
            key="arrival_date"
        )

    col1, col2 = st.columns(2)

    with col1:
        useful_life = st.number_input(
            "내용연수 (년)",
            min_value=0,
            value=existing_data['useful_life'] if existing_data and existing_data['useful_life'] else 0,
            key="useful_life"
        )

    with col2:
        # 폐기예정일 자동계산
        if useful_life > 0:
            disposal_date = arrival_date + timedelta(days=useful_life * 365)
            st.date_input("폐기예정일 (자동계산)", value=disposal_date, disabled=True)
        else:
            st.text_input("폐기예정일", value="", disabled=True)

    st.markdown("---")

    # 섹션2: 입력자 정보
    st.subheader("👤 입력자 정보")

    col1, col2, col3 = st.columns(3)

    with col1:
        registrant_name = st.text_input(
            "입력자 이름 *",
            value=existing_data['registrant_name'] if existing_data else "",
            key="registrant_name"
        )

    with col2:
        st.text_input("아이디", value=user['username'], disabled=True)

    with col3:
        st.text_input("입력날짜", value=datetime.now().strftime('%Y-%m-%d'), disabled=True)

    st.markdown("---")

    # 섹션3: 사진 첨부
    st.subheader("📷 사진 첨부")

    # 기존 사진 표시 (수정 모드)
    if is_edit and existing_photos:
        st.write("**기존 사진**")

        cols = st.columns(5)
        for idx, photo in enumerate(existing_photos):
            col_idx = idx % 5
            with cols[col_idx]:
                try:
                    st.image(photo['file_path'], caption=f"사진 {photo['sort_order']}", use_container_width=True)
                    if st.button(f"🗑️ 삭제", key=f"delete_photo_{photo['id']}"):
                        if delete_photo(photo['id']):
                            st.success("사진이 삭제되었습니다.")
                            st.rerun()
                except Exception as e:
                    st.error(f"이미지 로드 실패: {str(e)}")

        st.markdown("---")

    # 새 사진 업로드
    uploaded_files = st.file_uploader(
        "사진 추가 (최대 5장, jpg/png/jpeg, 장당 10MB)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        key="photo_upload"
    )

    # 파일 검증
    valid_files = []
    if uploaded_files:
        if len(uploaded_files) > 5:
            st.warning("최대 5장까지 업로드 가능합니다.")
            uploaded_files = uploaded_files[:5]

        for file in uploaded_files:
            if file.size > 10 * 1024 * 1024:  # 10MB
                st.warning(f"{file.name}: 파일 크기가 10MB를 초과합니다.")
            else:
                valid_files.append(file)

    st.markdown("---")

    # 섹션4: 비고
    st.subheader("📄 비고")
    note = st.text_area(
        "비고",
        value=existing_data['note'] if existing_data and existing_data['note'] else "",
        height=100,
        key="note"
    )

    st.markdown("---")

    # 버튼
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("❌ 취소", use_container_width=True):
            st.session_state.page = 'list'
            st.session_state.edit_mode = False
            st.session_state.edit_item_id = None
            st.rerun()

    with col2:
        if st.button("💾 저장", use_container_width=True, type="primary"):
            # 필수항목 검증
            if not item_code_input or not item_code_input.strip():
                st.error("⚠️ 품목코드를 입력하세요. (시설팀 부여 코드 필수)")
            elif not item_name:
                st.error("품목명을 입력하세요.")
            elif not registrant_name:
                st.error("입력자 이름을 입력하세요.")
            elif quantity <= 0:
                st.error("수량은 1 이상이어야 합니다.")
            elif unit_price < 0:
                st.error("단가를 확인하세요.")
            else:
                # 데이터 준비
                data = {
                    'item_code': item_code_input.strip(),
                    'asset_code': asset_code.strip() if asset_code else None,
                    'budget_dept': budget_dept.strip() if budget_dept else None,
                    'item_name': item_name,
                    'category': category if category else None,
                    'spec': spec if spec else None,
                    'dept_code': dept_code,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                    'arrival_date': arrival_date.strftime('%Y-%m-%d'),
                    'vendor': vendor if vendor else None,
                    'asset_type': asset_type,
                    'location': location if location else None,
                    'useful_life': useful_life if useful_life > 0 else None,
                    'disposal_date': disposal_date.strftime('%Y-%m-%d') if useful_life > 0 else None,
                    'note': note if note else None,
                    'registrant_name': registrant_name
                }

                # 저장 실행
                success, message, saved_item_id = save_equipment(data, user, is_edit, item_id)

                if success:
                    st.success(message)

                    # 사진 저장 (신규 또는 수정 모두 가능)
                    if valid_files and saved_item_id:
                        item_code = existing_data['item_code'] if existing_data else item_code_input.strip()
                        photo_count = save_uploaded_photos(
                            valid_files,
                            saved_item_id,
                            item_code,
                            user['college_code'],
                            user['username']
                        )
                        if photo_count > 0:
                            st.success(f"사진 {photo_count}장이 저장되었습니다.")

                    # 목록으로 이동
                    st.session_state.page = 'list'
                    st.session_state.edit_mode = False
                    st.session_state.edit_item_id = None
                    st.rerun()
                else:
                    st.error(message)


if __name__ == "__main__":
    # 테스트용
    st.set_page_config(page_title="기자재 등록", layout="wide")

    # 테스트 사용자
    test_user = {
        'username': 'hlt_1',
        'role': 'college',
        'college_code': 'HLT',
        'college_name': '보건대학'
    }

    show_register_form(test_user)
