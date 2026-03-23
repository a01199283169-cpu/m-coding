# 신한대학교 교육용 기자재 관리 시스템

## 📋 프로젝트 개요

신한대학교 6개 단과대학 37개 학과의 교육용 기자재를 체계적으로 관리하는 웹 기반 시스템입니다.

- **기술 스택**: Python 3.x, Streamlit, SQLite, bcrypt
- **개발 단계**: Phase 1 완료
- **주요 기능**: 로그인, 기자재 조회/등록/수정/삭제, 사진 관리

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
cd ~/m-coding/20260322/equipment_manager
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화 (선택)

```bash
python database.py
```

> **참고**: `streamlit run app.py` 실행 시 자동으로 DB가 초기화됩니다.

### 3. 실행

```bash
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501` 열림

## 🔐 초기 계정

### 관리자 계정
- **아이디**: admin
- **비밀번호**: admin1234
- **권한**: 전체 단과대학 조회 가능

### 단과대학 담당자 계정

| 단과대학 | 아이디 | 비밀번호 |
|---------|-------|---------|
| 공과대학 | eng_1 | eng1234 |
| 보건대학 | hlt_1 | hlt1234 |
| 디자인예술대학 | art_1 | art1234 |
| 경영대학 | biz_1 | biz1234 |
| 사회과학대학 | soc_1 | soc1234 |
| 태권도·체육대학 | spt_1 | spt1234 |

## 📁 프로젝트 구조

```
equipment_manager/
├── app.py                # 메인 실행 파일
├── database.py           # DB 초기화 및 연결
├── auth.py               # 로그인/세션 관리
├── requirements.txt      # 의존성 목록
├── README.md            # 프로젝트 문서
├── pages/
│   ├── list_view.py     # 기자재 조회 화면
│   └── register.py      # 기자재 등록·수정 폼
├── utils/
│   └── code_gen.py      # 품목코드 자동생성
├── data/
│   └── equipment.db     # SQLite 데이터베이스 (자동 생성)
└── uploads/             # 사진 파일 저장소
    └── {college_code}/
        └── {item_code}/
            └── {item_code}_photo_001.jpg
```

## 🎯 Phase 1 구현 기능

### ✅ 완료된 기능

1. **로그인/로그아웃**
   - bcrypt 암호화
   - 30분 자동 로그아웃
   - 권한별 접근 제어 (admin, college)

2. **기자재 조회**
   - 계층형 필터 (단과대학 > 학과 > 자산구분)
   - 입고일 범위 검색
   - 브레드크럼 네비게이션
   - 요약 카드 (건수/수량/금액)
   - 사진 썸네일 표시

3. **기자재 등록**
   - 품목코드 자동생성 (DH-2026-0001 형식)
   - 총액 자동계산
   - 폐기예정일 자동계산
   - 사진 업로드 (최대 5장, 10MB)
   - 필수항목 검증

4. **기자재 수정**
   - 기존 데이터 로드
   - 기존 사진 관리 (삭제 가능)
   - 추가 사진 업로드

5. **기자재 삭제**
   - 소프트 삭제 (is_deleted=1)
   - 2단계 확인 (경고 + 확인 버튼)

6. **권한 관리**
   - admin: 전체 조회/관리
   - college: 본인 소속 단과대학만 조회/관리

### 🔨 데이터베이스 스키마

#### departments (학과 마스터)
- 37개 학과 정보
- dept_code (PK), dept_name, college, college_code

#### users (사용자 계정)
- bcrypt 암호화
- username (Unique), password, college_code, role

#### equipment (기자재 메인)
- 품목코드 (Unique), 품목명, 학과, 자산구분, 수량, 단가, 총액
- 구매일, 입고일, 내용연수, 폐기예정일
- 입력자 정보, 소프트 삭제 플래그

#### equipment_photos (기자재 사진)
- equipment_id (FK), file_name, file_path
- sort_order (1번이 대표사진)

#### equipment_repairs (수리·점검 이력)
- Phase 2에서 활용 예정

## 🔮 Phase 2 예정 기능

- [ ] 기자재 상세보기 (사진 갤러리)
- [ ] 수리·점검 이력 관리
- [ ] 엑셀 다운로드
- [ ] 계정 관리 (admin 전용)
- [ ] 통계 대시보드

## 📊 품목코드 규칙

**형식**: `[학과코드(2자리)]-[연도(4자리)]-[일련번호(4자리)]`

**예시**:
- DH-2026-0001 (치위생학과 2026년 첫 번째 품목)
- EV-2026-0012 (미래자동차공학과 2026년 12번째 품목)

**규칙**:
- 같은 학과+연도 내에서 일련번호 자동 증가
- DB에서 MAX 번호 조회 후 +1
- 중복 방지 체크

## 🔒 보안 기능

- ✅ bcrypt 비밀번호 해싱
- ✅ 세션 타임아웃 (30분)
- ✅ 권한별 접근 제어
- ✅ 소프트 삭제 (데이터 복구 가능)
- ✅ 파일 업로드 검증 (확장자, 용량)
- ✅ SQL Injection 방지 (Parameterized Query)

## 🐛 알려진 이슈

- 사진 미리보기 크기가 고정되어 있음 (추후 개선 예정)
- 엑셀 다운로드 버튼 비활성화 (Phase 2 구현 예정)
- 계정 관리 기능 미구현 (Phase 2 예정)

## 📝 라이선스

신한대학교 내부 사용 목적

---

**개발**: Claude Code
**작성일**: 2026-03-23
**버전**: 1.0 (Phase 1)
