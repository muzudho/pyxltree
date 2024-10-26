import datetime
import pandas as pd

# 実際には、
#
#   import xltree as tr
#
# のように書きたい。
# テストでは以下のように書く
#
#   パッケージをインストールした場合は、 `from src.xltree`  の部分を `from xltree` に変えてください
#
from src.xltree import xltree_in_src as tr


def execute():

    # 森作成
    # ------
    forest = tr.planting()
    o360 = forest.tree_root(None, '360')
    if True: # インデントしたいだけ
        o360_1_120 = o360.grow('(1/3)', '120')
        if True:
            o360_1_120.leaf('(1/4)', '30')
            o360_1_120_2_30 = o360_1_120.grow('(2/4)', '30')
            if True:
                o360_1_120_2_30.leaf('(1/2)', '15')
                o360_1_120_2_30.leaf('(2/2)', '15')
            o360_1_120.grow('(3/4)', '30')
            o360_1_120.grow('(4/4)', '30')
        o360.grow('(2/3)', '120')

        # 既存チェック
        if o360.has_child(edge_text='(3/3)', node_text='120'):
            raise ValueError("既存チェック関数の不具合")

        # 子要素取得のチェック
        child_node = o360.get_child(edge_text='(3/3)', node_text='120')
        if child_node is not None:
            raise ValueError(f"子要素取得関数の不具合  {child_node=}")

        child_node = o360.get_child(edge_text='(3/3)', node_text='120', default=123)
        if child_node != 123:
            raise ValueError(f"子要素取得関数の不具合  {child_node=}")

        o360.grow('(3/3)', '120')

        # 既存チェック
        if not o360.has_child('(3/3)', '120'):
            raise ValueError("既存チェック関数の不具合")

        # 子要素取得のチェック
        child_node = o360.get_child(edge_text='(3/3)', node_text='120')
        if child_node is None:
            raise ValueError(f"子要素取得関数の不具合  {child_node=}")


    # 余り列の出力順を指定する
    #forest.remainder_column_name_list = []

    # 任意。葉要素に番号を振っていく。葉に連番を振る機能があって、 TreeEntry#leaf_th プロパティで取り出せます
    forest.renumbering()

    # ターミナル用表示文字列
    terminal_text = forest._stringify_like_tree('')
#       print(f"""\
# 森表示：
# {terminal_text}""")

    # ターミナル表示のダンプを出力
    with open('./tests/diff_dump/actual/test_o6o1o0_same_node_text_terminal.txt', mode='w', encoding='utf8') as f:
        f.write(terminal_text)


    # ツリー構造をCSV形式でファイルへ保存
    # -----------------------------------
    csv_file_path = './tests/diff_dump/actual/test_o6o1o0_same_node_text_table.txt'
    forest.to_csv(csv_file_path=csv_file_path)
    print(f"[{datetime.datetime.now()}] please look {csv_file_path}")
