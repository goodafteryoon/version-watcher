import requests
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 환경 변수 로드
load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
CHROME_URL = os.getenv("CHROME_URL")

# 버전 기록 파일
VERSION_FILE = "last_version.txt"

def fetch_chrome_version():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=options)
    driver.get(CHROME_URL)
    time.sleep(10)

    elements = driver.find_elements(
        By.XPATH,
        '//div[contains(text(),"버전") or contains(text(),"Version")]/following-sibling::div'
    )
    if not elements:
        print(driver.page_source)
        driver.quit()
        raise Exception("크롬 스토어 버전 정보를 찾을 수 없습니다.")

    version_value = elements[0].text.strip()
    driver.quit()
    return version_value

def load_last_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def save_version(version):
    with open(VERSION_FILE, "w") as f:
        f.write(version)

def send_slack_notification(version):
    message = {
        "text": (
            "🔔 Sentencify 크롬 확장 버전이 업데이트되었습니다!\n"
            f"- **Chrome Web Store:** {version}"
        )
    }
    res = requests.post(SLACK_WEBHOOK_URL, json=message)
    if res.status_code != 200:
        raise Exception(f"슬랙 알림 실패: {res.text}")

def main():
    print("🔍 최신 버전 확인 중...")
    chrome_version = fetch_chrome_version()
    print(f"✅ 크롬 스토어 버전: {chrome_version}")

    last_version = load_last_version()
    if chrome_version != last_version:
        print("🚀 버전이 업데이트되었습니다!")
        send_slack_notification(chrome_version)
        save_version(chrome_version)
    else:
        print("ℹ️ 버전 변경 없음.")

if __name__ == "__main__":
    main()