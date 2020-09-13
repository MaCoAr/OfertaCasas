import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OfertacasasItems


class ProprietarySpider(CrawlSpider):
    name = 'proprietary'
    allowed_domain = ['propiedades.com']
    start_urls = ['https://propiedades.com/colima/residencial-venta']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//span[@class="swiper-pagination-bullet"]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//p[@class="title-property"]/a')),
             callback='parse_item', follow=False)
    }

    def start_requests(self):
        urls = [
            'https://propiedades.com/colima/residencial-venta'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        print("\nLA URL ES: "+response.url+"\n\n")
        container = response.xpath('//div[@class="details-property"]')
        for i in range(len(container)):
            OfCa_Items = OfertacasasItems()
            OfCa_Items['house_id'] = container[i].xpath('.//button[@class="icon-favorito prop-fav"]').attrib['data-id']
            OfCa_Items['url'] = container[i].xpath('.//p[@class="title-property"]/a').attrib['href']
            OfCa_Items['location'] = container[i].xpath('.//p[contains(@class,"address-property")]/text()')[i].get()
            OfCa_Items['description'] = ''

            selector_general_description = container[i].xpath('.//ul[@class="gral-description"]//li')
            for n in range(len(selector_general_description)):
                try:
                    class_name = selector_general_description.css('i')[n].attrib['class']
                    attrib_val = selector_general_description.css('li')[n].attrib['data-value']
                    if 'icon-recamaras' == class_name: OfCa_Items['bedrooms'] = attrib_val
                    if 'icon-bano' == class_name: OfCa_Items['baths'] = attrib_val
                    if 'icon-tamano-construccion' == class_name: OfCa_Items['area'] = attrib_val
                except:
                    pass

            OfCa_Items['price'] = container[i].xpath('.//p[@class="precio"]').css('span::text').get()
            OfCa_Items['garage'] = 0

            geolocation = container[i].xpath('//*[@id="list-properties"]//div[@itemprop="geo"]')
            geolocation = geolocation[i].xpath('.//meta')
            OfCa_Items['latitude'] = geolocation.css('meta')[0].attrib['content']
            OfCa_Items['longitude'] = geolocation.css('meta')[1].attrib['content']

            parameters = {"ofca_items": OfCa_Items}
            url_images = OfCa_Items['url']
            yield scrapy.Request(url=url_images, callback=self.parse_images, cb_kwargs=parameters)

    def parse_images(self, response, ofca_items):
        img_items = []
        selectorImages = response.xpath('.//div[@class="slider-listing"]//div[@class="center"]')
        selectorImages = selectorImages.xpath('.//div[@class="slider"]').css('div').css('.open-gallery-slick')
        selectorImages = selectorImages.xpath('.//div[@class="hidden"]//meta[@itemprop="image"]')
        len_images = int(len(selectorImages) / 2)
        for i in range(len_images):
            img = selectorImages[i].xpath('.').attrib['content']
            img_items.append(img)

        ofca_items['images'] = img_items
        yield ofca_items
