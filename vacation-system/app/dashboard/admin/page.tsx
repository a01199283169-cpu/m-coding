'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';
import { Profile, LeaveRequest, LeaveStatus } from '@/lib/types';
import AdminRequestCard from '@/components/AdminRequestCard';

export default function AdminPage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<LeaveStatus | 'all'>('pending');
  const router = useRouter();
  const supabase = createClient();

  const fetchData = useCallback(async () => {
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      router.push('/');
      return;
    }

    // Fetch profile and check admin role
    const { data: profileData } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.id)
      .single();

    if (!profileData || profileData.role !== 'admin') {
      router.push('/dashboard');
      return;
    }

    setProfile(profileData);

    // Fetch all leave requests with user profiles
    let query = supabase
      .from('leave_requests')
      .select(`
        *,
        profiles:user_id (id, email, name, annual_leave_balance),
        reviewer:reviewed_by (id, email, name)
      `)
      .order('created_at', { ascending: false });

    if (filter !== 'all') {
      query = query.eq('status', filter);
    }

    const { data: requestsData } = await query;

    if (requestsData) {
      setRequests(requestsData);
    }

    setLoading(false);
  }, [supabase, router, filter]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!profile || profile.role !== 'admin') {
    return null;
  }

  const pendingCount = requests.filter((r) => r.status === 'pending').length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">관리자 대시보드</h1>
          <p className="text-gray-600">
            대기중인 신청: <span className="font-semibold text-blue-600">{pendingCount}건</span>
          </p>
        </div>

        {/* Filter */}
        <div className="flex gap-2">
          {(['all', 'pending', 'approved', 'rejected'] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === status
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              {status === 'all' && '전체'}
              {status === 'pending' && '대기중'}
              {status === 'approved' && '승인됨'}
              {status === 'rejected' && '거절됨'}
            </button>
          ))}
        </div>
      </div>

      {/* Request Cards */}
      {requests.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
          <p className="text-gray-500">해당하는 휴가 신청이 없습니다.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {requests.map((request) => (
            <AdminRequestCard key={request.id} request={request} onUpdate={fetchData} />
          ))}
        </div>
      )}
    </div>
  );
}
