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
        container = response.xpath('//div[@class="details-property"]')
        for i in range(len(container)):
            OfCa_Items = OfertacasasItems()
            OfCa_Items['house_id'] = container[i].xpath('//button[@class="icon-favorito prop-fav"]').attrib['data-id']
            OfCa_Items['url'] = container[i].xpath('//p[@class="title-property"]/a').attrib['href']
            OfCa_Items['location'] = container[i].xpath('//p[contains(@class,"address-property")]/text()')[i].get()
            OfCa_Items['description'] = ''
            selector_general_description = container[i].xpath('//ul[@class="gral-description"]')
            OfCa_Items['bedrooms'] = container[i].xpath('//ul[@class="gral-description"]//li[1]').get()
            OfCa_Items['baths'] = container[i].xpath('//ul[@class="gral-description"]//li[2]').get()
            OfCa_Items['area'] = container[i].xpath('//ul[@class="gral-description"]//li[3]').get()
            OfCa_Items['price'] = container[i].xpath('//p[@class="precio"]').get()
            OfCa_Items['garage'] = 0
            OfCa_Items['latitude'] = container[i].xpath('//div[@itemprop="geo"]/meta[@itemprop="latitude"]').get()
            OfCa_Items['longitude'] = container[i].xpath('//div[@itemprop="geo"]/meta[@itemprop="longitude"]').get()

            parameters = {"ofca_items": OfCa_Items}
            url_images = OfCa_Items['url']
            yield scrapy.Request(url=url_images, callback=self.parse_images, cb_kwargs=parameters)

    def parse_images(self, response, ofca_items):
        img_items = []
        selectorImages = response.xpath('//div[@class="slick-track"]/div')
        for i in range(1, len(selectorImages)):
            img = selectorImages.xpath('.//div[@class="slick-track"]/div/img"]')[i].attrib['src']
            img_items.append(img)

        ofca_items['images'] = img_items
        yield ofca_items
