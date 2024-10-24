import datetime

# 実際には、
#
#   import xltree as tr
#
# のように書きたい。
# テストでは以下のように書く
#
#   パッケージをインストールした場合は、 `from src.xltree`  の部分を `from xltree` に変えてください
#
from src.xltree import xltree_in_src as tr

# テストツール
from tests.worksheets import WorksheetDumpControl


def execute():

    # 出力先ワークブックを指定し、ワークブックハンドル取得
    b = tr.prepare_workbook(target='./examples/temp/example_o1o0_tree_drive.xlsx', mode='w')

    # 読取元CSVを指定し、ワークシートハンドル取得
    # あとでテストに使うので、メモリ解放しません
    s = b.prepare_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv')

    # ワークシートへ木構造図を描画
    s.render_tree()

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    b.remove_worksheet(target='Sheet')

    # 保存
    b.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {b.workbook_file_path}")

    # テストに使用するために返す
    return b


def execute_example():

    # サンプル実行
    b = execute()

    # ワークシート取得
    ws = b.get_worksheet(sheet_name='Drive')

    # ワークシートのダンプを出力
    WorksheetDumpControl.dump(worksheet=ws, file='./tests/diff_dump/actual/example_o1o0_tree_drive_Drive.txt')
