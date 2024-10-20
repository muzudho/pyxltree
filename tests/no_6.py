import datetime
from src.xltree import Settings, WorkbookControl


def execute():
    """描画テスト"""

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/rainbow.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='Shiritori', based_on='./examples/data/rainbow.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
