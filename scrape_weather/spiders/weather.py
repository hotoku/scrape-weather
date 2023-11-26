import re

import scrapy
from scrapy.http import HtmlResponse

from ..db import load_blocks
from ..items import WeatherInfo


def load_start_urls(year: str, month: str) -> list[str]:
    blocks = load_blocks()
    return [
        f"https://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no={block['prefecture_number']}&block_no={block['number']}&year={year}&month={month}"
        for block in blocks
    ]


def try_parse(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return float("nan")


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["www.data.jma.go.jp"]

    def __init__(self, year: str, month: str):
        self.start_urls = load_start_urls(year, month)
        self.blocks = load_blocks()
        self.year = year
        self.month = month

    def parse(self, response):
        if type(response) is not HtmlResponse:
            return
        res: HtmlResponse = response
        prec_no = re.sub(r".*prec_no=([0-9]+).*", r"\1", res.url)
        block_no = re.sub(r".*block_no=([0-9]+).*", r"\1", res.url)
        trs = res.xpath('//tr[descendant::a[contains(@href, "hourly")]]')
        for tr in trs:
            tds = tr.xpath('.//td//text()').extract()
            yield WeatherInfo(
                year=self.year,
                month=self.month,
                day=int(tds[0]),
                prec_no=prec_no,
                block_no=block_no,
                precipitation=try_parse(tds[1]),
                temperature_avg=try_parse(tds[4]),
                temperature_high=try_parse(tds[5]),
                temperature_low=try_parse(tds[6]),
                snow_fall=try_parse(tds[16])
            )
