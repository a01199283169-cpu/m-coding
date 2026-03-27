# 휴가등록앱 Implementation Guide (Do Phase)

> **Summary**: FastAPI + bkend.ai BaaS 기반 휴가 관리 시스템 구현 가이드
>
> **Project**: 휴가등록앱
> **Version**: 0.1.0
> **Author**: snowwon5
> **Date**: 2026-02-12
> **Status**: In Progress
> **Design Doc**: [휴가등록앱.design.md](02-design/features/휴가등록앱.design.md)

---

## 1. Pre-Implementation Checklist

### 1.1 Documents Verified

- [x] Plan document reviewed: `docs/01-plan/features/휴가등록앱.plan.md`
- [x] Design document reviewed: `docs/02-design/features/휴가등록앱.design.md`
- [ ] bkend.ai account created and MCP configured

### 1.2 Environment Setup

```bash
# 1. Python 가상환경 생성 (Python 3.11+ 권장)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 2. Git 초기화 (이미 완료)
git status

# 3. 프로젝트 구조 생성
mkdir -p app/{routes,services,templates/partials}
mkdir -p static/{css,js}
touch app/__init__.py app/routes/__init__.py app/services/__init__.py
```

### 1.3 Environment Variables

Create `.env` file at project root:

```env
# bkend.ai Configuration
BKEND_API_KEY=bkapi_your_api_key_here
BKEND_PROJECT_ID=proj_your_project_id
BKEND_ENV_ID=env_production

# FastAPI Configuration
SECRET_KEY=your-secret-key-generate-random
DEBUG=True

# Application
APP_NAME=휴가등록앱
APP_VERSION=0.1.0
```

---

## 2. Implementation Order

### Phase 1: Project Setup (30분)

| Priority | Task | Command/File | Status |
|:--------:|------|--------------|:------:|
| 1 | Create requirements.txt | `requirements.txt` | ☐ |
| 2 | Install dependencies | `pip install -r requirements.txt` | ☐ |
| 3 | Create .env file | `.env` | ☐ |
| 4 | Create .gitignore | `.gitignore` | ☐ |

**requirements.txt**:
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
jinja2==3.1.4
python-dotenv==1.0.1
httpx==0.27.2
pydantic==2.9.0
python-multipart==0.0.12
```

### Phase 2: Data Models (45분)

| Priority | Task | File/Location | Status |
|:--------:|------|---------------|:------:|
| 3 | Define LeaveType enum | `app/models.py` | ☐ |
| 4 | Create Leave model | `app/models.py` | ☐ |
| 5 | Create request/response models | `app/models.py` | ☐ |

**Key Models to Implement**:
- `LeaveType(str, Enum)` - 년가, 지참, 조퇴, 외출, 병가, 공가
- `Leave(BaseModel)` - Main entity
- `LeaveCreateRequest(BaseModel)` - POST request
- `LeaveUpdateRequest(BaseModel)` - PUT request

### Phase 3: bkend.ai Integration (1시간)

| Priority | Task | File/Location | Status |
|:--------:|------|---------------|:------:|
| 6 | Set up bkend.ai project | bkend.ai dashboard | ☐ |
| 7 | Create `leaves` table | MCP or API | ☐ |
| 8 | Implement BkendService | `app/services/bkend.py` | ☐ |
| 9 | Test API connection | Manual test | ☐ |

**bkend.ai Table Schema (leaves)**:
```json
{
  "name": "leaves",
  "columns": [
    {"name": "user_id", "type": "string", "required": true},
    {"name": "leave_type", "type": "string", "required": true},
    {"name": "start_date", "type": "date", "required": true},
    {"name": "end_date", "type": "date", "required": true},
    {"name": "reason", "type": "string", "required": false}
  ],
  "indexes": [
    {"fields": ["user_id"]},
    {"fields": ["start_date", "end_date"]}
  ]
}
```

### Phase 4: API Routes (2시간)

| Priority | Task | File/Location | Status |
|:--------:|------|---------------|:------:|
| 10 | Implement auth routes | `app/routes/auth.py` | ☐ |
| 11 | Implement leaves CRUD | `app/routes/leaves.py` | ☐ |
| 12 | Create FastAPI app | `app/main.py` | ☐ |
| 13 | Test API endpoints | Postman/curl | ☐ |

**Routes to Implement**:
```python
# auth.py
GET  /login       - 로그인 페이지
POST /login       - 로그인 처리
GET  /signup      - 회원가입 페이지
POST /signup      - 회원가입 처리
GET  /logout      - 로그아웃

