"""
수리·점검 이력 관리 화면
"""
import streamlit as st
from database import get_connection
from datetime import datetime, date, timedelta


def get_equipment_list(college_code: str, role: str) -> list:
    """기자재 목록 조회 (수리이력 등록용)"""
    conn = get_connection()
    cursor = conn.cursor()

    if role == 'admin':
        cursor.execute("""
            SELECT e.id, e.item_code, e.item_name, d.dept_name, d.college
            FROM equipment e
            LEFT JOIN departments d ON e.dept_code = d.dept_code
            WHERE e.is_deleted = 0
            ORDER BY e.item_code DESC
        """)
    else:
        cursor.execute("""
            SELECT e.id, e.item_code, e.item_name, d.dept_name, d.college
            FROM equipment e
            LEFT JOIN departments d ON e.dept_code = d.dept_code
            WHERE e.is_deleted = 0 AND e.college_code = ?
            ORDER BY e.item_code DESC
        """, (college_code,))

    items = cursor.fetchall()
    conn.close()
    return [dict(item) for item in items]


def get_repair_history(equipment_id: int = None, college_code: str = None, role: str = 'college') -> list:
    """수리·점검 이력 조회"""
    conn = get_connection()
    cursor = conn.cursor()

    if equipment_id:
        # 특정 기자재의 이력
        cursor.execute("""
            SELECT r.*, e.item_code, e.item_name, d.dept_name
            FROM equipment_repairs r
            JOIN equipment e ON r.equipment_id = e.id
            LEFT JOIN departments d ON e.dept_code = d.dept_code
            WHERE r.equipment_id = ?
            ORDER BY r.repair_date DESC
        """, (equipment_id,))
    else:
        # 전체 이력
        if role == 'admin':
            cursor.execute("""
                SELECT r.*, e.item_code, e.item_name, d.dept_name, d.college
                FROM equipment_repairs r
                JOIN equipment e ON r.equipment_id = e.id
                LEFT JOIN departments d ON e.dept_code = d.dept_code
                ORDER BY r.repair_date DESC
            """)
        else:
            cursor.execute("""
                SELECT r.*, e.item_code, e.item_name, d.dept_name, d.college
                FROM equipment_repairs r
                JOIN equipment e ON r.equipment_id = e.id
                LEFT JOIN departments d ON e.dept_code = d.dept_code
                WHERE e.college_code = ?
                ORDER BY r.repair_date DESC
            """, (college_code,))

    repairs = cursor.fetchall()
    conn.close()
    return [dict(r) for r in repairs]


def add_repair_record(data: dict, user: dict) -> tuple:
    """수리·점검 이력 등록"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO equipment_repairs (
                equipment_id, repair_type, repair_date, description,
                vendor, cost, status, next_check_date, memo,
                created_by_name, created_by_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['equipment_id'],
            data['repair_type'],
            data['repair_date'],
            data['description'],
            data.get('vendor'),
            data.get('cost', 0),
            data.get('status', '완료'),
            data.get('next_check_date'),
            data.get('memo'),
            user['username'],
            user['username']
        ))

        conn.commit()
        conn.close()
        return True, "수리·점검 이력이 등록되었습니다."
    except Exception as e:
        return False, f"등록 실패: {str(e)}"


def delete_repair_record(repair_id: int) -> tuple:
    """수리·점검 이력 삭제"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM equipment_repairs WHERE id = ?", (repair_id,))

        conn.commit()
        conn.close()
        return True, "삭제되었습니다."
    except Exception as e:
        return False, f"삭제 실패: {str(e)}"


def show_repairs(user: dict):
    """수리·점검 이력 관리 메인 화면"""
    st.title("🔧 수리·점검 이력")

    st.info("""
    💡 **안내**
    - 기자재의 수리, 점검, 부품교체 등의 이력을 관리합니다.
    - 정기점검 시 다음 점검일을 설정할 수 있습니다.
    """)

    st.markdown("---")

    # 탭 구성
    tab1, tab2 = st.tabs(["📋 이력 조회", "➕ 이력 등록"])

    with tab1:
        show_repair_list(user)

    with tab2:
        show_add_repair_form(user)


