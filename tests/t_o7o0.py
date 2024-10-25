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

# テスト用
from tests.worksheets import print_child


def execute():
    """描画テスト"""

    items = []

    # 出力先ワークブックを指定し、ワークブックハンドル取得
    with tr.prepare_workbook(target='./tests/temp/test_o7o0_same_node_text_terminal.xlsx', mode='w') as b:

        # 読取元CSVを指定し、ワークシートハンドル取得
        with b.prepare_worksheet(target='SameNodeText', based_on='./tests/data/same_node_text.csv') as s:

            # 木構造のターミナル表示
            for root_entry in s.multiple_root_entry.values():
                items.append(f"📁 {root_entry.node_text}")
                print_child(output_list=items, indent='', node=root_entry)


    # ターミナル表示のダンプを出力
    with open('./tests/diff_dump/actual/test_o7o0_same_node_text_terminal.txt', mode='w', encoding='utf8') as f:
        f.write('\n'.join(items))
