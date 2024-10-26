# TODO

* [x] セル結合をオプションでするようにするか？
* [x] CSV読込時点で、列を edge, node, edge, node の順に並び変えて正規化したい
* [x] ツリー構造を操作して、テーブル（.csv）を出力できるようにしたい（逆操作）。 node列や edge列を可変長で自動生成してほしい ----> Forest クラス実装
* [ ] 辞書のキーに (エッジテキスト, ノードテキスト) のようなタプルを入れているが、メモリ消費が大きくなりすぎないか？ いっそ、辞書のキーを本体、値を子要素の辞書にしてはどうか？
* [x] edge, node と、［edgeとnodeのペアのentry］ の３単語を使い分けるか？
* [x] print_child() はエグザンプルを除いて廃止方針。 TreeEntry._stringify_like_tree() を使っていく
* [x] WorksheetHandle クラスの multiple_root_entry を Forest に変更できないか？ TreeStructureBasedOnTable.read_multiple_root() の改造が必要か？
* [ ] 処理が長くなるものは、引数に timeup を付けたい。秒の浮動小数点数で指定
