# 휴가 등록 시스템

Next.js + Supabase + Tailwind CSS를 사용한 휴가 등록 시스템입니다.

## 기능

### 직원
- 로그인/회원가입
- 잔여 연차 확인
- 휴가 신청 (연차, 병가, 개인사유)
- 본인 신청 내역 조회
- 대기중인 신청 취소

### 관리자
- 전체 휴가 신청 목록 조회
- 상태별 필터링 (전체, 대기중, 승인됨, 거절됨)
- 휴가 신청 승인/거절

## 기술 스택

- **Frontend**: Next.js 14 (App Router)
- **Backend/DB**: Supabase (PostgreSQL + Auth)
- **Styling**: Tailwind CSS
- **배포**: Vercel

## 시작하기

### 1. Supabase 프로젝트 생성

1. [Supabase](https://supabase.com)에서 무료 계정 생성
2. "New Project" 클릭하여 새 프로젝트 생성
3. 프로젝트 생성 완료까지 대기

### 2. 환경 변수 설정

1. Supabase Dashboard > Project Settings > API로 이동
2. `.env.local.example`을 복사하여 `.env.local` 생성
3. 환경 변수 설정:

```bash
cp .env.local.example .env.local
```

`.env.local` 파일:
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. 데이터베이스 스키마 설정

1. Supabase Dashboard > SQL Editor로 이동
2. `supabase/schema.sql` 파일 내용을 복사하여 실행

### 4. Authentication 설정

1. Supabase Dashboard > Authentication > Providers로 이동
2. Email 프로바이더가 활성화되어 있는지 확인
3. 필요시 "Confirm email" 옵션을 비활성화하여 개발 중 빠른 테스트 가능

### 5. 로컬 실행

```bash
npm install
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000) 접속

## 관리자 계정 설정

회원가입 후 관리자 권한을 부여하려면:

1. Supabase Dashboard > Table Editor > profiles 테이블로 이동
2. 해당 사용자의 `role` 컬럼을 `admin`으로 변경

또는 SQL Editor에서:
```sql
UPDATE profiles SET role = 'admin' WHERE email = 'admin@example.com';
```

## 프로젝트 구조

```
vacation-system/
├── app/
│   ├── layout.tsx          # 루트 레이아웃
│   ├── page.tsx            # 로그인 페이지
│   ├── auth/
│   │   └── callback/route.ts
│   ├── dashboard/
│   │   ├── layout.tsx      # 대시보드 레이아웃 (헤더, 네비게이션)
│   │   ├── page.tsx        # 직원 대시보드
│   │   └── admin/
│   │       └── page.tsx    # 관리자 대시보드
│   └── api/
│       └── leave/
│           └── route.ts    # 휴가 API
├── components/
│   ├── LoginForm.tsx       # 로그인/회원가입 폼
│   ├── LeaveRequestForm.tsx # 휴가 신청 폼
│   ├── LeaveRequestList.tsx # 휴가 신청 목록
│   ├── LeaveBalance.tsx    # 잔여 연차 표시
│   └── AdminRequestCard.tsx # 관리자용 신청 카드
├── lib/
│   ├── supabase/
│   │   ├── client.ts       # 클라이언트 Supabase
│   │   └── server.ts       # 서버 Supabase
│   └── types.ts            # TypeScript 타입
├── supabase/
│   └── schema.sql          # DB 스키마
└── middleware.ts           # 인증 미들웨어
```

## 배포 (Vercel)

1. GitHub에 프로젝트 푸시
2. [Vercel](https://vercel.com)에서 프로젝트 import
3. 환경 변수 설정:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. 배포 완료

## 라이선스

MIT
