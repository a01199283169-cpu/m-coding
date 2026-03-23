"""
기자재 조회 화면 - 계층형 필터 + 목록 테이블
"""
import streamlit as st
from database import get_connection
from datetime import datetime, date
from utils.excel_export import export_to_excel, get_excel_filename


def get_college_list(role: str, user_college_code: str) -> list:
    """단과대학 목록 반환"""
    if role == 'admin':
        return [
            '전체',
            '공과대학',
            '보건대학',
            '디자인예술대학',
            '경영대학',
            '사회과학대학',
            '태권도ㆍ체육대학'
        ]
    else:
        # college 권한: 본인 소속 단과대학만
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT college
            FROM departments
            WHERE college_code = ?
        """, (user_college_code,))
        result = cursor.fetchone()
        conn.close()
        return [result['college']] if result else []


def get_dept_list(college_name: str) -> list:
    """선택된 단과대학의 학과 목록 반환"""
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

    dept_list = ['전체'] + [f"{d['dept_code']} - {d['dept_name']}" for d in depts]
    return dept_list


def get_asset_type_list() -> list:
    """DB에서 자산구분 목록 반환"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT asset_type
        FROM equipment
        WHERE is_deleted = 0
        ORDER BY asset_type
    """)
    types = cursor.fetchall()
    conn.close()

    type_list = ['전체'] + [t['asset_type'] for t in types]

    # 교육용기자재가 없으면 추가 (향후 사용을 위해)
    if '교육용기자재' not in type_list:
        type_list.insert(1, '교육용기자재')

    return type_list


def get_category_list() -> list:
    """카테고리 테이블에서 카테고리 목록 반환"""
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

    category_list = ['전체'] + [c['name'] for c in categories]
    return category_list


def get_item_name_list(category: str = None) -> list:
    """실제 등록된 기자재의 품목명 목록 반환 (카테고리 필터링)"""
    conn = get_connection()
    cursor = conn.cursor()

    if category and category != '전체':
        cursor.execute("""
            SELECT DISTINCT item_name
            FROM equipment
            WHERE is_deleted = 0 AND category = ?
            ORDER BY item_name
        """, (category,))
    else:
        cursor.execute("""
            SELECT DISTINCT item_name
            FROM equipment
            WHERE is_deleted = 0
            ORDER BY item_name
        """)

    items = cursor.fetchall()
    conn.close()

    item_list = ['전체'] + [i['item_name'] for i in items]
    return item_list


def build_query(filters: dict, user_role: str, user_college_code: str) -> tuple:
    """조회 쿼리 생성"""
    base_query = """
        SELECT
            e.id,
            e.item_code,
            e.item_name,
            e.category,
            e.spec,
            e.dept_code,
            d.dept_name,
            d.college,
            e.asset_type,
            e.quantity,
            e.unit_price,
            e.total_price,
            e.arrival_date,
            e.vendor,
            e.location,
            e.useful_life,
            e.disposal_date,
            e.registrant_name,
            e.created_at,
            e.note,
            (SELECT file_path FROM equipment_photos
             WHERE equipment_id = e.id AND sort_order = 1
             LIMIT 1) as thumbnail,
            (SELECT COUNT(*) FROM equipment_repairs
             WHERE equipment_id = e.id) as repair_count
        FROM equipment e
        LEFT JOIN departments d ON e.dept_code = d.dept_code
        WHERE e.is_deleted = 0
    """

    params = []

    # 권한별 필터
    if user_role == 'college':
        base_query += " AND e.college_code = ?"
        params.append(user_college_code)

    # 단과대학 필터
    if filters.get('college') and filters['college'] != '전체':
        base_query += " AND d.college = ?"
        params.append(filters['college'])

    # 학과 필터
    if filters.get('dept') and filters['dept'] != '전체':
        dept_code = filters['dept'].split(' - ')[0]
        base_query += " AND e.dept_code = ?"
        params.append(dept_code)

    # 자산구분 필터
    if filters.get('asset_type') and filters['asset_type'] != '전체':
        base_query += " AND e.asset_type = ?"
        params.append(filters['asset_type'])

    # 카테고리 필터
    if filters.get('category') and filters['category'] != '전체':
        base_query += " AND e.category = ?"
        params.append(filters['category'])

    # 품목명 필터 (부분 일치 검색)
    if filters.get('item_name'):
        base_query += " AND e.item_name LIKE ?"
        params.append(f"%{filters['item_name']}%")

    # 입고일 범위 필터 (시작일~종료일)
    if filters.get('date_from'):
        base_query += " AND e.arrival_date >= ?"
        params.append(filters['date_from'])

    if filters.get('date_to'):
        base_query += " AND e.arrival_date <= ?"
        params.append(filters['date_to'])

    # 내용연수 필터
    if filters.get('useful_life') and filters['useful_life'] != '전체':
        if filters['useful_life'] == '없음':
            base_query += " AND (e.useful_life IS NULL OR e.useful_life = 0)"
        else:
            base_query += " AND e.useful_life = ?"
            params.append(int(filters['useful_life']))

    base_query += " ORDER BY e.arrival_date DESC, e.item_code DESC"

    return base_query, params


def show_list_view(user: dict):
    """기자재 조회 화면 메인"""
    st.title("📋 기자재 조회")

    # 필터 영역
    st.subheader("🔍 조회 조건")

    # 첫 번째 줄: 단과대학, 학과, 카테고리, 자산구분
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        college_list = get_college_list(user['role'], user['college_code'])
        selected_college = st.selectbox(
            "단과대학",
            college_list,
            index=0,
            key="filter_college"
        )

    with col2:
        dept_list = get_dept_list(selected_college)
        selected_dept = st.selectbox(
            "학과",
            dept_list,
            index=0,
            key="filter_dept"
        )

    with col3:
        # 카테고리 목록
        category_list = get_category_list()
        selected_category = st.selectbox(
            "카테고리",
            category_list,
            index=0,
            key="filter_category"
        )

    with col4:
        # DB에서 자산구분 목록 불러오기
        asset_type_list = get_asset_type_list()
        selected_asset_type = st.selectbox(
            "자산구분",
            asset_type_list,
            index=0,
            key="filter_asset"
        )

    # 두 번째 줄: 품목명, 입고일(시작), 입고일(종료), 내용연수
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        # 품목명 검색 (부분 일치)
        search_item_name = st.text_input(
            "품목명 검색",
            placeholder="품목명 입력 (부분 검색 가능)",
            key="filter_item_name"
        )

    with col6:
        date_from = st.date_input(
            "입고일 (시작)",
            value=None,
            key="filter_date_from"
        )

    with col7:
        date_to = st.date_input(
            "입고일 (종료)",
            value=None,
            key="filter_date_to"
        )

    with col8:
        # 내용연수 필터
        useful_life_options = ['전체', '없음', '1', '3', '5', '7', '10', '15', '20']
        selected_useful_life = st.selectbox(
            "내용연수 (년)",
            useful_life_options,
            index=0,
            key="filter_useful_life"
        )

    # 조회 버튼
    st.markdown("")  # 약간의 여백
    search_button = st.button("🔍 조회", use_container_width=False, type="primary")

    # 조회 버튼을 눌렀을 때만 조회 실행
    if search_button:
        st.session_state.search_clicked = True
        st.session_state.search_filters = {
            'college': selected_college if selected_college != '전체' else None,
            'dept': selected_dept if selected_dept != '전체' else None,
            'asset_type': selected_asset_type if selected_asset_type != '전체' else None,
            'category': selected_category if selected_category != '전체' else None,
            'item_name': search_item_name.strip() if search_item_name and search_item_name.strip() else None,
            'date_from': date_from.strftime('%Y-%m-%d') if date_from else None,
            'date_to': date_to.strftime('%Y-%m-%d') if date_to else None,
            'useful_life': selected_useful_life if selected_useful_life != '전체' else None
        }

    st.markdown("---")

    # 조회 버튼을 눌렀을 때만 결과 표시
    if st.session_state.get('search_clicked', False):
        filters = st.session_state.search_filters

        # 브레드크럼 표시
        breadcrumb = "전체"
        if filters.get('college'):
            breadcrumb = f"전체 › {filters['college']}"
            if filters.get('dept'):
                breadcrumb += f" › {filters['dept'].split(' - ')[1] if ' - ' in filters['dept'] else filters['dept']}"

        st.caption(f"📍 {breadcrumb}")

        query, params = build_query(filters, user['role'], user['college_code'])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # 요약 카드
        if results:
            total_count = len(results)
            total_quantity = sum(r['quantity'] for r in results)
            total_price = sum(r['total_price'] for r in results)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("조회 건수", f"{total_count:,} 건")
            with col2:
                st.metric("총 수량", f"{total_quantity:,} 개")
            with col3:
                st.metric("총 금액", f"{total_price:,} 원")

        st.markdown("---")

        # 툴바 버튼
        col1, col2, col3, col4 = st.columns([1, 1, 1, 5])

        with col1:
            if st.button("➕ 신규 입력", use_container_width=True):
                st.session_state.page = 'register'
                st.session_state.edit_mode = False
                st.session_state.edit_item_id = None
                st.rerun()
    
        with col2:
            # 수정 버튼 (선택된 행이 있을 때만 활성화)
            selected_item = st.session_state.get('selected_item_id', None)
            if st.button("✏️ 수정", disabled=(selected_item is None), use_container_width=True):
                st.session_state.page = 'register'
                st.session_state.edit_mode = True
                st.session_state.edit_item_id = selected_item
                st.rerun()
    
        with col3:
            # 삭제 버튼
            if st.button("🗑️ 삭제", disabled=(selected_item is None), use_container_width=True):
                st.session_state.show_delete_confirm = True
    
        with col4:
            if st.button("📥 엑셀 저장", use_container_width=True):
                if results:
                    # 엑셀 파일 생성
                    college_name = selected_college if selected_college != '전체' else '전체'
                    excel_data = export_to_excel([dict(r) for r in results], college_name)
                    filename = get_excel_filename(college_name)
    
                    st.download_button(
                        label="⬇️ 다운로드",
                        data=excel_data,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.warning("다운로드할 데이터가 없습니다.")
    
        # 삭제 확인 팝업
        if st.session_state.get('show_delete_confirm', False):
            st.warning("⚠️ 선택한 품목을 삭제하시겠습니까?")
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ 삭제 확인", type="primary"):
                    # 소프트 삭제 실행
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE equipment
                        SET is_deleted = 1, updated_at = ?
                        WHERE id = ?
                    """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), selected_item))
                    conn.commit()
                    conn.close()
    
                    st.success("삭제되었습니다.")
                    st.session_state.show_delete_confirm = False
                    st.session_state.selected_item_id = None
                    st.rerun()
    
            with col2:
                if st.button("❌ 취소"):
                    st.session_state.show_delete_confirm = False
                    st.rerun()
    
        # 목록 테이블
        if not results:
            st.info("조회된 데이터가 없습니다.")
        else:
            st.subheader(f"📊 목록 ({len(results)}건)")
    
            # 테이블 헤더
            header_cols = st.columns([0.5, 0.8, 1.2, 1.5, 2, 1, 0.8, 1, 1, 1, 0.8, 0.7])
            headers = ["선택", "사진", "단과대학", "학과", "품목코드", "품목명", "자산구분", "수량", "단가", "입고일", "입력자", "수리이력"]

            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            st.markdown("---")

            # 데이터 행
            for idx, row in enumerate(results):
                cols = st.columns([0.5, 0.8, 1.2, 1.5, 2, 1, 0.8, 1, 1, 1, 0.8, 0.7])
    
                # 선택 체크박스
                with cols[0]:
                    if st.checkbox("선택", key=f"select_{row['id']}", label_visibility="collapsed"):
                        st.session_state.selected_item_id = row['id']
    
                # 사진 썸네일
                with cols[1]:
                    if row['thumbnail']:
                        try:
                            st.image(row['thumbnail'], width=40)
                        except:
                            st.write("📷")
                    else:
                        st.write("📷")
    
                with cols[2]:
                    st.write(row['college'])
    
                with cols[3]:
                    st.write(row['dept_name'])
    
                with cols[4]:
                    st.write(row['item_code'])
    
                with cols[5]:
                    st.write(row['item_name'])
    
                with cols[6]:
                    badge_color = {
                        '교육용기자재': '🟪',
                        '비품': '🟦',
                        '소모품': '🟩',
                        '대여품': '🟨'
                    }
                    st.write(f"{badge_color.get(row['asset_type'], '⚪')} {row['asset_type']}")
    
                with cols[7]:
                    st.write(f"{row['quantity']:,}")
    
                with cols[8]:
                    st.write(f"{row['unit_price']:,}원")
    
                with cols[9]:
                    st.write(row['arrival_date'])
    
                with cols[10]:
                    st.write(row['registrant_name'])

                with cols[11]:
                    repair_count = row['repair_count'] or 0
                    if repair_count > 0:
                        st.write(f"🔧 {repair_count}건")
                    else:
                        st.write("-")

                if idx < len(results) - 1:
                    st.markdown("<hr style='margin: 5px 0; opacity: 0.3;'>", unsafe_allow_html=True)
    else:
        # 조회 버튼을 누르지 않았을 때
        st.info("💡 조회 조건을 선택하고 **🔍 조회** 버튼을 눌러주세요.")


if __name__ == "__main__":
    # 테스트용
    st.set_page_config(page_title="기자재 조회", layout="wide")

    # 테스트 사용자
    test_user = {
        'username': 'admin',
        'role': 'admin',
        'college_code': 'ALL',
        'college_name': '전체'
    }

    show_list_view(test_user)
