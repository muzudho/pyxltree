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

# テスト用
from tests.worksheets import WorksheetDumpHandle


def execute():
    """描画テスト"""

    # 出力先ワークブックを指定し、ワークブックハンドル取得
    with tr.prepare_workbook(target='./tests/temp/test_o2o0_tree_multisheet.xlsx', mode='w') as b:

        # 読取元CSVを指定し、ワークシートハンドル取得
        with b.prepare_worksheet(target='Shiritori', based_on='./tests/data/tree.csv') as s:

            # ワークシートへ木構造図を描画
            s.render_tree()
            WorksheetDumpHandle.dump(worksheet=s._ws, file='./tests/diff_dump/actual/test_o2o0_tree_multisheet_Shiritori.txt')     # テスト用

        # 読取元CSVを指定し、ワークシートハンドル取得
        with b.prepare_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv') as s:

            # ワークシートへ木構造図を描画
            s.render_tree()
            WorksheetDumpHandle.dump(worksheet=s._ws, file='./tests/diff_dump/actual/test_o2o0_tree_multisheet_Drive.txt')     # テスト用

        # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
        b.remove_worksheet(target='Sheet')

        # 保存
        b.save_workbook()
        print(f"[{datetime.datetime.now()}] Please look {b.workbook_file_path}")
