"""
로그인/로그아웃 및 세션 관리 (동시 접속 5명 제한)
"""
import streamlit as st
import bcrypt
from database import get_connection
from datetime import datetime, timedelta
import json
import hashlib
import uuid
from pathlib import Path


MAX_CONCURRENT_SESSIONS = 5  # 동시 접속 제한 (5명)


def get_session_file(username: str = None):
    """세션 파일 경로 반환 (사용자별)"""
    session_dir = Path(__file__).parent / "data" / "sessions"
    session_dir.mkdir(parents=True, exist_ok=True)
    if username:
        # 사용자별 세션 파일 (다중 접속 지원)
        return session_dir / f"session_{username}.json"
    else:
        # 기본 세션 파일 (하위 호환성)
        return session_dir / "session.json"


def create_session_id() -> str:
    """고유 세션 ID 생성 (브라우저/탭 구분용)"""
    return str(uuid.uuid4())


def create_session_token(username: str) -> str:
    """세션 토큰 생성"""
    data = f"{username}_{datetime.now().isoformat()}"
    return hashlib.sha256(data.encode()).hexdigest()


def clean_expired_sessions(sessions: list, max_inactive_minutes: int = 30) -> list:
    """만료된 세션 제거 (30분 이상 활동 없음)"""
    now = datetime.now()
    active_sessions = []

    for session in sessions:
        try:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if now - last_activity < timedelta(minutes=max_inactive_minutes):
                active_sessions.append(session)
        except:
            continue

    return active_sessions


def save_session(user: dict, token: str, session_id: str = None):
    """세션을 파일에 저장 (사용자별, 다중 세션 지원)"""
    session_file = get_session_file(user['username'])

    # 기존 세션 파일 로드
    if session_file.exists():
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            sessions = data.get('sessions', [])
        except:
            sessions = []
    else:
        sessions = []

    # 만료된 세션 제거
    sessions = clean_expired_sessions(sessions)

    # 새 세션 ID 생성 또는 사용
    if not session_id:
        session_id = create_session_id()

    # 기존 세션 업데이트 또는 새 세션 추가
    session_found = False
    for session in sessions:
        if session['session_id'] == session_id:
            session['last_activity'] = datetime.now().isoformat()
            session_found = True
            break

    if not session_found:
        # 세션 개수 제한 확인
        if len(sessions) >= MAX_CONCURRENT_SESSIONS:
            # 가장 오래된 세션 제거
            sessions.sort(key=lambda x: x['last_activity'])
            sessions = sessions[1:]  # 첫 번째(가장 오래된) 세션 제거

        # 새 세션 추가
        new_session = {
            'session_id': session_id,
            'token': token,
            'login_time': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
        sessions.append(new_session)

    # 파일 저장
    session_data = {
        'user': user,
        'sessions': sessions,
        'last_updated': datetime.now().isoformat()
    }

    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return session_id


def load_session(username: str = None, session_id: str = None) -> dict | None:
    """파일에서 세션 로드"""
    if username:
        session_file = get_session_file(username)
    else:
        # 가장 최근 세션 찾기
        sessions = load_all_sessions()
        if not sessions:
            return None
        session_data = max(sessions, key=lambda x: x.get('last_updated', ''))
        username = session_data['user']['username']
        session_file = get_session_file(username)

    if not session_file.exists():
        return None

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 세션 배열 가져오기
        sessions = data.get('sessions', [])

        # 만료된 세션 제거
        sessions = clean_expired_sessions(sessions)

        # 세션 ID가 있으면 해당 세션 확인
        if session_id:
            session_found = False
            for session in sessions:
                if session['session_id'] == session_id:
                    # 세션 유효성 검사 (3개월)
                    last_activity = datetime.fromisoformat(session['last_activity'])
                    if datetime.now() - last_activity > timedelta(days=90):
                        # 만료된 세션 제거
                        sessions.remove(session)
                        break

                    # 세션 활동 시간 갱신
                    session['last_activity'] = datetime.now().isoformat()
                    session_found = True
                    break

            if not session_found:
                return None
        elif sessions:
            # 세션 ID가 없으면 가장 최근 세션 사용
            sessions.sort(key=lambda x: x['last_activity'], reverse=True)
            session_id = sessions[0]['session_id']
            sessions[0]['last_activity'] = datetime.now().isoformat()
        else:
            return None

        # 파일 업데이트
        data['sessions'] = sessions
        data['last_updated'] = datetime.now().isoformat()
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {
            'user': data['user'],
            'session_id': session_id,
            'sessions': sessions
        }
    except:
        return None


def load_all_sessions() -> list:
    """모든 세션 파일 로드"""
    session_dir = Path(__file__).parent / "data" / "sessions"
    if not session_dir.exists():
        return []

    all_data = []
    for session_file in session_dir.glob("session_*.json"):
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            all_data.append(data)
        except:
            continue

    return all_data


def clear_session(username: str = None, session_id: str = None):
    """세션 파일에서 특정 세션 제거"""
    if not username:
        return

    session_file = get_session_file(username)
    if not session_file.exists():
        return

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        sessions = data.get('sessions', [])

        if session_id:
            # 특정 세션만 제거
            sessions = [s for s in sessions if s['session_id'] != session_id]
        else:
            # 모든 세션 제거
            sessions = []

        if sessions:
            data['sessions'] = sessions
            data['last_updated'] = datetime.now().isoformat()
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            # 세션이 없으면 파일 삭제
            session_file.unlink()
    except:
        pass


def get_active_session_count(username: str) -> int:
    """현재 활성 세션 개수 반환"""
    session_file = get_session_file(username)
    if not session_file.exists():
        return 0

    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        sessions = data.get('sessions', [])
        sessions = clean_expired_sessions(sessions)

        return len(sessions)
    except:
        return 0


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


def reset_password(username: str, current_password: str, new_password: str) -> tuple[bool, str]:
    """
    비밀번호 재설정
    반환: (성공여부, 메시지)
    """
    # 현재 비밀번호 확인
    user = check_password(username, current_password)
    if not user:
        return False, "아이디 또는 현재 비밀번호가 올바르지 않습니다."

    # 새 비밀번호 해시
    new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # DB 업데이트
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (new_password_hash, username))
    conn.commit()
    conn.close()

    return True, "비밀번호가 성공적으로 변경되었습니다."


