from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Query
from fastapi.responses import JSONResponse
from app.db import get_connection, close_connection
from app.utils.ml_pipeline import analyze_video
from app.schemas.video_schema import VideoUploadResponse, VideoAnalysis, VideoList
import shutil
import os
import uuid
from typing import Optional
from datetime import datetime

UPLOAD_DIR = "app/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/video", tags=["Video"])

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    exercise_type: Optional[str] = Form(None)
):
    """Upload and analyze a Zumba video"""
    
    # Validate file type
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Please upload a video file")
    
    # Generate unique filename
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Analyze video using ML model
        feedback, predicted_class, confidence = analyze_video(file_path)
        
        # Store in database
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        try:
            # Insert video record
            cursor.execute(
                """INSERT INTO videos 
                   (user_id, video_name, file_path, class_label, exercise_type, processing_status) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, filename, file_path, predicted_class, exercise_type, "processed")
            )
            video_id = cursor.lastrowid
            
            # Insert feedback report
            cursor.execute(
                """INSERT INTO feedback_reports 
                   (video_id, user_id, feedback_text) 
                   VALUES (%s, %s, %s)""",
                (video_id, user_id, feedback)
            )
            
            conn.commit()
            
            return VideoUploadResponse(
                message="✅ Video uploaded & analyzed successfully",
                video_id=video_id,
                feedback=feedback,
                class_label=predicted_class,
                confidence=confidence
            )
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            close_connection(conn, cursor)
            
    except Exception as e:
        # Clean up file if analysis fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Video processing failed: {str(e)}")

@router.get("/user/{user_id}", response_model=VideoList)
def get_user_videos(
    user_id: int,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get videos for a specific user"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get total count
        cursor.execute("SELECT COUNT(*) as count FROM videos WHERE user_id = %s", (user_id,))
        total_count = cursor.fetchone()["count"]
        
        # Get videos with pagination
        cursor.execute(
            """SELECT v.video_id, v.user_id, v.class_label, v.processing_status, 
                      v.upload_time, fr.feedback_text
               FROM videos v
               LEFT JOIN feedback_reports fr ON v.video_id = fr.video_id
               WHERE v.user_id = %s
               ORDER BY v.upload_time DESC
               LIMIT %s OFFSET %s""",
            (user_id, limit, offset)
        )
        
        videos = []
        for row in cursor.fetchall():
            videos.append(VideoAnalysis(
                video_id=row["video_id"],
                user_id=row["user_id"],
                class_label=row["class_label"],
                feedback_text=row["feedback_text"] or "",
                processing_status=row["processing_status"],
                upload_time=row["upload_time"]
            ))
        
        return VideoList(videos=videos, total_count=total_count)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch videos: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.get("/{video_id}")
def get_video_details(video_id: int):
    """Get detailed information about a specific video"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """SELECT v.*, fr.feedback_text, u.name as user_name
               FROM videos v
               LEFT JOIN feedback_reports fr ON v.video_id = fr.video_id
               LEFT JOIN users u ON v.user_id = u.user_id
               WHERE v.video_id = %s""",
            (video_id,)
        )
        
        video = cursor.fetchone()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return video
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video details: {str(e)}")
    finally:
        close_connection(conn, cursor)
