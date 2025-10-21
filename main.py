from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time
import random
import logging

# Configuration
CONFIG = {
    'username': 'YOUR_INSTAGRAM_USERNAME',
    'password': 'YOUR_INSTAGRAM_PASSWORD',
    'target_account': 'rohitsharma45', #YOUR_TARGET_ACCOUNT
    'max_follows': 10,
    'follow_delay': (25, 40)
}

class InstagramFollowingBot:
    def __init__(self, config):
        self.config = config
        self.followed = 0
        self.setup_logging()
        self.setup_browser()
    
    def setup_logging(self):
        """Simple console logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.log = logging.getLogger()
    
    def setup_browser(self):
        """Initialize stealth browser"""
        opts = webdriver.ChromeOptions()
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=opts)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        self.actions = ActionChains(self.driver)
    
    def sleep(self, min_s=2, max_s=5):
        """Random human-like delay"""
        time.sleep(random.uniform(min_s, max_s))
    
    def move_mouse(self):
        """Natural mouse movement"""
        try:
            for _ in range(2):
                self.actions.move_by_offset(
                    random.randint(-50, 50), 
                    random.randint(-50, 50)
                ).perform()
            self.actions.move_by_offset(0, 0).perform()
        except:
            pass
    
    def check_blocked(self):
        """Detect Instagram blocks"""
        keywords = ['try again later', 'restrict', 'action blocked', 'wait a few']
        try:
            page = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            for keyword in keywords:
                if keyword in page:
                    self.log.error(f"BLOCKED: '{keyword}' detected!")
                    return True
        except:
            pass
        return False
    
    def type_human(self, element, text):
        """Human-like typing with occasional mistakes"""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.sleep(0.5, 1)
        element.click()
        self.sleep(0.3, 0.7)
        
        for i, char in enumerate(text):
            element.send_keys(char)
            
            # 5% chance of typo
            if random.random() < 0.05 and i < len(text) - 1:
                element.send_keys(random.choice('abcdef'))
                time.sleep(0.3)
                element.send_keys('\b')
            
            time.sleep(random.uniform(0.1, 0.3))
        
        self.sleep(0.5, 1)
    
    def js_click(self, element):
        """Force click using JavaScript"""
        self.driver.execute_script("arguments[0].click();", element)
    
    def wait_and_click(self, by, value, timeout=15, js_click=True):
        """Wait for element and click reliably"""
        try:
            elem = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            self.sleep(0.5, 1)
            
            if js_click:
                self.js_click(elem)
            else:
                elem.click()
            
            self.sleep(1, 2)
            return True
        except Exception as e:
            self.log.error(f"Click failed: {e}")
            return False
    
    def dismiss_popups(self):
        """Handle post-login popups"""
        popup_texts = ['Not Now', 'Save Info', 'Not now', 'Cancel']
        
        for text in popup_texts:
            try:
                popup = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]"))
                )
                self.js_click(popup)
                self.log.info(f"Dismissed popup: {text}")
                self.sleep(2, 3)
                return True
            except:
                continue
        return False
    
    def browse_naturally(self):
        """Simulate natural browsing"""
        self.log.info("Browsing homepage...")
        for _ in range(3):
            self.driver.execute_script(f"window.scrollBy(0, {random.randint(300, 600)})")
            self.sleep(2, 4)
            self.move_mouse()
    
    def login(self):
        """Login to Instagram"""
        self.log.info("Logging in...")
        self.driver.get('https://www.instagram.com/')
        self.driver.maximize_window()
        self.sleep(3, 5)
        
        try:
            # Username
            username = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            self.type_human(username, self.config['username'])
            
            # Password
            password = self.driver.find_element(By.NAME, "password")
            self.type_human(password, self.config['password'])
            
            # Submit
            login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            self.js_click(login_btn)
            self.sleep(6, 9)
            
            if self.check_blocked():
                return False
            
            # Handle popups
            self.dismiss_popups()
            
            self.log.info("Login successful")
            return True
            
        except Exception as e:
            self.log.error(f"Login failed: {e}")
            return False
    
    def goto_profile(self):
        """Navigate to target profile"""
        self.log.info(f"Searching for {self.config['target_account']}...")
        
        try:
            # Method 1: Try direct URL navigation (most reliable)
            self.driver.get(f"https://www.instagram.com/{self.config['target_account']}/")
            self.sleep(4, 6)
            
            # Verify we're on the correct profile
            if self.config['target_account'] in self.driver.current_url:
                self.log.info("Profile opened (direct URL)")
                return True
            
            # Method 2: Use search if direct URL failed
            self.log.info("Trying search method...")
            
            # Click search icon
            search_selectors = [
                "//a[@href='#']//span[contains(@class, 'x1lliihq')]//svg[@aria-label='Search']",
                "//svg[@aria-label='Search']/..",
                "//span[text()='Search']",
                "//a[contains(@href, '/explore')]"
            ]
            
            clicked = False
            for selector in search_selectors:
                try:
                    search_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.js_click(search_btn)
                    self.sleep(2, 3)
                    clicked = True
                    break
                except:
                    continue
            
            if not clicked:
                self.log.error("Could not click search")
                return False
            
            # Wait for and click search input
            search_input_selectors = [
                "//input[@aria-label='Search input']",
                "//input[@placeholder='Search']",
                "//input[contains(@class, 'x1lugfcp')]"
            ]
            
            search_box = None
            for selector in search_input_selectors:
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not search_box:
                self.log.error("Search box not found")
                return False
            
            # Clear any existing text and type
            self.driver.execute_script("arguments[0].value = '';", search_box)
            self.sleep(0.5, 1)
            self.type_human(search_box, self.config['target_account'])
            self.sleep(3, 5)
            
            # Click on profile from results
            profile_selectors = [
                f"//span[text()='{self.config['target_account']}']",
                f"//div[contains(text(), '{self.config['target_account']}')]",
                f"//a[contains(@href, '/{self.config['target_account']}/')]"
            ]
            
            for selector in profile_selectors:
                try:
                    profile = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.js_click(profile)
                    self.sleep(3, 5)
                    self.log.info("Profile opened (search)")
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.log.error(f"Navigation failed: {e}")
            return False
    
    def open_following(self):
        """Open following list (instead of followers)"""
        self.log.info("Opening following list...")
        
        selectors = [
            f"//a[contains(@href, '/{self.config['target_account']}/following/')]",
            "//a[contains(@href, '/following/')]",
            "//a[text()='following']",
            "//button[contains(@class, '_acan')]//span[text()='following']/.."
        ]
        
        for sel in selectors:
            try:
                link = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, sel))
                )
                self.js_click(link)
                self.sleep(4, 6)
                
                # Wait for dialog
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
                self.log.info("Following list opened")
                return True
            except Exception as e:
                self.log.debug(f"Selector failed: {sel}")
                continue
        
        self.log.error("Could not open following list")
        return False
    
    def follow_accounts(self):
        """Follow accounts from the following list with safety measures"""
        self.log.info("Starting to follow accounts from following list...")
        
        try:
            container = self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog'] div[style*='overflow']")
        except:
            self.log.error("Following container not found")
            return 0
        
        # Browse first to appear natural
        self.log.info("Browsing following list...")
        for i in range(3):
            self.driver.execute_script(f"arguments[0].scrollTop += {random.randint(300, 500)}", container)
            self.sleep(3, 5)
            self.move_mouse()
        
        # Reset to top
        self.driver.execute_script("arguments[0].scrollTop = 0", container)
        self.sleep(3, 5)
        
        # Follow accounts
        max_follows = self.config['max_follows']
        attempts = 0
        
        while self.followed < max_follows and attempts < 15:
            if self.check_blocked():
                break
            
            # Find follow buttons in the following list
            buttons = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//button[.//div[text()='Follow']]")
            
            if not buttons:
                attempts += 1
                self.driver.execute_script("arguments[0].scrollTop += 400", container)
                self.sleep(3, 5)
                continue
            
            for btn in buttons[:1]:  # Only take first button to be safe
                try:
                    if "Follow" not in btn.text:
                        continue
                    
                    # Scroll to button
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                    self.sleep(2, 3)
                    
                    # Click follow button
                    self.move_mouse()
                    self.js_click(btn)
                    self.followed += 1
                    self.log.info(f"Followed {self.followed}/{max_follows}")
                    
                    # Critical delay between follows
                    delay = random.randint(*self.config['follow_delay'])
                    self.log.info(f"Waiting {delay}s before next follow...")
                    time.sleep(delay)
                    
                    if self.check_blocked():
                        return self.followed
                    
                    # Browse between follows
                    self.driver.execute_script("arguments[0].scrollTop += 300", container)
                    self.sleep(2, 4)
                    
                    # Break if we reached the limit
                    if self.followed >= max_follows:
                        break
                        
                except Exception as e:
                    self.log.warning(f"Skipped account: {e}")
                    continue
            
            attempts = 0
        
        self.log.info(f"Completed: {self.followed} accounts followed")
        return self.followed
    
    def run(self):
        """Main execution"""
        try:
            self.log.info("=== Instagram Following Bot Starting ===")
            
            if not self.login():
                self.log.error("Login failed")
                return
            
            self.browse_naturally()
            
            if not self.goto_profile():
                self.log.error("Navigation to profile failed")
                return
            
            if not self.open_following():
                self.log.error("Failed to open following list")
                return
            
            self.follow_accounts()
            
            if self.followed > 0:
                self.log.info(f"SUCCESS: {self.followed} accounts followed from {self.config['target_account']}'s following list")
                self.log.info("Wait 3-4 hours before next run!")
            else:
                self.log.info("No accounts were followed")
            
        except KeyboardInterrupt:
            self.log.info("Stopped by user")
        except Exception as e:
            self.log.error(f"Error: {e}")
        finally:
            self.sleep(5, 8)
            self.driver.quit()
            self.log.info("=== Session Ended ===")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("INSTAGRAM FOLLOWING BOT")
    print("="*60)
    print("\nPURPOSE:")
    print(f"Follows accounts that {CONFIG['target_account']} follows")
    print("\nSAFETY RULES:")
    print("1. Wait 48+ hours after any block")
    print("2. Use account manually for 30+ min first")
    print("3. Run ONCE per day maximum")
    print(f"4. Current limit: {CONFIG['max_follows']} follows")
    print("5. Stop if any warning appears")
    print("\n" + "="*60)
    
    input("\nPress ENTER to start (Ctrl+C to cancel)...")
    
    bot = InstagramFollowingBot(CONFIG)
    bot.run()