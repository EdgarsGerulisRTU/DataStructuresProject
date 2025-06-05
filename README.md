# DataStructuresProject

Šī Python programma automātiski ievāc produktu informāciju no AliExpress tīmekļa veikala, atlasa tikai produktus, kuru cena nepārsniedz 10 eiro, un saglabā šos datus SQLite datubāzē. Tā ir lietderīga rīks pircējiem, kas meklē izdevīgus pirkumus, vai pētniekiem, kas analizē e-komercijas tendences.

Kā tas strādā?
Meklēšanas process:
* Programma izmanto Selenium tīmekļa pārlūku, lai piekļūtu AliExpress
* Dinamiski ielādē meklēšanas rezultātus (piemēram, "telefona aksesuāri")
* Imitē reālu lietotāju, lai izvairītos no bloķēšanas

Datu iegūšana:
* Identificē produktu elementus lapā
* Iegūst produktu nosaukumus, cenas un saites
* Automātiski konvertē cenas no vietējās valūtas uz eiro
* Atlasa tikai produktus līdz 10.00 €

Datu glabāšana:
Izveido SQLite datubāzi aliexpress_products.db
Saglabā produktus struktūrētā tabulā:
* Nosaukums
* Cena (EUR)
* Saite uz produktu

Tehniskās prasības
Obligātās bibliotēkas:
bash
pip install selenium webdriver-manager sqlite3
Sistēmas prasības:
* Python 3.7 vai jaunāks
* Google Chrome pārlūks
* Interneta pieslēgums

Kā lietot programmu?
Instalācija:
bash
# 1. Lejupielādēt programmas failu
git clone https://github.com/tavs_lietotajvards/aliexpress-scraper.git

# 2. Pāriet projekta mapē
cd aliexpress-scraper

# 3. Instalēt nepieciešamās bibliotēkas
pip install -r requirements.txt

Palaišana:
bash
python aliexpress_scraper.py

Konfigurēšana:
python
# Mainīt meklēšanas vaicājumu (scrape_aliexpress.py failā)
search_terms = [
    "telefona aksesuāri",
    "USB kabeļi",
    "atslēgas piekariņi",
    "uzlīmes"
]

# Mainīt maksimālo cenu (pēc noklusējuma 10.00 €)
scrape_aliexpress("meklējamais produkts", max_price=15.0)

## Rezultātu apskate
Datubāzes apskate:
Izmantot SQLite pārlūku (piemēram, DB Browser for SQLite)
Vai arī Python skriptu:
python
import sqlite3
conn = sqlite3.connect('aliexpress_products.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM products ORDER BY price ASC")

for row in cursor.fetchall():
    print(f"Produkts: {row[1]}")
    print(f"Cena: {row[2]:.2f}€")
    print(f"Saites: {row[3]}\n")

Datu eksportēšana:
python
import csv

conn = sqlite3.connect('aliexpress_products.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM products")

with open('produkti.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Nosaukums', 'Cena', 'Saite'])
    writer.writerows(cursor.fetchall())
    
Biežāk sastopamas problēmas
Elementi netiek atrasti:
Atjaunināt CSS selektorus failā
Pārbaudīt saglabāto lapas avotu (page_source.html)

Bloķēšana:
* Pievienot lielākus aiztures laikus (time.sleep())
* Mainīt lietotāja aģentu (user-agent)
* Izmantot rotējošus IP adreses
* Cenu konvertācijas kļūdas:
* Pārbaudīt valūtas simbolus
* Pielāgot regulārās izteiksmes
