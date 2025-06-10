from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# CONFIG
USERNAME = 'your_instagram_username'
PASSWORD = 'your_instagram_password'
DELAY_SECONDS = 10  # delay between messages

# Read message from text file
with open('message.txt', 'r', encoding='utf-8') as file:
    MESSAGE = file.read().strip()

# Read usernames from file
with open('usernames.txt', 'r', encoding='utf-8') as file:
    usernames = [line.strip() for line in file if line.strip()]

# Start Selenium
driver = webdriver.Chrome()  # Make sure chromedriver is in PATH
driver.get("https://www.instagram.com/accounts/login/")

time.sleep(5)

# Login
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)

time.sleep(5)

# Bypass popups
try:
    not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
    not_now.click()
except:
    pass

time.sleep(5)

# Messaging users
for user in usernames:
    driver.get(f"https://www.instagram.com/direct/new/")
    time.sleep(5)

    to_input = driver.find_element(By.NAME, 'queryBox')
    to_input.send_keys(user)
    time.sleep(2)

    try:
        user_result = driver.find_element(By.XPATH, f"//div[text()='{user}']")
        user_result.click()
    except:
        print(f"❌ User not found: {user}")
        continue

    time.sleep(2)
    next_button = driver.find_element(By.XPATH, "//div[contains(text(),'Next')]")
    next_button.click()

    time.sleep(5)
    message_box = driver.find_element(By.TAG_NAME, 'textarea')
    message_box.send_keys(MESSAGE)
    message_box.send_keys(Keys.RETURN)

    print(f"✅ Sent message to {user}")
    time.sleep(DELAY_SECONDS)

driver.quit()
