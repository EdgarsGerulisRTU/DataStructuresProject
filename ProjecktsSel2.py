from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

url = "https://www.temu.com/lv-en/channel/lightning-deals.html"

# Configure browser options
options = Options()
options.binary_location = "C:/Users/Valdis/AppData/Local/Programs/Opera GX/opera.exe"  # Opera GX path
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/118.0.0.0")

# Set up automatic ChromeDriver management
service = Service(ChromeDriverManager().install())

# Initialize browser
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the page
    driver.get(url)
    print("Page loaded successfully")
    
    # Wait for dynamic content to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='product-item']"))
    )
    print("Products container loaded")
    
    # Add extra delay for safety
    time.sleep(2)
    
    # Save rendered HTML for debugging
    with open("temu_rendered.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    # Parse products
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all('div', class_=lambda x: x and 'product-item' in x.lower())
    print(f"Products found: {len(products)}")
    
    cheap_items = []
    for product in products:
        try:
            # Extract product name
            name = product.find('h3', class_="_2BvQbnbN").text.strip()
            
            # Extract price components
            integer_part = product.find('span', class_='_2de9ERAH').text.strip()
            decimal_part = product.find('span', class_='_3SrxhhHh').text.strip().replace(',', '.')
            
            # Combine price parts
            full_price = f"{integer_part}.{decimal_part}"
            price = float(full_price)
            
            if price < 10.0:
                cheap_items.append({
                    'name': name,
                    'price': f"€{price:.2f}"
                })
        except (AttributeError, ValueError) as e:
            continue

    print(f"\nFound {len(cheap_items)} items under €10:")
    for idx, item in enumerate(cheap_items, 1):
        print(f"{idx}. {item['name']} - {item['price']}")

except Exception as e:
    print(f"Error occurred: {str(e)}")
finally:
    # Clean up
    driver.quit()
    print("Browser closed")