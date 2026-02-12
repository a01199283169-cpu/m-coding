import LoginForm from '@/components/LoginForm';

export const dynamic = 'force-dynamic';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">휴가 등록 시스템</h1>
        <p className="text-gray-600">간편하게 휴가를 신청하고 관리하세요</p>
      </div>
      <LoginForm />
    </main>
  );
}
