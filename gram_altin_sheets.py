import requests
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# ---------- GOOGLE SHEETS ----------
SHEET_ID = "16SBlQGk7KF05ZniHJmlFk1SUg0IYakwUWc4ZbkiI4DE"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# SECRET'TAN JSON OKU
google_json = json.loads(os.environ["GOOGLE_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_json, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# ---------- ALTINKAYNAK GERÇEK AJAX ENDPOINT ----------
URL = "https://www.altinkaynak.com/Home/GetGoldPrices"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.altinkaynak.com/canli-kurlar/altin"
}

resp = requests.get(URL, headers=headers, timeout=10)
resp.raise_for_status()
data = resp.json()

# ---------- SADECE GRAM ALTIN (24 AYAR) ----------
gram = next(
    x for x in data["data"]
    if x["name"].lower().startswith("gram")
)

alis = gram["buy"]
satis = gram["sell"]

# ---------- SHEETS'E YAZ ----------
sheet.update("A1:C1", [["Ürün", "Alış", "Satış"]])
sheet.update("A2:C2", [["Gram Altın", alis, satis]])

print("✅ Gram Altın güncellendi")
print("Alış:", alis, "Satış:", satis)
