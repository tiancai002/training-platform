"""Logging utility for the training platform"""
import os
import json
from datetime import datetime
from pathlib import Path

# Log directory
LOG_DIR = Path("/var/www/training-platform/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

class ActivityLogger:
    """User activity logger"""
    
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.log_file = LOG_DIR / f"user_{user_id}_activity.log"
    
    def log(self, action: str, details: dict = None):
        """Log user activity"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": self.user_id,
            "username": self.username,
            "action": action,
            "details": details or {}
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        # Also print to console
        print(f"[USER_ACTIVITY] {self.username}: {action}")
    
    def log_practice(self, question_id: int, bank_id: int, is_correct: bool, time_spent: int):
        """Log practice activity"""
        self.log("practice", {
            "question_id": question_id,
            "bank_id": bank_id,
            "is_correct": is_correct,
            "time_spent": time_spent
        })
    
    def log_course_start(self, course_id: int):
        """Log course start"""
        self.log("course_start", {"course_id": course_id})
    
    def log_course_complete(self, course_id: int, duration: int):
        """Log course completion"""
        self.log("course_complete", {
            "course_id": course_id,
            "duration": duration
        })
    
    def log_community_post(self, post_id: int, action: str):
        """Log community activity"""
        self.log("community", {
            "post_id": post_id,
            "action": action  # create, like, comment
        })
    
    def get_activity_summary(self, days: int = 7) -> dict:
        """Get activity summary for last N days"""
        if not self.log_file.exists():
            return {"total_actions": 0, "actions": []}
        
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        actions = []
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry_time = datetime.fromisoformat(entry["timestamp"])
                    if entry_time >= cutoff:
                        actions.append(entry)
                except:
                    continue
        
        # Count by action type
        action_counts = {}
        for action in actions:
            action_type = action.get("action", "unknown")
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        return {
            "total_actions": len(actions),
            "action_counts": action_counts,
            "recent_actions": actions[-10:]  # Last 10 actions
        }


# Global activity log for all users
ALL_ACTIVITY_LOG = LOG_DIR / "all_activity.log"

def log_global_activity(user_id: int, username: str, action: str, details: dict = None):
    """Log to global activity file"""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "username": username,
        "action": action,
        "details": details or {}
    }
    
    with open(ALL_ACTIVITY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
