from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import tempfile
import time
import os

def check_product(product_code_or_link):
    options = Options()
    # Headless modda yeni chrome başlatma komutu
    options.add_argument("--headless=new")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")

    # Chromium binary yolunu belirt (Render veya Docker ortamında kullanmak için)
    chromium_path = os.getenv("CHROME_BIN", "/usr/bin/chromium-browser")
    options.binary_location = chromium_path

    # Geçici kullanıcı profili klasörü (Render platformu için önerilir)
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    # ChromeDriver servisini webdriver_manager ile yükle ve başlat
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        if product_code_or_link.startswith("http"):
            url = product_code_or_link
        else:
            url = f"https://www.zara.com/tr/tr/search?searchTerm={product_code_or_link}"

        driver.get(url)
        time.sleep(5)  # Sayfanın yüklenmesi için bekle

        products = driver.find_elements(By.CSS_SELECTOR, "a.product-link")
        if products:
            link = products[0].get_attribute("href")
            return {"available": True, "url": link}
        return {"available": False, "url": None}
    except Exception as e:
        print("Hata:", e)
        return {"available": False, "url": None}
    finally:
        driver.quit()
