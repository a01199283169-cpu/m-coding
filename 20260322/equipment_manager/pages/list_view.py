"""
기자재 조회 화면 - 계층형 필터 + 목록 테이블
"""
import streamlit as st
import streamlit.components.v1 as components
from database import get_connection
from datetime import datetime, date
from utils.excel_export import export_to_excel, get_excel_filename


def get_repair_history(equipment_id: int) -> list:
    """특정 기자재의 수리·점검 이력 조회"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM equipment_repairs
        WHERE equipment_id = ?
        ORDER BY repair_date DESC
    """, (equipment_id,))
    repairs = cursor.fetchall()
    conn.close()
    return repairs


def show_print_list_view(results: list, filters: dict):
    """A4 가로 목록형 출력 화면 - iframe으로 표시하고 인쇄 버튼 제공"""
    from datetime import datetime

    # 출력 정보
    print_date = datetime.now().strftime('%Y년 %m월 %d일')
    total_count = len(results)

    # 필터 정보 문자열
    filter_text = "전체"
    if filters.get('college'):
        filter_text = filters['college']
        if filters.get('dept'):
            filter_text += f" > {filters['dept']}"

    # 안내 메시지
    st.info("💡 **인쇄 방법:** 아래 미리보기 화면의 '🖨️ 인쇄하기' 버튼을 클릭하거나 Ctrl+P를 누르세요.")

    # HTML 생성 (iframe용)

    # HTML 생성
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>교육용 기자재 목록</title>
    <style>
        @media print {{
            @page {{ size: A4 landscape; margin: 10mm; }}
            body {{ margin: 0; padding: 0; }}
            .no-print {{ display: none !important; }}
            .header {{ margin-bottom: 10px; padding-bottom: 5px; }}
            .info {{ margin-bottom: 8px; font-size: 9pt; }}
            table {{ font-size: 8pt; }}
            th {{ padding: 4px 2px; }}
            td {{ padding: 3px 2px; }}
        }}

        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            padding: 20px;
            font-size: 10pt;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        .info {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 10pt;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            table-layout: fixed;
        }}
        th {{
            background-color: #4a5568;
            color: white;
            border: 1px solid #333;
            padding: 6px 4px;
            text-align: center;
            font-size: 9pt;
            font-weight: bold;
            word-wrap: break-word;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 4px 3px;
            text-align: center;
            font-size: 8.5pt;
            word-wrap: break-word;
            word-break: keep-all;
            overflow-wrap: break-word;
            white-space: normal;
            vertical-align: middle;
        }}
        td.left {{
            text-align: left;
            padding-left: 4px;
        }}
        td.right {{
            text-align: right;
            padding-right: 4px;
        }}
        .footer {{
            margin-top: 20px;
            text-align: right;
            color: #666;
            font-size: 9pt;
        }}
        .print-btn {{
            margin: 20px 0;
            text-align: center;
        }}
        button {{
            padding: 10px 30px;
            font-size: 16px;
            cursor: pointer;
            background: #1976d2;
            color: white;
            border: none;
            border-radius: 5px;
        }}
        button:hover {{
            background: #1565c0;
        }}
    </style>
</head>
<body>
    <div class="print-btn no-print">
        <button onclick="window.print()">🖨️ 인쇄하기</button>
    </div>
    <div class="header"><h1>📋 교육용 기자재 목록</h1></div>
    <div class="info">
        <div><strong>조회 범위:</strong> {filter_text} | <strong>총 {total_count:,}건</strong></div>
        <div><strong>출력일:</strong> {print_date}</div>
    </div>
    <table>
        <colgroup>
            <col style="width: 3%;">
            <col style="width: 8%;">
            <col style="width: 8%;">
            <col style="width: 9%;">
            <col style="width: 10%;">
            <col style="width: 7%;">
            <col style="width: 16%;">
            <col style="width: 10%;">
            <col style="width: 8%;">
            <col style="width: 7%;">
            <col style="width: 5%;">
            <col style="width: 7%;">
            <col style="width: 6%;">
            <col style="width: 4%;">
        </colgroup>
        <thead>
            <tr>
                <th>번호</th><th>품목코드</th><th>자산코드</th><th>단과대학</th><th>학과</th><th>카테고리</th>
                <th>품목명</th><th>보관장소</th><th>예산부서</th><th>자산구분</th><th>수량</th><th>단가</th><th>입고일</th><th>수리</th>
            </tr>
        </thead>
        <tbody>
