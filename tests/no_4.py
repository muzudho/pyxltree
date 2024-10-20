import datetime
from src.xltree import WorkbookControl

# テスト用
from src.xltree.workbooks.testing import WorksheetDumpControl


def execute():

    # 各種設定
    settings = {
        # 列の幅
        #'column_width_of_no':                          4,     # A列の幅。no列
        #'column_width_of_root_side_padding':           3,     # B列の幅。ツリー構造図の根側パディング
        #'column_width_of_leaf_side_padding':           3,     # ツリー構造図の葉側パディング
        'column_width_of_node':                        7,     # 例：C, F, I ...列の幅。ノードの箱の幅
        #'column_width_of_parent_side_edge':            2,     # 例：D, G, J ...列の幅。エッジの水平線のうち、親ノードの方
        'column_width_of_child_side_edge':            22,     # 例：E, H, K ...列の幅。エッジの水平線のうち、子ノードの方

        # 行の高さ
        'row_height_of_header':                     13,     # 第１行。ヘッダー
        'row_height_of_column_header_separator':    13,     # 第２行。空行
        'row_height_of_upper_side_of_node':         13,     # ノードの上側のセルの高さ
        'row_height_of_lower_side_of_node':         6,      # ノードの下側のセルの高さ
        'row_height_of_node_spacing':               6,      # ノード間の高さ

        # 背景色関連
        'bgcolor_of_tree':                   'FFFFFF',      # ツリー構造図の背景
        'bgcolor_of_header_1':               'CCCCFF',      # ヘッダーの背景色その１
        'bgcolor_of_header_2':               '333366',      # ヘッダーの背景色その２
        'bgcolor_of_node':                   'EEFFCC',      # 背景色

        # 文字色関連
        'fgcolor_of_header_1':               '111122',      # ヘッダーの文字色その１
        'fgcolor_of_header_2':               'EEEEFF',      # ヘッダーの文字色その２

        # 文字寄せ関連
        'horizontal_alignment_of_node':      'left',        # 文字の水平方向の寄せ。規定値 None。'left', 'fill', 'centerContinuous', 'center', 'right', 'general', 'justify', 'distributed' のいずれか。指定しないなら None
        'vertical_alignment_of_node':        None,          # 文字の垂直方向の寄せ。規定値 None。'bottom', 'center', 'top', 'justify', 'distributed' のいずれか。指定しないなら None
    }

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/no_4_uneven_coin.xlsx', mode='w', settings=settings)

    # ワークシート描画
    wbc.render_worksheet(target='UnevenCoin', based_on='./examples/data/uneven_coin.csv')
    WorksheetDumpControl.dump(worksheet=wbc._ws, file='./tests/temp/actual/no_4_uneven_coin_UnevenCoin.log')     # テスト用

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
    print(f"[{datetime.datetime.now()}] Please look {wbc.workbook_file_path}")
