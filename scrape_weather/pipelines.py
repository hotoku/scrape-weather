from .db import insert_prefecture, insert_block, connect, insert_weather
from .items import PrefectureInfo, BlockInfo, WeatherInfo


class InsertPrefecture:
    def process_item(self, item, _):
        if type(item) is not PrefectureInfo:
            return item
        insert_prefecture(item)


class InsertBlock:
    def process_item(self, item, _):
        if type(item) is not BlockInfo:
            return item
        conn = connect()
        cur = conn.cursor()
        sql = """
        select
          count(*) as cnt
        from
          blocks
        where
          prec_no = ? and
          block_no = ?         
        """
        ret = cur.execute(sql, (item["prefecture_number"], item["number"]))
        if ret.fetchone()["cnt"] == 0:
            insert_block(item)
        conn.close()


class InsertWeather:
    def process_item(self, item, _):
        if type(item) is not WeatherInfo:
            return item
        insert_weather(item)
