# test_post.py
from instagram.bot import InstagramBot
from instagram.utils import load_credentials_from_csv

def test_post():
    username, password = load_credentials_from_csv("instagram/credentials.csv")
    bot = InstagramBot(username, password)
    
    if bot.login():
        print("Testing photo upload...")
        success = bot.post_photo(
            "instagram/uploads/photo1.png",  # Your test image
            "Test post from script"       # Test caption
        )
        print("Success!" if success else "Failed!")
    
    bot.close()

if __name__ == "__main__":
    test_post()