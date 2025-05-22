import requests
from bs4 import BeautifulSoup

# adrese = "https://www.ikea.lv/lv/rooms/dzivojama-istaba/divani/auduma-divani"
adrese = "https://www.ikea.lv/lv/last-chance"

# https://www.ikea.lv/lv/rooms/dzivojama-istaba/divani/auduma-divani?&product-room=product&page=2&order=RECOMMENDED

lapa = requests.get(adrese)
# print(lapa.status_code)
if lapa.status_code == 200:
    lapas_saturs = BeautifulSoup(lapa.content, "html.parser")
    # print(lapas_saturs.prettify())
    atradu_card = lapas_saturs.find_all(class_="card")
    print(len(atradu_card))
    atrad_itemBlock = lapas_saturs.find_all(class_="itemBlock")
    print(len(atrad_itemBlock))
    preces_lapa = []
    for prece in atrad_itemBlock:
        konkreta_prece = []
        kermenis = prece.find(class_="card-body")
        # print(kermenis.prettify())
        nosaukums = kermenis.find("h3")
        print(nosaukums.contents) # iespēja paņemt visu kas ir iekšā tag, t.sk. kodu
        print(nosaukums.string) # iespēja paņemt tikai tekstu, kas ir iekšā tag
        nosaukums = nosaukums.string
        konkreta_prece.append(nosaukums)
        fakti = prece.find("h4", class_="itemFacts")
        # print(fakti.prettify())
        fakti = fakti.string
        konkreta_prece.append(fakti)
        
        cenas_info = prece.find(class_="itemPriceBox").find("p").find("span")
        cena = 0
        try:
            print(cenas_info.attrs["data-price"])
            cena = cenas_info.attrs["data-price"]
        except:
            try:
                print(cenas_info.attrs["data-pricefamily"])
                cena = cenas_info.attrs["data-pricefamily"]
            except:
                # print(cenas_info.prettify())
                vesela_dala = cenas_info.find(class_= "price__integer")
                # print(vesela_dala.string)
                vesela_dala = vesela_dala.string
                komata_dala = cenas_info.find(class_= "price__decimals")
                # print(komata_dala.prettify())
                # print(komata_dala.contents[-1])
                komata_dala = komata_dala.contents[-1]
                # print(komata_dala.string)
                if vesela_dala.isdigit():
                   cena = vesela_dala+"."
                else:
                    cena = "0."
                if komata_dala.isdigit(): 
                     cena += komata_dala
                else:
                    cena += "00"
                print(cena)
        konkreta_prece.append(cena)
        # print(konkreta_prece)
        preces_lapa.append(konkreta_prece)
        
        
    print()
    print(preces_lapa)