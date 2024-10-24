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
from tests.worksheets import WorksheetDumpControl


def execute():

    items = []

    # 出力先ワークブックを指定し、ワークブックハンドル取得
    with tr.prepare_workbook(target='./examples/temp/example_o1o0_tree_drive.xlsx', mode='w') as b:

        # 読取元CSVを指定し、ワークシートハンドル取得
        with b.prepare_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv') as s:

            def print_child(indent, node):
                """再帰的に子ノードを表示"""
                succ_indent = indent + '    '
                for child_node in node.child_nodes.values():
                    # エッジテキスト
                    if child_node.edge_text is not None:
                        et = f"─{child_node.edge_text}─"
                    else:
                        et = '──'
                    
                    # 葉ノード
                    if len(child_node.child_nodes) < 1:
                        items.append(f"{indent}└{et} 📄 ({child_node.leaf_th}) {child_node.text}")
                    
                    # 中間ノード
                    else:
                        items.append(f"{indent}└{et} 📁 {child_node.text}")
                        print_child(indent=succ_indent, node=child_node) # 再帰

            # 木構造のターミナル表示
            for root_node in s.multiple_root_node.values():
                items.append(f"📁 {root_node.text}")
                print_child(indent='', node=root_node)

    # テストに使用するために返す
    return '\n'.join(items)


def execute_example():

    # サンプル実行、ログテキスト取得
    log_text = execute()

    # ワークシートのダンプを出力
    with open('./tests/diff_dump/actual/example_o4o0_terminal.txt', mode='w', encoding='utf8') as f:
        f.write(log_text)
