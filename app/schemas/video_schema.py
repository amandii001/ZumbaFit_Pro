from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoUploadResponse(BaseModel):
    message: str
    video_id: int
    feedback: str
    class_label: str
    confidence: float

class VideoAnalysis(BaseModel):
    video_id: int
    user_id: int
    class_label: str
    feedback_text: str
    processing_status: str
    upload_time: datetime

class VideoList(BaseModel):
    videos: list[VideoAnalysis]
    total_count: int
