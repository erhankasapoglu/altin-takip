import os
import json
import time
from datetime import datetime, timezone, timedelta

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

SHEET_ID = "16SBlQGk7KF05ZniHJmlFk1SUg0IYakwUWc4ZbkiI4DE"

# ---- GOOGLE CREDS (SECRET'TAN) ----
google_creds = json.loads(os.environ["GOOGLE_CREDENTIALS"])

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# ---- CHROME OPTIONS ----
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

driver.get("https://www.altinkaynak.com/canli-kurlar/altin")
time.sleep(10)

rows = driver.find_elements(By.XPATH, "//table//tbody//tr")

alis = satis = None

for row in rows:
    if "Gram" in row.text and "24" in row.text:
        tds = row.find_elements(By.TAG_NAME, "td")
        alis = tds[1].text
        satis = tds[2].text
        break

driver.quit()

if not alis or not satis:
    raise Exception("❌ Gram Altın bulunamadı")

# ---- TÜRKİYE SAATİ (UTC+3) ----
turkey_time = datetime.now(timezone.utc) + timedelta(hours=3)
formatted_time = turkey_time.strftime("%d.%m.%Y %H:%M")

# ---- SHEETS'E YAZ ----
sheet.update(
    "A1:D1",
    [["Ürün", "Alış", "Satış", "Son Güncelleme"]]
)

sheet.update(
    "A2:D2",
    [["Gram Altın", alis, satis, formatted_time]]
)

print("✅ Güncellendi:", alis, satis, formatted_time)