def show_repair_list(user: dict):
    """수리·점검 이력 목록"""
    st.subheader("📋 수리·점검 이력 목록")

    # 필터
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        equipment_list = get_equipment_list(user['college_code'], user['role'])
        equipment_options = ["전체"] + [f"[{e['item_code']}] {e['item_name']}" for e in equipment_list]
        selected_equipment = st.selectbox(
            "기자재 선택",
            equipment_options,
            key="repair_filter_equipment"
        )

    with col2:
        repair_types = ["전체", "수리", "정기점검", "부품교체", "보증수리", "자체수리"]
        selected_type = st.selectbox(
            "수리 유형",
            repair_types,
            key="repair_filter_type"
        )

    with col3:
        st.write("")  # 여백
        st.write("")  # 여백
        if st.button("🔍 조회", use_container_width=True, key="repair_list_search"):
            st.session_state.repair_list_searched = True

    # 검색 버튼을 눌렀을 때만 조회
    if not st.session_state.get('repair_list_searched', False):
        st.info("💡 조회 조건을 선택하고 **🔍 조회** 버튼을 눌러주세요.")
        return

    # 조회
    if selected_equipment != "전체":
        equipment_id = equipment_list[equipment_options.index(selected_equipment) - 1]['id']
        repairs = get_repair_history(equipment_id=equipment_id)
    else:
        repairs = get_repair_history(college_code=user['college_code'], role=user['role'])

    # 유형 필터 적용
    if selected_type != "전체":
        repairs = [r for r in repairs if r['repair_type'] == selected_type]

    if not repairs:
        st.warning("조회된 이력이 없습니다. 다른 조건으로 검색하세요.")
        return

    # 통계
    total_count = len(repairs)
    total_cost = sum(r['cost'] or 0 for r in repairs)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 이력 건수", f"{total_count:,} 건")
    with col2:
        st.metric("총 수리 비용", f"{total_cost:,} 원")

    st.markdown("---")

    # 이력 목록
    for idx, repair in enumerate(repairs):
        with st.expander(
            f"[{repair['repair_date']}] {repair['item_code']} - {repair['item_name']} ({repair['repair_type']})",
            expanded=False
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**품목코드:** {repair['item_code']}")
                st.write(f"**품목명:** {repair['item_name']}")
                st.write(f"**학과:** {repair['dept_name']}")
                st.write(f"**수리 유형:** {repair['repair_type']}")
                st.write(f"**수리일자:** {repair['repair_date']}")

            with col2:
                st.write(f"**업체:** {repair['vendor'] or '-'}")
                st.write(f"**비용:** {repair['cost']:,} 원" if repair['cost'] else "**비용:** -")
                st.write(f"**상태:** {repair['status']}")
                if repair['next_check_date']:
                    st.write(f"**다음 점검일:** {repair['next_check_date']}")
                st.write(f"**작성자:** {repair['created_by_name']}")

            st.write(f"**내용:** {repair['description']}")

            if repair['memo']:
                st.write(f"**메모:** {repair['memo']}")

            # 삭제 버튼
            if user['role'] == 'admin' or user['username'] == repair['created_by_id']:
                if st.button("🗑️ 삭제", key=f"delete_repair_{repair['id']}"):
                    success, message = delete_repair_record(repair['id'])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)


def get_colleges(role: str, user_college_code: str) -> list:
    """단과대학 목록"""
    if role == 'admin':
        return ['전체', '공과대학', '보건대학', '디자인예술대학', '경영대학', '사회과학대학', '태권도ㆍ체육대학']
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT college FROM departments WHERE college_code = ?", (user_college_code,))
        result = cursor.fetchone()
        conn.close()
        return [result['college']] if result else []


def get_depts_by_college(college_name: str) -> list:
    """단과대학별 학과 목록"""
    if not college_name or college_name == '전체':
        return ['전체']

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

    return ['전체'] + [f"{d['dept_code']} - {d['dept_name']}" for d in depts]


