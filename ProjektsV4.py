import sqlite3
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Configure and return a headless Chrome driver with automatic ChromeDriver management"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def create_database():
    """Create SQLite database and products table if not exists"""
    conn = sqlite3.connect('aliexpress_products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'EUR',
            link TEXT NOT NULL UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def scrape_aliexpress(search_query, max_price=10.0):
    """Scrape AliExpress for products under max_price and store in database"""
    driver = setup_driver()
    conn = create_database()
    cursor = conn.cursor()
    
    # Prepare search URL
    search_query = search_query.replace(' ', '+')
    url = f"https://www.aliexpress.com/ssr/300002535/choiceday?spm=a2g0o.home.sale_banner.11.159e76dbTHyY9d&disableNav=YES&pha_manifest=ssr&_immersiveMode=true&businessCode=guide"
    
    try:
        driver.get(url)
        print(f"Accessing: {url}")
        
        # Wait for search results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-product-id]"))
        )
        
        # Add delay to prevent blocking
        time.sleep(3)
        
        # Find all product containers
        products = driver.find_elements(By.CSS_SELECTOR, "[data-product-id]")
        print(f"Found {len(products)} products on page")
        
        for i, product in enumerate(products, 1):
            try:
                # Extract product title and link
                title_element = product.find_element(By.CSS_SELECTOR, 'a[href*="/item/"]')
                title = title_element.text.strip()[:200]  # Truncate long titles
                link = title_element.get_attribute('href')
                
                # Extract price
                price_element = product.find_element(By.CSS_SELECTOR, ".multi--price-sale--U-S0jtj")
                price_text = price_element.text.replace('€', '').replace(',', '.').strip()
                
                # Handle price ranges (e.g., "1.99 - 5.99")
                if '-' in price_text:
                    price_text = price_text.split('-')[0].strip()
                
                # Convert to float
                price = float(re.search(r'[\d.]+', price_text).group())
                
                # Skip products above max price
                if price > max_price:
                    continue
                
                # Insert into database
                cursor.execute('''
                    INSERT OR IGNORE INTO products (title, price, link)
                    VALUES (?, ?, ?)
                ''', (title, price, link))
                
                print(f"Added product {i}: {title[:30]}... - €{price:.2f}")
                
            except (NoSuchElementException, ValueError, TypeError) as e:
                print(f"  Skipping product {i}: {str(e)}")
                continue
        
        conn.commit()
        print(f"\nScraping complete. Database updated with affordable products.")
        
    except TimeoutException:
        print("Error: Page elements didn't load in time. Try again later.")
    except Exception as e:
        print(f"Critical error: {str(e)}")
    finally:
        driver.quit()
        conn.close()

if __name__ == "__main__":
    # Example search query
    scrape_aliexpress("phone accessories")
    
    # View database content
    conn = sqlite3.connect('aliexpress_products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    print(f"\nDatabase contains {count} affordable products")
    conn.close()