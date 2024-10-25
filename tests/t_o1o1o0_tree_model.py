import datetime

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

# テストツール
from tests.worksheets import WorksheetDumpHandle


def execute():

    # 森作成
    forest = tr.planting()
    # root = forest.tree_root(None, 'C')
    # root.grow(None, 'Users')
    documents = forest.tree_root(None, 'C').grow(None, 'Users').grow(None, 'Muzudho').grow(None, 'OneDrive').grow(None, 'Documents')
    if True: # I just want to indent
        documents.leaf(None, 'GitHub', {'last_modified':'2024/10/18  12:31:00'})

        tools = documents.grow(None, 'Tools')
        if True:
            shogidokoro = tools.grow(None, 'Shogidokoro')
            if True:
                engine = shogidokoro.grow(None, 'Engine')
                if True:
                    engine.leaf(None, 'Lesserkai.exe', {'last_modified':'2022/3/7  21:03:00', 'size':'1 KB'})
                    engine.leaf(None, 'Lesserkai_ja.txt', {'last_modified':'2012/12/5  22:37:00', 'size':'1 KB'})
                    engine.leaf(None, 'public.bin', {'last_modified':'2002/5/11  22:12:00', 'size':'5,213 KB'})
                shogidokoro.grow(None, 'js').leaf(None, 'Shogidokoro.resources.dll', {'last_modified':'2024/5/11  20:43:00', 'size':'257 KB'})
                shogidokoro.leaf(None, 'Engine.xml', {'last_modified':'2024/9/13  20:20:00', 'size':'4 KB'})
                shogidokoro.leaf(None, 'GameResult.xml', {'last_modified':'2024/9/13  20:20:00', 'size':'2,357 KB'})
                shogidokoro.leaf(None, 'Shogidokoro.exe', {'last_modified':'2024/5/11  20:43:00', 'size':'4,902 KB', 'comment':'version 5.4.1'})
                shogidokoro.leaf(None, 'Shogidokoro.xml', {'last_modified':'2024/9/13  20:20:00', 'size':'8 KB'})
                shogidokoro.leaf(None, 'お読みください.txt', {'last_modified':'2024/5/11  15:24:00', 'size':'3.104 KB'})
            tools.leaf(None, 'Shogidokoro.zip', {'last_modified':'2024/4/27  20:23:00', 'size':'3.104 KB'})
        documents.leaf(None, 'Visual Studio 2022', {'last_modified':'2024/7/22  13:47:00'})
        documents.leaf(None, 'Default.rdp', {'last_modified':'2023/9/23  14:05:00'})

    # TODO ツリーモデル作成
    # 葉要素に番号を振っていく
    forest.renumbering()

    # デバッグ表示
    print(f"""\
森表示：
{forest._stringify_like_tree('')}""")

    # TODO ツリーモデルをCSV形式で保存 file='./tests/diff_dump/actual/example_o1o1o0_tree_model_Drive.txt'
    pass

