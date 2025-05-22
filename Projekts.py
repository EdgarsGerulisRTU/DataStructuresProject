import requests
from bs4 import BeautifulSoup

url = "https://www.temu.com/lv-en/channel/lightning-deals.html"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.temu.com/'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    cheap_items = []

    products = soup.find_all('div', class_=lambda x: x and 'product-item' in x.lower())
    print(soup.prettify())
    print("Number of product divs found:", len(products))
    for product in products:
        try:
            # Product name
            name = product.find('h3', class_="_2BvQbnbN").text.strip()
            
            # Price components
            integer_part = product.find('span', class_='_2de9ERAH').text.strip()
            decimal_part = product.find('span', class_='_3SrxhhHh').text.strip().replace(',', '.')
            
            # Combine price parts with a decimal point
            full_price = f"{integer_part}.{decimal_part}"
            price = float(full_price)
            
            if price < 10.0:
                cheap_items.append({
                    'name': name,
                    'price': f"€{price:.2f}"
                })
        except AttributeError:
            continue  # Skip products with missing price components
        except ValueError:
            continue  # Skip products with invalid price format

    print(f"\nFound {len(cheap_items)} items under €10:")
    for idx, item in enumerate(cheap_items, 1):
        print(f"{idx}. {item['name']} - {item['price']}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except Exception as e:
    print(f"Error: {e}")