def get_equipment_by_filters(college: str = None, dept_code: str = None, category: str = None, item_name: str = None, user_role: str = 'college', user_college_code: str = None) -> list:
    """필터링된 기자재 목록"""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT e.id, e.item_code, e.item_name, e.category, d.dept_name, d.college
        FROM equipment e
        LEFT JOIN departments d ON e.dept_code = d.dept_code
        WHERE e.is_deleted = 0
    """
    params = []

    if user_role != 'admin':
        query += " AND e.college_code = ?"
        params.append(user_college_code)

    if college and college != '전체':
        query += " AND d.college = ?"
        params.append(college)

    if dept_code and dept_code != '전체':
        query += " AND e.dept_code = ?"
        params.append(dept_code)

    if category and category != '전체':
        query += " AND e.category = ?"
        params.append(category)

    if item_name and item_name.strip():
        query += " AND e.item_name LIKE ?"
        params.append(f"%{item_name}%")

    query += " ORDER BY e.item_code DESC"

    cursor.execute(query, params)
    items = cursor.fetchall()
    conn.close()

    return [dict(item) for item in items]


def show_add_repair_form(user: dict):
    """수리·점검 이력 등록 폼"""
    st.subheader("➕ 수리·점검 이력 등록")

    st.markdown("#### 🔍 기자재 선택")

    # 필터링 섹션
    col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1, 1.5, 0.8])

    with col1:
        colleges = get_colleges(user['role'], user['college_code'])
        selected_college = st.selectbox("단과대학", colleges, key="repair_add_college")

    with col2:
        depts = get_depts_by_college(selected_college)
        selected_dept = st.selectbox("학과", depts, key="repair_add_dept")
        dept_code = selected_dept.split(' - ')[0] if selected_dept != '전체' else None

    with col3:
        # 카테고리 목록
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name FROM categories WHERE is_active = 1 ORDER BY sort_order")
        categories = ['전체'] + [c['name'] for c in cursor.fetchall()]
        conn.close()
        selected_category = st.selectbox("카테고리", categories, key="repair_add_category")

    with col4:
        # 품명 검색
        item_name_search = st.text_input(
            "품명 검색",
            placeholder="품명 입력",
            key="repair_add_item_name",
            help="품명의 일부만 입력해도 검색됩니다"
        )

    with col5:
        st.write("")  # 여백
        st.write("")  # 여백
        if st.button("🔍 검색", use_container_width=True):
            st.session_state.repair_search_clicked = True

    # 검색 결과
    if st.session_state.get('repair_search_clicked', False):
        equipment_list = get_equipment_by_filters(
            college=selected_college if selected_college != '전체' else None,
            dept_code=dept_code,
            category=selected_category if selected_category != '전체' else None,
            item_name=item_name_search,
            user_role=user['role'],
            user_college_code=user['college_code']
        )

        if not equipment_list:
            st.warning("조회된 기자재가 없습니다. 다른 조건으로 검색하세요.")
            return

        st.success(f"✅ {len(equipment_list)}개 기자재 검색됨")

        equipment_options = [f"[{e['item_code']}] {e['item_name']} ({e['dept_name']})" for e in equipment_list]

        selected_equipment = st.selectbox(
            "기자재 선택 *",
            equipment_options,
            key="add_repair_equipment"
        )

        equipment_id = equipment_list[equipment_options.index(selected_equipment)]['id']
    else:
        st.info("💡 위에서 조건을 선택하고 🔍 검색 버튼을 눌러 기자재를 찾으세요.")
        return

    st.markdown("---")
    st.markdown("#### 📝 수리·점검 정보 입력")

    col1, col2 = st.columns(2)

    with col1:
        repair_types = ["수리", "정기점검", "부품교체", "보증수리", "자체수리"]
        repair_type = st.selectbox(
            "수리 유형 *",
            repair_types,
            key="add_repair_type"
        )

    with col2:
        repair_date = st.date_input(
            "수리일자 *",
            value=date.today(),
            key="add_repair_date"
        )

    description = st.text_area(
        "수리 내용 *",
        placeholder="수리/점검 내용을 상세히 입력하세요",
        key="add_repair_description"
    )

    col1, col2 = st.columns(2)

    with col1:
        vendor = st.text_input(
            "수리 업체",
            placeholder="업체명",
            key="add_repair_vendor"
        )

    with col2:
        cost = st.number_input(
            "수리 비용 (원)",
            min_value=0,
            step=10000,
            key="add_repair_cost"
        )

    col1, col2 = st.columns(2)

    with col1:
        status_options = ["완료", "진행중", "대기"]
        status = st.selectbox(
            "상태 *",
            status_options,
            key="add_repair_status"
        )

    with col2:
        # 정기점검인 경우 다음 점검일 입력
        if repair_type == "정기점검":
            next_check_date = st.date_input(
                "다음 점검일",
                value=date.today() + timedelta(days=180),  # 기본 6개월 후
                key="add_repair_next_check"
            )
        else:
            next_check_date = None

    memo = st.text_area(
        "메모",
        placeholder="추가 메모 사항",
        key="add_repair_memo"
    )

    st.markdown("---")

    # 저장 버튼
    if st.button("💾 저장", type="primary", use_container_width=True):
        if not description.strip():
            st.error("수리 내용을 입력하세요.")
        else:
            data = {
                'equipment_id': equipment_id,
                'repair_type': repair_type,
                'repair_date': repair_date.strftime('%Y-%m-%d'),
                'description': description.strip(),
                'vendor': vendor.strip() if vendor else None,
                'cost': cost,
                'status': status,
                'next_check_date': next_check_date.strftime('%Y-%m-%d') if next_check_date else None,
                'memo': memo.strip() if memo else None
            }

            success, message = add_repair_record(data, user)

            if success:
                st.success(message)
                st.balloons()
                # 폼 초기화를 위해 rerun
                st.rerun()
            else:
                st.error(message)


if __name__ == "__main__":
    # 테스트용
    st.set_page_config(page_title="수리·점검 이력", layout="wide")

    test_user = {
        'username': 'hlt_1',
        'role': 'college',
        'college_code': 'HLT',
        'college_name': '보건대학'
    }

    show_repairs(test_user)
