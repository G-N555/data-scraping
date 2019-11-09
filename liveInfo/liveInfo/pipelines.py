# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.exceptions import DropItem

class LiveinfoPipeline(object):
    def process_item(self, item, spider):
        return item

class ValidationPipeline(object):
    def process_item(self, item, spider):
        if not (item['title'] or item['date'] or item['lineUp']):
            raise DropItem('Missing title')
        return item

class MySQLPipeline(object):
    def open_spider(self, spider):
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'liveInfo'),
            'user': settings.get('MYSQL_USER', 'root'),
            'password': settings.get('MYSQL_PASSWORD', ''),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS info (
                id INTEGER NOT NULL AUTO_INCREMENT,
                title VARCHAR(200) NOT NULL,
                date VARCHAR(200),
                lineUp VARCHAR(400),
                liveHouseId INTEGER,
                url VARCHAR(400),
                PRIMARY KEY(id)
            )
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        print("item",item)
        self.c.execute('INSERT INTO info (title,date,lineUp,liveHouseId,url) VALUES(%(title)s, %(date)s, %(lineUp)s, %(liveHouseId)s, %(url)s)', dict(item))
        self.conn.commit()
        return item

