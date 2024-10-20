# パッケージを iport した場合は、 `from src.xltree`  の部分を `from xltree` に変えてください
from src.xltree import WorkbookControl

# テスト用
from tests.worksheets import WorksheetDumpControl


def execute():

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./examples/temp/no_1_tree_drive.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./examples/temp/actual/no_1_tree_drive_Drive.txt')     # テスト用

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
