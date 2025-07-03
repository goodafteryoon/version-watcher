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
CHROME_URL = os.getenv("URL")
WHALE_URL = os.getenv("WHALE_URL")

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

    elements = driver.find_elements(By.XPATH, '//div[contains(text(),"버전") or contains(text(),"Version")]/following-sibling::div')
    if not elements:
        print(driver.page_source)
        driver.quit()
        raise Exception("크롬 스토어 버전 정보를 찾을 수 없습니다.")

    version_value = elements[0].text.strip()
    driver.quit()
    return version_value

def fetch_whale_version():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(options=options)

    driver.get(WHALE_URL)
    time.sleep(10)

    # 네이버 웨일 스토어 버전 XPath 예시 (필요시 수정)
    elements = driver.find_elements(By.XPATH, '//em[contains(text(),"버전")]/following-sibling::em')
    if not elements:
        # 혹은 아래 XPath 시도 (실제 페이지 확인 필요)
        elements = driver.find_elements(By.XPATH, '//span[contains(text(),"버전")]/following-sibling::span')
    if not elements:
        print(driver.page_source)
        driver.quit()
        raise Exception("웨일 스토어 버전 정보를 찾을 수 없습니다.")

    version_value = elements[0].text.strip()
    driver.quit()
    return version_value

def load_last_versions():
    if not os.path.exists(VERSION_FILE):
        return (None, None)
    with open(VERSION_FILE, "r") as f:
        lines = f.readlines()
        if len(lines) != 2:
            return (None, None)
        return (lines[0].strip(), lines[1].strip())

def save_versions(chrome_version, whale_version):
    with open(VERSION_FILE, "w") as f:
        f.write(f"{chrome_version}\n{whale_version}\n")

def send_slack_notification(chrome_version, whale_version):
    message = {
        "text": (
            "🔔 Sentencify 확장 버전이 업데이트되었습니다!\n"
            f"- **Chrome Web Store:** {chrome_version}\n"
            f"- **Naver Whale Store:** {whale_version}"
        )
    }
    res = requests.post(SLACK_WEBHOOK_URL, json=message)
    if res.status_code != 200:
        raise Exception(f"슬랙 알림 실패: {res.text}")

def main():
    print("🔍 최신 버전 확인 중...")

    chrome_version = fetch_chrome_version()
    print(f"✅ 크롬 스토어 버전: {chrome_version}")

    whale_version = fetch_whale_version()
    print(f"✅ 웨일 스토어 버전: {whale_version}")

    last_chrome, last_whale = load_last_versions()

    if chrome_version != last_chrome or whale_version != last_whale:
        print("🚀 버전이 업데이트되었습니다!")
        send_slack_notification(chrome_version, whale_version)
        save_versions(chrome_version, whale_version)
    else:
        print("ℹ️ 버전 변경 없음.")

if __name__ == "__main__":
    main()