import scrapy
from bs4 import BeautifulSoup
import requests
from scrapy.exceptions import CloseSpider


class GITSpider(scrapy.Spider):
    name = "WikiMovies"
    start_urls = [
        "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"]

    def parse(self, response):

        for item in response.xpath("//div[@id='mw-pages']//div[@class='mw-category-group']//ul//li"):
            link = "https://ru.wikipedia.org/" + item.xpath(".//a/@href").get()
            yield self.parse_movie_data(link)

        page_link = response.xpath("//div[@id='mw-pages']//a/@href")[-1].extract()
        page_type = response.xpath("//div[@id='mw-pages']//a/text()")[-1].extract()
        if page_type != "Следующая страница":
            raise CloseSpider('Дошли до последней страницы')

        yield response.follow(page_link, self.parse)

    def parse_movie_data(self, url):
        soup = BeautifulSoup(requests.get(url).text)

        item = {
            "name": soup.find("th", class_="infobox-above").getText().strip()
        }
        if "Оглавление:…в начало" == item["name"]:
            return None

        table = soup.find("table")
        for row in table.findAll("tr"):
            if row.find("td") and row.find("th"):
                th = row.find("th").getText().strip()
                td = row.find("td").getText().strip()
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
                #     imdb_soup = BeautifulSoup(requests.get(
                #         row.find("td").find("a")['href'],
                #         headers={
                #             "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                #         }).text, features="lxml")
                #
                #     rating = imdb_soup.find(
                #         class_="sc-bde20123-1 cMEQkK"
                #     ).getText()
                #
                #     item["Рейтинг IMDb"] = rating

        self.log(f"movie {item['name']} has been parsed")
        return item