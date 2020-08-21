# https://www.youtube.com/watch?v=nuF5lCI49XM
# https://www.youtube.com/watch?v=1epYjGrkvnE
# https://www.youtube.com/watch?v=ctfTUC4DuxU
# https://www.youtube.com/watch?v=Nhk8C9JNvVw

# other links
# https://www.youtube.com/watch?v=OJ8isyws2yw

# 25 videos
# https://www.youtube.com/watch?v=ve_0h4Y8nuI&list=PLhTjy8cBISEqkN-5Ku_kXG4QW33sxQo0t

# scrapy cralw ofertacasas -o OfCa_items.json
# scrapy genspider {nombre archivo} {URL} -> genera un new file
# user agent
# https://developers.whatismybrowser.com/useragents/explore/software_name/googlebot/
# install package scrapy user agents

# Sample master-detail with scrapy
# https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-iii-bcd94a2e8bf3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OfertacasasItems


class OfertaCasasSpider(CrawlSpider):
    name = 'ofertacasas'
    allowed_domain = ['www.vivanuncios.com.mx']
    start_url = ['https://www.vivanuncios.com.mx/s-casas-en-venta/colima-col/v1c1293l10256p1']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="pag-box"]')))
    }

    def start_requests(self):
        urls = [
            'https://www.vivanuncios.com.mx/s-casas-en-venta/colima-col/v1c1293l10256p1'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        OfCa_items = OfertacasasItems()

        contenedor = response.xpath('//*[@id="tileRedesign"]/div')

        for i in range(len(contenedor)):
            OfCa_items['url'] = contenedor[i].xpath('.//div[@class="tile-desc one-liner"]/a/@href').get()
            OfCa_items['location'] = contenedor[i].xpath('.//div[@class="tile-location one-liner"]/b').get()
            OfCa_items['description'] = contenedor[i].xpath('.//div[@class="expanded-description"]/text()').get()
            OfCa_items['bedrooms'] = contenedor[i].xpath(
                './/div[@class="chiplets-inline-block re-bedroom"]/text()').get()
            OfCa_items['baths'] = contenedor[i].xpath('.//div[@class="chiplets-inline-block re-bathroom"]/text()').get()
            garage = contenedor[i].xpath('.//div[contains(@class,"car-parking")]/text()').get()
            OfCa_items['garage'] = 0
            if garage != None:
                OfCa_items['garage'] = garage
            OfCa_items['area'] = contenedor[i].xpath('.//div[@class="chiplets-inline-block surface-area"]/text()').get()
            OfCa_items['price'] = contenedor[i].xpath('.//span[@class="ad-price"]/text()').get()

            # yield OfCa_items
            url_images = "https://www.vivanuncios.com.mx"+OfCa_items['url']
            print(url_images)
            yield scrapy.Request(url=url_images, callback=self.parseImages)

    def parseImages(self, response):
        selectorImages = response.xpath('//div[@class="gallery-slide"]/div/div/picture')
        listImages = []
        for i in range(1, len(selectorImages)):
            # img = selectorImages.xpath('.//img')[i].attrib['src']
            img = selectorImages.xpath('.//source[@type="image/jpeg"]')[i].attrib['data-srcset']
            print(img)
            listImages.append(img)

        return(yield)
