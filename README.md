# 天気データのスクレイピング

[気象庁のホームページ][jma]から、天気データを取得する。

## データ取得元の概要

気象庁のページでは、

`https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=45&block_no=47682&year=2023&month=1&day=&view=`
のように、

1. 県のid
2. 地域のid
3. 年
4. 月

をURLパラメータで渡すと1ヶ月分の天気データがHTMLで得られる。

## 実行方法とデータの保存先

コマンドは、全てこの`README.md`が置いてあるディレクトリで実行する。
実行すると、このディレクトリの直下に`db.sqlite`というsqlite3のデータベースが作成される。

## スパイダー

### pref.py

県名と県のidの対応を取得し、DBに保存する。

実行方法 `scrapy crawl pref`

### block.py

全県のブロックとidを取得し、DBに保存する。

実行方法 `scrapy crawl block`

### weather.py

開始,終了の年月を指定し、その期間の全ブロックの天気データを取得してDBに保存する。

実行方法（例） `scrapy crawl weather -a start=2021-01 -a end=2023-11`

コマンド実行の開始時刻を`%Y%m%d%H%M%S`形式で表示した文字列を`run_id`として、テーブルの`run_id`列に書き込んでいる。
読み取る際に、`run_id`が最大のレコードに絞り込むと、最も最近に実行した結果だけを参照できる。

### キャッシュ

HTTPリクエストの結果が`.scrapy`という名前でカレントディレクトリに保存されている。
キャッシュを消したければ、このディレクトリを削除する。

<!-- link -->
[jma]: https://www.data.jma.go.jp
