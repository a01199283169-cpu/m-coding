"""Authentication routes"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """로그인 페이지"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """로그인 처리

    TODO: bkend.ai 인증 구현
    - bkend.ai API로 로그인 검증
    - JWT 토큰 발급
    - 세션/쿠키에 저장
    """
    # Temporary implementation
    # TODO: Replace with actual bkend.ai authentication
    if username and password:
        # Success - redirect to main page
        return RedirectResponse(url="/", status_code=303)
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """회원가입 페이지"""
    return templates.TemplateResponse(
        "signup.html",
        {"request": request}
    )


@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """회원가입 처리

    TODO: bkend.ai 회원가입 구현
    - bkend.ai API로 사용자 생성
    - 자동 로그인 또는 로그인 페이지로 리다이렉트
    """
    # Temporary implementation
    # TODO: Replace with actual bkend.ai user creation
    if username and email and password:
        # Success - redirect to login
        return RedirectResponse(url="/login", status_code=303)
    else:
        raise HTTPException(status_code=400, detail="Invalid signup data")


@router.get("/logout")
async def logout(request: Request):
    """로그아웃

    TODO: 세션/토큰 삭제
    """
    return RedirectResponse(url="/login", status_code=303)
