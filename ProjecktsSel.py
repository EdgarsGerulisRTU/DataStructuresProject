from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

url = "https://www.temu.com/lv-en/channel/lightning-deals.html"

# Configure Selenium
options = Options()
options.add_argument("--headless")  # Run in background (remove to see the browser)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.get(url)

# Wait for JavaScript to load content
time.sleep(5)  # Adjust delay if needed

# Parse the rendered HTML
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Rest of your parsing logic (from previous code)
cheap_items = []
products = soup.find_all('div', class_=lambda x: x and 'product-item' in x.lower())

print(f"Number of product divs found: {len(products)}")  # Debug

for product in products:
    try:
        name = product.find('h3', class_="_2BvQbnbN").text.strip()
        integer_part = product.find('span', class_='_2de9ERAH').text.strip()
        decimal_part = product.find('span', class_='_3SrxhhHh').text.strip().replace(',', '.')
        full_price = f"{integer_part}.{decimal_part}"
        price = float(full_price)
        if price < 10.0:
            cheap_items.append({'name': name, 'price': f"€{price:.2f}"})
    except (AttributeError, ValueError):
        continue

print(f"\nFound {len(cheap_items)} items under €10:")
for idx, item in enumerate(cheap_items, 1):
    print(f"{idx}. {item['name']} - {item['price']}")