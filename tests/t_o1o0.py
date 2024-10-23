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

# テスト用
from tests.worksheets import WorksheetDumpControl


def execute():
    """入力補完テスト"""

    # 出力先ワークブック指定
    wbc = tr.prepare_workbook(target='./tests/temp/test_o1o0_drive_by_tree.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='DriveByTable', based_on='./examples/data/drive_by_table.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./tests/diff_dump/actual/test_o1o0_drive_by_table_DriveByTable.txt')     # テスト用

    # ワークシート描画
    wbc.render_worksheet(target='DriveByTree', based_on='./examples/data/drive_by_tree.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./tests/diff_dump/actual/test_o1o0_drive_by_tree_DriveByTree.txt')     # テスト用

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
