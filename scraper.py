import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

CASE_LINKS = {
    "Revolution Case": "https://steamcommunity.com/market/listings/730/Revolution%20Case",
    "Kilowatt Case": "https://steamcommunity.com/market/listings/730/Kilowatt%20Case",
    "Recoil Case": "https://steamcommunity.com/market/listings/730/Recoil%20Case",
    "Dreams & Nightmares Case": "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case",
    "Snakebite Case": "https://steamcommunity.com/market/listings/730/Snakebite%20Case",
    "Operation Broken Fang Case": "https://steamcommunity.com/market/listings/730/Operation%20Broken%20Fang%20Case",
    "Fracture Case": "https://steamcommunity.com/market/listings/730/Fracture%20Case",
    "Prisma Case": "https://steamcommunity.com/market/listings/730/Prisma%20Case",
    "Prisma 2 Case": "https://steamcommunity.com/market/listings/730/Prisma%202%20Case",
    "Horizon Case": "https://steamcommunity.com/market/listings/730/Horizon%20Case",
    "Danger Zone Case": "https://steamcommunity.com/market/listings/730/Danger%20Zone%20Case",
    "Clutch Case": "https://steamcommunity.com/market/listings/730/Clutch%20Case",
    "Spectrum Case": "https://steamcommunity.com/market/listings/730/Spectrum%20Case",
    "Spectrum 2 Case": "https://steamcommunity.com/market/listings/730/Spectrum%202%20Case",
    "Glove Case": "https://steamcommunity.com/market/listings/730/Glove%20Case",
    "Chroma Case": "https://steamcommunity.com/market/listings/730/Chroma%20Case",
    "Chroma 2 Case": "https://steamcommunity.com/market/listings/730/Chroma%202%20Case",
    "Chroma 3 Case": "https://steamcommunity.com/market/listings/730/Chroma%203%20Case",
    "Falchion Case": "https://steamcommunity.com/market/listings/730/Falchion%20Case",
    "Gamma Case": "https://steamcommunity.com/market/listings/730/Gamma%20Case",
    "Gamma 2 Case": "https://steamcommunity.com/market/listings/730/Gamma%202%20Case",
    "Shadow Case": "https://steamcommunity.com/market/listings/730/Shadow%20Case",
    "Huntsman Weapon Case": "https://steamcommunity.com/market/listings/730/Huntsman%20Weapon%20Case",
    "Operation Phoenix Weapon Case": "https://steamcommunity.com/market/listings/730/Operation%20Phoenix%20Weapon%20Case",
    "Operation Breakout Weapon Case": "https://steamcommunity.com/market/listings/730/Operation%20Breakout%20Weapon%20Case",
    "Operation Wildfire Case": "https://steamcommunity.com/market/listings/730/Operation%20Wildfire%20Case",
    "Operation Hydra Case": "https://steamcommunity.com/market/listings/730/Operation%20Hydra%20Case",
    "Operation Vanguard Weapon Case": "https://steamcommunity.com/market/listings/730/Operation%20Vanguard%20Weapon%20Case",
    "Operation Bravo Case": "https://steamcommunity.com/market/listings/730/Operation%20Bravo%20Case",
    "CS20 Case": "https://steamcommunity.com/market/listings/730/CS20%20Case",
    "CS:GO Weapon Case": "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case",
    "CS:GO Weapon Case 2": "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case%202",
    "CS:GO Weapon Case 3": "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case%203",
    "Winter Offensive Weapon Case": "https://steamcommunity.com/market/listings/730/Winter%20Offensive%20Weapon%20Case",
    "Revolver Case": "https://steamcommunity.com/market/listings/730/Revolver%20Case",
    "Gallery Case": "https://steamcommunity.com/market/listings/730/Gallery%20Case",
    "Sealed Genesis Terminal": "https://steamcommunity.com/market/listings/730/Sealed%20Genesis%20Terminal",
    "Fever Case": "https://steamcommunity.com/market/listings/730/Fever%20Case",
    "X-Ray P250 Package": "https://steamcommunity.com/market/listings/730/X-Ray%20P250%20Package",
    "eSports 2013 Case": "https://steamcommunity.com/market/listings/730/eSports%202013%20Case",
    "eSports 2013 Winter Case": "https://steamcommunity.com/market/listings/730/eSports%202013%20Winter%20Case",
    "eSports 2014 Summer Case": "https://steamcommunity.com/market/listings/730/eSports%202014%20Summer%20Case"
}

def scrape_price(url):
    try:
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        price = soup.find("span", class_="market_listing_price_with_fee")
        if not price:
            return "N/A"
        return price.text.strip()
    except:
        return "N/A"

def get_all_cases():
    results = []
    for name, url in CASE_LINKS.items():
        results.append({
            "name": name,
            "price": scrape_price(url)
        })
    return results
