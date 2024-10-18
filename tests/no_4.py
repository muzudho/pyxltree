from src.xltree import Settings, WorkbookControl


def execute():

    # 各種設定
    settings = Settings(
            # 省略可能
            dictionary = {
                # 列の幅
                #'no_width':                         4,      # A列の幅。no列
                #'row_header_separator_width':       3,      # B列の幅。空列
                'node_width':                        7,     # 例：C, F, I ...列の幅。ノードの箱の幅
                #'parent_side_edge_width':           2,      # 例：D, G, J ...列の幅。エッジの水平線のうち、親ノードの方
                'child_side_edge_width':            22,      # 例：E, H, K ...列の幅。エッジの水平線のうち、子ノードの方

                # 行の高さ
                'header_height':                    13,     # 第１行。ヘッダー
                'column_header_separator_height':   13,     # 第２行。空行

                # ノード関連
                'node_horizontal_alignment':        'left',
                'node_vertical_alignment':          None,
            })

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/tree_uneven_coin.xlsx', mode='w', settings=settings)

    # ワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./examples/data/tree_uneven_coin.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