"""

    for idx, row in enumerate(results, 1):
        repair_count = row['repair_count'] or 0
        repair_text = f"{repair_count}건" if repair_count > 0 else "-"
        location = row['location'] if row['location'] else '-'
        asset_code = row['asset_code'] if row['asset_code'] else '-'
        budget_dept = row['budget_dept'] if row['budget_dept'] else '-'

        html += f"""
            <tr>
                <td>{idx}</td>
                <td>{row['item_code']}</td>
                <td>{asset_code}</td>
                <td>{row['college'] or '-'}</td>
                <td class="left">{row['dept_name'] or '-'}</td>
                <td>{row['category']}</td>
                <td class="left">{row['item_name']}</td>
                <td class="left">{location}</td>
                <td class="left">{budget_dept}</td>
                <td>{row['asset_type']}</td>
                <td>{row['quantity']:,}</td>
                <td class="right">{row['unit_price']:,}원</td>
                <td>{row['arrival_date']}</td>
                <td>{repair_text}</td>
            </tr>
"""

    html += """
        </tbody>
    </table>
    <div class="footer">신한대학교 교육용 기자재 관리 시스템</div>
</body>
</html>
"""

    # iframe으로 렌더링
    components.html(html, height=650, scrolling=True)

    # 닫기 버튼
    st.markdown("---")
    if st.button("❌ 목록으로 돌아가기", use_container_width=False, key="close_print_view", type="primary"):
        st.session_state.show_print_list = False
        st.rerun()


def generate_equipment_card_html(equipment, photos):
    """개별 기자재 카드 HTML 생성"""
    import base64

    # 사진을 base64로 인코딩 (최대 2장)
    photo_html = ""
    for i in range(2):
        if i < len(photos):
            try:
                import os
                if os.path.exists(photos[i]['file_path']):
                    with open(photos[i]['file_path'], 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode()
                        photo_html += f'<img src="data:image/jpeg;base64,{img_data}" style="width: 100%; height: 140px; object-fit: contain; border: 1px solid #ddd; background: #f9f9f9;">'
                else:
                    photo_html += '<div style="width: 100%; height: 140px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd;">사진 없음</div>'
            except:
                photo_html += '<div style="width: 100%; height: 140px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd;">사진 없음</div>'
        else:
            photo_html += '<div style="width: 100%; height: 140px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd;">-</div>'

    card_html = f"""
    <div class="equipment-card">
        <div class="card-header">{equipment['item_name']}</div>
        <table class="card-table">
            <tr class="section-row">
                <td colspan="4" class="section-title">🏫 소속 정보</td>
            </tr>
            <tr>
                <th>단과대학</th>
                <td>{equipment['college']}</td>
                <th>학과</th>
                <td>{equipment['dept_name']}</td>
            </tr>
            <tr>
                <th>보관장소</th>
                <td colspan="3">{equipment['location'] or '-'}</td>
            </tr>
            <tr>
                <th>예산부서</th>
                <td colspan="3">{equipment['budget_dept'] or '-'}</td>
            </tr>

            <tr class="section-row">
                <td colspan="4" class="section-title">📋 기본 정보</td>
            </tr>
            <tr>
                <th>품목코드</th>
                <td>{equipment['item_code']}</td>
                <th>자산코드</th>
                <td>{equipment['asset_code'] or '-'}</td>
            </tr>
            <tr>
                <th>카테고리</th>
                <td colspan="3">{equipment['category']}</td>
            </tr>
            <tr>
                <th>규격</th>
                <td>{equipment['spec'] or '-'}</td>
                <th>자산구분</th>
                <td>{equipment['asset_type']}</td>
            </tr>
            <tr>
                <th>수량</th>
                <td>{equipment['quantity']:,}개</td>
                <th>공급업체</th>
                <td>{equipment['vendor'] or '-'}</td>
            </tr>

            <tr class="section-row">
                <td colspan="4" class="section-title">💰 금액 정보</td>
            </tr>
            <tr>
                <th>단가</th>
                <td>{equipment['unit_price']:,}원</td>
                <th>총액</th>
                <td>{equipment['total_price']:,}원</td>
            </tr>
            <tr>
                <th>구매일</th>
                <td>{equipment['purchase_date']}</td>
                <th>입고일</th>
                <td>{equipment['arrival_date']}</td>
            </tr>

            <tr class="section-row">
                <td colspan="4" class="section-title">📷 사진</td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 5px;">{photo_html.split('</div>')[0] + '</div>' if len(photo_html.split('</div>')) > 0 else ''}</td>
                <td colspan="2" style="padding: 5px;">{photo_html.split('</div>')[1] + '</div>' if len(photo_html.split('</div>')) > 1 else ''}</td>
            </tr>
        </table>
    </div>
    """
    return card_html


def show_detail_print_view(equipment_ids):
    """기자재 카드 인쇄 화면 (A4 세로, 한 장에 2개씩)"""
    from datetime import datetime

    if not isinstance(equipment_ids, list):
        equipment_ids = [equipment_ids]

    conn = get_connection()
    cursor = conn.cursor()

    all_cards = []

    for equipment_id in equipment_ids:
        # 기자재 정보 조회
        cursor.execute("""
            SELECT e.*, d.dept_name, d.college
            FROM equipment e
            LEFT JOIN departments d ON e.dept_code = d.dept_code
            WHERE e.id = ?
        """, (equipment_id,))
        equipment = cursor.fetchone()

        # 사진 조회
        cursor.execute("""
            SELECT file_path, sort_order
            FROM equipment_photos
            WHERE equipment_id = ?
            ORDER BY sort_order
            LIMIT 2
        """, (equipment_id,))
        photos = cursor.fetchall()

        if equipment:
            all_cards.append(generate_equipment_card_html(equipment, photos))

    conn.close()

    if not all_cards:
        st.error("기자재 정보를 찾을 수 없습니다.")
        return

    print_date = datetime.now().strftime('%Y년 %m월 %d일')

    # HTML 생성
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>교육용 기자재 카드</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 12mm;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            .equipment-card {{
                page-break-inside: avoid;
                max-height: 48vh;
            }}
            body {{
                width: 210mm;
                padding: 0;
                margin: 0;
            }}
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            padding: 10px;
            font-size: 9pt;
            line-height: 1.3;
            max-width: 210mm;
            margin: 0 auto;
        }}
        .print-btn {{
            margin: 15px 0;
            text-align: center;
        }}
        button {{
            padding: 10px 30px;
            font-size: 16px;
            cursor: pointer;
            background: #1976d2;
            color: white;
            border: none;
            border-radius: 5px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 12px;
            border-bottom: 2px solid #90caf9;
            padding-bottom: 8px;
        }}
        .header h1 {{
            font-size: 16pt;
            margin: 5px 0;
            color: #1976d2;
        }}
        .info-line {{
            text-align: right;
            font-size: 8pt;
            color: #666;
            margin-bottom: 8px;
        }}
        .equipment-card {{
            border: 2px solid #90caf9;
            margin-bottom: 12px;
            padding: 0;
            background: white;
            width: 100%;
        }}
        .card-header {{
            background: #e8f4f8;
            color: #1a5490;
            padding: 8px;
            font-size: 12pt;
            font-weight: bold;
            text-align: center;
            border-bottom: 2px solid #90caf9;
        }}
        .card-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .card-table th {{
            background: #e3f2fd;
            padding: 5px 6px;
            text-align: left;
            border: 1px solid #90caf9;
            width: 25%;
            font-size: 8.5pt;
            font-weight: bold;
            color: #1976d2;
        }}
        .card-table td {{
            padding: 5px 6px;
            border: 1px solid #cbd5e0;
            font-size: 8.5pt;
            word-wrap: break-word;
        }}
        .section-row {{
            background: #fafafa;
        }}
        .section-title {{
            background: #e3f2fd;
            color: #1976d2;
            font-weight: bold;
            padding: 5px 6px;
            text-align: center;
            font-size: 9pt;
            border: 1px solid #90caf9;
        }}
        .footer {{
            margin-top: 15px;
            text-align: center;
            font-size: 7pt;
            color: #666;
            padding-top: 8px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="print-btn no-print">
        <button onclick="window.print()">🖨️ 인쇄하기</button>
    </div>
    <div class="header">
        <h1>📦 교육용 기자재 카드</h1>
    </div>
    <div class="info-line">출력일: {print_date} | 총 {len(all_cards)}건</div>
"""

    # 카드 추가 (2개씩 페이지 구분)
    for idx, card in enumerate(all_cards):
        html += card
        # 2개마다 페이지 나누기 (마지막 제외)
        if (idx + 1) % 2 == 0 and idx + 1 < len(all_cards):
            html += '<div style="page-break-after: always;"></div>'

    html += """
    <div class="footer">신한대학교 교육용 기자재 관리 시스템</div>
</body>
</html>
"""

    # iframe으로 렌더링
    components.html(html, height=800, scrolling=True)

    # 닫기 버튼
    st.markdown("---")
    if st.button("❌ 닫기", key="close_detail_print", type="primary"):
        st.session_state.show_detail_print = False
        st.rerun()


