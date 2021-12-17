import scrapy
from ..items import ScrapItem

class scrapspider(scrapy.Spider):
    name = 'scrap'
    page_num = 2
    start_urls = ['https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1']

    def parse(self, response):
        items = ScrapItem()
        all_products = response.css('div.product')

        for prd in all_products:
            print(prd)
            title = prd.css('.catalog-item-name::text')[0].extract()
            price = prd.css('span.price span::text')[0].extract()
            manufacturer = prd.css('.catalog-item-brand::text')[0].extract()
            stock_status = prd.css('span.status span::text')[0].extract()

            items['price'] = price
            items['title'] = title
            items['stock'] = stock_status
            items['maftr'] = manufacturer

            yield items

        next = response.css('.pagination span#MainContent_dpProductsTop a::text').extract()
        last = max([int(i) for i in next if i.isdigit()])
        next_page = 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=' + str(scrapspider.page_num)
        if scrapspider.page_num <=last:
            scrapspider.page_num+=1
            yield response.follow(next_page, callback=self.parse)