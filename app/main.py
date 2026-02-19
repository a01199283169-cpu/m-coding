"""FastAPI 엔트리포인트 - 휴가등록앱"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "휴가등록앱"),
    version=os.getenv("APP_VERSION", "0.1.0"),
    description="직원 휴가 신청/조회 시스템 - FastAPI + bkend.ai BaaS",
    debug=os.getenv("DEBUG", "False") == "True"
)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Import and register routers
from app.routes import auth, leaves

app.include_router(auth.router)
app.include_router(leaves.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": os.getenv("APP_NAME", "휴가등록앱"),
        "version": os.getenv("APP_VERSION", "0.1.0")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
