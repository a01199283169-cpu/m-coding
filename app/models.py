"""Data models for 휴가등록앱"""
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
