'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import {
  LeaveRequest,
  LEAVE_TYPE_LABELS,
  LEAVE_STATUS_LABELS,
  LEAVE_STATUS_COLORS,
} from '@/lib/types';

interface LeaveRequestListProps {
  requests: LeaveRequest[];
  onUpdate: () => void;
}

export default function LeaveRequestList({ requests, onUpdate }: LeaveRequestListProps) {
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const supabase = createClient();

  const handleDelete = async (id: string) => {
    if (!confirm('정말 이 신청을 취소하시겠습니까?')) return;

    setDeletingId(id);
    try {
      const { error } = await supabase.from('leave_requests').delete().eq('id', id);
      if (error) throw error;
      onUpdate();
    } catch (error) {
      alert('취소 중 오류가 발생했습니다.');
      console.error(error);
    } finally {
      setDeletingId(null);
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

  if (requests.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">내 휴가 신청 내역</h3>
        <p className="text-gray-500 text-center py-8">신청 내역이 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">내 휴가 신청 내역</h3>

      <div className="space-y-4">
        {requests.map((request) => (
          <div
            key={request.id}
            className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-800">
                    {LEAVE_TYPE_LABELS[request.leave_type]}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      LEAVE_STATUS_COLORS[request.status]
                    }`}
                  >
                    {LEAVE_STATUS_LABELS[request.status]}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  {formatDate(request.start_date)} ~ {formatDate(request.end_date)}
                  <span className="text-gray-400 ml-2">
                    ({calculateDays(request.start_date, request.end_date)}일)
                  </span>
                </p>
                {request.reason && (
                  <p className="text-sm text-gray-500 mt-1">{request.reason}</p>
                )}
              </div>

              {request.status === 'pending' && (
                <button
                  onClick={() => handleDelete(request.id)}
                  disabled={deletingId === request.id}
                  className="text-red-500 hover:text-red-700 text-sm font-medium disabled:opacity-50"
                >
                  {deletingId === request.id ? '취소중...' : '취소'}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
