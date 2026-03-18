# 사용 예시 모음

> hwpx-bogosu 스킬 활용 시나리오별 예시

## 목차

1. [분기 보고서](#1-분기-보고서)
2. [신사업 제안](#2-신사업-제안)
3. [공식 제안서](#3-공식-제안서)
4. [기술 문서](#4-기술-문서)
5. [프로젝트 보고서](#5-프로젝트-보고서)
6. [배치 생성](#6-배치-생성)

---

## 1. 분기 보고서

### 시나리오: 영업팀 1분기 실적 보고

**자연어 요청:**
```
"2026년 1분기 영업팀 실적 보고서 만들어줘. 작성자는 홍길동이야."
```

**명령어:**
```bash
python3 hwpx_generator.py -t 2 \
    --title "2026년 1분기 실적 보고서" \
    --department "영업팀" \
    --author "홍길동 과장" \
    --overview "2026년 1분기 주요 사업 추진 현황 및 성과" \
    --approaches "목표 달성률 분석" "주요 성과" "개선 방안" \
    --notes "전년 대비 20% 성장" "신규 고객 50개사 확보" "하반기 목표 수립"
```

**결과:**
```
✅ hwpx 파일 생성 완료: output/2026년 1분기 실적 보고서_20260311.hwpx
```

---

## 2. 신사업 제안

### 시나리오 A: AI 챗봇 시스템 도입

**자연어 요청:**
```
"AI 챗봇 시스템 도입 보고서 만들어줘.
IT혁신부서, 김철수 부장이 작성.
개요는 '최신 AI 기술을 활용한 고객 서비스 혁신'이야."
```

**명령어:**
```bash
python3 hwpx_generator.py -t 2 \
    --title "AI 챗봇 시스템 도입 보고서" \
    --department "IT혁신부서" \
    --author "김철수 부장" \
    --overview "최신 AI 기술을 활용한 고객 서비스 혁신" \
    --approaches "AI 모델 선정 및 검증" "시스템 설계 및 구축" "테스트 및 배포" \
    --budget "AI모델 라이선스:10억원" "개발비:30억원" "운영비:5억원" \
    --notes "6개월 구축 예정" "고객 만족도 30% 향상 목표" "24시간 자동 응대 가능"
```

### 시나리오 B: 클라우드 전환 사업

**자연어 요청:**
```
"클라우드 전환 사업 제안서 만들어줘. 디지털혁신부, 이영희 팀장"
```

**명령어:**
```bash
python3 hwpx_generator.py -t 2 \
    --title "2027년 클라우드 전환 사업 제안" \
    --department "디지털혁신부" \
    --author "이영희 팀장" \
    --overview "온프레미스 시스템의 클라우드 마이그레이션을 통한 비용 절감 및 확장성 확보" \
    --approaches "현황 분석 및 전략 수립" "AWS 인프라 구축" "데이터 마이그레이션" \
    --budget "AWS 비용:연 5억원" "컨설팅:3억원" "마이그레이션:10억원"
```

---

## 3. 공식 제안서

### 시나리오: 정부 과제 제안서

**자연어 요청:**
```
"정부 R&D 과제 제안서 만들어줘. 연구개발부, 박영수 연구소장"
```

**명령어:**
```bash
python3 hwpx_generator.py -t 1 \
    --title "차세대 AI 반도체 개발 사업 제안서" \
    --department "연구개발부" \
    --author "박영수 연구소장" \
    --recipient "과학기술정보통신부" \
    --date "2026.03.15"
```

**특징:**
- 양식1 사용 (정식 보고서)
- 수신처 명시
- 날짜 지정

---

## 4. 기술 문서

### 시나리오: 시스템 구축 보고서

**명령어:**
```bash
python3 hwpx_generator.py -t 2 \
    --title "ERP 시스템 구축 완료 보고서" \
    --department "IT운영팀" \
    --author "최민석 차장" \
    --overview "전사 ERP 시스템 구축 완료 및 안정화 현황" \
    --approaches "시스템 구축" "데이터 이관" "사용자 교육" \
    --budget "시스템 구축:50억원" "교육:3억원" "유지보수:연 10억원" \
    --notes "2026년 1월 오픈" "3개월 안정화 완료" "전 직원 교육 이수"
```

---

## 5. 프로젝트 보고서

### 시나리오: 월간 프로젝트 진행 보고

**명령어:**
```bash
python3 hwpx_generator.py -t 2 \
    --title "3월 프로젝트 진행 현황 보고" \
    --department "PMO" \
    --author "정수민 PM" \
    --overview "진행 중인 5개 프로젝트의 3월 진행 현황 및 이슈 사항" \
    --approaches "주요 진행 사항" "이슈 및 리스크" "향후 계획" \
    --notes "프로젝트 A: 95% 완료" "프로젝트 B: 일정 지연 (2주)" "프로젝트 C: 정상 진행 중"
```

---

## 6. 배치 생성

### 시나리오: 부서별 보고서 일괄 생성

**Bash 스크립트:**
```bash
#!/bin/bash

# 부서 목록
departments=("영업팀" "마케팅팀" "개발팀" "인사팀" "재무팀")

# 각 부서별 보고서 생성
for dept in "${departments[@]}"; do
    echo "생성 중: $dept"

    python3 hwpx_generator.py -t 2 \
        --title "2026년 1분기 실적 보고서" \
        --department "$dept" \
        --author "부서장" \
        --overview "2026년 1분기 ${dept} 주요 사업 추진 현황"

    echo "완료: $dept"
    echo "---"
done

echo "전체 부서 보고서 생성 완료!"
```

**실행:**
```bash
chmod +x batch_generate.sh
./batch_generate.sh
```

---

## 7. 고급 활용

### 시나리오: 템플릿 기반 반복 생성

**Python 스크립트:**
```python
#!/usr/bin/env python3
import subprocess
import json

# 데이터 파일 (data.json)
data = [
    {
        "title": "AI 프로젝트 보고서",
        "department": "IT팀",
        "author": "김철수",
        "overview": "AI 도입 현황"
    },
    {
        "title": "클라우드 전환 보고서",
        "department": "디지털혁신부",
        "author": "이영희",
        "overview": "클라우드 전환 진행 상황"
    }
]

# 각 데이터로 문서 생성
for item in data:
    cmd = [
        "python3", "hwpx_generator.py",
        "-t", "2",
        "--title", item["title"],
        "--department", item["department"],
        "--author", item["author"],
        "--overview", item["overview"]
    ]

    subprocess.run(cmd)
    print(f"✅ {item['title']} 생성 완료")
```

---

## 8. 실무 시나리오

### 시나리오: 이사회 보고 자료

**명령어:**
```bash
python3 hwpx_generator.py -t 1 \
    --title "2026년 상반기 경영실적 보고" \
    --department "경영기획실" \
    --author "강민호 이사" \
    --recipient "이사회" \
    --date "2026.07.01"
```

### 시나리오: 주간 업무 보고

**명령어:**
```bash
python3 hwpx_generator.py -t 2 \
    --title "3월 2주차 주간 업무 보고" \
    --department "개발팀" \
    --author "박지훈 팀장" \
    --overview "금주 개발 진행 사항 및 다음 주 계획" \
    --approaches "완료 사항" "진행 사항" "예정 사항" \
    --notes "Bug fix 20건 완료" "Feature A 개발 중 (80%)" "다음 주 배포 예정"
```

---

## 9. 자주 묻는 질문 (FAQ)

### Q: 여러 명의 작성자를 넣고 싶어요
```bash
--author "홍길동, 김철수, 이영희"
```

### Q: 긴 제목을 사용하고 싶어요
```bash
--title "2026년 상반기 AI 기반 고객 관리 시스템 구축 및 운영 계획 보고서"
```

### Q: 날짜를 과거로 설정하고 싶어요
```bash
--date "2026.01.15"
```

### Q: 추진방안이 5개 이상이에요
```bash
--approaches "1단계" "2단계" "3단계" "4단계" "5단계" "6단계"
```

---

## 10. 템플릿 모음

### 템플릿 1: 최소 옵션
```bash
python3 hwpx_generator.py -t 2 --title "보고서" --department "팀" --author "작성자"
```

### 템플릿 2: 표준 보고서
```bash
python3 hwpx_generator.py -t 2 \
    --title "제목" \
    --department "부서" \
    --author "작성자" \
    --overview "개요"
```

### 템플릿 3: 상세 보고서
```bash
python3 hwpx_generator.py -t 2 \
    --title "제목" \
    --department "부서" \
    --author "작성자" \
    --overview "개요" \
    --approaches "방안1" "방안2" "방안3" \
    --budget "항목1:금액1" "항목2:금액2" \
    --notes "사항1" "사항2" "사항3"
```

### 템플릿 4: 공식 문서
```bash
python3 hwpx_generator.py -t 1 \
    --title "제목" \
    --department "부서" \
    --author "작성자" \
    --recipient "수신처" \
    --date "YYYY.MM.DD"
```

---

## 참고

- 더 많은 옵션은 [README.md](README.md) 참조
- 빠른 시작은 [QUICKSTART.md](QUICKSTART.md) 참조
- 스킬 정의는 [SKILL.md](SKILL.md) 참조
