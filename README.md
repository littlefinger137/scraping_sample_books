# scraping_sample_books
公式教科書(日本)のサンプルコードで価格が取得できなかった人向け
※※※ジュピターノートブックで動作します。学習用にお使いください※※※

原因：
サイトの構造が変更になった。
→価格がテキスト内の埋め込みになってしまった

解決：
次の要素を指定する関数を利用
→find_next("p")

