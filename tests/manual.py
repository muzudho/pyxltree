import traceback
import os
import datetime

from src.xltree import Settings, WorkbookControl


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
    settings = Settings(
            # 省略可能
            dictionary = {
                # 列の幅
                'column_width_of_no':                         4,      # A列の幅。no列
                'column_width_of_row_header_separator':       3,      # B列の幅。空列
                'column_width_of_node':                       20,     # 例：C, F, I ...列の幅。ノードの箱の幅
                'column_width_of_parent_side_edge':           2,      # 例：D, G, J ...列の幅。エッジの水平線のうち、親ノードの方
                'column_width_of_child_side_edge':            4,      # 例：E, H, K ...列の幅。エッジの水平線のうち、子ノードの方

                # 行の高さ
                'row_height_of_header':                    13,     # 第１行。ヘッダー
                'row_height_of_column_header_separator':   13,     # 第２行。空行
            })

    # 出力先ワークブック指定
    wbc = WorkbookControl(target=wb_file_path, mode='w', settings=settings)

    # ワークシート描画
    wbc.render_worksheet(target='Tree', based_on=csv_file_path)

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # ワークブック保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
