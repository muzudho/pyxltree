from xltree import WorkbookControl


def execute():

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./examples/temp/no_1_tree_drive.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./examples/data/drive_by_table.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
