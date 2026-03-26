#!/bin/bash
# 간편 Git 푸시 스크립트
# 사용법: ./git-push.sh "커밋 메시지"

cd /home/snowwon5/m-coding/20260322

# 커밋 메시지 확인
if [ -z "$1" ]; then
    echo "❌ 사용법: ./git-push.sh \"커밋 메시지\""
    echo "예시: ./git-push.sh \"기능 추가\""
    exit 1
fi

MESSAGE="$1"

# Git 작업 수행
echo "📦 변경사항 확인 중..."
git status --short

echo ""
echo "📝 커밋 중..."
git add equipment_manager/
git commit -m "$MESSAGE

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

echo ""
echo "🚀 GitHub에 푸시 중..."
git push origin feature/todo-app-and-updates

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ GitHub 푸시 완료!"
    echo "🔗 https://github.com/a01199283169-cpu/m-coding"
else
    echo ""
    echo "❌ 푸시 실패. 에러를 확인하세요."
fi
