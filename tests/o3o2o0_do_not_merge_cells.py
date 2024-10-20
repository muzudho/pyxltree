import datetime
from src.xltree import WorkbookControl

# テスト用
from tests.worksheets import WorksheetDumpControl


def execute():

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/o3o2o0_do_not_merge_cells.xlsx', mode='w', settings={
        # その他の操作
        'do_not_merge_cells':                    True,      # セル結合しないなら真
    })

    # ワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./examples/data/word_chain_game.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./tests/temp/actual/o3o2o0_do_not_merge_cells.txt')     # テスト用

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
