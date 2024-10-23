import traceback
import os
import datetime

# 実際には、
#
#   import xltree as tr
#
# のように書きたい。
# テストでは以下のように書く
#
#   パッケージを iport した場合は、 `from src.xltree`  の部分を `from xltree` に変えてください
#
from src.xltree import xltree_in_src as tr


def execute():
    """描画テスト"""

    while True:
        csv_file_path = input(f"""\

CSVファイルへのパスを入力してください
Enter the path to the CSV file

    Example: ./tests/data/tree.csv

> """)

        if os.path.isfile(csv_file_path):
            break

        print(f"""\

CSVファイルが見つかりませんでした
`{csv_file_path}` file not found""")


    wb_file_path = input(f"""\

エクセルのワークブック・ファイルの書出し先のパスを入力してください
Enter the export path to the Excel workbook(.xlsx) file

    Example: ./tests/temp/tree.xlsx

> """)

    # 各種設定
    settings ={
        # 列の幅
        #'column_width_of_no':                         4,      # A列の幅。no列
        'column_width_of_root_side_padding':          3,      # B列の幅。ツリー構造図の根側パディング
        'column_width_of_leaf_side_padding':          3,      # ツリー構造図の葉側パディング
        'column_width_of_node':                      20,      # 例：C, F, I ...列の幅。ノードの箱の幅
        'column_width_of_parent_side_edge':           2,      # 例：D, G, J ...列の幅。エッジの水平線のうち、親ノードの方
        'column_width_of_child_side_edge':            4,      # 例：E, H, K ...列の幅。エッジの水平線のうち、子ノードの方

        # 行の高さ
        'row_height_of_header':                      13,      # 第１行。ヘッダー
        'row_height_of_lower_side_padding':          13,      # 第２行。ツリー構造図の軸の番号が小さい側パティング
    }

    # 出力先ワークブックを指定し、ワークブックハンドル取得
    b = tr.prepare_workbook(target=wb_file_path, mode='w', settings=settings)

    # 読取元CSVを指定し、ワークシートハンドル取得
    with b.prepare_worksheet(target='Tree', based_on=csv_file_path) as s:

        # ワークシートへ木構造図を描画
        s.render_tree()

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    b.remove_worksheet(target='Sheet')

    # ワークブック保存
    b.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {b.workbook_file_path}")