def login():
    """로그인 화면"""
    # 자동 로그인 시도 (세션 파일 확인)
    if not st.session_state.get('logged_in', False):
        session_id = st.session_state.get('session_id')
        if session_id:
            # 현재 세션 ID로 로드 시도
            session_data = load_session(session_id=session_id)
            if session_data:
                st.session_state.logged_in = True
                st.session_state.user = session_data['user']
                st.session_state.session_id = session_data['session_id']
                st.session_state.last_activity = datetime.now()
                st.rerun()
        else:
            # 세션 ID가 없으면 최근 세션으로 로드
            session_data = load_session()
            if session_data:
                st.session_state.logged_in = True
                st.session_state.user = session_data['user']
                st.session_state.session_id = session_data['session_id']
                st.session_state.last_activity = datetime.now()
                st.rerun()

    st.title("🏫 신한대학교 교육용 기자재 관리 시스템")
    st.markdown("---")

    # 비밀번호 재설정 모드
    if st.session_state.get('show_password_reset', False):
        show_password_reset()
        return

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("로그인")

        # Form을 사용하여 엔터키로 로그인 가능하게 함
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("아이디", key="login_username")
            password = st.text_input("비밀번호", type="password", key="login_password")

            # 로그인 유지 체크박스
            remember_me = st.checkbox("로그인 유지 (3개월)", value=True, key="remember_me")

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                submitted = st.form_submit_button("로그인", use_container_width=True, type="primary")

            with col_btn2:
                reset = st.form_submit_button("초기화", use_container_width=True)

        # 비밀번호 재설정 링크
        if st.button("🔑 비밀번호 재설정", use_container_width=True):
            st.session_state.show_password_reset = True
            st.rerun()

        # 로그인 버튼 또는 엔터키 처리
        if submitted:
            if not username or not password:
                st.error("아이디와 비밀번호를 입력하세요.")
            else:
                user = check_password(username, password)
                if user:
                    # 동시 접속 제한 확인
                    active_count = get_active_session_count(username)

                    if active_count >= MAX_CONCURRENT_SESSIONS:
                        st.warning(f"⚠️ 동시 접속 제한: 이미 {MAX_CONCURRENT_SESSIONS}명이 접속 중입니다.")
                        st.info("가장 오래된 세션이 자동으로 종료되고 새 세션이 생성됩니다.")

                    # 세션 정보 저장 (메모리)
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.last_activity = datetime.now()

                    # 로그인 유지 체크박스에 따라 세션 파일 저장
                    if remember_me:
                        token = create_session_token(username)
                        session_id = save_session(user, token)
                        st.session_state.session_id = session_id

                        active_count = get_active_session_count(username)
                        st.success(f"{user['college_name']} {user['username']}님 환영합니다! (접속자: {active_count}명)")
                    else:
                        st.success(f"{user['college_name']} {user['username']}님 환영합니다!")

                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

        # 초기화 버튼 처리
        if reset:
            st.rerun()

        st.markdown("---")

        # 동시 접속 제한 안내
        st.info(f"""
        **동시 접속 제한: 최대 {MAX_CONCURRENT_SESSIONS}명**
        - 같은 아이디로 최대 {MAX_CONCURRENT_SESSIONS}명까지 동시 접속 가능
        - {MAX_CONCURRENT_SESSIONS}명 초과 시 가장 오래된 세션 자동 종료
        """)

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