# leaves.py
GET  /             - 메인 (캘린더 뷰)
GET  /leaves       - 휴가 목록
GET  /leaves/new   - 휴가 신청 폼
POST /leaves       - 휴가 생성
GET  /leaves/{id}  - 휴가 상세
POST /leaves/{id}/edit   - 휴가 수정
POST /leaves/{id}/delete - 휴가 삭제
```

### Phase 5: HTML Templates (2시간)

| Priority | Task | File/Location | Status |
|:--------:|------|---------------|:------:|
| 14 | Create base template | `app/templates/base.html` | ☐ |
| 15 | Create auth templates | `login.html`, `signup.html` | ☐ |
| 16 | Create leave templates | `calendar.html`, `list.html`, `new_leave.html` | ☐ |
| 17 | Create partial templates | `partials/header.html`, `footer.html` | ☐ |

**Template Structure**:
```
app/templates/
├── base.html           # Tailwind CDN, 공통 레이아웃
├── login.html          # 로그인 폼
├── signup.html         # 회원가입 폼
├── calendar.html       # 캘린더 뷰 (메인)
├── list.html           # 휴가 목록 (테이블)
├── new_leave.html      # 휴가 신청 폼
├── edit_leave.html     # 휴가 수정 폼
└── partials/
    ├── header.html     # 헤더 (네비게이션)
    ├── footer.html     # 푸터
    ├── leave_card.html # 휴가 카드 컴포넌트
    └── calendar_day.html # 캘린더 날짜 셀
```

### Phase 6: Static Assets (1시간)

| Priority | Task | File/Location | Status |
|:--------:|------|---------------|:------:|
| 18 | Add Tailwind CSS | `static/css/style.css` or CDN | ☐ |
| 19 | Implement calendar.js | `static/js/calendar.js` | ☐ |
| 20 | Add form validation | `static/js/validation.js` | ☐ |

### Phase 7: Testing & Refinement (1시간)

| Priority | Task | Description | Status |
|:--------:|------|-------------|:------:|
| 21 | Manual E2E test | 로그인 → 신청 → 확인 | ☐ |
| 22 | Error handling test | 401, 403, 404 케이스 | ☐ |
| 23 | Code quality check | Flake8 린트 | ☐ |
| 24 | Format code | Black 포맷팅 | ☐ |

---

## 3. Key Files to Create

### 3.1 Core Application Files

| File Path | Purpose | Priority |
|-----------|---------|:--------:|
| `app/main.py` | FastAPI 엔트리포인트, 라우터 등록 | High |
| `app/models.py` | Pydantic 모델 (Leave, LeaveType) | High |
| `app/services/bkend.py` | bkend.ai API 클라이언트 | High |
| `app/routes/auth.py` | 로그인/회원가입 라우트 | High |
| `app/routes/leaves.py` | 휴가 CRUD 라우트 | High |

### 3.2 Configuration Files

| File Path | Purpose | Priority |
|-----------|---------|:--------:|
| `requirements.txt` | Python 의존성 목록 | High |
| `.env` | 환경 변수 (BKEND_API_KEY 등) | High |
| `.gitignore` | Git 제외 파일 | High |
| `.flake8` | 린트 설정 (선택) | Low |
| `pyproject.toml` | Black 설정 (선택) | Low |

---

## 4. Implementation Code Snippets

### 4.1 `app/main.py` (FastAPI 엔트리포인트)

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "휴가등록앱"),
    version=os.getenv("APP_VERSION", "0.1.0"),
    debug=os.getenv("DEBUG", "False") == "True"
)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Import and register routers
from app.routes import auth, leaves

app.include_router(auth.router)
app.include_router(leaves.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": os.getenv("APP_NAME")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### 4.2 `app/models.py` (Data Models)

```python
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class LeaveType(str, Enum):
    """휴가 종류"""
    ANNUAL = "년가"       # Annual Leave
    HALF_DAY = "지참"     # Half-day Leave
    EARLY_LEAVE = "조퇴"  # Early Leave
    OUTING = "외출"       # Outing
    SICK = "병가"         # Sick Leave
    PUBLIC = "공가"       # Public/Official Leave

