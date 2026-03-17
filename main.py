import os
import time
import schedule
from dotenv import load_dotenv
from openai import OpenAI
from instagrapi import Client

load_dotenv()

# OpenAI
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Instagram (Threads)
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()

try:
    cl.login(IG_USERNAME, IG_PASSWORD)
except Exception as e:
    print("Login error:", e)

def generate_post():
    prompt = """
    Напиши короткий лайфхак (до 180 символов).
    Добавь эмодзи.
    Сделай его вирусным.
    """

    response = client_ai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def job():
    try:
        text = generate_post()
        print("POST:", text)

        cl.thread_create(text)

        print("✅ Posted")

    except Exception as e:
        print("❌ Error:", e)


# тестовый пост
print("🚀 Test post")
job()

# расписание (UTC!)
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("16:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
