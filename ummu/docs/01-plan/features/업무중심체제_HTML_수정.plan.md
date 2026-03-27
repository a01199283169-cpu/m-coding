---
template: plan
version: 1.2
description: 업무중심체제_1페이지_요약.html 파일을 최신 조직 구조로 업데이트
variables:
  - feature: 업무중심체제_HTML_수정
  - date: 2026-03-24
  - author: Claude
  - project: ummu
  - version: 1.0
---

# 업무중심체제_HTML_수정 Planning Document

> **Summary**: 행정1팀 조직 구조 및 담당자 정보를 최신 상태로 업데이트
>
> **Project**: ummu
> **Version**: 1.0
> **Author**: Claude
> **Date**: 2026-03-24
> **Status**: Draft

---

## 1. Overview

### 1.1 Purpose

업무중심체제_1페이지_요약.html 파일의 조직 구조 정보를 최신 데이터로 업데이트하여, 행정1팀의 그룹별 업무 분장과 담당자 정보를 정확하게 반영한다.

### 1.2 Background

- 현재 HTML 파일이 구버전 조직 구조를 반영하고 있음
- 행정1팀-학사업무내용.pptx에 최신 조직 구조 정보 존재
- 그룹 A/B/C별 담당자 및 근무위치 정보 업데이트 필요

### 1.3 Related Documents

- 소스 파일: `/home/snowwon5/m-coding/ummu/업무중심체제_1페이지_요약.html`
- 참고 자료: `/mnt/c/Users/user/Desktop/cowork1/행정1팀-학사업무내용.pptx`
- 관련 문서: `업무중심체제_1페이지_요약.md`, `업무중심체제_전환계획안.md`

---

## 2. Scope

### 2.1 In Scope

- [x] **그룹별 조직 구조 업데이트**
  - 그룹 A: 경영대학, 사회과학대학
  - 그룹 B: 보건대학, 태권도·체육대학
  - 그룹 C: 공과대학, 디자인예술대학

- [x] **담당자 정보 업데이트**
  - 단과대학 담당: 홍주리(A), 고연지(B), 이스승(C)
  - 교무 담당: 김민주/임유빈/장유민/신입(A), 박규리(B), 양현진/최연희/정애린/전세린/송채영/표하늘(C)
  - 학사 담당: 백경윤(B)
  - 학생 담당: 임채현(B)
  - 교직/현장실습 담당: 모현미(A), 김지영/김주연/김다실/김태헌/권수진(전체)

- [x] **근무위치 정보 반영**
  - **현재 근무 중:**
    - 말씀관 1120: 홍주리, 김민주, 임유빈, 장유민, 신입, 백경윤, 박규리
    - 말씀관 1110: 이스승, 고연지, 양현진, 최연희, 정애린, 전세린, 송채영, 표하늘
    - 기도관 1층: 모현미
    - 행함관 5층: 김지영
  - **공실 (상주 안 함):**
    - 은혜관 1층, 5층
    - 에벤에셀 4층
    - 기도관 4층

- [x] **HTML 파일 구조 유지**
  - Marp 프레젠테이션 형식 유지
  - 기존 스타일 및 레이아웃 보존

### 2.2 Out of Scope

- 새로운 기능 추가
- HTML 디자인 변경
- 다른 파일(.md, .pptx) 수정
- 백엔드 연동

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-01 | 그룹 A/B/C 조직 구조를 HTML 테이블에 정확히 반영 | High | Pending |
| FR-02 | 각 담당자 이름을 올바른 그룹 및 업무 컬럼에 배치 | High | Pending |
| FR-03 | 근무위치 정보를 별도 섹션 또는 테이블로 표시 | Medium | Pending |
| FR-04 | 기존 HTML 파일의 Marp 형식 및 스타일 유지 | High | Pending |
| FR-05 | 한글 인코딩(UTF-8) 정상 처리 | High | Pending |

### 3.2 Non-Functional Requirements

| Category | Criteria | Measurement Method |
|----------|----------|-------------------|
| 정확성 | 담당자 정보 100% 일치 | 수동 검증 |
| 유지보수성 | HTML 구조 명확하게 유지 | 코드 리뷰 |
| 호환성 | 주요 브라우저(Chrome, Firefox, Safari) 정상 표시 | 브라우저 테스트 |

---

## 4. Success Criteria

### 4.1 Definition of Done

- [x] 모든 그룹(A/B/C) 정보가 HTML에 정확히 반영됨
- [x] 담당자 이름 및 업무 배정이 제공된 데이터와 100% 일치
- [x] 근무위치 정보가 명확히 표시됨
- [x] HTML 파일이 브라우저에서 정상적으로 렌더링됨
- [x] 기존 Marp 프레젠테이션 형식이 유지됨

### 4.2 Quality Criteria

- [x] HTML 유효성 검증 통과
- [x] 한글 깨짐 현상 없음
- [x] 테이블 레이아웃 정상 표시

---

## 5. Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| HTML 파일 크기가 너무 커서(130KB) 직접 수정 어려움 | High | High | 특정 섹션만 추출하여 수정, 또는 원본 .md 파일 수정 후 재생성 |
| Marp 형식 손상 가능성 | Medium | Medium | 수정 전 백업 생성, HTML 구조 분석 후 신중히 수정 |
| PPTX 파일 읽기 제약 | Low | High | 사용자 제공 텍스트 데이터로 우회 |
| 인코딩 문제 (한글 깨짐) | Medium | Low | UTF-8 인코딩 명시, 테스트 후 확인 |

---

## 6. Architecture Considerations

### 6.1 Project Level Selection

