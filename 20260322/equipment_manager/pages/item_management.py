"""
카테고리 관리 화면 - 기자재 카테고리 추가/삭제
"""
import streamlit as st
from database import get_connection


def get_categories() -> list:
    """카테고리 목록 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, sort_order
        FROM categories
        WHERE is_active = 1
        ORDER BY sort_order, name
    """)
    categories = cursor.fetchall()
    conn.close()
    return [dict(cat) for cat in categories]


def add_category(name: str, sort_order: int = 0) -> tuple:
    """카테고리 추가"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO categories (name, sort_order)
            VALUES (?, ?)
        """, (name, sort_order))
        conn.commit()
        conn.close()
        return True, "카테고리가 추가되었습니다."
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, f"'{name}' 카테고리가 이미 존재합니다."
        return False, f"추가 실패: {str(e)}"


def delete_category(category_id: int) -> tuple:
    """카테고리 삭제 (소프트 삭제)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE categories
            SET is_active = 0
            WHERE id = ?
        """, (category_id,))
        conn.commit()
        conn.close()
        return True, "카테고리가 삭제되었습니다."
    except Exception as e:
        return False, f"삭제 실패: {str(e)}"


def show_category_management():
    """카테고리 관리 화면"""
    st.subheader("🏷️ 카테고리 관리")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 카테고리 목록")
        categories = get_categories()

        if not categories:
            st.info("등록된 카테고리가 없습니다.")
        else:
            for idx, cat in enumerate(categories):
                col_name, col_order, col_del = st.columns([3, 1, 1])

                with col_name:
                    st.write(f"🏷️ **{cat['name']}**")

                with col_order:
                    st.write(f"순서: {cat['sort_order']}")

                with col_del:
                    if st.button("🗑️", key=f"del_cat_{cat['id']}"):
                        success, message = delete_category(cat['id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

                if idx < len(categories) - 1:
                    st.markdown("<hr style='margin: 5px 0; opacity: 0.3;'>", unsafe_allow_html=True)

    with col2:
        st.markdown("### ➕ 카테고리 추가")

        new_category = st.text_input(
            "카테고리명 *",
            placeholder="예: 전자기기",
            key="new_category_name"
        )

        sort_order = st.number_input(
            "정렬 순서",
            min_value=0,
            max_value=999,
            value=0,
            help="작은 숫자가 먼저 표시됩니다"
        )

        if st.button("💾 추가", type="primary", use_container_width=True, key="add_category_btn"):
            if not new_category.strip():
                st.error("카테고리명을 입력하세요.")
            else:
                success, message = add_category(new_category.strip(), sort_order)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def show_item_management(user: dict):
    """카테고리 관리 메인 화면"""
    st.title("🏷️ 카테고리 관리")

    st.info("""
    💡 **안내**
    - 기자재 등록 시 사용할 카테고리를 관리합니다.
    - 카테고리는 기자재 분류에 사용됩니다.
    - 정렬 순서가 작은 숫자가 먼저 표시됩니다.
    """)

    st.markdown("---")

    # admin만 카테고리 관리 가능
    if user['role'] == 'admin':
        show_category_management()
    else:
        st.warning("⚠️ 카테고리 관리는 관리자만 가능합니다.")
        st.markdown("### 📋 카테고리 목록 (읽기 전용)")

        categories = get_categories()
        if not categories:
            st.info("등록된 카테고리가 없습니다.")
        else:
            for cat in categories:
                st.write(f"🏷️ **{cat['name']}** (순서: {cat['sort_order']})")


if __name__ == "__main__":
    # 테스트용
    st.set_page_config(page_title="카테고리 관리", layout="wide")

    test_user = {
        'username': 'admin',
        'role': 'admin',
        'college_code': 'ALL',
        'college_name': '전체'
    }

    show_item_management(test_user)
