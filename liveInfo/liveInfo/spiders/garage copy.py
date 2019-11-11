import scrapy
import re
from liveInfo.items import LiveinfoItem
from urllib.parse import unquote

class GardenSpider(scrapy.Spider):
    name = 'cyclone'
    allowed_domains = ['www.cyclone1997.com']
    start_urls = ['http://www.cyclone1997.com/schedule.html']

    def parse(self, response):
        for url in response.xpath('//body/div/iframe/@src').re(r'schedule/[0-9]{4}schedule_\d{0,2}.html'):
            yield scrapy.Request(response.urljoin(url), self.parse_info)        
        
    def parse_info(self, response):
        item = LiveinfoItem()
        year_month = "".join(response.xpath('//body/font/b').re(r'\d{4}.[1-9]{0,2}')[0]).replace(".", "-")
        tables = response.xpath('//body/table')
        for table in tables:
            titleA = "".join(table.css('tr td p span[style="font-size: 10px"]::text').extract()).replace("\n","").strip()
            item['title'] = re.sub(' +', ' ', titleA)
            if len(titleA) == 0:
                titleB = "".join(table.css('tr td p span[style="font-size: 10px; color: #FFFFFF;"]::text').extract()).replace("\n","").strip()
                item['title'] = re.sub(' +',' ',titleB)
                if len(titleB) == 0:
                    titleC = "no title"
                    item['title'] = titleC
            date = "".join(table.css('tr td em strong img[src]').re(r'\d{2}')[0])
            day = "".join(table.css('tr td em strong img[src]')[1].re(r'\d{1}\w{3}'))[1:]
            item['date'] = year_month + "-" + date + "-" + day
            lineUp = table.css('tr td p span[style="font-size: 14px"] strong').xpath("string()").extract_first().replace("\n","").replace("×\u3000", "").strip()
            item['lineUp'] = re.sub(' +',' ',lineUp)
            item['url'] = ""
            item['liveHouseId'] = "4"
            yield item
