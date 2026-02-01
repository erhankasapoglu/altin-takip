from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


SHEET_ID = "16SBlQGk7KF05ZniHJmlFk1SUg0IYakwUWc4ZbkiI4DE"
JSON_KEY = "altin-takip-486119-70c66dd43ae4.json"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1


options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.altinkaynak.com/canli-kurlar/altin")
time.sleep(8)


rows = driver.find_elements(By.XPATH, "//table//tbody//tr")

alis = satis = None

for row in rows:
    text = row.text
    if "Gram" in text and "24" in text:
        tds = row.find_elements(By.TAG_NAME, "td")
        alis = tds[1].text
        satis = tds[2].text
        break

driver.quit()

if not alis or not satis:
    raise Exception("❌ Gram Altın bulunamadı")


sheet.update("A1:C1", [["Ürün", "Alış", "Satış"]])
sheet.update("A2:C2", [["Gram Altın", alis, satis]])

print("✅ Gram Altın başarıyla güncellendi")
print("Alış:", alis, "Satış:", satis)
