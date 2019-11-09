import scrapy
from liveInfo.items import LiveinfoItem

class GardenSpider(scrapy.Spider):
    name = 'shelter'
    allowed_domains = ['www.loft-prj.co.jp']
    start_urls = ['http://www.loft-prj.co.jp/SHELTER/']

    def parse(self, response):
        # print(len(response.xpath('//ul[@class="nav-menu"]/li[@id="menu-item-34"]').re(r'https?:\/\/?[-a-zA-Z]{1,256}\.[a-zA-Z]{1,6}\b\/\?m=\d+')))
        for url in response.xpath('//div[@id="gNavi"]/ul/li[@class="top02"]').re(r'http://www.loft-prj.co.jp/schedule/shelter'):
            yield scrapy.Request(response.urljoin(url), self.parse_info)        
        
    def parse_info(self, response):
        item = LiveinfoItem()
        tables = response.xpath('//table[@class="timetable"]/tr')
        for table in tables:
            liveTitle = table.css('td div h3').xpath('string()').extract()
            item['title'] = "".join(liveTitle)
            strDate = table.css('th').xpath('string()').extract()
            item['date'] = "".join(strDate)
            lineUp = table.css('td p.month_content').xpath('string()').extract()
            for band in lineUp:
                item['lineUp'] = "".join(band).replace("\n","").replace("\xa0","")
            item['liveHouseId'] = 1
            url = "".join(table.css('td div h3 a::attr(href)').extract())
            item['url'] = url
            yield item
