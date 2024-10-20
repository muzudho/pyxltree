import datetime
from src.xltree import Settings, WorkbookControl


def execute():
    """入力補完テスト"""

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/no_1_drive_by_tree.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='DriveByTable', based_on='./examples/data/drive_by_table.csv')

    # ワークシート描画
    wbc.render_worksheet(target='DriveByTree', based_on='./examples/data/drive_by_tree.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
