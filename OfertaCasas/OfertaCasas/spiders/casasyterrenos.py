import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OfertacasasItems

class Houses_And_Land_Spider(CrawlSpider):
    name = 'houses_and_land'
    allowed_domain = ['www.casasyterrenos.com/']
    start_urls = ['https://www.casasyterrenos.com/colima/colima/casas/venta']

    rules = {
         Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="__next"]/div/div/div/div[1]/div[2]//a')),
             callback='parse_item', follow=False)
    }

    def start_requests(self):
        urls = [
            'https://www.casasyterrenos.com/colima/colima/casas/venta'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contenedor = response.xpath('//div[@id="__next"]/div/div[contains(@class,"sc-Rmtcm")]/div[contains(@class,"sc-krvtoX")]/div/div[contains(@class,"sc-Rmtcm")]/div')

        # headers = {
        #     'Connection': 'keep-alive',
        #     'Cache-Control': 'max-age=0',
        #     'DNT': '1',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        #     'Sec-Fetch-User': '?1',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #     'Sec-Fetch-Site': 'same-origin',
        #     'Sec-Fetch-Mode': 'navigate',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'en-US,en;q=0.9',
        # }

        for i in range(len(contenedor)):
            OfCa_items = OfertacasasItems()
            OfCa_items['url'] = contenedor[i].xpath('//a').attrib['href']

            parametros = {"OfCa_items": OfCa_items}
            url_images = "https://www.casasyterrenos.com/" + OfCa_items['url']
            yield scrapy.Request(url=url_images, callback=self.parse_images, cb_kwargs=parametros)

    def parse_images(self, response, OfCa_items):
        OfCa_items['description'] = response.xpath('//div[@class="description"]').get()
        OfCa_items['location'] = response.xpath('//div[contains(@class,"sc-hwwEjo")]/div/p').get
        OfCa_items['area'] = response.xpath('//div[contains(@class,"units")]/div').get()
        OfCa_items['price'] = response.xpath('//div[contains(@class,"sc-ifAKCX")]/div/p[1]').get()
        Id = str(response.url).split('-')[-1]
        OfCa_items['house_id'] = Id
        features = response.xpath('//div[contains(@class,"sc-fMiknA")]/div')
        for n in range(len(features)):
            try:
                class_name = features.css('p')[n].attrib['class']
                attrib_val = features.css('p')[n].xpath('[@class="number"]')
                if 'Habitaciones' == class_name: OfCa_items['bedrooms'] = attrib_val
                if 'Baños' == class_name: OfCa_items['baths'] = attrib_val
                if 'Estacionamientos' == class_name: OfCa_items['garage'] = attrib_val
            except:
                pass

        img_items = []
        selectorImages = response.xpath('//div[contains(@class,"image-gallery-slides")]/div')
        for i in range(1, len(selectorImages)):
            img = selectorImages.xpath('.//img')[i].attrib['src']
            img_items.append(img)

        OfCa_items['images'] = img_items
        yield OfCa_items
