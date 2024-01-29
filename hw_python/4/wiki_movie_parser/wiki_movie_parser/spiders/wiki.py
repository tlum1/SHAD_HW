import scrapy
from services import *


class WikiSpider(scrapy.Spider):
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
            raise scrapy.exceptions.CloseSpider('Дошли до последней страницы')

        yield response.follow(page_link, self.parse)

    def parse_movie_data(self, url):
        item = parse_movie_data_bs4(url)

        self.log(f"movie {item['name']} has been parsed")
        return item
