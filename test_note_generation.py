#!/usr/bin/env python3
"""
Test script for the note generation functionality
"""

import requests
import json

def test_note_generation():
    """Test the note generation API with different languages"""
    
    base_url = "http://127.0.0.1:5001"
    
    # Test cases with different languages
    test_cases = [
        {
            "content": "Meeting with team tomorrow at 3pm in conference room A",
            "language": "English",
            "description": "English test case"
        },
        {
            "content": "去圖書館借書明天下午2點",
            "language": "繁體中文", 
            "description": "Traditional Chinese test case"
        },
        {
            "content": "Badminton match today 5pm @polyu sports center",
            "language": "日本語",
            "description": "Japanese output test case"
        }
    ]
    
    print("🧪 Testing Note Generation API")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['description']}")
        print(f"Input: {test_case['content']}")
        print(f"Target Language: {test_case['language']}")
        
        try:
            # Make API request
            response = requests.post(
                f"{base_url}/api/notes/generate",
                headers={"Content-Type": "application/json"},
                json={
                    "content": test_case["content"],
                    "language": test_case["language"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                note = result.get("note", {})
                
                print("✅ Success!")
                print(f"Title: {note.get('title', 'N/A')}")
                print(f"Content: {note.get('content', 'N/A')}")
                print(f"Tags: {note.get('tags', 'N/A')}")
                print(f"Date: {note.get('event_date', 'N/A')}")
                print(f"Time: {note.get('event_time', 'N/A')}")
            else:
                print(f"❌ Failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_note_generation()