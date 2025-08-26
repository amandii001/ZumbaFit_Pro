from fastapi import APIRouter, HTTPException, Query
from app.db import get_connection, close_connection
from app.schemas.feedback_schema import FeedbackReport, MusicRecommendation, PersonalizedFeedback
from typing import List, Optional

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.get("/user/{user_id}", response_model=List[FeedbackReport])
def get_user_feedback(
    user_id: int,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get feedback reports for a specific user"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """SELECT fr.*, v.class_label, v.exercise_type
               FROM feedback_reports fr
               JOIN videos v ON fr.video_id = v.video_id
               WHERE fr.user_id = %s
               ORDER BY fr.generated_at DESC
               LIMIT %s OFFSET %s""",
            (user_id, limit, offset)
        )
        
        feedback_reports = []
        for row in cursor.fetchall():
            feedback_reports.append(FeedbackReport(
                report_id=row["report_id"],
                video_id=row["video_id"],
                user_id=row["user_id"],
                feedback_text=row["feedback_text"],
                recommended_music_id=row["recommended_music_id"],
                generated_at=row["generated_at"]
            ))
        
        return feedback_reports
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch feedback: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.get("/music/recommendations", response_model=List[MusicRecommendation])
def get_music_recommendations(
    dance_style: Optional[str] = Query(None, description="Filter by dance style"),
    limit: int = Query(10, ge=1, le=50)
):
    """Get music recommendations"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        if dance_style:
            cursor.execute(
                """SELECT * FROM music_recommendations 
                   WHERE dance_style = %s AND is_active = TRUE
                   ORDER BY upload_time DESC
                   LIMIT %s""",
                (dance_style, limit)
            )
        else:
            cursor.execute(
                """SELECT * FROM music_recommendations 
                   WHERE is_active = TRUE
                   ORDER BY upload_time DESC
                   LIMIT %s""",
                (limit,)
            )
        
        recommendations = []
        for row in cursor.fetchall():
            recommendations.append(MusicRecommendation(
                music_id=row["music_id"],
                dance_style=row["dance_style"],
                music_title=row["music_title"],
                tempo_bpm=row["tempo_bpm"],
                duration_seconds=row["duration_seconds"],
                mp4_file_path=row["mp4_file_path"]
            ))
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch music recommendations: {str(e)}")
    finally:
        close_connection(conn, cursor)

@router.get("/personalized/{user_id}", response_model=PersonalizedFeedback)
def get_personalized_feedback(user_id: int):
    """Get personalized feedback and recommendations for a user"""
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get latest feedback report
        cursor.execute(
            """SELECT fr.*, v.class_label, v.exercise_type
               FROM feedback_reports fr
               JOIN videos v ON fr.video_id = v.video_id
               WHERE fr.user_id = %s
               ORDER BY fr.generated_at DESC
               LIMIT 1""",
            (user_id,)
        )
        
        latest_feedback = cursor.fetchone()
        if not latest_feedback:
            raise HTTPException(status_code=404, detail="No feedback found for user")
        
        # Get music recommendations based on exercise type
        exercise_type = latest_feedback["exercise_type"] or "general"
        cursor.execute(
            """SELECT * FROM music_recommendations 
               WHERE (dance_style = %s OR dance_style = 'general') 
               AND is_active = TRUE
               ORDER BY upload_time DESC
               LIMIT 5""",
            (exercise_type,)
        )
        
        music_recommendations = []
        for row in cursor.fetchall():
            music_recommendations.append(MusicRecommendation(
                music_id=row["music_id"],
                dance_style=row["dance_style"],
                music_title=row["music_title"],
                tempo_bpm=row["tempo_bpm"],
                duration_seconds=row["duration_seconds"],
                mp4_file_path=row["mp4_file_path"]
            ))
        
        # Generate improvement suggestions based on class label
        class_label = latest_feedback["class_label"]
        improvement_suggestions = generate_improvement_suggestions(class_label)
        
        feedback_report = FeedbackReport(
            report_id=latest_feedback["report_id"],
            video_id=latest_feedback["video_id"],
            user_id=latest_feedback["user_id"],
            feedback_text=latest_feedback["feedback_text"],
            recommended_music_id=latest_feedback["recommended_music_id"],
            generated_at=latest_feedback["generated_at"]
        )
        
        return PersonalizedFeedback(
            feedback=feedback_report,
            music_recommendations=music_recommendations,
            improvement_suggestions=improvement_suggestions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch personalized feedback: {str(e)}")
    finally:
        close_connection(conn, cursor)

def generate_improvement_suggestions(class_label: str) -> List[str]:
    """Generate improvement suggestions based on detected posture"""
    suggestions = []
    
    if "Squat" in class_label:
        if "Incorrect" in class_label:
            suggestions.extend([
                "Keep your knees aligned with your toes",
                "Lower your body as if sitting back into a chair",
                "Keep your chest up and back straight",
                "Make sure your knees don't go past your toes"
            ])
        else:
            suggestions.extend([
                "Great squat form! Keep practicing to maintain consistency",
                "Try adding some variations like jump squats",
                "Focus on controlled movement both down and up"
            ])
    
    elif "Arm_Raise" in class_label:
        if "Incorrect" in class_label:
            suggestions.extend([
                "Keep your arms straight but not locked",
                "Raise arms to shoulder level, not above",
                "Engage your core to maintain balance",
                "Keep your shoulders relaxed, not shrugged"
            ])
        else:
            suggestions.extend([
                "Excellent arm raise technique!",
                "Try adding some resistance with light weights",
                "Focus on smooth, controlled movements"
            ])
    
    elif "Knee_Extension" in class_label:
        if "Incorrect" in class_label:
            suggestions.extend([
                "Keep your supporting leg slightly bent",
                "Extend your leg fully but don't lock the knee",
                "Maintain good posture throughout the movement",
                "Focus on balance and stability"
            ])
        else:
            suggestions.extend([
                "Perfect knee extension form!",
                "Try adding ankle weights for more challenge",
                "Practice on both legs for balance"
            ])
    
    return suggestions
