import re
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import scrapy
from scrapy.http import HtmlResponse

from ..db import load_blocks
from ..items import WeatherInfo


def load_start_urls(start_: str, end_: str) -> list[str]:
    blocks = load_blocks()
    sy, sm = start_.split("-")
    ey, em = end_.split("-")
    start = date(int(sy), int(sm), 1)
    end = date(int(ey), int(em), 1)
    delta = relativedelta(months=1)
    d = start
    ret = []
    while d <= end:
        ret.extend([
            f"https://www.data.jma.go.jp/stats/etrn/view/daily_a1.php?prec_no={block['prefecture_number']}&block_no={block['number']}&year={d.year}&month={d.month}"
            for block in blocks
        ])
        d += delta
    return ret


def try_parse(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return float("nan")


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["www.data.jma.go.jp"]

    def __init__(self, start: str, end: str):
        self.start_urls = load_start_urls(start, end)
        self.run_id = datetime.now().strftime("%Y%m%d%H%M%S")

    def parse(self, response):
        if type(response) is not HtmlResponse:
            return
        res: HtmlResponse = response
        year = int(re.sub(r".*year=([0-9]+).*", r"\1", res.url))
        month = int(re.sub(r".*month=([0-9]+).*", r"\1", res.url))
        prec_no = re.sub(r".*prec_no=([0-9]+).*", r"\1", res.url)
        block_no = re.sub(r".*block_no=([0-9]+).*", r"\1", res.url)
        trs = res.xpath('//tr[descendant::a[contains(@href, "hourly")]]')
        for tr in trs:
            tds = tr.xpath('.//td//text()').extract()
            yield WeatherInfo(
                year=year,
                month=month,
                day=int(tds[0]),
                prec_no=prec_no,
                block_no=block_no,
                precipitation=try_parse(tds[1]),
                temperature_avg=try_parse(tds[4]),
                temperature_high=try_parse(tds[5]),
                temperature_low=try_parse(tds[6]),
                snow_fall=try_parse(tds[16]),
                run_id=self.run_id
            )
