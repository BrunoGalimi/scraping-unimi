import scrapy
from unimi_scraper.items import UnimiPageItem

class UnimiSpider(scrapy.Spider):
    name = "unimi"
    allowed_domains = ["unimi.it", "www.unimi.it"]
    start_urls = ["https://www.unimi.it/"]

    def parse(self, response):
        # crea l’item della pagina
        item = UnimiPageItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').get()
        item['html'] = response.text  # testo completo della pagina (HTML)

        yield item

        # estrai i link <a href> interni e seguili
        for href in response.css('a::attr(href)').getall():
            # usa response.follow per gestire relativi e assoluti
            yield response.follow(href, self.parse)
