"""Leave management routes"""
from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.bkend import bkend_service
from app.models import LeaveCreateRequest, LeaveType
from datetime import date

router = APIRouter(tags=["leaves"])
templates = Jinja2Templates(directory="app/templates")


def get_current_user_id(request: Request) -> str:
    """현재 로그인한 사용자 ID 반환

    TODO: 실제 세션/토큰에서 user_id 가져오기
    현재는 임시로 하드코딩된 값 반환
    """
    # TODO: Implement actual session/token validation
    # session_token = request.cookies.get("session_token")
    # user_id = validate_token(session_token)
    # return user_id
    return "user123"  # Temporary hardcoded value


@router.get("/", response_class=HTMLResponse)
async def calendar_view(request: Request):
    """캘린더 뷰 (메인 페이지)"""
    try:
        user_id = get_current_user_id(request)
        leaves = await bkend_service.get_user_leaves(user_id)

        return templates.TemplateResponse(
            "calendar.html",
            {"request": request, "leaves": leaves}
        )
    except Exception as e:
        # TODO: Better error handling
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )


@router.get("/leaves", response_class=HTMLResponse)
async def list_leaves(request: Request):
    """휴가 목록"""
    try:
        user_id = get_current_user_id(request)
        leaves = await bkend_service.get_user_leaves(user_id)

        return templates.TemplateResponse(
            "list.html",
            {"request": request, "leaves": leaves}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.get("/leaves/{leave_id}", response_class=HTMLResponse)
async def leave_detail(request: Request, leave_id: str):
    """휴가 상세/수정 폼"""
    user_id = get_current_user_id(request)

    try:
        leave = await bkend_service.get_leave(leave_id, user_id)
        return templates.TemplateResponse(
            "edit_leave.html",
            {"request": request, "leave": leave, "leave_types": LeaveType}
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    except Exception as e:
        raise HTTPException(status_code=404, detail="휴가를 찾을 수 없습니다")


@router.post("/leaves/{leave_id}/edit")
async def edit_leave(
    request: Request,
    leave_id: str,
    leave_type: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    reason: str = Form(None)
):
    """휴가 수정"""
    user_id = get_current_user_id(request)

    try:
        # 날짜 검증
        if start_date > end_date:
            raise ValueError("시작일은 종료일보다 이전이어야 합니다")

        update_data = {
            "leave_type": leave_type,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "reason": reason
        }

        await bkend_service.update_leave(leave_id, update_data, user_id)
        return RedirectResponse(url="/leaves", status_code=303)

    except PermissionError:
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@router.post("/leaves/{leave_id}/delete")
async def delete_leave(leave_id: str, request: Request):
    """휴가 삭제"""
    user_id = get_current_user_id(request)

    try:
        await bkend_service.delete_leave(leave_id, user_id)
        return RedirectResponse(url="/leaves", status_code=303)
    except PermissionError:
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    except Exception as e:
        raise HTTPException(status_code=404, detail="휴가를 찾을 수 없습니다")
