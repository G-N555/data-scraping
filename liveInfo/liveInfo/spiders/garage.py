import scrapy
from liveInfo.items import LiveinfoItem

class GardenSpider(scrapy.Spider):
    name = 'garage'
    allowed_domains = ['www.garage.or.jp']
    start_urls = ['https://www.garage.or.jp/']

    def parse(self, response):
        # print(response.xpath('//li[@id="menu-item-872"]/ul/li/a').re(r'http://www.garage.or.jp/date/\d{4}\/\d{1,2}'))
        for url in response.xpath('//li[@id="menu-item-872"]/ul/li/a').re(r'http://www.garage.or.jp/date/\d{4}\/\d{1,2}'):
            yield scrapy.Request(response.urljoin(url), self.parse_info)        
        
    def parse_info(self, response):
        month = "".join(response.css('h1.page-header-title-month span.tag-m').xpath("string()").extract()) + "/"
        item = LiveinfoItem()
        tables = response.xpath('//div[@id="blog-wrap"]/article')
        for table in tables:
            title = "".join(table.css('div.title a').xpath("string()").extract())
            item['title'] = title
            date = "/".join(table.css('div.blackdate p').xpath("string()").extract())
            item['date'] = "".join(month + date)
            lineUp = "".join(table.css('div.actor').xpath("string()").extract())
            item['lineUp'] = "".join(lineUp).replace("\r\n", "").replace("\xa0", "").replace("\u3000", "")
            url = "".join(table.css('div.kotira_sch a::attr(href)').extract())
            item['url'] = url
            item['liveHouseId'] = "3"
            yield item