def show_password_reset():
    """비밀번호 재설정 화면"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("🔑 비밀번호 재설정")

        with st.form("password_reset_form"):
            username = st.text_input("아이디")
            current_password = st.text_input("현재 비밀번호", type="password")
            new_password = st.text_input("새 비밀번호", type="password")
            confirm_password = st.text_input("새 비밀번호 확인", type="password")

            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                submitted = st.form_submit_button("변경", use_container_width=True, type="primary")

            with col_btn2:
                cancel = st.form_submit_button("취소", use_container_width=True)

        if cancel:
            st.session_state.show_password_reset = False
            st.rerun()

        if submitted:
            if not username or not current_password or not new_password or not confirm_password:
                st.error("모든 항목을 입력하세요.")
            elif new_password != confirm_password:
                st.error("새 비밀번호가 일치하지 않습니다.")
            elif len(new_password) < 4:
                st.error("새 비밀번호는 최소 4자 이상이어야 합니다.")
            else:
                success, message = reset_password(username, current_password, new_password)
                if success:
                    st.success(message)
                    st.session_state.show_password_reset = False
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)


def logout():
    """로그아웃"""
    # 현재 사용자명과 세션 ID 저장
    username = None
    session_id = None

    if 'user' in st.session_state:
        username = st.session_state.user.get('username')
    if 'session_id' in st.session_state:
        session_id = st.session_state.session_id

    # 세션 상태 삭제
    if 'logged_in' in st.session_state:
        del st.session_state.logged_in
    if 'user' in st.session_state:
        del st.session_state.user
    if 'last_activity' in st.session_state:
        del st.session_state.last_activity
    if 'session_id' in st.session_state:
        del st.session_state.session_id

    # 해당 세션만 파일에서 제거 (다른 세션 유지)
    if username and session_id:
        clear_session(username, session_id)

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
            # 활동 시간 갱신 (메모리 + 파일)
            st.session_state.last_activity = datetime.now()

            # 세션 파일도 갱신
            if 'user' in st.session_state and 'session_id' in st.session_state:
                username = st.session_state.user['username']
                session_id = st.session_state.session_id
                token = create_session_token(username)
                save_session(st.session_state.user, token, session_id)


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
