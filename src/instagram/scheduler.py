# instagram/scheduler.py
import schedule
import time
import threading
from datetime import datetime

def schedule_post(bot, image_path, caption, post_time):
    """Fully reliable scheduler with retries"""
    
    def job():
        print(f"\n⏰ ATTEMPTING POST AT {datetime.now().strftime('%H:%M:%S')}")
        
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"🔄 Attempt {attempt}/{max_retries}")
                if bot.post_photo(image_path, caption):
                    print(f"✅ POSTED AT {datetime.now().strftime('%H:%M:%S')}")
                    return
                time.sleep(30)  # Wait between retries
            except Exception as e:
                print(f"⚠️ Attempt {attempt} failed: {str(e)}")
                time.sleep(60)
        
        print("❌ POST FAILED AFTER MAX RETRIES")

    # Validate time format
    try:
        schedule.every().day.at(post_time).do(
            lambda: threading.Thread(target=job).start()
        )
        print(f"\n⏰ SCHEDULER ACTIVE | Next post at {post_time}")
    except Exception as e:
        print(f"❌ INVALID TIME: {post_time} | Use HH:MM (24h)")

    # Background scheduler
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(30)

    threading.Thread(target=run_scheduler, daemon=True).start()