import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def run_job_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # --- התיקון המרכזי ---
    # אנחנו יודעים שהדפדפן הוא גרסה 144.
    # נכריח את webdriver-manager להוריד את הדרייבר התואם.
    # נשתמש בגרסה ספציפית כדי למנוע בלבול.
    driver_version = "144.0.7559.109" # או גרסה קרובה מאוד
    service = Service(ChromeDriverManager(driver_version=driver_version).install())
    
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
