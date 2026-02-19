#!/bin/bash
# Setup script for 휴가등록앱

echo "🚀 휴가등록앱 Setup Script"
echo "======================================"

# Check Python version
echo "1. Checking Python version..."
python3 --version || { echo "Error: Python 3 not found"; exit 1; }

# Create virtual environment
echo "2. Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo "3. Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo "4. Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env from template
if [ ! -f .env ]; then
    echo "5. Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your bkend.ai credentials:"
    echo "   - BKEND_API_KEY"
    echo "   - BKEND_PROJECT_ID"
    echo "   - BKEND_ENV_ID"
    echo "   - SECRET_KEY"
else
    echo "5. .env file already exists"
fi

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Create 'leaves' table in bkend.ai"
echo "3. Run: python app/main.py"
echo "4. Visit: http://localhost:8000"
echo ""
echo "For more details, see README.md"
