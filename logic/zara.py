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
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Chromium binary yolunu belirt
    chromium_path = os.getenv("CHROME_BIN", "/usr/bin/chromium")
    options.binary_location = chromium_path

    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    # Webdriver servisini oluştur
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        if product_code_or_link.startswith("http"):
            url = product_code_or_link
        else:
            url = f"https://www.zara.com/tr/tr/search?searchTerm={product_code_or_link}"
        driver.get(url)
        time.sleep(5)
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
