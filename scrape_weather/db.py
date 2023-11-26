import sqlite3

from retry import retry

from .items import PrefectureInfo, BlockInfo, WeatherInfo


def connect():
    con = sqlite3.connect("db.sqlite")
    con.row_factory = sqlite3.Row
    return con


def create_tables():
    print("create_tables")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    create table if not exists prefectures (
        id integer primary key autoincrement,
        prec_no text not null,
        name text not null,
        href text not null
    )
""")
    cursor.execute("""
    create table if not exists blocks (
        id integer primary key autoincrement,
        prec_no text not null,
        block_no text not null,
        name text not null,
        href text not null
    )    
    """)
    cursor.execute("""
    create table if not exists weathers (
        id integer primary key autoincrement,
        year integer not null,
        month integer not null,
        day integer not null,
        prec_no text not null,
        block_no text not null,
        precipitation real nullable,
        temperature_avg real nullable,
        temperature_high real nullable,
        temperature_low real nullable,
        snow_fall real nullable,
        run_id text not null
    )
    """)
    conn.commit()
    conn.close()


create_tables()


def insert_prefecture(info: PrefectureInfo):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    insert into prefectures(prec_no, name, href) values (?, ?, ?)
    """, (info["number"], info["name"], info["href"]))
    conn.commit()
    conn.close()


def load_prefecture_href():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    select href from prefectures
    """)
    hrefs = [row["href"] for row in cursor.fetchall()]
    conn.close()
    return hrefs


@retry(delay=1e-2)
def insert_block(info: BlockInfo):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    insert into blocks(block_no, prec_no, name, href) values (?, ?, ?, ?)
    """, (info["number"], info["prefecture_number"], info["name"], info["href"]))
    conn.commit()
    conn.close()


def load_blocks() -> list[BlockInfo]:
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    select
      prec_no as prefecture_number,
      block_no as number
    from
      blocks
    order by
      prec_no,
      block_no
    """)
    blocks = [BlockInfo(**row) for row in cursor.fetchall()]
    conn.close()
    return blocks


@retry(delay=1e-2)
def insert_weather(info: WeatherInfo):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    insert into weathers(
        year,
        month,
        day,
        prec_no,
        block_no,
        precipitation,
        temperature_avg,
        temperature_high,
        temperature_low,
        snow_fall,
        run_id
    ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (info["year"], info["month"], info["day"],
          info["prec_no"], info["block_no"],
          info["precipitation"], info["temperature_avg"], info["temperature_high"],
          info["temperature_low"], info["snow_fall"], info["run_id"]))
    conn.commit()
    conn.close()
