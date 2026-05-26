"""Main FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.database import engine, Base
from app.api import question, auth, user, course, order, chat, community


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    # Startup
    print("🚀 Starting Training Platform...")
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    print("👋 Shutting down Training Platform...")


app = FastAPI(
    title="培训平台 API",
    description="综合性培训平台 - 课程管理 + 在线售卖 + 题库系统 + 社区互动",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/user", tags=["用户"])
app.include_router(question.router, prefix="/api/question", tags=["题库"])
app.include_router(course.router, prefix="/api/course", tags=["课程"])
app.include_router(order.router, prefix="/api/order", tags=["订单"])
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])
app.include_router(community.router, prefix="/api/community", tags=["社区"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "培训平台 API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}
