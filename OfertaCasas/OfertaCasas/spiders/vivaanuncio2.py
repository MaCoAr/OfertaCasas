from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OfertacasasItems

class OfertaCasasSpider(CrawlSpider):
    name = 'houses'
    allowed_domain = ['www.vivanuncios.com.mx']
    start_urls = ['https://www.vivanuncios.com.mx/s-casas-en-venta/colima-col/v1c1293l10256p1']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="icon-pagination-right"]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="href-link tile-title-text"]')),
             callback='parse_item', follow=False)
    }

    listImages = []

    def parse_item(self, response):
        OfCa_items = OfertacasasItems()

        # Info Houses
        OfCa_items['url'] = response.url
        OfCa_items['location'] = response.xpath('//div[@class="location-name"]/text()').get()
        OfCa_items['description'] = response.xpath('//div[@class="description-content"]/span[@class=""]/text()').get()
        # Datos generales
        DatosGenerales = response.xpath('//*[@id="wrapper"]/div[@class="vip-content"]/div[@class="revip-content"]/div[@class="fixed-container"]/div[@class="revip-details"]/div')
        OfCa_items['bedrooms'] = DatosGenerales.xpath('').get()

        yield OfCa_items

# https://luisramirez.dev/tutorial-de-web-scraping-python-en-espanol-scrapy/
# continuar con el video 4
