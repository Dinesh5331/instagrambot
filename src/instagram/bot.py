import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 20)
        self.logged_in = False

    def _init_driver(self):
        """Initialize ChromeDriver with enhanced settings"""
        options = Options()

        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Performance
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--enable-unsafe-webgpu")
        options.add_argument("--enable-unsafe-swiftshader")

        service = Service(executable_path="./chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def _random_delay(self, min=1, max=3):
        """Human-like random delay"""
        time.sleep(random.uniform(min, max))

    def login(self):
        """More reliable login method"""
        try:
            print("🌐 Loading Instagram...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self._random_delay(2, 4)

            # Wait for login form or homepage
            WebDriverWait(self.driver, 20).until(
                lambda d: d.find_elements(By.NAME, "username") or 
                          d.find_elements(By.XPATH, "//nav")
            )

            # Already logged in
            if self.driver.find_elements(By.XPATH, "//nav"):
                print("✅ Already logged in")
                self.logged_in = True
                return True

            print("🔑 Entering credentials...")
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")

            for char in self.username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            for char in self.password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            self._random_delay(3, 5)

            self._dismiss_popups()

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//nav"))
            )
            print("✅ Login successful!")
            self.logged_in = True
            return True

        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            return False

    def _dismiss_popups(self):
        """Handle all possible popups"""
        popups = [
            ("Save Info", "//button[contains(., 'Not Now')]"),
            ("Notifications", "//button[contains(., 'Not Now')]"),
            ("Use App", "//button[contains(., 'Cancel')]")
        ]

        for name, xpath in popups:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                ).click()
                print(f"🗑️ Dismissed '{name}' popup")
                self._random_delay()
            except:
                continue

    def post_photo(self, image_path, caption):
        """Post a photo to Instagram"""
        print("📤 Starting photo upload process...")
        try:
            self.driver.get("https://www.instagram.com/")
            self._random_delay(2, 4)

            # Click create (+) button
            create_btn_xpath = "//svg[@aria-label='New post']/ancestor::button"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, create_btn_xpath))).click()
            self._random_delay(2, 3)

            # Upload file
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@accept='image/jpeg,image/png']")))
            file_input.send_keys(os.path.abspath(image_path))
            self._random_delay(2, 3)

            # Click Next button
            next_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']/..")))
            next_btn.click()
            self._random_delay(2, 3)

            # Enter caption
            caption_area = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            caption_area.clear()
            caption_area.send_keys(caption)
            self._random_delay()

            # Share
            share_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Share']/..")))
            share_btn.click()
            self._random_delay(5, 6)

            print("✅ Post uploaded successfully.")

        except Exception as e:
            self.take_screenshot("post_error")
            print(f"❌ Failed to upload post: {str(e)}")
            raise

    def take_screenshot(self, name="error"):
        """Save screenshot for debugging"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        self.driver.save_screenshot(filename)
        print(f"📸 Saved screenshot as {filename}")

    def close(self):
        """Graceful shutdown"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                print("🛑 Browser closed")
        except:
            pass
