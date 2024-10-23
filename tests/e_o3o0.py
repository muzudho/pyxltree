# テスト対象
from examples.o3o0 import execute

# テストツール
from tests.worksheets import WorksheetDumpControl


def execute_example():

    # サンプル実行
    b = execute()

    # ワークシート取得
    ws = b.get_worksheet(sheet_name='UnevenCoin')

    # ワークシートのダンプを出力
    WorksheetDumpControl.dump(worksheet=ws, file='./tests/diff_dump/actual/example_o3o0_uneven_coin_UnevenCoin.txt')
