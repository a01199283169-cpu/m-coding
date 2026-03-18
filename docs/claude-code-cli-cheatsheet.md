# Claude Code CLI 명령어 치트시트

## 실행 옵션 (터미널)

| 명령어 | 설명 |
|--------|------|
| `claude` | 대화형 세션 시작 |
| `claude "질문"` | 초기 프롬프트와 함께 시작 |
| `claude -p "질문"` | 결과 출력 후 즉시 종료 (파이프 활용) |
| `claude -c` | 이전 대화 이어서 시작 |
| `claude -r "이름"` | 이름으로 세션 재개 |
| `claude --model sonnet` | 모델 지정 (sonnet / opus / haiku) |
| `claude --add-dir ../경로` | 작업 디렉터리 추가 |
| `cat file.txt \| claude -p "요약해줘"` | 파일 내용 파이프로 전달 |

---

## 슬래시 명령어 (`/`)

### 세션 관리

| 명령어 | 설명 |
|--------|------|
| `/clear` | 대화 기록 초기화 |
| `/compact` | 대화 압축 (컨텍스트 절약) |
| `/context` | 컨텍스트 사용량 시각화 |
| `/cost` | 토큰·비용 사용 현황 |
| `/fork` | 현재 지점에서 대화 분기 |
| `/exit` | CLI 종료 |

### 설정·모델

| 명령어 | 설명 |
|--------|------|
| `/model` | 모델 변경 |
| `/effort [low\|high\|max]` | 응답 노력 수준 설정 |
| `/config` | 테마·출력 설정 열기 |
| `/vim` | Vim 편집 모드 토글 |
| `/memory` | CLAUDE.md 메모리 편집 |
| `/permissions` | 도구 권한 확인·변경 |

### 정보·유틸

| 명령어 | 설명 |
|--------|------|
| `/help` | 도움말 보기 |
| `/status` | 버전·모델·계정 상태 |
| `/diff` | 미커밋 변경사항 diff 뷰어 |
| `/init` | 프로젝트 CLAUDE.md 초기화 |
| `/doctor` | 설치 환경 진단 |

---

## 키보드 단축키

| 단축키 | 동작 |
|--------|------|
| `Ctrl+C` | 입력·생성 취소 |
| `Ctrl+D` | CLI 종료 |
| `Ctrl+L` | 화면 지우기 |
| `Ctrl+G` | 외부 에디터로 프롬프트 편집 |
| `Ctrl+R` | 명령어 히스토리 검색 |
| `Shift+Tab` | 권한 모드 전환 (Auto/Plan/Normal) |
| `Alt+P` | 모델 선택기 열기 |
| `Alt+T` | 확장 사고 모드 토글 |
| `Esc+Esc` | 직전 상태로 되돌리기 |
| `↑ / ↓` | 이전·다음 명령 히스토리 |
| `\ + Enter` | 다음 줄 입력 (멀티라인) |

---

## 입력 접두사

| 접두사 | 동작 |
|--------|------|
| `/명령어` | 슬래시 명령 또는 스킬 실행 |
| `!bash명령` | 쉘 명령 직접 실행 |
| `@파일경로` | 파일 경로 자동완성·첨부 |

---

## 자주 쓰는 패턴

```bash
# 파일 리뷰 요청
claude -p "이 코드 리뷰해줘" < main.py

# 이전 작업 이어서
claude -c

# 특정 모델로 빠른 질문
claude --model haiku -p "파이썬 리스트 컴프리헨션 예시"

# 작업 디렉터리 추가하며 시작
claude --add-dir ../shared-lib
```

---

> **공식 문서**: [code.claude.com/docs](https://code.claude.com/docs)
> Claude Code 버전 확인: `claude --version`
