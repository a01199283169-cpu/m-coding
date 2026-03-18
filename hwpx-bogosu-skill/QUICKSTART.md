# 빠른 시작 가이드

> 5분 안에 hwpx-bogosu 스킬 사용하기

## 1단계: 스킬 등록 (1분)

### Claude Code에 스킬 추가

```bash
# 방법 1: 프로젝트 스킬로 등록
cp -r hwpx-bogosu-skill /path/to/your/project/.claude/skills/

# 방법 2: 사용자 스킬로 등록
cp -r hwpx-bogosu-skill ~/.claude/skills/
```

### CLAUDE.md에 추가 (선택사항)

```markdown
## Custom Skills

### hwpx-bogosu
한글(hwpx) 보고서 자동 생성

**트리거**: hwpx, 한글 문서, 보고서 생성
**위치**: `.claude/skills/hwpx-bogosu-skill/`
```

## 2단계: 첫 문서 만들기 (2분)

### 방법 1: 자연어 요청 (추천)

Claude에게 말하기:
```
"2026년 1분기 실적 보고서를 만들어줘.
영업팀이고 작성자는 홍길동이야."
```

Claude가 자동으로:
1. 양식 선택 (양식2)
2. 명령어 구성
3. 파일 생성
4. 경로 알려줌

### 방법 2: 직접 명령어 실행

```bash
cd hwpx-bogosu-skill

python3 hwpx_generator.py -t 2 \
    --title "2026년 1분기 실적 보고서" \
    --department "영업팀" \
    --author "홍길동"
```

**출력:**
```
✅ hwpx 파일 생성 완료: output/2026년 1분기 실적 보고서_20260311.hwpx
```

## 3단계: 파일 확인 (1분)

### Linux/WSL
```bash
ls -lh output/
```

### Windows
```
탐색기 → \\wsl.localhost\Ubuntu-24.04\home\사용자명\hwpx-bogosu-skill\output\
```

### 파일 열기
- 한컴오피스 2014 이상에서 열기
- 더블클릭 또는 "열기" 메뉴 사용

## 4단계: 다양한 양식 시도 (1분)

### 요약 보고서 (양식2)
```bash
python3 hwpx_generator.py -t 2 \
    --title "신사업 제안" \
    --department "기획팀" \
    --author "김철수" \
    --overview "AI 기반 고객 관리 시스템 도입" \
    --approaches "분석" "설계" "구현" \
    --budget "개발:5억" "운영:2억"
```

### 정식 제안서 (양식1)
```bash
python3 hwpx_generator.py -t 1 \
    --title "클라우드 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희"
```

## 자주 사용하는 3가지 패턴

### 패턴 1: 분기 보고서
```bash
python3 hwpx_generator.py -t 2 \
    --title "2026년 1분기 실적 보고서" \
    --department "영업팀" \
    --author "홍길동" \
    --overview "2026년 1분기 주요 사업 추진 현황 및 성과"
```

### 패턴 2: 신사업 제안
```bash
python3 hwpx_generator.py -t 2 \
    --title "AI 프로젝트 제안" \
    --department "IT팀" \
    --author "김철수" \
    --overview "생성형 AI를 활용한 업무 자동화" \
    --approaches "요구사항 분석" "AI 모델 선정" "시스템 구축" \
    --budget "AI모델:10억" "개발:30억" "운영:5억"
```

### 패턴 3: 공식 제안서
```bash
python3 hwpx_generator.py -t 1 \
    --title "2027년 디지털 전환 사업 제안서" \
    --department "디지털혁신부" \
    --author "이영희 팀장" \
    --recipient "경영진"
```

## 팁

### 💡 Tip 1: 따옴표 사용
특수문자가 있으면 따옴표로 감싸기
```bash
--title "2026년 \"특별\" 프로젝트"
```

### 💡 Tip 2: 줄바꿈
긴 명령어는 백슬래시(`\`)로 줄바꿈
```bash
python3 hwpx_generator.py \
    -t 2 \
    --title "제목" \
    --department "부서"
```

### 💡 Tip 3: 자동화
자주 사용하는 명령어는 alias 설정
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias hwpx-report='cd ~/hwpx-bogosu-skill && python3 hwpx_generator.py -t 2'

# 사용
hwpx-report --title "보고서" --department "영업팀" --author "홍길동"
```

## 문제 해결

### ❌ "템플릿 파일을 찾을 수 없습니다"
```bash
# assets/ 폴더에 템플릿 파일이 있는지 확인
ls -la assets/
```

### ❌ "파일이 열리지 않아요"
- 한컴오피스 2014 이상인지 확인
- 파일 크기가 0이 아닌지 확인
- 다른 hwpx 파일이 열리는지 테스트

### ❌ "Python을 찾을 수 없습니다"
```bash
# Python 3 설치 확인
python3 --version

# 없으면 설치 (Ubuntu/Debian)
sudo apt install python3
```

## 다음 단계

- 📖 [README.md](README.md) - 전체 문서 읽기
- 📝 [EXAMPLES.md](EXAMPLES.md) - 더 많은 예시 보기
- 🎓 [SKILL.md](SKILL.md) - 스킬 정의 이해하기

## 5분 체크리스트

- [ ] 스킬 등록 완료
- [ ] 첫 문서 생성 성공
- [ ] 한컴오피스에서 열기 성공
- [ ] 자연어 요청 시도
- [ ] 다양한 양식 테스트

축하합니다! 🎉 이제 hwpx-bogosu 스킬을 사용할 준비가 되었습니다.
