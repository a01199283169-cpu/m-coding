'use client';

import { useEffect, useState, useCallback, useMemo } from 'react';
import { createClient } from '@/lib/supabase/client';
import { Profile, LeaveRequest } from '@/lib/types';
import LeaveBalance from '@/components/LeaveBalance';
import LeaveRequestForm from '@/components/LeaveRequestForm';
import LeaveRequestList from '@/components/LeaveRequestList';

const DEFAULT_PROFILE: Profile = {
  id: 'temp-user',
  email: 'guest@example.com',
  name: '게스트 사용자',
  role: 'employee',
  annual_leave_balance: 15,
  created_at: new Date().toISOString(),
};

export default function DashboardPage() {
  const [profile, setProfile] = useState<Profile>(DEFAULT_PROFILE);
  const [requests, setRequests] = useState<LeaveRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const supabase = useMemo(() => createClient(), []);

  const fetchData = useCallback(async () => {
    const {
      data: { user },
    } = await supabase.auth.getUser();

    // Fetch profile
    if (user) {
      const { data: profileData } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.id)
        .single();

      if (profileData) {
        setProfile(profileData);
      }

      // Fetch leave requests
      const { data: requestsData } = await supabase
        .from('leave_requests')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false });

      if (requestsData) {
        setRequests(requestsData);
      }
    }

    setLoading(false);
  }, [supabase]);

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

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">직원 대시보드</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Balance and Form */}
        <div className="lg:col-span-1 space-y-6">
          <LeaveBalance profile={profile} />
          <LeaveRequestForm userId={profile.id} onSuccess={fetchData} />
        </div>

        {/* Right Column - Request List */}
        <div className="lg:col-span-2">
          <LeaveRequestList requests={requests} onUpdate={fetchData} />
        </div>
      </div>
    </div>
  );
}
