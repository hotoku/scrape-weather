import re

import scrapy
from scrapy.http import HtmlResponse

from ..db import load_prefecture_href
from ..items import BlockInfo

def load_start_urls() -> list[str]:
    hrefs = load_prefecture_href()
    return [
        f"https://www.data.jma.go.jp/stats/etrn/select/{href}"
        for href in hrefs
    ]

class BlockSpider(scrapy.Spider):
    name = "block"
    allowed_domains = ["www.data.jma.go.jp"]
    start_urls = load_start_urls()

    def parse(self, response):
        if type(response) is not HtmlResponse:
            return
        res: HtmlResponse = response
        tags = res.xpath("//map[@name='point']//area")
        alts = tags.xpath("@alt").extract()
        hrefs = tags.xpath("@href").extract()
        prec_nums = [
            re.sub(r".*prec_no=([0-9]+).*", r"\1", href)
            for href in hrefs
        ]
        block_nums = [
            re.sub(r".*block_no=([0-9]+).*", r"\1", href)
            for href in hrefs
        ]
        for alt, href, prec_num, block_num in zip(alts, hrefs, prec_nums, block_nums):
            if re.match(r"^[0-9]+$", block_num) is not None:
                yield BlockInfo(name=alt, href=href,
                                number=block_num, prefecture_number=prec_num)
