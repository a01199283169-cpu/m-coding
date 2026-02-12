'use client';

import { Profile } from '@/lib/types';

interface LeaveBalanceProps {
  profile: Profile;
}

export default function LeaveBalance({ profile }: LeaveBalanceProps) {
  return (
    <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-blue-100 text-sm">잔여 연차</p>
          <p className="text-4xl font-bold mt-1">{profile.annual_leave_balance}일</p>
        </div>
        <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-8 h-8"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5"
            />
          </svg>
        </div>
      </div>
      <div className="mt-4 pt-4 border-t border-white/20">
        <p className="text-sm text-blue-100">
          안녕하세요, <span className="font-semibold text-white">{profile.name}</span>님
        </p>
      </div>
    </div>
  );
}
