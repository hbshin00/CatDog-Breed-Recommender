import requests
from bs4 import BeautifulSoup
import pandas as pd

link = "https://cattime.com/cat-breeds"
pg = requests.get(link)
temp_soup = BeautifulSoup(pg.content, 'html.parser')
refs = temp_soup.find_all("a", class_="list-item-title")
URLs = []
breeds = []
for ref in refs:
    breeds.append(ref.get_text())
    URLs.append(ref["href"])

pg2 = requests.get(URLs[0])
soup2 = BeautifulSoup(pg2.content, 'html.parser')
titles_raw = soup2.find_all("div", class_='characteristic-title')
titles = []
for thing in titles_raw:
    titles.append(thing.get_text())

intros = []
stars = []
for URL in URLs:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    intros.append(soup.find("div", class_='breeds-single-intro').get_text())
    stars_raw = soup.find_all("div", class_='characteristic-star-block')
    star = []
    for i in range(len(stars_raw)):
        s = stars_raw[i].get_text()
        if s != "":
            star.append(s)
    stars.append(star)


panda = pd.DataFrame({
    "breed": breeds,
    "intro": intros
})

for i in range(len(titles)):
    panda[titles[i]] = [int(stars[j][i]) if i < len(stars[j]) else -100 for j in range(len(stars))]

panda.to_csv('data/cats.csv', index=False)