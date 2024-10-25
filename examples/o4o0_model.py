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


# 出力先ワークブックを指定し、ワークブックハンドル取得
with tr.prepare_workbook(target='./examples/temp/example_o1o0_tree_drive.xlsx', mode='w') as b:

    # 読取元CSVを指定し、ワークシートハンドル取得
    with b.prepare_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv') as s:

        def print_child(indent, node):
            """再帰的に子ノードを表示"""
            succ_indent = indent + '    '
            for child_entry in node.child_entries.values():
                # エッジテキスト
                if child_entry.edge_text is not None:
                    et = f"─{child_entry.edge_text}─"
                else:
                    et = '──'
                
                # 葉ノード
                if len(child_entry.child_entries) < 1:
                    print(f"{indent}└{et} 📄 ({child_entry.leaf_th}) {child_entry.node_text}")
                
                # 中間ノード
                else:
                    print(f"{indent}└{et} 📁 {child_entry.node_text}")
                    print_child(indent=succ_indent, node=child_entry) # 再帰

        # 木構造のターミナル表示
        for root_entry in s.multiple_root_entry.values():
            print(f"📁 {root_entry.node_text}")
            print_child(indent='', node=root_entry)
