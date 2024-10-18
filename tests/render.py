import traceback
import os
import datetime

from src.xltree import Config, WorkbookControl


def test_render():
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

    # 構成
    config = Config(
            # 省略可能
            dictionary = {
                # 列の幅
                'no_width':                         4,      # A列の幅。no列
                'row_header_separator_width':       3,      # B列の幅。空列
                'node_width':                       20,     # 例：C, F, I ...列の幅。ノードの箱の幅
                'parent_side_edge_width':           2,      # 例：D, G, J ...列の幅。エッジの水平線のうち、親ノードの方
                'child_side_edge_width':            4,      # 例：E, H, K ...列の幅。エッジの水平線のうち、子ノードの方

                # 行の高さ
                'header_height':                    13,     # 第１行。ヘッダー
                'column_header_separator_height':   13,     # 第２行。空行
            })

    # ワークブック制御生成
    wbc = WorkbookControl(target=wb_file_path, config=config)

    # シート描画
    wbc.render_sheet(target='Tree', based_on=csv_file_path)

    # 'Sheet' 以外のワークシートを生成したあとで、'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # ワークブック保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