class Leave(BaseModel):
    """휴가 엔티티"""
    id: str | None = None
    user_id: str
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str | None = Field(max_length=500, default=None)
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "leave_type": "년가",
                "start_date": "2026-02-15",
                "end_date": "2026-02-17",
                "reason": "가족 여행"
            }
        }

class LeaveCreateRequest(BaseModel):
    """휴가 신청 요청"""
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str | None = Field(max_length=500, default=None)

    def validate_dates(self):
        """날짜 검증"""
        if self.start_date > self.end_date:
            raise ValueError("시작일은 종료일보다 이전이어야 합니다")

class LeaveUpdateRequest(BaseModel):
    """휴가 수정 요청"""
    leave_type: LeaveType | None = None
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = Field(max_length=500, default=None)
```

### 4.3 `app/services/bkend.py` (bkend.ai Service)

```python
import httpx
import os
from typing import List, Optional
from app.models import Leave, LeaveCreateRequest

class BkendService:
    """bkend.ai BaaS API 클라이언트"""

    def __init__(self):
        self.api_key = os.getenv("BKEND_API_KEY")
        self.project_id = os.getenv("BKEND_PROJECT_ID")
        self.env_id = os.getenv("BKEND_ENV_ID")
        self.base_url = f"https://api.bkend.ai/v1/{self.project_id}/environments/{self.env_id}"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def create_leave(self, leave_data: LeaveCreateRequest, user_id: str) -> Leave:
        """휴가 생성"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tables/leaves/rows",
                json={
                    "user_id": user_id,
                    "leave_type": leave_data.leave_type.value,
                    "start_date": str(leave_data.start_date),
                    "end_date": str(leave_data.end_date),
                    "reason": leave_data.reason
                },
                headers=self.headers
            )
            response.raise_for_status()
            return Leave(**response.json())

    async def get_user_leaves(self, user_id: str, month: Optional[str] = None) -> List[Leave]:
        """사용자 휴가 목록 조회"""
        params = {"filter": f"user_id={user_id}"}
        if month:
            # TODO: Add month filter
            pass

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tables/leaves/rows",
                params=params,
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return [Leave(**item) for item in data.get("items", [])]

    async def get_leave(self, leave_id: str, user_id: str) -> Leave:
        """휴가 상세 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tables/leaves/rows/{leave_id}",
                headers=self.headers
            )
            response.raise_for_status()
            leave = Leave(**response.json())

            # RLS 검증 (본인 데이터만)
            if leave.user_id != user_id:
                raise PermissionError("권한이 없습니다")

            return leave

    async def update_leave(self, leave_id: str, leave_data: dict, user_id: str) -> Leave:
        """휴가 수정"""
        # RLS 검증
        await self.get_leave(leave_id, user_id)

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/tables/leaves/rows/{leave_id}",
                json=leave_data,
                headers=self.headers
            )
            response.raise_for_status()
            return Leave(**response.json())

    async def delete_leave(self, leave_id: str, user_id: str):
        """휴가 삭제"""
        # RLS 검증
        await self.get_leave(leave_id, user_id)

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/tables/leaves/rows/{leave_id}",
                headers=self.headers
            )
            response.raise_for_status()

