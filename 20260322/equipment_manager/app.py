"""
신한대학교 교육용 기자재 관리 시스템
메인 실행 파일
"""
import streamlit as st
from database import init_database
from auth import login, logout, is_logged_in, get_current_user, require_login
from pages.list_view import show_list_view
from pages.register import show_register_form
from pages.item_management import show_item_management
from pages.bulk_upload import show_bulk_upload
from pages.repairs import show_repairs


# 페이지 설정
st.set_page_config(
    page_title="신한대학교 기자재 관리",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터베이스 초기화
init_database()

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'list'

if 'selected_item_id' not in st.session_state:
    st.session_state.selected_item_id = None


def main():
    """메인 함수"""

    # 로그인 체크
    if not is_logged_in():
        login()
        return

    # 로그인된 사용자 정보
    user = get_current_user()

    # 사이드바
    with st.sidebar:
        st.title("🏫 기자재 관리")
        st.markdown("---")

        # 사용자 정보
        st.write(f"**{user['college_name']}**")
        st.write(f"👤 {user['username']}")
        st.caption(f"권한: {user['role']}")

        st.markdown("---")

        # 메뉴
        st.subheader("📂 메뉴")

        if st.button("📋 기자재 조회", use_container_width=True, type="primary" if st.session_state.page == 'list' else "secondary"):
            st.session_state.page = 'list'
            st.session_state.edit_mode = False
            st.session_state.edit_item_id = None
            st.session_state.selected_item_id = None
            st.rerun()

        if st.button("➕ 기자재 등록", use_container_width=True, type="primary" if st.session_state.page == 'register' else "secondary"):
            st.session_state.page = 'register'
            st.session_state.edit_mode = False
            st.session_state.edit_item_id = None
            st.rerun()

        if st.button("🏷️ 카테고리 관리", use_container_width=True, type="primary" if st.session_state.page == 'item_management' else "secondary"):
            st.session_state.page = 'item_management'
            st.rerun()

        if st.button("📤 엑셀 일괄등록", use_container_width=True, type="primary" if st.session_state.page == 'bulk_upload' else "secondary"):
            st.session_state.page = 'bulk_upload'
            st.rerun()

        if st.button("🔧 수리·점검 이력", use_container_width=True, type="primary" if st.session_state.page == 'repairs' else "secondary"):
            st.session_state.page = 'repairs'
            st.rerun()

        st.markdown("---")

        # 관리자 전용 메뉴
        if user['role'] == 'admin':
            st.subheader("⚙️ 관리자 메뉴")

            if st.button("👥 계정 관리", use_container_width=True, disabled=True):
                st.info("Phase 2에서 구현 예정")

            st.markdown("---")

        # 로그아웃
        if st.button("🚪 로그아웃", use_container_width=True):
            logout()

        st.markdown("---")

        # 하단 정보
        st.caption("신한대학교 교육용 기자재 관리 시스템")
        st.caption("v1.0 Phase 1")

    # 메인 컨텐츠 영역
    if st.session_state.page == 'list':
        show_list_view(user)
    elif st.session_state.page == 'register':
        show_register_form(user)
    elif st.session_state.page == 'item_management':
        show_item_management(user)
    elif st.session_state.page == 'bulk_upload':
        show_bulk_upload(user)
    elif st.session_state.page == 'repairs':
        show_repairs(user)
    else:
        st.error("잘못된 페이지입니다.")


if __name__ == "__main__":
    main()
