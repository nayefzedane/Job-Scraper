import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os # ייבוא חדש

def run_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # מומלץ להוסיף בסביבת לינוקס
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # בדיקה אם אנחנו רצים בסביבת Streamlit Cloud
    if "STREAMLIT_IS_RUNNING" in os.environ:
        # נתיבים קבועים בסביבת Streamlit Cloud
        CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
        CHROME_PATH = "/usr/bin/chromium-browser"
        chrome_options.binary_location = CHROME_PATH
        service = Service(executable_path=CHROME_DRIVER_PATH)
    else:
        # שימוש ב-webdriver-manager לסביבה מקומית (כמו המחשב שלך)
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())

    URL = "https://remoteok.com/remote-python-jobs"
    
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options )
        driver.get(URL)
        time.sleep(5)

        jobs = driver.find_elements(By.XPATH, "//tr[@data-id]")
        job_data = []

        for job in jobs:
            try:
                title = job.find_element(By.TAG_NAME, 'h2').text.strip()
                company = job.find_element(By.TAG_NAME, 'h3').text.strip()
                tags_elements = job.find_elements(By.CLASS_NAME, 'location')
                tags = [tag.text for tag in tags_elements if tag.text]
                job_data.append([title, company, ', '.join(tags)])
            except Exception:
                continue

        csv_file = 'remoteok_python_jobs.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Job Title', 'Company', 'Tags'])
            writer.writerows(job_data)
            
        return csv_file

    finally:
        if driver:
            driver.quit()