def show_detail_full_print_view(equipment_ids):
    """기자재 상세 전체 인쇄 (A4 세로, 한 장에 1개씩, 모든 정보 포함)"""
    from datetime import datetime
    import base64

    if not isinstance(equipment_ids, list):
        equipment_ids = [equipment_ids]

    conn = get_connection()
    cursor = conn.cursor()

    all_pages = []

    for equipment_id in equipment_ids:
        # 기자재 정보 조회
        cursor.execute("""
            SELECT e.*, d.dept_name, d.college
            FROM equipment e
            LEFT JOIN departments d ON e.dept_code = d.dept_code
            WHERE e.id = ?
        """, (equipment_id,))
        equipment = cursor.fetchone()

        # 사진 조회
        cursor.execute("""
            SELECT file_path, sort_order
            FROM equipment_photos
            WHERE equipment_id = ?
            ORDER BY sort_order
        """, (equipment_id,))
        photos = cursor.fetchall()

        # 수리 이력 조회
        repairs = get_repair_history(equipment_id)

        if not equipment:
            continue

        # 사진 HTML 생성
        photos_html = ""
        for photo in photos[:4]:  # 최대 4장
            try:
                import os
                if os.path.exists(photo['file_path']):
                    with open(photo['file_path'], 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode()
                        photos_html += f'''
                        <div style="display: inline-block; width: 48%; margin: 1%; vertical-align: top;">
                            <img src="data:image/jpeg;base64,{img_data}" style="width: 100%; height: 180px; object-fit: contain; border: 1px solid #ddd; background: #f9f9f9;">
                        </div>
                        '''
            except:
                pass

        # 수리 이력 HTML 생성
        repairs_html = ""
        if repairs:
            for repair in repairs:
                repairs_html += f'''
                <tr>
                    <td>{repair['repair_date']}</td>
                    <td>{repair['repair_type']}</td>
                    <td style="text-align: left;">{repair['description'] or '-'}</td>
                    <td>{repair['cost']:,}원</td>
                    <td>{repair['vendor'] or '-'}</td>
                </tr>
                '''
        else:
            repairs_html = '<tr><td colspan="5" style="text-align: center; color: #999;">수리·점검 이력 없음</td></tr>'

        # 페이지 HTML 생성
        page_html = f'''
        <div class="detail-page">
            <div class="detail-header">
                <h1>📦 교육용 기자재 상세 정보</h1>
                <div class="item-title">{equipment['item_name']}</div>
            </div>

            <table class="detail-table">
                <tr class="section-row">
                    <td colspan="4" class="section-title">🏫 소속 정보</td>
                </tr>
                <tr>
                    <th>단과대학</th>
                    <td>{equipment['college']}</td>
                    <th>학과</th>
                    <td>{equipment['dept_name']}</td>
                </tr>
                <tr>
                    <th>보관장소</th>
                    <td colspan="3">{equipment['location'] or '-'}</td>
                </tr>
                <tr>
                    <th>예산부서</th>
                    <td colspan="3">{equipment['budget_dept'] or '-'}</td>
                </tr>

                <tr class="section-row">
                    <td colspan="4" class="section-title">📋 기본 정보</td>
                </tr>
                <tr>
                    <th>품목코드</th>
                    <td>{equipment['item_code']}</td>
                    <th>자산코드</th>
                    <td>{equipment['asset_code'] or '-'}</td>
                </tr>
                <tr>
                    <th>카테고리</th>
                    <td>{equipment['category']}</td>
                    <th>품목명</th>
                    <td>{equipment['item_name']}</td>
                </tr>
                <tr>
                    <th>규격</th>
                    <td colspan="3">{equipment['spec'] or '-'}</td>
                </tr>
                <tr>
                    <th>자산구분</th>
                    <td>{equipment['asset_type']}</td>
                    <th>수량</th>
                    <td>{equipment['quantity']:,}개</td>
                </tr>
                <tr>
                    <th>공급업체</th>
                    <td colspan="3">{equipment['vendor'] or '-'}</td>
                </tr>

                <tr class="section-row">
                    <td colspan="4" class="section-title">💰 금액 정보</td>
                </tr>
                <tr>
                    <th>단가</th>
                    <td>{equipment['unit_price']:,}원</td>
                    <th>총액</th>
                    <td>{equipment['total_price']:,}원</td>
                </tr>
                <tr>
                    <th>구매일</th>
                    <td>{equipment['purchase_date']}</td>
                    <th>입고일</th>
                    <td>{equipment['arrival_date']}</td>
                </tr>

                <tr class="section-row">
                    <td colspan="4" class="section-title">📝 추가 정보</td>
                </tr>
                <tr>
                    <th>입력자</th>
                    <td>{equipment['registrant_name'] or '-'}</td>
                    <th>입력일</th>
                    <td>{equipment['created_at'] or '-'}</td>
                </tr>
                <tr>
                    <th>비고</th>
                    <td colspan="3">{equipment['note'] or '-'}</td>
                </tr>
            </table>

            <div class="photos-section">
                <div class="section-title-standalone">📷 사진</div>
                <div class="photos-grid">
                    {photos_html if photos_html else '<div style="text-align: center; color: #999; padding: 20px;">등록된 사진이 없습니다.</div>'}
                </div>
            </div>

            <div class="repairs-section">
                <div class="section-title-standalone">🔧 수리·점검 이력</div>
                <table class="repair-table">
                    <thead>
                        <tr>
                            <th style="width: 15%;">날짜</th>
                            <th style="width: 15%;">구분</th>
                            <th style="width: 40%;">내용</th>
                            <th style="width: 15%;">비용</th>
                            <th style="width: 15%;">업체</th>
                        </tr>
                    </thead>
                    <tbody>
                        {repairs_html}
                    </tbody>
                </table>
            </div>

            <div class="detail-footer">신한대학교 교육용 기자재 관리 시스템 | 출력일: {datetime.now().strftime('%Y년 %m월 %d일')}</div>
        </div>
        '''
        all_pages.append(page_html)

    conn.close()

    if not all_pages:
        st.error("기자재 정보를 찾을 수 없습니다.")
        return

    # HTML 생성
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>교육용 기자재 상세 정보</title>
    <style>
        @media print {{
            @page {{ size: A4 portrait; margin: 12mm; }}
            .no-print {{ display: none !important; }}
            .detail-page {{ page-break-after: always; page-break-inside: avoid; }}
            .detail-page:last-child {{ page-break-after: auto; }}
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            padding: 15px;
            font-size: 10pt;
            line-height: 1.4;
        }}
        .print-btn {{
            margin: 15px 0;
            text-align: center;
        }}
        button {{
            padding: 10px 30px;
            font-size: 16px;
            cursor: pointer;
            background: #1976d2;
            color: white;
            border: none;
            border-radius: 5px;
        }}
        .detail-page {{
            margin-bottom: 30px;
        }}
        .detail-header {{
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #90caf9;
        }}
        .detail-header h1 {{
            font-size: 20pt;
            margin: 5px 0;
            color: #1976d2;
        }}
        .item-title {{
            font-size: 14pt;
            font-weight: bold;
            color: #333;
            margin-top: 8px;
        }}
        .detail-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .detail-table th {{
            background: #e3f2fd;
            padding: 8px;
            text-align: left;
            border: 1px solid #90caf9;
            width: 20%;
            font-size: 9pt;
            font-weight: bold;
            color: #1976d2;
        }}
        .detail-table td {{
            padding: 8px;
            border: 1px solid #cbd5e0;
            font-size: 9pt;
        }}
        .section-row {{
            background: #f7fafc;
        }}
        .section-title {{
            background: #e3f2fd;
            color: #1976d2;
            font-weight: bold;
            padding: 8px;
            text-align: center;
            font-size: 10pt;
            border: 1px solid #90caf9;
        }}
        .section-title-standalone {{
            background: #e3f2fd;
            color: #1976d2;
            font-weight: bold;
            padding: 8px;
            text-align: center;
            font-size: 11pt;
            border: 1px solid #90caf9;
            margin-bottom: 10px;
        }}
        .photos-section {{
            margin-bottom: 20px;
        }}
        .photos-grid {{
            text-align: center;
            padding: 10px;
            background: #fafafa;
            border: 1px solid #ddd;
        }}
        .repairs-section {{
            margin-bottom: 20px;
        }}
        .repair-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .repair-table th {{
            background: #e3f2fd;
            padding: 6px;
            text-align: center;
            border: 1px solid #90caf9;
            font-size: 9pt;
            font-weight: bold;
            color: #1976d2;
        }}
        .repair-table td {{
            padding: 6px;
            border: 1px solid #cbd5e0;
            font-size: 9pt;
            text-align: center;
        }}
        .detail-footer {{
            text-align: center;
            font-size: 8pt;
            color: #666;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="print-btn no-print">
        <button onclick="window.print()">🖨️ 인쇄하기</button>
    </div>
'''

    # 페이지 추가
    for page in all_pages:
        html += page

    html += '''
</body>
</html>
'''

    # iframe으로 렌더링
    components.html(html, height=900, scrolling=True)

    # 닫기 버튼
    st.markdown("---")
    if st.button("❌ 닫기", key="close_full_detail_print", type="primary"):
        st.session_state.show_full_detail_print = False
        st.rerun()


def show_equipment_detail(equipment_id: int):
    """기자재 상세 정보 + 사진 + 수리 이력 표시"""
    conn = get_connection()
    cursor = conn.cursor()

    # 기자재 정보 조회
    cursor.execute("""
        SELECT e.*, d.dept_name, d.college
        FROM equipment e
        LEFT JOIN departments d ON e.dept_code = d.dept_code
        WHERE e.id = ?
    """, (equipment_id,))
    equipment = cursor.fetchone()

    # 사진 조회
    cursor.execute("""
        SELECT file_path, sort_order
        FROM equipment_photos
        WHERE equipment_id = ?
        ORDER BY sort_order
    """, (equipment_id,))
    photos = cursor.fetchall()

    conn.close()

    if not equipment:
        st.error("기자재 정보를 찾을 수 없습니다.")
        return

    # 인쇄 버튼
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🖨️ 카드 인쇄", key="btn_detail_print", use_container_width=True, type="primary"):
            st.session_state.show_detail_print = True
            st.session_state.detail_print_ids = [equipment_id]
            st.rerun()

    st.markdown("---")

    # 기자재 정보 표시
    st.subheader(f"📦 {equipment['item_name']}")
    st.caption(f"품목코드: {equipment['item_code']}")

    # 사진 표시
    if photos:
        st.markdown("### 📷 사진")
        photo_cols = st.columns(min(len(photos), 4))
        for idx, photo in enumerate(photos):
            with photo_cols[idx % 4]:
                try:
                    st.image(photo['file_path'], caption=f"사진 {photo['sort_order']}", use_column_width=True)
                except:
                    st.warning(f"사진 {photo['sort_order']}를 불러올 수 없습니다.")
        st.markdown("---")
    else:
        st.info("📷 등록된 사진이 없습니다.")
        st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🏫 소속 정보**")
        st.write(f"단과대학: {equipment['college']}")
        st.write(f"학과: {equipment['dept_name']}")
        st.write(f"자산구분: {equipment['asset_type']}")

    with col2:
        st.markdown("**📋 기본 정보**")
        st.write(f"카테고리: {equipment['category']}")
        st.write(f"규격: {equipment['spec'] or '-'}")
        st.write(f"수량: {equipment['quantity']:,}개")
        st.write(f"보관장소: {equipment['location'] or '-'}")

    with col3:
        st.markdown("**💰 금액 정보**")
        st.write(f"단가: {equipment['unit_price']:,}원")
        st.write(f"총액: {equipment['total_price']:,}원")
        st.write(f"입고일: {equipment['arrival_date']}")

    if equipment['note']:
        st.markdown("**📝 비고**")
        st.info(equipment['note'])

    st.markdown("---")

    # 수리·점검 이력 표시
    st.markdown("### 🔧 수리·점검 이력")

    repairs = get_repair_history(equipment_id)

    if not repairs:
        st.info("등록된 수리·점검 이력이 없습니다.")
    else:
        st.write(f"**총 {len(repairs)}건의 이력**")

        for repair in repairs:
            with st.expander(f"📅 {repair['repair_date']} - {repair['repair_type']}", expanded=False):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**수리·점검 구분**: {repair['repair_type']}")
                    st.write(f"**수리 일자**: {repair['repair_date']}")
                    st.write(f"**업체**: {repair['vendor'] or '-'}")
                    st.write(f"**비용**: {(repair['cost'] or 0):,}원")

                with col2:
                    st.write(f"**상태**: {repair['status'] or '-'}")
                    st.write(f"**다음 점검일**: {repair['next_check_date'] or '-'}")
                    st.write(f"**등록자**: {repair['created_by_name'] or '-'}")
                    created_at = repair['created_at'] or ''
                    if created_at and len(created_at) >= 10:
                        st.write(f"**등록일**: {created_at[:10]}")
                    else:
                        st.write(f"**등록일**: -")

                if repair['description']:
                    st.markdown("**상세 내용**")
                    st.text_area("", repair['description'], key=f"desc_{repair['id']}", disabled=True, label_visibility="collapsed", height=100)

                if repair['memo']:
                    st.markdown("**메모**")
                    st.text_area("", repair['memo'], key=f"memo_{repair['id']}", disabled=True, label_visibility="collapsed", height=80)


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
            e.asset_code,
            e.budget_dept,
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

    # 보관장소 필터 (부분 일치 검색)
    if filters.get('location'):
        base_query += " AND e.location LIKE ?"
        params.append(f"%{filters['location']}%")

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

    # 세 번째 줄: 보관장소
    col9, col10, col11, col12 = st.columns(4)

    with col9:
        # 보관장소 검색 (부분 일치)
        search_location = st.text_input(
            "보관장소 검색",
            placeholder="보관장소 입력 (부분 검색 가능)",
            key="filter_location"
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
            'location': search_location.strip() if search_location and search_location.strip() else None,
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

        # 출력 화면 표시 (버튼 클릭 후 재로드 시)
        if st.session_state.get('show_print_list', False):
            show_print_list_view(results, filters)
            return

        if st.session_state.get('show_detail_print', False):
            show_detail_print_view(st.session_state.detail_print_ids)
            return

        if st.session_state.get('show_full_detail_print', False):
            show_detail_full_print_view(st.session_state.full_detail_print_ids)
            return

        # 툴바 버튼
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1.2, 1.2, 1.5, 3.1])

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
            # 목록 출력 버튼
            if st.button("🖨️ 목록 출력", use_container_width=True):
                if results:
                    st.session_state.show_print_list = True
                else:
                    st.warning("출력할 데이터가 없습니다.")

        with col5:
            # 전체 카드 인쇄 버튼
            if st.button("📇 카드 인쇄", use_container_width=True):
                if results:
                    # 모든 결과의 ID 수집
                    all_ids = [row['id'] for row in results]
                    st.session_state.show_detail_print = True
                    st.session_state.detail_print_ids = all_ids
                    st.rerun()
                else:
                    st.warning("출력할 데이터가 없습니다.")

        with col6:
            # 상세 전체 인쇄 버튼
            if st.button("📄 상세 전체", use_container_width=True):
                if results:
                    # 모든 결과의 ID 수집
                    all_ids = [row['id'] for row in results]
                    st.session_state.show_full_detail_print = True
                    st.session_state.full_detail_print_ids = all_ids
                    st.rerun()
                else:
                    st.warning("출력할 데이터가 없습니다.")

        with col7:
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
    
        # 다중 삭제 확인 팝업
        if st.session_state.get('show_bulk_delete_confirm', False):
            selected_ids = st.session_state.get('selected_items_to_delete', [])
            st.warning(f"⚠️ 선택한 {len(selected_ids)}개 품목을 삭제하시겠습니까?")
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ 삭제 확인", type="primary", key="confirm_bulk_delete"):
                    # 다중 소프트 삭제 실행
                    conn = get_connection()
                    cursor = conn.cursor()
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    for item_id in selected_ids:
                        cursor.execute("""
                            UPDATE equipment
                            SET is_deleted = 1, updated_at = ?
                            WHERE id = ?
                        """, (now, item_id))

                    conn.commit()
                    conn.close()

                    # 체크박스 상태 초기화
                    for item_id in selected_ids:
                        checkbox_key = f"select_{item_id}"
                        if checkbox_key in st.session_state:
                            del st.session_state[checkbox_key]

                    st.success(f"{len(selected_ids)}개 품목이 삭제되었습니다.")
                    st.session_state.show_bulk_delete_confirm = False
                    st.session_state.selected_items_to_delete = []
                    st.rerun()

            with col2:
                if st.button("❌ 취소", key="cancel_bulk_delete"):
                    st.session_state.show_bulk_delete_confirm = False
                    st.rerun()

        # 단일 삭제 확인 팝업 (기존 유지)
        if st.session_state.get('show_delete_confirm', False):
            st.warning("⚠️ 선택한 품목을 삭제하시겠습니까?")
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ 삭제 확인", type="primary", key="confirm_single_delete"):
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
                if st.button("❌ 취소", key="cancel_single_delete"):
                    st.session_state.show_delete_confirm = False
                    st.rerun()
    
        # 목록 테이블
        if not results:
            st.info("조회된 데이터가 없습니다.")
        else:
            st.subheader(f"📊 목록 ({len(results)}건)")

            # 테이블 헤더
            header_cols = st.columns([0.4, 0.6, 1, 1.2, 1.5, 1, 1.8, 1, 0.9, 0.7, 0.8, 0.9, 0.8, 0.6, 0.6, 0.7])
            headers = ["선택", "사진", "단과대학", "학과", "품목코드", "자산코드", "품목명", "보관장소", "예산부서", "자산구분", "수량", "단가", "입고일", "입력자", "수리", "상세"]

            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            st.markdown("---")

            # 데이터 행
            for idx, row in enumerate(results):
                cols = st.columns([0.4, 0.6, 1, 1.2, 1.5, 1, 1.8, 1, 0.9, 0.7, 0.8, 0.9, 0.8, 0.6, 0.6, 0.7])

                # 선택 체크박스 (다중 선택)
                with cols[0]:
                    st.checkbox(
                        "선택",
                        key=f"select_{row['id']}",
                        label_visibility="collapsed"
                    )

                # 사진 유무 표시
                with cols[1]:
                    if row['thumbnail']:
                        try:
                            st.image(row['thumbnail'], width=40)
                            st.caption("✅ 있음")
                        except:
                            st.write("❌ 없음")
                    else:
                        st.write("❌ 없음")

                with cols[2]:
                    st.write(row['college'])

                with cols[3]:
                    st.write(row['dept_name'])

                with cols[4]:
                    st.write(row['item_code'])

                with cols[5]:
                    asset_code = row['asset_code'] if row['asset_code'] else '-'
                    st.write(asset_code)

                with cols[6]:
                    st.write(row['item_name'])

                with cols[7]:
                    location = row['location'] if row['location'] else '-'
                    st.write(location)

                with cols[8]:
                    budget_dept = row['budget_dept'] if row['budget_dept'] else '-'
                    st.write(budget_dept)

                with cols[9]:
                    badge_color = {
                        '교육용기자재': '🟪',
                        '비품': '🟦',
                        '소모품': '🟩',
                        '대여품': '🟨'
                    }
                    st.write(f"{badge_color.get(row['asset_type'], '⚪')} {row['asset_type']}")

                with cols[10]:
                    st.write(f"{row['quantity']:,}")

                with cols[11]:
                    st.write(f"{row['unit_price']:,}원")

                with cols[12]:
                    st.write(row['arrival_date'])

                with cols[13]:
                    st.write(row['registrant_name'])

                with cols[14]:
                    repair_count = row['repair_count'] or 0
                    if repair_count > 0:
                        st.write(f"🔧 {repair_count}건")
                    else:
                        st.write("-")

                with cols[15]:
                    if st.button("🔍", key=f"detail_{row['id']}", help="상세보기"):
                        st.session_state.show_detail_id = row['id']
                        st.rerun()

                if idx < len(results) - 1:
                    st.markdown("<hr style='margin: 5px 0; opacity: 0.3;'>", unsafe_allow_html=True)

            # 다중 삭제 버튼 (테이블 아래)
            st.markdown("---")

            # 체크박스 상태 수집
            selected_ids = []
            for row in results:
                checkbox_key = f"select_{row['id']}"
                if st.session_state.get(checkbox_key, False):
                    selected_ids.append(row['id'])

            # 삭제 버튼
            col1, col2, col3 = st.columns([3, 1, 1])
            with col2:
                selected_count = len(selected_ids)
                button_label = f"🗑️ 선택 삭제 ({selected_count}개)" if selected_count > 0 else "🗑️ 선택 삭제"
                if st.button(button_label, type="primary", use_container_width=True, disabled=selected_count == 0, key="bulk_delete_btn"):
                    st.session_state.selected_items_to_delete = selected_ids
                    st.session_state.show_bulk_delete_confirm = True
                    st.rerun()

            # 상세보기 다이얼로그 표시
            if 'show_detail_id' in st.session_state and st.session_state.show_detail_id:
                with st.container():
                    st.markdown("---")
                    col1, col2 = st.columns([10, 1])
                    with col2:
                        if st.button("❌ 닫기", key="close_detail"):
                            del st.session_state.show_detail_id
                            st.rerun()
                    with col1:
                        show_equipment_detail(st.session_state.show_detail_id)
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
