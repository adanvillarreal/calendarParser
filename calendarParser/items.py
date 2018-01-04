# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    summary = scrapy.Field()
    location = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    recurrence = scrapy.Field()

class DayItem(scrapy.Item):
    dateTime = scrapy.Field()
    timeZone = scrapy.Field()
