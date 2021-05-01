import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

link = "https://cattime.com/cat-breeds"
pg = requests.get(link)
temp_soup = BeautifulSoup(pg.content, 'html.parser')
parent = temp_soup.find("div", class_="group with-image-mobile-only")
refs = parent.find_all("a", class_="list-item-title")
URLs = []
breeds = []
imgs = []
for ref in refs:
    breeds.append(ref.get_text())
    URLs.append(ref["href"])
for url in URLs:
    pg1 = requests.get(url)
    temp = BeautifulSoup(pg1.content, 'html.parser')
    img = temp.find("img", class_="breed-featured-img")
    imgs.append(img["src"])

pg2 = requests.get(URLs[0])
soup2 = BeautifulSoup(pg2.content, 'html.parser')
titles_raw = soup2.find_all("div", class_='characteristic-title')
titles = []
for thing in titles_raw:
    titles.append(thing.get_text())

intros = []
stars = []
descriptions = []
for URL in URLs:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    des = soup.find_all("li", class_="breed-data-item js-accordion-item item-expandable-content")
    text = ""
    for d in des:
        text += " " + d.get_text()
    descriptions.append(text)
    parent_intro = soup.find("div", class_='breeds-single-intro')
    intros.append(parent_intro.find_all("p").get_text())
    stars_raw = soup.find_all("div", class_='characteristic-star-block')
    star = []
    for i in range(len(stars_raw)):
        s = stars_raw[i].get_text()
        if s != "":
            star.append(s)
    stars.append(star)

panda = pd.DataFrame({
    "breed": breeds,
    "imgs": imgs,
    "urls": URLs,
    "intro": intros,
    "description": descriptions
})
for i in range(len(titles)):
    panda[titles[i]] = [int(stars[j][i]) if i < len(stars[j]) else -100 for j in range(len(stars))]
panda.to_csv('data/cats.csv')