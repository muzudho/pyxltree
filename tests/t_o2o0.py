import datetime
from src.xltree import WorkbookControl

# テスト用
from tests.worksheets import WorksheetDumpControl


def execute():
    """描画テスト"""

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/test_o2o0_tree_multisheet.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='Shiritori', based_on='./tests/data/tree.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./tests/diff_dump/actual/test_o2o0_tree_multisheet_Shiritori.txt')     # テスト用

    # ２つ目のワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./tests/diff_dump/actual/test_o2o0_tree_multisheet_Drive.txt')     # テスト用

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
