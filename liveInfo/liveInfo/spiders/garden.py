import scrapy
from liveInfo.items import LiveinfoItem

class GardenSpider(scrapy.Spider):
    name = 'garden'
    allowed_domains = ['gar-den.in']
    start_urls = ['http://gar-den.in/']

    def parse(self, response):
        # print(len(response.xpath('//ul[@class="nav-menu"]/li[@id="menu-item-34"]').re(r'https?:\/\/?[-a-zA-Z]{1,256}\.[a-zA-Z]{1,6}\b\/\?m=\d+')))
        for url in response.xpath('//ul[@class="nav-menu"]/li[@id="menu-item-34"]').re(r'https?:\/\/?[-a-zA-Z]{1,256}\.[a-zA-Z]{1,6}\b\/\?m=\d+'):
            yield scrapy.Request(response.urljoin(url), self.parse_info)        
        
    def parse_info(self, response):
        liveTitle = LiveinfoItem()
        tables = response.css('section div article')
        for table in tables:
            item = LiveinfoItem()
            liveTitle = table.css('div header.entry-header h1 a::text').extract_first()
            item['title'] = liveTitle
            strDate = table.css('div footer time::attr("datetime")').extract_first()[0:10]
            item['date'] = strDate
            lineUp = table.css("div.entry_headerpost p").xpath('string()').extract()
            for band in lineUp:
                item['lineUp'] = "".join(band).replace("\r\n", "").replace("\xa0", "").replace("\u3000", "")
            item['liveHouseId'] = "2"
            item['url'] = ""
            yield item
