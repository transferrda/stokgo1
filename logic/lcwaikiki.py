from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def check_product(product_code_or_link):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("--headless=new")  # İstersen başsız da çalışır

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        if product_code_or_link.startswith("http"):
            url = product_code_or_link
        else:
            url = f"https://www.lcw.com/arama?q={product_code_or_link}"

        driver.get(url)

        # Çerez kabul et (varsa)
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
        except:
            pass

        # Ürün kartlarını bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-optionid]"))
        )

        links = driver.find_elements(By.CSS_SELECTOR, "a[data-optionid]")
        if links:
            href = links[0].get_attribute("href")
            if not href.startswith("http"):
                href = "https://www.lcw.com" + href
            return {"available": True, "url": href}
        else:
            return {"available": False, "url": None}

    except Exception as e:
        print("LC Waikiki Hatası:", e)
        return {"available": False, "url": None}
    finally:
        driver.quit()
