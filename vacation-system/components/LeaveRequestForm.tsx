'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { LeaveType, LEAVE_TYPE_LABELS } from '@/lib/types';

interface LeaveRequestFormProps {
  userId: string;
  onSuccess: () => void;
}

export default function LeaveRequestForm({ userId, onSuccess }: LeaveRequestFormProps) {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [leaveType, setLeaveType] = useState<LeaveType>('annual');
  const [timeValue, setTimeValue] = useState('');
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const supabase = createClient();

  const needsTimeInput = leaveType === 'early_leave' || leaveType === 'late_arrival';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validate dates
    if (new Date(endDate) < new Date(startDate)) {
      setError('종료일은 시작일 이후여야 합니다.');
      setLoading(false);
      return;
    }

    try {
      const { error: insertError } = await supabase.from('leave_requests').insert({
        user_id: userId,
        start_date: startDate,
        end_date: endDate,
        leave_type: leaveType,
        reason: reason || null,
      });

      if (insertError) throw insertError;

      // Reset form
      setStartDate('');
      setEndDate('');
      setLeaveType('annual');
      setReason('');
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : '휴가 신청 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">휴가 신청</h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-1">
              시작일
            </label>
            <input
              id="startDate"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              min={today}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-1">
              종료일
            </label>
            <input
              id="endDate"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              min={startDate || today}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <div>
          <label htmlFor="leaveType" className="block text-sm font-medium text-gray-700 mb-1">
            휴가 유형
          </label>
          <select
            id="leaveType"
            value={leaveType}
            onChange={(e) => setLeaveType(e.target.value as LeaveType)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {(Object.keys(LEAVE_TYPE_LABELS) as LeaveType[]).map((type) => (
              <option key={type} value={type}>
                {LEAVE_TYPE_LABELS[type]}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="reason" className="block text-sm font-medium text-gray-700 mb-1">
            사유 (선택)
          </label>
          <textarea
            id="reason"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="휴가 사유를 입력하세요..."
          />
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-red-100 text-red-700 text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors"
        >
          {loading ? '신청 중...' : '휴가 신청'}
        </button>
      </form>
    </div>
  );
}
