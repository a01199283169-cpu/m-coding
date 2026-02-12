'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import {
  LeaveRequest,
  LEAVE_TYPE_LABELS,
  LEAVE_STATUS_LABELS,
  LEAVE_STATUS_COLORS,
} from '@/lib/types';

interface AdminRequestCardProps {
  request: LeaveRequest;
  onUpdate: () => void;
}

export default function AdminRequestCard({ request, onUpdate }: AdminRequestCardProps) {
  const [loading, setLoading] = useState(false);
  const supabase = createClient();

  const handleAction = async (status: 'approved' | 'rejected') => {
    if (!confirm(`이 휴가 신청을 ${status === 'approved' ? '승인' : '거절'}하시겠습니까?`)) return;

    setLoading(true);
    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      const { error } = await supabase
        .from('leave_requests')
        .update({
          status,
          reviewed_by: user?.id,
          reviewed_at: new Date().toISOString(),
        })
        .eq('id', request.id);

      if (error) throw error;

      // If approved and it's annual leave, decrease the user's balance
      if (status === 'approved' && request.leave_type === 'annual') {
        const days = calculateDays(request.start_date, request.end_date);
        const { error: updateError } = await supabase.rpc('decrement_leave_balance', {
          user_id: request.user_id,
          days: days,
        });
        // If RPC doesn't exist, try direct update
        if (updateError) {
          await supabase
            .from('profiles')
            .update({
              annual_leave_balance: (request.profiles?.annual_leave_balance || 15) - days,
            })
            .eq('id', request.user_id);
        }
      }

      onUpdate();
    } catch (error) {
      alert('처리 중 오류가 발생했습니다.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const calculateDays = (start: string, end: string) => {
    const startDate = new Date(start);
    const endDate = new Date(end);
    const diffTime = Math.abs(endDate.getTime() - startDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    return diffDays;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h4 className="font-semibold text-gray-800">
            {request.profiles?.name || '알 수 없음'}
          </h4>
          <p className="text-sm text-gray-500">{request.profiles?.email}</p>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-sm font-medium ${
            LEAVE_STATUS_COLORS[request.status]
          }`}
        >
          {LEAVE_STATUS_LABELS[request.status]}
        </span>
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-gray-600">휴가 유형:</span>
          <span className="font-medium">{LEAVE_TYPE_LABELS[request.leave_type]}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">기간:</span>
          <span className="font-medium">
            {formatDate(request.start_date)} ~ {formatDate(request.end_date)}
            <span className="text-gray-400 ml-2">
              ({calculateDays(request.start_date, request.end_date)}일)
            </span>
          </span>
        </div>
        {request.reason && (
          <div>
            <span className="text-gray-600">사유:</span>
            <p className="mt-1 text-gray-800">{request.reason}</p>
          </div>
        )}
        <div className="text-sm text-gray-400">
          신청일: {new Date(request.created_at).toLocaleDateString('ko-KR')}
        </div>
      </div>

      {request.status === 'pending' && (
        <div className="flex gap-2">
          <button
            onClick={() => handleAction('approved')}
            disabled={loading}
            className="flex-1 py-2 px-4 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-medium rounded-lg transition-colors"
          >
            {loading ? '처리중...' : '승인'}
          </button>
          <button
            onClick={() => handleAction('rejected')}
            disabled={loading}
            className="flex-1 py-2 px-4 bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white font-medium rounded-lg transition-colors"
          >
            {loading ? '처리중...' : '거절'}
          </button>
        </div>
      )}

      {request.status !== 'pending' && request.reviewer && (
        <p className="text-sm text-gray-500">
          처리자: {request.reviewer.name} ({new Date(request.reviewed_at!).toLocaleDateString('ko-KR')})
        </p>
      )}
    </div>
  );
}
