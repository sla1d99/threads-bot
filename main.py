import os
import time
import schedule
from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")


def generate_post():
    prompt = "Напиши короткий лайфхак до 180 символов с эмодзи"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def post_to_threads(text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Открываем Threads
        page.goto("https://www.threads.net/login")

        time.sleep(5)

        # Ввод логина
        page.fill('input[name="username"]', IG_USERNAME)
        page.fill('input[name="password"]', IG_PASSWORD)

        page.click('button[type="submit"]')

        time.sleep(10)

        # Нажимаем "Create"
        page.goto("https://www.threads.net/")

        time.sleep(5)

        # Поле ввода поста (может меняться!)
        page.click('text="Start a thread"')

        time.sleep(2)

        page.fill('textarea', text)

        time.sleep(2)

        page.click('text="Post"')

        print("✅ Posted:", text)

        browser.close()


def job():
    try:
        text = generate_post()
        print("POST:", text)
        post_to_threads(text)
    except Exception as e:
        print("ERROR:", e)


print("🚀 TEST POST")
job()

schedule.every().day.at("08:00").do(job)
schedule.every().day.at("16:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
