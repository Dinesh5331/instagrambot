import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, 
                                     NoSuchElementException)

class InstagramInteractions:
    def __init__(self, bot):
        self.bot = bot
        self.driver = bot.driver

    def _random_delay(self, min=1, max=3):
        """Human-like random delay"""
        time.sleep(random.uniform(min, max))

    def _verify_profile_accessible(self, username):
        """Check if profile is accessible"""
        try:
            self.driver.get(f"https://www.instagram.com/{username}/")
            self._random_delay(3, 5)
            
            # Check for "Sorry, this page isn't available"
            if "isn't available" in self.driver.page_source:
                print(f"❌ Profile @{username} is private or doesn't exist")
                return False
                
            # Check for posts container
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article"))
            )
            return True
            
        except Exception as e:
            print(f"❌ Error accessing profile: {str(e)}")
            return False

    def like_and_comment_on_recent_posts(self, username, comment_text="hi", num_posts=5):
        """Like and comment on recent posts of a user"""
        if not self.bot.logged_in:
            print("❌ Not logged in!")
            return False

        # Verify profile first
        if not self._verify_profile_accessible(username):
            return False

        try:
            print(f"\n🔍 Scanning @{username}'s profile...")
            self._random_delay(5, 8)  # Initial delay
            
            # Scroll to load more posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self._random_delay(2, 3)
            
            # Get posts with retry logic
            posts = []
            attempts = 0
            while len(posts) < num_posts and attempts < 3:
                posts = self.driver.find_elements(
                    By.XPATH, "//article//a[contains(@href, '/p/')]"
                )[:num_posts]
                if len(posts) < num_posts:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    self._random_delay(2, 3)
                    attempts += 1

            if not posts:
                print(f"❌ No posts found after {attempts} attempts")
                return False

            print(f"📸 Found {len(posts)} posts to interact with")

            for i, post in enumerate(posts, 1):
                try:
                    post_url = post.get_attribute("href")
                    print(f"\n📝 Processing post {i}/{len(posts)}: {post_url}")
                    
                    # Open post in new tab
                    self.driver.execute_script("window.open(arguments[0]);", post_url)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self._random_delay(3, 5)

                    # Like the post
                    try:
                        like_buttons = self.driver.find_elements(
                            By.XPATH, "//*[local-name()='svg'][@aria-label='Like']/ancestor::button"
                        )
                        if like_buttons:
                            like_button = like_buttons[0]
                            svg = like_button.find_element(By.XPATH, ".//*[local-name()='svg']")
                            liked = "unlike" in svg.get_attribute("aria-label").lower()
                            
                            if not liked:
                                like_button.click()
                                print("❤️ Liked post")
                                self._random_delay(1, 2)
                            else:
                                print("ℹ️ Post already liked")
                    except Exception as e:
                        print(f"⚠️ Couldn't like post: {str(e)}")
                        self.bot.take_screenshot(f"like_error_{i}")

                    # Add comment
                    try:
                        comment_box = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//textarea[@placeholder='Add a comment...']")
                            )
                        )
                        comment_box.click()
                        self._random_delay(0.5, 1)
                        
                        # Clear existing text if any
                        comment_box.clear()
                        self._random_delay(0.2, 0.5)
                        
                        # Type comment
                        for char in comment_text:
                            comment_box.send_keys(char)
                            time.sleep(random.uniform(0.05, 0.15))
                        
                        # Post comment
                        post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[contains(., 'Post')]")
                            )
                        )
                        post_button.click()
                        print(f"💬 Commented '{comment_text}'")
                        self._random_delay(2, 3)
                    except Exception as e:
                        print(f"⚠️ Couldn't comment on post: {str(e)}")
                        self.bot.take_screenshot(f"comment_error_{i}")

                    # Close the tab and switch back
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self._random_delay(10, 15)  # Important delay between posts

                except Exception as e:
                    print(f"⚠️ Error processing post {i}: {str(e)}")
                    self.bot.take_screenshot(f"post_error_{i}")
                    continue

            print(f"\n✅ Successfully processed {len(posts)} posts")
            return True

        except Exception as e:
            print(f"❌ Error processing {username}'s posts: {str(e)}")
            self.bot.take_screenshot("interaction_error")
            return False