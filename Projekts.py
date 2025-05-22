import requests
from bs4 import BeautifulSoup

# Temu Lightning Deals URL
url = "https://www.temu.com/lv-en/channel/lightning-deals.html"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
cheap_items = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find product containers - adjust class based on actual structure
    products = soup.find_all('div', class_='product-item')  # Update class name
    
    for product in products:
        name_tag = product.find('h3', class_='product-name')  # Update class
        price_tag = product.find('span', class_='current-price')  # Update class
        
        if name_tag and price_tag:
            name = name_tag.text.strip()
            price_str = price_tag.text.strip()
            
            # Clean price (remove currency symbol and commas)
            try:
                price = float(price_str.replace('€', '').replace(',', '').strip())
            except ValueError:
                continue
            
            if price < 10.0:
                cheap_items.append({
                    'name': name,
                    'price': price
                })

    # Print results
    print(f"Found {len(cheap_items)} items under €10:")
    for item in cheap_items:
        print(f"{item['name']} - €{item['price']:.2f}")
else:
    print("Failed to fetch page")