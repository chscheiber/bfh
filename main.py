from urllib import request
from bs4 import BeautifulSoup
import requests
import pandas as pd


entscheidungen_url = 'entscheidung/entscheidungen-online/detail'
base_url = "https://www.bundesfinanzhof.de"

last_page = 1000 #320
ctr = 0
elements = []
publishing_dates = []

for i in range(0, last_page, 10):

    url = f"{base_url}/de/entscheidungen/entscheidungen-online/?tx_eossearch_eossearch%5Boffset%5D={i}#search-form"
    # filtered_by_date = r"https://www.bundesfinanzhof.de/de/entscheidungen/entscheidungen-online/?tx_eossearch_eossearch%5BdateRange%5D%5Bend%5D=03.02.2022&tx_eossearch_eossearch%5BdateRange%5D%5Bstart%5D=01.01.2021&tx_eossearch_eossearch%5Boffset%5D="+f"{i}"+r"&tx_eossearch_eossearch%5BsearchTerms%5D%5Baktenzeichen%5D=&tx_eossearch_eossearch%5BsearchTerms%5D%5Becli%5D=&tx_eossearch_eossearch%5BsearchTerms%5D%5Bnorm%5D=&tx_eossearch_eossearch%5BsearchTerms%5D%5BsearchTerm%5D=&tx_eossearch_eossearch%5BsearchTerms%5D%5Bsorting%5D=precedentDateDesc&tx_eossearch_eossearch%5B__referrer%5D%5B%40action%5D=index&tx_eossearch_eossearch%5B__referrer%5D%5B%40controller%5D=Standard&tx_eossearch_eossearch%5B__referrer%5D%5B%40extension%5D=&tx_eossearch_eossearch%5B__referrer%5D%5B%40request%5D=a%3A3%3A%7Bs%3A10%3A%22%40extension%22%3BN%3Bs%3A11%3A%22%40controller%22%3Bs%3A8%3A%22Standard%22%3Bs%3A7%3A%22%40action%22%3Bs%3A5%3A%22index%22%3B%7D0f14452ba288c7ae3edc63ada67d4e974f1f9ddb&tx_eossearch_eossearch%5B__referrer%5D%5Barguments%5D=YTowOnt9a31a9a47afbf5c13105ce3f5c41128a22bff97c2&tx_eossearch_eossearch%5B__trustedProperties%5D=a%3A2%3A%7Bs%3A11%3A%22searchTerms%22%3Ba%3A5%3A%7Bs%3A12%3A%22aktenzeichen%22%3Bi%3A1%3Bs%3A4%3A%22ecli%22%3Bi%3A1%3Bs%3A4%3A%22norm%22%3Bi%3A1%3Bs%3A10%3A%22searchTerm%22%3Bi%3A1%3Bs%3A7%3A%22sorting%22%3Bi%3A1%3B%7Ds%3A9%3A%22dateRange%22%3Ba%3A2%3A%7Bs%3A5%3A%22start%22%3Bi%3A1%3Bs%3A3%3A%22end%22%3Bi%3A1%3B%7D%7D7146f9256a02b1ccf0070dbb4310cbd53ce42eb2&cHash=5b8898762bbbab67342abc4dd4c9a044#search-form"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    cells = soup.find_all('td')
    for cell in cells:
        if(cell['data-label'] == 'Veröffentlichung am'):
            date = cell.text.strip()
            publishing_dates.append(date)

    for link in soup.find_all('a'):
        href: str = link.get('href')
        if entscheidungen_url in href:
            id = href.split('/')[-2]
            details_url = f"{base_url}/de/entscheidung/entscheidungen-online/detail/{id}"
            details_page = requests.get(details_url).text
            details_soup = BeautifulSoup(details_page, 'html.parser')
            title = details_soup.find('div', 'm-article__intro').div.p.text
            leitsatze_html = details_soup.find('div', 'm-decisions')
            leitsaetze_text = ''
            for p in leitsatze_html:
                leitsaetze_text += f"{p.text}\n"
            elements.append({'id': id, 'date': publishing_dates[ctr], 'title': title, 'leitsaetze': leitsaetze_text, 'url':details_url})
            print(f"{ctr}: {publishing_dates[ctr]}\tAdded {id}\t{title}")
            ctr += 1

df = pd.DataFrame(elements)
df.to_excel('filtered_date.xlsx',index=False)