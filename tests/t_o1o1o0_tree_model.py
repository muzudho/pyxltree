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
                shogidokoro.grow(None, 'ja').leaf(None, 'Shogidokoro.resources.dll', {'last_modified':'2024/5/11  20:43:00', 'size':'257 KB'})
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
    terminal_text = forest._stringify_like_tree('')
    print(f"""\
森表示：
{terminal_text}""")

    # ターミナル表示のダンプを出力
    with open('./tests/diff_dump/actual/test_o1o1o0_tree_model_terminal.txt', mode='w', encoding='utf8') as f:
        f.write(terminal_text)

    # TODO ツリーモデルをCSV形式で保存 file='./tests/diff_dump/actual/example_o1o1o0_tree_model_Drive.txt'


    class Context():
        def __init__(self):
            self._cur_depth = 0
            self._max_depth = 0
            self._leaf_entries = []
                

    context = Context()


    def find_leaf(context, entry):
        """葉を収集する。葉の最大深さも調べる"""

        context._cur_depth += 1


        # 最大深さ
        if context._max_depth < context._cur_depth:
            context._max_depth = context._cur_depth


        # 葉要素
        if not entry.has_children():
            context._leaf_entries.append(entry)
        else:
            for child_entry in entry.child_entries.values():
                find_leaf(context, child_entry) # 再帰


        context._cur_depth -= 1


    # 全ての葉を収集
    for root_entry in forest.multiple_root_entry.values():
        find_leaf(context, root_entry)


    # 余り列の名前
    # ------------
    remainder_column_name_set = set()

    for leaf in context._leaf_entries:
        for name, value in leaf.remainder_columns.items():
            remainder_column_name_set.add(name)


    # 順序を固定する
    remainder_column_name_list = list(remainder_column_name_set)
    print(f"余り列の名前：{remainder_column_name_list=}")



    print(f"最大深さ：{context._max_depth=}")

    # テーブルの列を作成する
    #
    #   TODO 余り列を作成したい
    #
    column_names = ['no']

    for i in range(0, context._max_depth + 1):
        column_names.append(f'edge{i}')
        column_names.append(f'node{i}')

    # 余り列を追加
    for remainder_column_name in remainder_column_name_list:
        column_names.append(remainder_column_name)

    # print(f"列名：{column_names=}")
    # print(f"列名の要素数：{len(column_names)=}")


    df = pd.DataFrame(columns=column_names)
    df.set_index('no', inplace=True)
    print(f"""\
new df:
{df}
""")


    # TODO 葉のすべての親を出力
    for leaf_th, leaf in enumerate(context._leaf_entries, 1):


        cur_entry = leaf
        path = [cur_entry]

        while cur_entry.parent_entry is not None:
            # 逆順で親エントリーが入っていく
            cur_entry = cur_entry.parent_entry
            path.append(cur_entry)


        # エッジ、ノードを交互に入れたリストを作る
        #
        #   TODO 余り列を作成したい
        #
        column_values = [None] * ((context._max_depth + 1) * 2 + len(remainder_column_name_list))
        for entry_no, entry in enumerate(reversed(path)):
            column_values[entry_no * 2] = entry.edge_text
            column_values[entry_no * 2 + 1] = entry.node_text

        # 余り列を追加
        column_no = (context._max_depth + 1) * 2
        for remainder_column_name in remainder_column_name_list:
            if remainder_column_name in leaf.remainder_columns:
                value = leaf.remainder_columns[remainder_column_name]
            else: 
                value = None

            column_values[column_no] = value
            column_no += 1

#         print(f"""\
# 列名の要素数：{len(column_names[1:])=}
# 値の要素数　：{len(column_values)=}
# 列名　　　　：{column_names[1:]=}
# 値　　　　　：{column_values=}
# """)

        # 行の追加
        # if len(df) == 0:
        #     new_row_no = 0
        # else:
        #     new_row_no = -1

        df.loc[leaf_th] = column_values


    # 全部欠損している列を削除
    df.dropna(how='all', axis=1, inplace=True)

    print(f"""\
df:
{df}
""")

    # テーブルをCSV形式でファイルへ保存
    df.to_csv('./tests/diff_dump/actual/test_o1o1o0_tree_model_table.txt', encoding='utf8')
