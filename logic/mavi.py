from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def check_product(product_code_or_link):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    # options.add_argument("--headless")  # İstersen kapalı pencere açar

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        if product_code_or_link.startswith("http"):
            url = product_code_or_link
        else:
            url = f"https://www.mavi.com/search/?text={product_code_or_link}"

        driver.get(url)

        # Popup varsa kapat
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
            ).click()
        except:
            pass

        # Ürün kartlarını bekle
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-card-info"))
        )

        products = driver.find_elements(By.CSS_SELECTOR, "a.product-card-info")
        if products:
            href = products[0].get_attribute("href")
            if not href.startswith("http"):
                href = "https://www.mavi.com" + href
            return {"available": True, "url": href}
        else:
            return {"available": False, "url": None}

    except Exception as e:
        print("Mavi Hatası:", e)
        return {"available": False, "url": None}
    finally:
        driver.quit()
