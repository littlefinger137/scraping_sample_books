from datetime import datetime
import requests
from bs4 import BeautifulSoup
from IPython.display import display, HTML
import pandas as pd
from urllib.parse import urljoin
import os

# ターゲットURL
url = "http://www.seshop.com/product/616"

# HTTPリクエストを送信してHTMLを取得
res = requests.get(url)

# BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(res.text, "html.parser")

# 書籍情報を格納するリスト
books = []

# 書籍情報が含まれる要素を取得
divs = soup.select("div.list div.inner")

# 各要素に対してループ処理
for div in divs:
    # 画像URLの取得
    img_tag = div.find("img")
    img_url = urljoin(url, img_tag["src"]) if img_tag else None

    # 発売日の取得と整形
    day = div.find("span", class_="date").text.strip()
    day = day.replace("発売", "")
    published = datetime.strptime(day, "%Y.%m.%d")

    # タイトルと詳細ページURLの取得
    div_txt = div.find("div", class_="txt")
    a_tag = div_txt.find("a")
    title = a_tag.text.strip()
    detail_url = a_tag["href"]

    # 価格の取得と整形
    price_tag = div_txt.find("p").find_next("p")
    if price_tag:
        price_text = price_tag.text.strip()
        price_s = price_text.split('円')[0].replace(',', '')

        try:
            price = int(price_s)
        except ValueError:
            price = "価格が無効です: " + price_text

        # 書籍情報を辞書に格納してリストに追加
        book = {
            "title": title,
            "img_url": img_url,
            "price": price,
            "published": published,
        }
        books.append(book)

# 書籍情報をDataFrameに変換
df = pd.DataFrame(books)

# 画像URLの整形関数
def format_img_url(img_url):
    if img_url and not img_url.startswith("http"):
        img_url = urljoin("http://www.seshop.com", img_url)
    return img_url

# 画像URLの整形関数を適用
df['img_url'] = df['img_url'].apply(format_img_url)

# 画像プレビュー生成関数
def image_preview(img_url):
    if img_url:
        return f'<img src="{img_url}" style="max-width:200px;"/>'
    else:
        return 'No Image'

# 画像プレビューをDataFrameに追加
df['Image Preview'] = df['img_url'].apply(image_preview)

# DataFrameを表示
display(HTML(df.head(3).to_html(escape=False)))

# CSVファイルへの出力 (title, img_url, price, published の4項目)
csv_filename = "books_data.csv"
df[['title', 'img_url', 'price', 'published']].to_csv(csv_filename, index=False)
print(f"CSVファイル '{csv_filename}' が生成されました。")