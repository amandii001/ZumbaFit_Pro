from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, video, feedback, admin

# Create FastAPI app
app = FastAPI(
    title="ZumbaFit Pro API",
    description="AI-powered Zumba dance analysis and feedback system",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded videos
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(video.router)
app.include_router(feedback.router)
app.include_router(admin.router)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "🎵 ZumbaFit Pro API is running!",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "video": "/video", 
            "feedback": "/feedback",
            "admin": "/admin",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "ZumbaFit Pro API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
