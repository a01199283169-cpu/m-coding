export type UserRole = 'admin' | 'employee';

export type LeaveType = 'annual' | 'early_leave' | 'late_arrival';

export type LeaveStatus = 'pending' | 'approved' | 'rejected';

export interface Profile {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  annual_leave_balance: number;
  created_at: string;
}

export interface LeaveRequest {
  id: string;
  user_id: string;
  start_date: string;
  end_date: string;
  leave_type: LeaveType;
  time_value: string | null;
  reason: string;
  status: LeaveStatus;
  reviewed_by: string | null;
  reviewed_at: string | null;
  created_at: string;
  // Joined data
  profiles?: Profile;
  reviewer?: Profile;
}

export const LEAVE_TYPE_LABELS: Record<LeaveType, string> = {
  annual: '연차',
  early_leave: '조퇴',
  late_arrival: '지각',
};

export const LEAVE_STATUS_LABELS: Record<LeaveStatus, string> = {
  pending: '대기중',
  approved: '승인됨',
  rejected: '거절됨',
};

export const LEAVE_STATUS_COLORS: Record<LeaveStatus, string> = {
  pending: 'bg-yellow-100 text-yellow-800',
  approved: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
};
