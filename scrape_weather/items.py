# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PrefectureInfo(scrapy.Item):
    name = scrapy.Field()
    href = scrapy.Field()
    number = scrapy.Field()

class BlockInfo(scrapy.Item):
    name = scrapy.Field()
    href = scrapy.Field()
    number = scrapy.Field()
    prefecture_number = scrapy.Field()

class WeatherInfo(scrapy.Item):
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    prec_no = scrapy.Field()
    block_no = scrapy.Field()
    precipitation = scrapy.Field()
    temperature_avg = scrapy.Field()
    temperature_high = scrapy.Field()
    temperature_low = scrapy.Field()
    snow_fall = scrapy.Field()
