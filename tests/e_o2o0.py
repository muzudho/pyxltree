# テスト対象
from examples.o2o0 import execute

# テストツール
from tests.worksheets import WorksheetDumpControl


def execute_example():

    # サンプル実行
    b = execute()

    # ワークシート取得
    ws = b.get_worksheet(sheet_name='WordChainGame')

    # ワークシートのダンプを出力
    WorksheetDumpControl.dump(worksheet=ws, file='./tests/diff_dump/actual/example_o2o0_word_chain_game_WordChainGame.txt')