# Singleton instance
bkend_service = BkendService()
```

### 4.4 `app/routes/leaves.py` (Leaves Routes)

```python
from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.bkend import bkend_service
from app.models import LeaveCreateRequest, LeaveType
from datetime import date

router = APIRouter(tags=["leaves"])
templates = Jinja2Templates(directory="app/templates")

# TODO: Implement session/auth middleware
def get_current_user_id(request: Request) -> str:
    """현재 로그인한 사용자 ID 반환 (임시 구현)"""
    # TODO: 세션에서 user_id 가져오기
    return "user123"  # Temporary hardcoded

@router.get("/", response_class=HTMLResponse)
async def calendar_view(request: Request):
    """캘린더 뷰 (메인 페이지)"""
    user_id = get_current_user_id(request)
    leaves = await bkend_service.get_user_leaves(user_id)

    return templates.TemplateResponse(
        "calendar.html",
        {"request": request, "leaves": leaves}
    )

@router.get("/leaves", response_class=HTMLResponse)
async def list_leaves(request: Request):
    """휴가 목록"""
    user_id = get_current_user_id(request)
    leaves = await bkend_service.get_user_leaves(user_id)

    return templates.TemplateResponse(
        "list.html",
        {"request": request, "leaves": leaves}
    )

@router.get("/leaves/new", response_class=HTMLResponse)
async def new_leave_form(request: Request):
    """휴가 신청 폼"""
    return templates.TemplateResponse(
        "new_leave.html",
        {"request": request, "leave_types": LeaveType}
    )

