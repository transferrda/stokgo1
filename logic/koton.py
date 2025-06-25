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
    # options.add_argument("--headless")  # İstersen aç kapa

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        if product_code_or_link.startswith("http"):
            url = product_code_or_link
        else:
            url = f"https://www.koton.com/list/?search_text={product_code_or_link}"

        driver.get(url)

        # Cookie popup varsa kapatmaya çalış
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-consent-accept"))
            ).click()
        except:
            pass

        # Ürün kartlarının yüklenmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.js-product-link"))
        )

        products = driver.find_elements(By.CSS_SELECTOR, "a.js-product-link")
        if products:
            href = products[0].get_attribute("href")
            if not href.startswith("http"):
                href = "https://www.koton.com" + href
            return {"available": True, "url": href}
        else:
            return {"available": False, "url": None}

    except Exception as e:
        print("Koton Hatası:", e)
        return {"available": False, "url": None}
    finally:
        driver.quit()

if __name__ == "__main__":
    # Deneme ürün kodu, değiştirebilirsin
    product_code = "5SAM60023HW"
    result = check_product(product_code)
    print(result)
