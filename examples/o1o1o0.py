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


# 森作成
# ------
#
#   複数の根を持つことができます
#
forest = tr.planting()
# 根を追加するなら tree_root()、辺と中間節を追加するなら grow()、 葉を明示するなら leaf() を使ってください
documents = forest.tree_root(edge_text=None, node_text='C').grow(edge_text=None, node_text='Users').grow(None, 'Muzudho').grow(None, 'OneDrive').grow(None, 'Documents')
if True: # インデントしたいだけ
    documents.leaf(edge_text=None, node_text='GitHub', remainder_columns={'last_modified':'2024/10/18 12:31'})
    tools = documents.grow(None, 'Tools')
    if True:
        shogidokoro = tools.grow(None, 'Shogidokoro')
        if True:
            engine = shogidokoro.grow(None, 'Engine')
            if True:
                engine.leaf(None, 'Lesserkai.exe', {'last_modified':'2022/03/07 21:03', 'size':'266 KB'})
                engine.leaf(None, 'Lesserkai_ja.txt', {'last_modified':'2012/12/05 22:37', 'size':'1 KB'})
                engine.leaf(None, 'public.bin', {'last_modified':'2002/05/11 22:12', 'size':'5,213 KB'})
            shogidokoro.grow(None, 'ja').leaf(None, 'Shogidokoro.resources.dll', {'last_modified':'2024/05/11 20:43', 'size':'257 KB'})
            shogidokoro.leaf(None, 'Engine.xml', {'last_modified':'2024/09/13 20:20', 'size':'4 KB'})
            shogidokoro.leaf(None, 'GameResult.xml', {'last_modified':'2024/09/13 20:20', 'size':'2,357 KB'})
            shogidokoro.leaf(None, 'Shogidokoro.exe', {'last_modified':'2024/05/11 20:43', 'size':'4,902 KB', 'comment':'version 5.4.1'})
            shogidokoro.leaf(None, 'Shogidokoro.xml', {'last_modified':'2024/09/13 20:20', 'size':'8 KB'})
            shogidokoro.leaf(None, 'お読みください.txt', {'last_modified':'2024/05/11 15:24', 'size':'49 KB'})
        tools.leaf(None, 'Shogidokoro.zip', {'last_modified':'2024/04/27 20:23', 'size':'3.104 KB'})
    documents.leaf(None, 'Visual Studio 2022', {'last_modified':'2024/07/22 13:47'})
    documents.leaf(None, 'Default.rdp', {'last_modified':'2023/09/23 14:05'})

# 任意。余り列の出力順を指定する
forest.order_of_remainder_columns = ['last_modified', 'size', 'comment']

# 任意。葉要素に番号を振っていく。葉に連番を振る機能があって、 leaf_th プロパティで取り出せます
#forest.renumbering()


# 森をCSV形式でファイルへ保存
# ---------------------------
forest.to_csv(csv_file_path='./tests/diff_dump/actual/example_o1o1o0_tree_model_table.txt')
