# パッケージを iport した場合は、 `from src.xltree`  の部分を `from xltree` に変えてください
from src.xltree import WorkbookControl


def execute():

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./examples/temp/example_o2o0_word_chain_game.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='WordChainGame', based_on='./examples/data/word_chain_game.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()

    # テストに使用するために返す
    return wbc