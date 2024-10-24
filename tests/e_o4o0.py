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
from tests.worksheets import print_child


def execute():

    items = []

    # 出力先ワークブックを指定し、ワークブックハンドル取得
    with tr.prepare_workbook(target='./examples/temp/example_o1o0_tree_drive.xlsx', mode='w') as b:

        # 読取元CSVを指定し、ワークシートハンドル取得
        with b.prepare_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv') as s:

            # 木構造のターミナル表示
            for root_node in s.multiple_root_node.values():
                items.append(f"📁 {root_node.text}")
                print_child(output_list=items, indent='', node=root_node)

    # テストに使用するために返す
    return '\n'.join(items)


def execute_example():

    # サンプル実行、ログテキスト取得
    log_text = execute()

    # ターミナル表示のダンプを出力
    with open('./tests/diff_dump/actual/example_o4o0_terminal.txt', mode='w', encoding='utf8') as f:
        f.write(log_text)
