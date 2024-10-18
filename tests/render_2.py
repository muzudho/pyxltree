import traceback
import os
import datetime

from src.xltree import Config, WorkbookControl

SHEET_NAME = 'Tree'


def test_render():
    """描画テスト"""

    # ワークブック制御生成
    wbc = WorkbookControl(target='./tests/temp/tree.xlsx')

    # シート描画
    wbc.render_sheet(target='Tree_1', based_on='./tests/data/tree.csv')

    # ２つ目のシート描画
    wbc.render_sheet(target='Tree_2', based_on='./tests/data/tree_drive.csv')

    # 'Sheet' 以外のワークシートを生成したあとで、'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.wb_file_path}")
