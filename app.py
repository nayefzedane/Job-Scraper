import streamlit as st
import pandas as pd
import os
# התיקון כאן: שימוש בשם הפונקציה הנכון
from scraper_logic import run_job_scraper 

# הגדרת כותרת ומידע בסיסי על האפליקציה
st.set_page_config(page_title="Python Job Scraper", page_icon="🤖")
st.title("🤖 Python Remote Job Scraper")
st.write("This app scrapes the latest Python jobs from remoteok.com.")
st.write("Click the button below to start scraping.")

# יצירת כפתור להפעלת הסקרייפר
if st.button("Scrape Latest Python Jobs"):
    
    # הצגת הודעת "אנא המתן" בזמן שהסקריפט רץ
    with st.spinner("Scraping in progress... This might take 20-30 seconds."):
        try:
            # קריאה לפונקציה שמפעילה את הסקרייפר
            csv_file_path = run_job_scraper()
            
            # קריאת המידע מקובץ ה-CSV שנוצר
            df = pd.read_csv(csv_file_path)
            
            st.success(f"Done! Found {len(df)} jobs.")
            
            # הצגת התוצאות בטבלה אינטראקטיבית
            st.dataframe(df)
            
            # מתן אפשרות להורדת הקובץ
            with open(csv_file_path, "rb") as file:
                st.download_button(
                    label="Download data as CSV",
                    data=file,
                    file_name=csv_file_path,
                    mime='text/csv',
                )

        except Exception as e:
            st.error(f"An error occurred during scraping: {e}")