@router.post("/leaves")
async def create_leave(
    request: Request,
    leave_type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    reason: str = Form(None)
):
    """휴가 생성"""
    user_id = get_current_user_id(request)

    try:
        leave_data = LeaveCreateRequest(
            leave_type=LeaveType(leave_type),
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        leave_data.validate_dates()

        await bkend_service.create_leave(leave_data, user_id)
        return RedirectResponse(url="/leaves", status_code=303)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/leaves/{leave_id}", response_class=HTMLResponse)
async def leave_detail(request: Request, leave_id: str):
    """휴가 상세"""
    user_id = get_current_user_id(request)

    try:
        leave = await bkend_service.get_leave(leave_id, user_id)
        return templates.TemplateResponse(
            "edit_leave.html",
            {"request": request, "leave": leave, "leave_types": LeaveType}
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="권한이 없습니다")

@router.post("/leaves/{leave_id}/delete")
async def delete_leave(leave_id: str, request: Request):
    """휴가 삭제"""
    user_id = get_current_user_id(request)

    try:
        await bkend_service.delete_leave(leave_id, user_id)
        return RedirectResponse(url="/leaves", status_code=303)
    except PermissionError:
        raise HTTPException(status_code=403, detail="권한이 없습니다")
```

### 4.5 `app/templates/base.html` (Base Template)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}휴가등록앱{% endblock %}</title>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Custom CSS -->
    <link rel="stylesheet" href="/static/css/style.css">

    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50">
    <!-- Header -->
    {% include "partials/header.html" %}

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    {% include "partials/footer.html" %}

    <!-- Scripts -->
    <script src="/static/js/calendar.js"></script>
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

---

## 5. Coding Conventions (PEP8 + FastAPI)

### 5.1 Naming Conventions

| Target | Rule | Example |
|--------|------|---------|
| Functions | snake_case | `get_user_leaves()`, `create_leave()` |
| Classes | PascalCase | `Leave`, `LeaveType`, `BkendService` |
| Constants | UPPER_SNAKE_CASE | `MAX_REASON_LENGTH`, `API_BASE_URL` |
| Variables | snake_case | `user_id`, `start_date`, `leave_data` |
| Files | snake_case.py | `leaves.py`, `bkend.py` |
| Templates | snake_case.html | `new_leave.html`, `calendar.html` |

### 5.2 Import Order

```python
# 1. 표준 라이브러리
from datetime import date, datetime
from enum import Enum
import os

# 2. 서드파티 라이브러리
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import httpx

# 3. 로컬 모듈
from app.services.bkend import BkendService
from app.models import Leave, LeaveType
```

### 5.3 Docstring Convention

```python
def get_user_leaves(user_id: str, month: str | None = None) -> list[Leave]:
    """사용자의 휴가 목록을 조회합니다.

    Args:
        user_id: 사용자 ID
        month: 조회할 월 (YYYY-MM 형식, 선택)

    Returns:
        휴가 객체 리스트

    Raises:
        HTTPException: API 호출 실패 시
    """
    # 구현...
```

---

## 6. Testing Checklist

### 6.1 Manual API Testing

```bash
# 서버 실행
python app/main.py

# Health check
curl http://localhost:8000/health

# 휴가 목록 조회 (브라우저)
open http://localhost:8000/leaves

# 휴가 신청 폼
open http://localhost:8000/leaves/new
```

### 6.2 Test Scenarios

- [ ] **Happy Path**
  - [ ] 로그인 → 캘린더 뷰 접근
  - [ ] 휴가 신청 폼 작성 → 생성 성공
  - [ ] 휴가 목록에서 신청한 휴가 확인
  - [ ] 휴가 수정 → 변경사항 반영
  - [ ] 휴가 삭제 → 목록에서 제거

- [ ] **Error Cases**
  - [ ] start_date > end_date → 에러 메시지 표시
  - [ ] 타인의 휴가 수정 시도 → 403 Forbidden
  - [ ] 존재하지 않는 휴가 조회 → 404 Not Found

### 6.3 Code Quality

```bash
# Flake8 린트 검사
pip install flake8
flake8 app/

# Black 포맷팅
pip install black
black app/
```

---

## 7. Troubleshooting

### 7.1 Common Issues

| Issue | Solution |
|-------|----------|
| bkend.ai API 401 Unauthorized | `.env` 파일의 `BKEND_API_KEY` 확인 |
| 템플릿을 찾을 수 없음 | `templates` 폴더 경로 확인 (`app/templates/`) |
| CORS 에러 | FastAPI에 CORSMiddleware 추가 (필요시) |
| 날짜 형식 오류 | ISO 8601 형식 사용 (YYYY-MM-DD) |

---

## 8. Post-Implementation Checklist

### 8.1 Self-Review

- [ ] 모든 CRUD 기능 작동
- [ ] 에러 처리 완료 (try-except, HTTPException)
- [ ] PEP8 코딩 컨벤션 준수
- [ ] 환경 변수 하드코딩 없음
- [ ] 타입 힌트 추가 (Python 3.10+ 스타일)

### 8.2 Ready for Gap Analysis

구현이 완료되면:

```bash
# Gap Analysis 실행
/pdca analyze 휴가등록앱
```

이 명령은 Design 문서와 실제 구현 코드를 비교하여 Match Rate를 계산합니다.

---

## 9. Next Steps After Implementation

1. **Gap Analysis** (`/pdca analyze 휴가등록앱`)
   - Design vs Implementation 비교
   - Match Rate 계산 (목표: ≥ 90%)

2. **Iteration (필요시)** (`/pdca iterate 휴가등록앱`)
   - Match Rate < 90% 시 자동 개선
   - 최대 5회 반복

3. **Completion Report** (`/pdca report 휴가등록앱`)
   - Match Rate ≥ 90% 달성 후
   - 전체 PDCA 사이클 보고서 생성

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-02-12 | Initial implementation guide | snowwon5 |
