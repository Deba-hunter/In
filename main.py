from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        insta_username = request.form['insta_username']
        insta_password = request.form['insta_password']
        delay = int(request.form['delay'])

        usernames_file = request.files['usernames']
        message_file = request.files['message']

        usernames = usernames_file.read().decode('utf-8').splitlines()
        message = message_file.read().decode('utf-8')

        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

        driver = webdriver.Chrome(options=chrome_options)

        # login and messaging logic goes here
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        # login steps here...

        driver.quit()

        return "✅ Messages sent!"

    return render_template('form.html')
    