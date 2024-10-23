# テスト対象
from examples.o1o0 import execute

# テストツール
from tests.worksheets import WorksheetDumpControl


def execute_example():

    # サンプル実行
    b = execute()

    # ワークシート取得
    ws = b.get_worksheet(sheet_name='Drive')

    # ワークシートのダンプを出力
    WorksheetDumpControl.dump(worksheet=ws, file='./tests/diff_dump/actual/example_o1o0_tree_drive_Drive.txt')
