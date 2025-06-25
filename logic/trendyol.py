from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def check_product(product_code_or_link):
    options = Options()
    options.headless = True  # Tarayıcı arka planda çalışır
    driver = webdriver.Chrome(options=options)

    try:
        if product_code_or_link.startswith("http"):
            url = product_code_or_link
        else:
            url = f"https://www.trendyol.com/sr?q={product_code_or_link}"
        driver.get(url)
        time.sleep(5)  # Sayfanın JS ile tam yüklenmesi için bekle
        products = driver.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr a")
        if products:
            link = products[0].get_attribute("href")
            return {"available": True, "url": link}
        else:
            return {"available": False, "url": None}
    except Exception as e:
        print("Hata:", e)
        return {"available": False, "url": None}
    finally:
        driver.quit()
