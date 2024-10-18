import traceback
import os
import datetime

from src.xltree import Config, Renderer

SHEET_NAME = 'Tree'


def test_render():
    """描画テスト"""

    csv_file_path = './tests/data/tree.csv'
    wb_file_path = './tests/temp/tree.xlsx'
    sheet_name = 'Tree_1'

    # レンダラー生成、描画
    renderer = Renderer()
    renderer.render(
            csv_file_path=csv_file_path,
            wb_file_path=wb_file_path,
            sheet_name=sheet_name)

    print(f"[{datetime.datetime.now()}] Please look {wb_file_path}")


    # 連続描画
    csv_file_path = './tests/data/tree_drive.csv'
    # 同じ wb_file_path
    sheet_name = 'Tree_2'

    renderer.render(
            csv_file_path=csv_file_path,
            wb_file_path=wb_file_path,
            sheet_name=sheet_name)

    print(f"[{datetime.datetime.now()}] Please look {wb_file_path}")
