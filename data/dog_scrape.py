import requests
from bs4 import BeautifulSoup
import pandas as pd

URLs = []
breeds = []
imgs = []
links = ["https://dogtime.com/tag/purebred","https://dogtime.com/tag/purebred/page/2","https://dogtime.com/tag/purebred/page/3","https://dogtime.com/tag/purebred/page/4","https://dogtime.com/tag/purebred/page/5","https://dogtime.com/tag/purebred/page/6","https://dogtime.com/tag/purebred/page/7","https://dogtime.com/tag/purebred/page/8","https://dogtime.com/tag/purebred/page/9","https://dogtime.com/tag/purebred/page/10"]
for link in links:
    pg = requests.get(link)
    temp_soup = BeautifulSoup(pg.content, 'html.parser')
    refs = temp_soup.find_all("a", class_="list-item-title")
    img = temp_soup.find_all("img", class_="list-item-breed-img")
    for ref in refs:
        breeds.append(ref.get_text())
        URLs.append(ref["href"])
    for i in img:
        imgs.append(i["src"])

# link = "https://dogtime.com/tag/purebred"
# pg = requests.get(link)
# temp_soup = BeautifulSoup(pg.content, 'html.parser')
# refs = temp_soup.find_all("a", class_="list-item-title")
# img = temp_soup.find_all("img", class_="list-item-breed-img")
# URLs = []
# breeds = []
# imgs = []
# for ref in refs:
#     breeds.append(ref.get_text())
#     URLs.append(ref["href"])
# for i in img:
#     imgs.append(i["src"])

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
    "imgs": imgs,
    "urls": URLs,
    "intro": intros
})
for i in range(len(titles)):
    panda[titles[i]] = [int(stars[j][i]) if i < len(stars[j]) else -100 for j in range(len(stars))]
panda.to_csv('data/dogs.csv')