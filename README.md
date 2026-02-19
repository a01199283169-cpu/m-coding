# 휴가등록앱 (Vacation Registration App)

> 직원 휴가 신청/조회 시스템 - FastAPI + bkend.ai BaaS + Jinja2

## 📋 Overview

직원들이 휴가(년가, 지참, 조퇴, 외출, 병가, 공가)를 신청하고, 신청 내역을 조회할 수 있는 웹 애플리케이션입니다. 캘린더 형태로 휴가 일정을 시각화하여 사용자가 직관적으로 휴가 현황을 파악할 수 있습니다.

## 🎯 Features

- ✅ 6가지 휴가 종류 지원 (년가, 지참, 조퇴, 외출, 병가, 공가)
- ✅ 휴가 CRUD (생성, 조회, 수정, 삭제)
- ✅ 캘린더 뷰 (월별 휴가 시각화)
- ✅ 휴가 목록 뷰 (테이블 형식)
- ✅ 반응형 웹 디자인 (Tailwind CSS)
- ✅ bkend.ai BaaS 인증 및 데이터 관리

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.115.0
- **Frontend**: Jinja2 Templates + Tailwind CSS
- **Database**: bkend.ai BaaS (MongoDB)
- **Authentication**: bkend.ai JWT
- **Python**: 3.11+

## 📁 Project Structure

```
휴가등록앱/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 엔트리포인트
│   ├── models.py            # Pydantic 모델
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # 로그인/회원가입
│   │   └── leaves.py        # 휴가 CRUD
│   ├── services/
│   │   ├── __init__.py
│   │   └── bkend.py         # bkend.ai API 클라이언트
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       ├── calendar.html
│       ├── list.html
│       ├── new_leave.html
│       ├── edit_leave.html
│       ├── error.html
│       └── partials/
│           ├── header.html
│           └── footer.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── calendar.js
├── docs/                    # PDCA 문서
│   ├── 01-plan/
│   ├── 02-design/
│   └── do-guide-휴가등록앱.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11 or higher
- bkend.ai account and API credentials

### 2. Installation

```bash
# Clone repository (if using git)
cd /home/snowwon5/m-coding

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your credentials
# Required:
#   - BKEND_API_KEY
#   - BKEND_PROJECT_ID
#   - BKEND_ENV_ID
#   - SECRET_KEY
```

### 4. bkend.ai Setup

Create `leaves` table in bkend.ai dashboard or via MCP:

```json
{
  "name": "leaves",
  "columns": [
    {"name": "user_id", "type": "string", "required": true},
    {"name": "leave_type", "type": "string", "required": true},
    {"name": "start_date", "type": "date", "required": true},
    {"name": "end_date", "type": "date", "required": true},
    {"name": "reason", "type": "string", "required": false}
  ]
}
```

### 5. Run Application

```bash
# Development server
python app/main.py

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000

## 📖 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | 캘린더 뷰 (메인) |
| GET | `/login` | 로그인 페이지 |
| POST | `/login` | 로그인 처리 |
| GET | `/signup` | 회원가입 페이지 |
| POST | `/signup` | 회원가입 처리 |
| GET | `/logout` | 로그아웃 |
| GET | `/leaves` | 휴가 목록 |
| GET | `/leaves/new` | 휴가 신청 폼 |
| POST | `/leaves` | 휴가 생성 |
| GET | `/leaves/{id}` | 휴가 상세/수정 |
| POST | `/leaves/{id}/edit` | 휴가 수정 |
| POST | `/leaves/{id}/delete` | 휴가 삭제 |

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/health

# Manual testing
# 1. Open browser: http://localhost:8000/login
# 2. Login (temporary auth)
# 3. Navigate to calendar/list views
# 4. Create/edit/delete leaves
```

## 📝 Development Notes

### TODO Items

- [ ] Implement actual bkend.ai authentication (currently hardcoded)
- [ ] Add session/cookie management
- [ ] Implement interactive calendar with JavaScript
- [ ] Add month navigation functionality
- [ ] Implement leave type filtering
- [ ] Add pagination for leave list
- [ ] Implement proper error handling UI
- [ ] Add loading states
- [ ] Write automated tests

### Known Issues

- Authentication is temporary (hardcoded user_id: "user123")
- Calendar month navigation not implemented
- No session management yet

## 🔧 Code Quality

```bash
# Lint with Flake8
pip install flake8
flake8 app/

# Format with Black
pip install black
black app/
```

## 📚 Documentation

- [Plan Document](docs/01-plan/features/휴가등록앱.plan.md)
- [Design Document](docs/02-design/features/휴가등록앱.design.md)
- [Implementation Guide](docs/do-guide-휴가등록앱.md)

## 🤝 Contributing

This is a personal learning project following PDCA methodology with bkit.

## 📄 License

MIT License

## 👤 Author

snowwon5

## 🙏 Acknowledgments

- FastAPI framework
- bkend.ai BaaS platform
- Tailwind CSS
- bkit Development Kit

---

**Version**: 0.1.0
**Last Updated**: 2026-02-12