| Level | Characteristics | Recommended For | Selected |
|-------|-----------------|-----------------|:--------:|
| **Starter** | Simple structure (`components/`, `lib/`, `types/`) | Static sites, portfolios, landing pages | ☑ |
| **Dynamic** | Feature-based modules, BaaS integration (bkend.ai) | Web apps with backend, SaaS MVPs, fullstack apps | ☐ |
| **Enterprise** | Strict layer separation, DI, microservices | High-traffic systems, complex architectures | ☐ |

**선택 근거**: 정적 HTML 파일 수정 작업으로 Starter 레벨이 적합

### 6.2 Key Architectural Decisions

| Decision | Options | Selected | Rationale |
|----------|---------|----------|-----------|
| 수정 방식 | HTML 직접 수정 / MD 수정 후 재생성 | MD 수정 후 재생성 (권장) | 유지보수 용이, Marp 형식 보장 |
| 백업 전략 | Git commit / 파일 복사 | Git commit | 버전 관리 및 복원 용이 |
| 검증 방법 | 수동 검증 / 자동 스크립트 | 수동 검증 | 간단한 작업으로 수동이 효율적 |

### 6.3 File Structure

```
ummu/
├── 업무중심체제_1페이지_요약.md      (원본 Markdown - 이 파일 수정)
├── 업무중심체제_1페이지_요약.html    (Marp 출력 - 재생성)
├── 업무중심체제_전환계획안.md
├── 업무중심체제_전환계획안_marp.html
└── docs/
    ├── 01-plan/
    │   └── features/
    │       └── 업무중심체제_HTML_수정.plan.md  (이 문서)
    ├── 02-design/
    │   └── features/
    │       └── 업무중심체제_HTML_수정.design.md (다음 단계)
    └── .bkit-memory.json
```

---

## 7. Convention Prerequisites

### 7.1 Existing Project Conventions

- [ ] `CLAUDE.md` has coding conventions section
- [ ] `docs/01-plan/conventions.md` exists
- [ ] HTML/Markdown 코딩 스타일 가이드 없음
- [ ] Marp 설정 파일 확인 필요

### 7.2 Conventions to Define/Verify

| Category | Current State | To Define | Priority |
|----------|---------------|-----------|:--------:|
| **파일 인코딩** | UTF-8 사용 중 | UTF-8 유지 | High |
| **Marp 설정** | 확인 필요 | Marp 빌드 명령어 | High |
| **테이블 스타일** | 기존 유지 | - | Low |
| **백업 규칙** | 없음 | Git 커밋 전 확인 | Medium |

### 7.3 Environment Variables Needed

이 작업은 정적 파일 수정이므로 환경 변수 불필요.

### 7.4 Pipeline Integration

이 작업은 독립적인 문서 업데이트 작업으로 9-phase Pipeline 적용 불필요.

---

## 8. Implementation Strategy

### 8.1 추천 방식: Markdown 수정 후 재생성

1. **업무중심체제_1페이지_요약.md** 파일 확인 및 수정
2. 조직 구조 테이블 업데이트
3. Marp CLI로 HTML 재생성
4. 브라우저 검증

### 8.2 대안: HTML 직접 수정

HTML 파일이 너무 크고(130KB) 복잡하므로 권장하지 않음.

---

## 9. Next Steps

1. [x] Plan 문서 작성 완료
2. [ ] Design 문서 작성 (`/pdca design 업무중심체제_HTML_수정`)
   - HTML/Markdown 파일 구조 분석
   - 수정 대상 섹션 식별
   - 테이블 스키마 정의
3. [ ] Implementation (Do phase)
   - Markdown 파일 수정
   - Marp 재생성
   - 브라우저 테스트
4. [ ] Gap Analysis (`/pdca analyze 업무중심체제_HTML_수정`)

---

## 10. Data Reference

### 10.1 조직 구조 (그룹별)

| 그룹 | 단과대학 | 교무 | 학사 | 학생 (상담,휴복학,취창업) | 교직/현장실습/기타 |
|------|----------|------|------|---------------------------|-------------------|
| **A** | 경영대학<br>사회과학대학 | 홍주리 | 김민주 (자율전공) | 임유빈 | 신입 | 장유민 | 모현미 (교직/유아교육과 현장실습) |
| **B** | 보건대학<br>태권도·체육대학 | 고연지 | 박규리 | 백경윤 | 임채현 (태권도) | 김지영 | 현장실습/기타<br>김주연 (상담심리/사회복지) |
| **C** | 공과대학<br>디자인예술대학 | 이스승 | 양현진 | 정애린 | 전세린 (실습) | 송채영 | 김다실 (식품영양/치위생)<br>김태헌 (치기공/안경광학)<br>권수진 (임상병리/방사선) |

### 10.2 근무위치

#### 현재 근무 중

| 위치 | 담당자 |
|------|--------|
| **말씀관 1120** | 홍주리, 김민주, 임유빈, 장유민, 신입, 백경윤, 박규리 |
| **말씀관 1110** | 이스승, 고연지, 양현진, 최연희, 정애린, 전세린, 송채영, 표하늘 |
| **기도관 1층** | 모현미 |
| **행함관 5층** | 김지영 |

#### 공실 (기존 근무지, 현재 상주 안 함)

- **은혜관 1층** (기존: 임채현 - 현재 상주 안 함)
- **은혜관 5층** (기존: 임상병리, 방사선 관련 - 현재 상주 안 함)
- **에벤에셀 4층** (기존: 디자인예술 관련 - 현재 상주 안 함)
- **기도관 4층** (기존: 치기공, 안경광학 관련 - 현재 상주 안 함)

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-03-24 | Initial draft | Claude |
| 0.2 | 2026-03-24 | 근무위치 정보 수정 - 공실(은혜관1층/5층, 에벤에셀4층, 기도관4층) 명확히 구분 | Claude |
