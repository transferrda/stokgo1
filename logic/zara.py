from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import tempfile

def check_product(product_code_or_link):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")            # sandbox kapatıldı
    options.add_argument("--disable-dev-shm-usage") # shared memory kullanımını devre dışı bırak
    options.add_argument("--disable-gpu")            # GPU kapalı (bazı sistemlerde gerekebilir)
    
    # Geçici benzersiz user-data-dir (bunu ekle, Render hatası için)
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=options)

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
