# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobfinderItem(scrapy.Item):
   
    portal = scrapy.Field()
    searched_position = scrapy.Field()
    position_name = scrapy.Field()
    company = scrapy.Field()
    location =  scrapy.Field()
    wage =  scrapy.Field()
    link =  scrapy.Field()
    id =  scrapy.Field()
    page = scrapy.Field()
    crawler_timestamp = scrapy.Field()




