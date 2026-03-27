"""bkend.ai BaaS API 클라이언트"""
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

        if not all([self.api_key, self.project_id, self.env_id]):
            raise ValueError(
                "Missing bkend.ai credentials. Please check .env file for "
                "BKEND_API_KEY, BKEND_PROJECT_ID, BKEND_ENV_ID"
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def create_leave(self, leave_data: LeaveCreateRequest, user_id: str) -> Leave:
        """휴가 생성

        Args:
            leave_data: 휴가 신청 데이터
            user_id: 사용자 ID

        Returns:
            생성된 휴가 객체
        """
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

    async def get_user_leaves(
        self,
        user_id: str,
        month: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Leave]:
        """사용자 휴가 목록 조회

        Args:
            user_id: 사용자 ID
            month: 조회할 월 (YYYY-MM 형식, 선택)
            limit: 결과 개수 제한
            offset: 페이지네이션 오프셋

        Returns:
            휴가 객체 리스트
        """
        params = {
            "filter": f"user_id={user_id}",
            "limit": limit,
            "offset": offset
        }

        if month:
            # TODO: Add month filter implementation
            # params["filter"] += f" AND start_date >= {month}-01"
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
        """휴가 상세 조회

        Args:
            leave_id: 휴가 ID
            user_id: 사용자 ID (권한 검증용)

        Returns:
            휴가 객체

        Raises:
            PermissionError: 본인 데이터가 아닌 경우
        """
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

    async def update_leave(
        self,
        leave_id: str,
        leave_data: dict,
        user_id: str
    ) -> Leave:
        """휴가 수정

        Args:
            leave_id: 휴가 ID
            leave_data: 수정할 데이터
            user_id: 사용자 ID (권한 검증용)

        Returns:
            수정된 휴가 객체
        """
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
        """휴가 삭제

        Args:
            leave_id: 휴가 ID
            user_id: 사용자 ID (권한 검증용)
        """
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
