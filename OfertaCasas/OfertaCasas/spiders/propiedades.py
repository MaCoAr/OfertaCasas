from scrapy.spiders import CrawlSpider

class propiedades_Spider(CrawlSpider):
    name = 'propiedades'
    allowed_domain = ['propiedades.com']
    start_urls = ['https://propiedades.com/colima/residencial-venta?__cf_chl_jschl_tk__=4730c894ecb328ea3696f08b47d420aa165f8b0d-1599099240-0-AUViY3KncXtT7KTckVlR9GSkFXsF6WA-44k8hIa4UBrcffxwIUsDGDW_YLw-S9e5kVs90m-CyeP5pOOQF4mkLjXsWco3qpyCZeajKxR2KWlbvVD0Et3bobtXMKclUINQNEKBDtQR8_h7wQXPjn1U6T3Qvl3dGjXuK4J2-m9DW-nhpitfq2CtScluFyOC_DnxDGvsQcIr4DUCJm2vWJK5OjElhorQ9SgNgxNUajTOyhUi4yNwCAV5YFkOkPtGIs7AqmVO8G6oCe6-1U8ThwHjGkY']

