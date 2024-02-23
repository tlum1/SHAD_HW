import re


def clear_string(s: str) -> str:
    s = s.replace(" ", "")
    s = re.sub(r"\[.*?]", "", s)
    return s


from bs4 import BeautifulSoup
import requests


def parse_movie_data_bs4(url):
    soup = BeautifulSoup(requests.get(url).text)

    item = {
        "name": soup.find("th", class_="infobox-above").getText().strip()
    }
    if "Оглавление:…в начало" == item["name"]:
        return None

    table = soup.find("table", class_="infobox")
    for row in table.findAll("tr"):
        if row.find("td") and row.find("th"):
            th = row.find("th").getText().strip()
            td = clear_string(row.find("td").getText().strip())
            if th in "РежиссёрРежиссёры":
                item["Режиссёр"] = td
            if th in "ЖанрыЖанр":
                item["Жанры"] = td
            if th in "СтранаСтраны":
                item["Страна"] = td
            if th in "ГодГода":
                item["Год"] = td

            # Парсинг оценок

            # if th == "IMDb":
            #     rating = _parse_rating(row.find("td").find("a")['href'])
            #     item["Рейтинг IMDb"] = rating

    return item


def _parse_rating(url):
    imdb_soup = BeautifulSoup(requests.get(
        url,
        headers={
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }).text, features="lxml")

    rating = imdb_soup.find(
        class_="sc-bde20123-1 cMEQkK"
    ).getText()

    return rating
