from instagram.bot import InstagramBot
from instagram.utils import load_credentials_from_csv
from instagram.scheduler import schedule_post
from instagram.interactions import InstagramInteractions
import time
import os

def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Create screenshots directory
    os.makedirs("screenshots", exist_ok=True)

    # 1. Load credentials
    try:
        username, password = load_credentials_from_csv("instagram/credentials.csv")
    except Exception as e:
        print(f"❌ Failed to load credentials: {str(e)}")
        return

    # 2. Start bot
    bot = InstagramBot(username, password)

    if bot.login():
        print("✅ Logged in successfully")
        
        # Initialize interactions
        interactions = InstagramInteractions(bot)

        while True:
            clear_screen()
            print("\nInstagram Bot Menu")
            print("-----------------")
            print("1. Schedule a post")
            print("2. Like and comment on recent posts")
            print("3. Exit")
            
            choice = input("\nChoose an action (1/2/3): ").strip()

            if choice == "1":
                clear_screen()
                print("\nSchedule a Post")
                print("--------------")
                image_path = input("Enter image path (default: instagram/uploads/photo1.png): ") or "instagram/uploads/photo1.png"
                caption = input("Enter caption (default: Scheduled post by Python Bot 🤖): ") or "Scheduled post by Python Bot 🤖"
                post_time = input("Enter post time in 24hr format (HH:MM): ").strip()
                
                if not post_time:
                    print("❌ Post time is required")
                    time.sleep(2)
                    continue
                
                schedule_post(bot, image_path, caption, post_time)
                print("\n🚀 Scheduler started, waiting for posting time...")
                try:
                    while True:
                        time.sleep(60)
                except KeyboardInterrupt:
                    print("\n🛑 Returning to main menu...")
                    time.sleep(2)
                    continue

            elif choice == "2":
                clear_screen()
                print("\nLike and Comment on Posts")
                print("-----------------------")
                target_username = input("Enter Instagram username to interact with: ").strip()
                if not target_username:
                    print("❌ Username cannot be empty")
                    time.sleep(2)
                    continue
                
                comment_text = input("Enter comment text (default 'hi'): ") or "hi"
                num_posts = input("Number of posts to interact with (default 5): ") or "5"
                
                try:
                    num_posts = int(num_posts)
                    if num_posts <= 0:
                        print("❌ Number of posts must be positive")
                        time.sleep(2)
                        continue
                except ValueError:
                    print("❌ Please enter a valid number")
                    time.sleep(2)
                    continue

                print("\nStarting interaction...")
                success = interactions.like_and_comment_on_recent_posts(
                    username=target_username,
                    comment_text=comment_text,
                    num_posts=num_posts
                )

                if success:
                    print("\n✅ Interaction completed successfully!")
                else:
                    print("\n❌ Some interactions failed")
                
                input("\nPress Enter to return to menu...")

            elif choice == "3":
                print("\n👋 Exiting...")
                break

            else:
                print("\n❌ Invalid choice, please try again")
                time.sleep(1)

    else:
        print("\n❌ Failed to login. Please check your credentials and try again")

    # Close bot
    bot.close()

if __name__ == "__main__":
    main()