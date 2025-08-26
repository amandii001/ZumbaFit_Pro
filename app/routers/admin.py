from fastapi import APIRouter, HTTPException
from app.db import get_connection, close_connection
from typing import Dict, Any

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        stats = {}
        
        # Get total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        stats["total_users"] = result["count"] if result else 0
        
        # Get total videos
        cursor.execute("SELECT COUNT(*) as count FROM videos")
        result = cursor.fetchone()
        stats["total_videos"] = result["count"] if result else 0
        
        # Get correct postures
        cursor.execute("""
            SELECT COUNT(*) as count FROM videos 
            WHERE class_label LIKE '%_Correct'
        """)
        result = cursor.fetchone()
        stats["correct_postures"] = result["count"] if result else 0
        
        # Get incorrect postures
        cursor.execute("""
            SELECT COUNT(*) as count FROM videos 
            WHERE class_label LIKE '%_Incorrect'
        """)
        result = cursor.fetchone()
        stats["incorrect_postures"] = result["count"] if result else 0
        
        # Get total sessions (approximated by unique users with videos)
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) as count FROM videos
        """)
        result = cursor.fetchone()
        stats["total_sessions"] = result["count"] if result else 0
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.get("/videos")
def get_recent_videos():
    """Get recent video uploads"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT v.video_id, v.video_name, v.class_label, v.upload_time, 
                   v.processing_status, u.name as user_name
            FROM videos v
            JOIN users u ON v.user_id = u.user_id
            ORDER BY v.upload_time DESC
            LIMIT 10
        """)
        
        videos = cursor.fetchall()
        
        # Format the data
        formatted_videos = []
        for video in videos:
            formatted_videos.append({
                "video_id": f"#VID-{video['video_id']:04d}",
                "upload_date": video['upload_time'].strftime("%d/%m/%Y, %H:%M") if video['upload_time'] else "N/A",
                "analysis_result": video['class_label'].replace('_', ' '),
                "status": video['processing_status'],
                "user_name": video['user_name']
            })
        
        return {"videos": formatted_videos}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get videos: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.get("/users")
def get_user_stats():
    """Get user statistics"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get users with their video counts
        cursor.execute("""
            SELECT u.name, u.email, COUNT(v.video_id) as video_count,
                   MAX(v.upload_time) as last_upload
            FROM users u
            LEFT JOIN videos v ON u.user_id = v.user_id
            GROUP BY u.user_id, u.name, u.email
            ORDER BY video_count DESC
            LIMIT 10
        """)
        
        users = cursor.fetchall()
        
        # Format the data
        formatted_users = []
        for user in users:
            formatted_users.append({
                "name": user['name'],
                "email": user['email'],
                "video_count": user['video_count'],
                "last_upload": user['last_upload'].strftime("%d/%m/%Y") if user['last_upload'] else "Never"
            })
        
        return {"users": formatted_users}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user stats: {str(e)}")
    finally:
        close_connection(conn, cursor)
