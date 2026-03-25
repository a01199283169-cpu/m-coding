import sqlite3

conn = sqlite3.connect('data/equipment.db')
cursor = conn.cursor()

# 수리 이력 건수
cursor.execute('SELECT COUNT(*) FROM equipment_repairs')
repair_count = cursor.fetchone()[0]
print(f'수리 이력 건수: {repair_count}')

# 수리 이력 샘플
if repair_count > 0:
    cursor.execute('''
        SELECT r.id, r.equipment_id, e.item_name, r.repair_type, r.repair_date
        FROM equipment_repairs r
        JOIN equipment e ON r.equipment_id = e.id
        LIMIT 5
    ''')
    print('\n수리 이력 샘플:')
    for row in cursor.fetchall():
        print(f'  이력ID: {row[0]}, 기자재ID: {row[1]}, 품명: {row[2]}, 유형: {row[3]}, 일자: {row[4]}')

# 기자재 건수
cursor.execute('SELECT COUNT(*) FROM equipment WHERE is_deleted = 0')
equipment_count = cursor.fetchone()[0]
print(f'\n기자재 건수: {equipment_count}')

conn.close()
