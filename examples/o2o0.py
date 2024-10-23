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


# 出力先ワークブックを指定し、ワークブックハンドル取得
b = tr.prepare_workbook(target='./examples/temp/example_o2o0_word_chain_game.xlsx', mode='w')

# 読取元CSVを指定し、ワークシートハンドル取得
with b.prepare_worksheet(target='WordChainGame', based_on='./examples/data/word_chain_game.csv') as s:

    # ワークシートへ木構造図を描画
    s.render_tree()

# 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
b.remove_worksheet(target='Sheet')

# 保存
b.save_workbook()
