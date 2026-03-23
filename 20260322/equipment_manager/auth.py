"""
로그인/로그아웃 및 세션 관리
"""
import streamlit as st
import bcrypt
from database import get_connection
from datetime import datetime, timedelta


def check_password(username: str, password: str) -> dict | None:
    """
    아이디/비밀번호 검증
    반환: 사용자 정보 dict 또는 None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password, college_code, college_name, role, is_active
        FROM users
        WHERE username = ? AND is_active = 1
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    # bcrypt 비밀번호 검증
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return {
            'id': user['id'],
            'username': user['username'],
            'college_code': user['college_code'],
            'college_name': user['college_name'],
            'role': user['role']
        }

    return None


def login():
    """로그인 화면"""
    st.title("🏫 신한대학교 교육용 기자재 관리 시스템")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("로그인")

        # Form을 사용하여 엔터키로 로그인 가능하게 함
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("아이디", key="login_username")
            password = st.text_input("비밀번호", type="password", key="login_password")

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                submitted = st.form_submit_button("로그인", use_container_width=True, type="primary")

            with col_btn2:
                reset = st.form_submit_button("초기화", use_container_width=True)

        # 로그인 버튼 또는 엔터키 처리
        if submitted:
            if not username or not password:
                st.error("아이디와 비밀번호를 입력하세요.")
            else:
                user = check_password(username, password)
                if user:
                    # 세션 정보 저장
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.last_activity = datetime.now()
                    st.success(f"{user['college_name']} {user['username']}님 환영합니다!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

        # 초기화 버튼 처리
        if reset:
            st.rerun()

        st.markdown("---")
        st.info("""
        **초기 계정 정보**
        - 관리자: admin / admin1234
        - 공과대학: eng_1 / eng1234
        - 보건대학: hlt_1 / hlt1234
        - 디자인예술대학: art_1 / art1234
        - 경영대학: biz_1 / biz1234
        - 사회과학대학: soc_1 / soc1234
        - 태권도·체육대학: spt_1 / spt1234
        """)


def logout():
    """로그아웃"""
    if 'logged_in' in st.session_state:
        del st.session_state.logged_in
    if 'user' in st.session_state:
        del st.session_state.user
    if 'last_activity' in st.session_state:
        del st.session_state.last_activity
    st.rerun()


def check_session_timeout():
    """
    세션 타임아웃 체크 (30분)
    """
    if 'last_activity' in st.session_state:
        elapsed = datetime.now() - st.session_state.last_activity
        if elapsed > timedelta(minutes=30):
            st.warning("30분 동안 활동이 없어 자동 로그아웃되었습니다.")
            logout()
        else:
            # 활동 시간 갱신
            st.session_state.last_activity = datetime.now()


def is_logged_in() -> bool:
    """로그인 상태 확인"""
    return st.session_state.get('logged_in', False)


def get_current_user() -> dict | None:
    """현재 로그인한 사용자 정보 반환"""
    return st.session_state.get('user', None)


def require_login():
    """로그인 필수 체크 (데코레이터 대용)"""
    if not is_logged_in():
        login()
        st.stop()
    check_session_timeout()
