from scrapy.spiders import CrawlSpider

class casas_y_terrenos_Spider(CrawlSpider):
    name = 'casasyterrenos'
    allowed_domain = ['www.casasyterrenos.com']
    start_urls = ['https://www.casasyterrenos.com/colima/manzanillo/la-pedregoza/casas/venta']
