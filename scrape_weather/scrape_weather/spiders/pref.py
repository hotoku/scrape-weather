import re

import scrapy
from scrapy.http import HtmlResponse

from ..items import PrefectureInfo

class PrefectureSpider(scrapy.Spider):
    name = "pref"
    allowed_domains = ["www.data.jma.go.jp"]
    start_urls = ["https://www.data.jma.go.jp/stats/etrn/select/prefecture00.php"]

    def parse(self, response):
        if type(response) is not HtmlResponse:
            return
        res: HtmlResponse = response
        tags = res.xpath("//map[@name='point']//area")
        alts = tags.xpath("@alt").extract()
        hrefs = tags.xpath("@href").extract()
        nums = [
            re.sub(r".*prec_no=([0-9]+).*", r"\1", href)
            for href in hrefs
        ]
        
        for alt, href, num in zip(alts, hrefs, nums):
            yield PrefectureInfo(name=alt, href=href, number=num)
