-- =============================================
-- 휴가 등록 시스템 데이터베이스 스키마
-- Supabase SQL Editor에서 이 파일을 실행하세요
-- =============================================

-- 1. profiles 테이블 생성
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'employee' CHECK (role IN ('admin', 'employee')),
  annual_leave_balance INTEGER NOT NULL DEFAULT 15,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. leave_requests 테이블 생성
CREATE TABLE IF NOT EXISTS leave_requests (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  leave_type TEXT NOT NULL CHECK (leave_type IN ('annual', 'sick', 'personal')),
  reason TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  reviewed_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
  reviewed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  CONSTRAINT valid_date_range CHECK (end_date >= start_date)
);

-- 3. Row Level Security (RLS) 활성화
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE leave_requests ENABLE ROW LEVEL SECURITY;

-- 4. profiles 테이블 RLS 정책
-- 모든 인증된 사용자는 자신의 프로필을 볼 수 있음
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

-- 관리자는 모든 프로필을 볼 수 있음
CREATE POLICY "Admins can view all profiles" ON profiles
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- 사용자는 자신의 프로필을 업데이트할 수 있음
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- 5. leave_requests 테이블 RLS 정책
-- 사용자는 자신의 휴가 신청을 볼 수 있음
CREATE POLICY "Users can view own leave requests" ON leave_requests
  FOR SELECT USING (auth.uid() = user_id);

-- 관리자는 모든 휴가 신청을 볼 수 있음
CREATE POLICY "Admins can view all leave requests" ON leave_requests
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- 사용자는 자신의 휴가를 신청할 수 있음
CREATE POLICY "Users can create own leave requests" ON leave_requests
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- 사용자는 대기중인 자신의 신청을 취소(삭제)할 수 있음
CREATE POLICY "Users can delete own pending requests" ON leave_requests
  FOR DELETE USING (auth.uid() = user_id AND status = 'pending');

-- 관리자는 휴가 신청을 업데이트할 수 있음 (승인/거절)
CREATE POLICY "Admins can update leave requests" ON leave_requests
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- 6. 새 사용자 등록 시 자동으로 프로필 생성하는 함수
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, name, role, annual_leave_balance)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'name', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'role', 'employee'),
    15
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 7. 트리거 생성 (이미 존재하면 삭제 후 재생성)
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 8. 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_leave_requests_user_id ON leave_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_leave_requests_status ON leave_requests(status);
CREATE INDEX IF NOT EXISTS idx_leave_requests_created_at ON leave_requests(created_at DESC);

-- =============================================
-- 테스트 데이터 (선택적)
-- 아래 주석을 해제하여 테스트 데이터를 추가할 수 있습니다
-- =============================================

-- 관리자 계정 생성 후 role 변경 예시:
-- UPDATE profiles SET role = 'admin' WHERE email = 'admin@example.com';
