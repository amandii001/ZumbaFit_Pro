from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FeedbackReport(BaseModel):
    report_id: int
    video_id: int
    user_id: int
    feedback_text: str
    recommended_music_id: Optional[int]
    generated_at: datetime

class MusicRecommendation(BaseModel):
    music_id: int
    dance_style: str
    music_title: str
    tempo_bpm: Optional[int]
    duration_seconds: int
    mp4_file_path: str

class PersonalizedFeedback(BaseModel):
    feedback: FeedbackReport
    music_recommendations: List[MusicRecommendation]
    improvement_suggestions: List[str]
