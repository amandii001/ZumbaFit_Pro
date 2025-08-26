#!/usr/bin/env python3
"""
Test Video Filtering Data
"""

import requests
import json

def test_video_data_for_filtering():
    """Test video data to ensure filtering functionality has data to work with"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Video Data for Filtering...")
    
    try:
        # Get videos data
        response = requests.get(
            f"{base_url}/admin/videos",
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('videos', [])
            
            print(f"✅ Retrieved {len(videos)} videos")
            
            if len(videos) > 0:
                print("\n📋 Sample Video Data:")
                for i, video in enumerate(videos[:3]):  # Show first 3 videos
                    print(f"   Video {i+1}:")
                    print(f"     ID: {video.get('video_id')}")
                    print(f"     Result: {video.get('analysis_result')}")
                    print(f"     Status: {video.get('status')}")
                    print(f"     User: {video.get('user_name')}")
                    print(f"     Date: {video.get('upload_date')}")
                    print()
                
                # Check for different types of videos
                correct_videos = [v for v in videos if 'correct' in v.get('analysis_result', '').lower()]
                incorrect_videos = [v for v in videos if 'incorrect' in v.get('analysis_result', '').lower()]
                processing_videos = [v for v in videos if v.get('status', '').lower() == 'processing']
                
                print("📊 Video Distribution:")
                print(f"   Correct: {len(correct_videos)}")
                print(f"   Incorrect: {len(incorrect_videos)}")
                print(f"   Processing: {len(processing_videos)}")
                print(f"   Total: {len(videos)}")
                
                print("\n🎉 Video filtering will work with this data!")
                print("🔍 You can now test:")
                print("   - All Videos filter")
                print("   - Correct filter")
                print("   - Incorrect filter")
                print("   - Processing filter")
                print("   - Search functionality")
                
            else:
                print("⚠️  No videos found. Consider uploading some test videos.")
                
        else:
            print(f"❌ Failed to get videos: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_video_data_for_filtering()
