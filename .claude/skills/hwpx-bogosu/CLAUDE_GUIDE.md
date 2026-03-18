# hwpx-bogosu 스킬 등록 가이드

## CLAUDE.md에 추가할 내용

아래 내용을 복사해서 `CLAUDE.md` 파일에 붙여넣으세요.

---

### hwpx-bogosu: 한글 문서 자동 생성기

**위치**: `.claude/skills/hwpx-bogosu/`

**기능**: 한글(hwpx) 보고서를 자동으로 생성합니다.

**트리거**: "hwpx", "한글 문서", "보고서 생성"

**사용법**:
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t [1|2] --title "제목" --department "부서" --author "작성자"
```

**양식 선택**:
- `1`: 정식 보고서 (공식 문서, 제안서) - 10+ 페이지
- `2`: 요약 보고서 (신사업, 내부 보고서) - 1-2 페이지

**양식2 추가 옵션**:
```bash
--overview "개요/목적"
--approaches "방안1" "방안2" "방안3"
--budget "항목:금액" "항목:금액"
--notes "사항1" "사항2" "사항3"
```

**예시 1: 신사업 보고서**
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 2 \
    --title "AI 챗봇 시스템 도입 보고서" \
    --department "IT혁신부서" \
    --author "김철수 부장" \
    --overview "최신 AI 기술을 활용한 고객 서비스 혁신" \
    --approaches "AI 모델 선정" "시스템 구축" "테스트" \
    --budget "AI모델:10억" "개발:30억"
```

**예시 2: 정식 제안서**
```bash
cd .claude/skills/hwpx-bogosu
python3 hwpx_generator.py -t 1 \
    --title "2027년 클라우드 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희 팀장"
```

**출력**: `.claude/skills/hwpx-bogosu/output/{제목}_{날짜}.hwpx`

**Windows 경로**: `\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\.claude\skills\hwpx-bogosu\output\`

**문서**:
- 사용 설명서: `README.md`
- 기술 문서: `hwpx-bogosu.skill.md`
- 예시 스크립트: `examples.sh`

---

## 사용 방법 (Claude에게 요청)

사용자가 다음과 같이 요청하면:

```
"2026년 1분기 실적 보고서를 hwpx로 만들어줘.
부서는 영업팀이고 작성자는 홍길동이야."
```

Claude는:
1. 위 가이드를 참고
2. 적절한 명령어 구성
3. 스크립트 실행
4. 생성된 파일 경로 제공

---

## 주의사항

- 한컴오피스 2014 이상에서 열 수 있음
- 특수문자 포함 시 따옴표로 감싸기
- 양식1: 공식/상세 문서용
- 양식2: 간략/빠른 보고서용
