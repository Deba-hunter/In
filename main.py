python
from flask import Flask, request, render_template
import time

app = Flask(_name_)

@app.route('/')
def index():
    return '''
    <form method="POST" action="/send_message">
        Username: <input type="text" name="user"><br>
        Message: <input type="text" name="message"><br>
        Delay (seconds): <input type="number" name="delay" value="0"><br>
        <input type="submit" value="Send Message">
    </form>
    '''

@app.route('/send_message', methods=['POST'])
def send_message():
    user = request.form.get('user')
    message = request.form.get('message')
    delay = int(request.form.get('delay', 0))

    time.sleep(delay)

    # Yahan actual message bhejne ka logic daalna hoga
    print(f"Message to {user}: {message}")

    return f"Message sent to {user} after {delay} seconds!"

if _name_ == '_main_':
    app.run(debug=True)

 


def create_driver() -> webdriver.Chrome:
    """Spin‑up a fresh headless Chrome session that works on Render."""
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    # IMPORTANT: On Render the chromedriver binary is in PATH after render-build.sh
    return webdriver.Chrome(options=chrome_options)


def insta_login(driver: webdriver.Chrome, username: str, password: str) -> None:
    """Log in to Instagram with the supplied credentials."""
    driver.get("https://www.instagram.com/accounts/login/")

    wait = WebDriverWait(driver, 20)
    # Wait for user & pass fields
    user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    pass_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)

    # Optional pop‑ups (Save login info / Turn on notifications)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
    except Exception:
        pass  # If popup not present, continue

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
    except Exception:
        pass


def send_dm(driver: webdriver.Chrome, recipient: str, message: str, wait: WebDriverWait) -> bool:
    """Send a single DM, returns True if sent, False otherwise."""
    try:
        driver.get("https://www.instagram.com/direct/new/")
        # Search recipient
        to_box = wait.until(EC.presence_of_element_located((By.NAME, "queryBox")))
        to_box.clear()
        to_box.send_keys(recipient)
        time.sleep(2)  # give results time to show

        # Click on first matching result
        user_entry_xpath = f"//div[text()='@{recipient}' or text()='{recipient}']"
        wait.until(EC.element_to_be_clickable((By.XPATH, user_entry_xpath))).click()

        # Click Next button
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Next')]"))).click()

        # Locate message area & send
        msg_area = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        msg_area.send_keys(message)
        msg_area.send_keys(Keys.RETURN)
        return True
    except Exception as e:
        print(f"[ERROR] Could not message {recipient}: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1️⃣  Grab form fields
        insta_username = request.form['insta_username']
        insta_password = request.form['insta_password']
        delay = int(request.form['delay'])

        usernames_file = request.files['usernames']
        message_file = request.files['message']

        usernames = [line.strip() for line in usernames_file.read().decode('utf-8').splitlines() if line.strip()]
        message = message_file.read().decode('utf-8')

        # 2️⃣  Start headless browser
        driver = create_driver()
        wait = WebDriverWait(driver, 20)

        # 3️⃣  Login to Instagram
        try:
            insta_login(driver, insta_username, insta_password)
        except Exception as e:
            driver.quit()
            return f"❌ Login failed: {e}"

        # 4️⃣  DM Loop
        success, failed = [], []
        for user in usernames:
            if send_dm(driver, user, message, wait):
                success.append(user)
            else:
                failed.append(user)
            time.sleep(delay)

        driver.quit()

        return (
            f"✅ Sent to: {', '.join(success) if success else 'none'}<br>"
            f"❌ Failed: {', '.join(failed) if failed else 'none'}"
        )

    # GET request
    return render_template('form.html')


if __name__ == '__main__':
    # Local testing only; on Render gunicorn main:app runs instead
    app.run(host='0.0.0.0', port=5000, debug=True)
