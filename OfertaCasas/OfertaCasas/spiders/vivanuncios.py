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
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OfertacasasItems
from ..Tools import CustomTools

class OfertaCasasSpider(CrawlSpider):
    name = 'ofertacasas'
    allowed_domain = ['www.vivanuncios.com.mx']
    start_url = ['https://www.vivanuncios.com.mx/s-casas-en-venta/colima-col/v1c1293l10256p1']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="icon-pagination-right"]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="href-link tile-title-text"]')),
             callback='parse_item', follow=False)
    }



    def start_requests(self):
        urls = [
            'https://www.vivanuncios.com.mx/s-casas-en-venta/colima-col/v1c1293l10256p1'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contenedor = response.xpath('//*[@id="tileRedesign"]/div')

        for i in range(len(contenedor)):
            OfCa_items = OfertacasasItems()
            # OfCa_items['house_id'] = contenedor[i].xpath('//div[@class="tile-contact-us"]').attrib['data-tileadid']
            OfCa_items['house_id'] = contenedor[i].xpath(
                '//div[contains(@class,"tileV2") and contains(@class, "REAdTileV2") and contains(@class,"regular")]')[
                i].attrib['data-tileadid']
            OfCa_items['url'] = contenedor[i].xpath('.//div[@class="tile-desc one-liner"]/a/@href').get()
            OfCa_items['location'] = contenedor[i].xpath('.//div[@class="tile-location one-liner"]/b').get()
            OfCa_items['description'] = contenedor[i].xpath('.//div[@class="expanded-description"]/text()').get()
            OfCa_items['bedrooms'] = contenedor[i].xpath(
                './/div[@class="chiplets-inline-block re-bedroom"]/text()').get()
            OfCa_items['baths'] = contenedor[i].xpath('.//div[@class="chiplets-inline-block re-bathroom"]/text()').get()
            OfCa_items['area'] = contenedor[i].xpath('.//div[@class="chiplets-inline-block surface-area"]/text()').get()
            OfCa_items['price'] = contenedor[i].xpath('.//span[@class="ad-price"]/text()').get()

            garage = contenedor[i].xpath('.//div[contains(@class,"car-parking")]/text()').get()
            OfCa_items['garage'] = 0
            if garage is not None:
                OfCa_items['garage'] = garage

            parametros = {"OfCa_items": OfCa_items}
            url_images = "https://www.vivanuncios.com.mx" + OfCa_items['url']
            yield scrapy.Request(url=url_images, callback=self.parse_images, cb_kwargs=parametros)

    def parse_images(self, response, OfCa_items):
        json_contenedor = response.xpath('//script[@type="application/ld+json"]').get()
        json_contenedor = CustomTools.CleanHtml(json_contenedor)
        jContend = json.loads(json_contenedor)
        OfCa_items['latitude'] = jContend[0]['geo']['latitude']
        OfCa_items['longitude'] = jContend[0]['geo']['longitude']
        OfCa_items['url'] = response.url

        img_items = []
        selectorImages = response.xpath('//div[@class="gallery-slide"]/div/div/picture')
        for i in range(1, len(selectorImages)):
            img = selectorImages.xpath('.//source[@type="image/jpeg"]')[i].attrib['data-srcset']
            img_items.append(img)

        OfCa_items['images'] = img_items
        yield OfCa_items
