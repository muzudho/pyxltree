import os
import datetime
import openpyxl as xl

from .database import TreeTable
from .workbooks import TreeDrawer, TreeEraser


class Settings():
    """各種設定"""


    def __init__(
        self,
        dictionary=None):
        """初期化
        
        Parameters
        ----------
        dictionary : dict
            設定

            列の幅設定。width はだいたい 'ＭＳ Ｐゴシック' サイズ11 の半角英文字の個数
            * `no_width` - A列の幅。no列
            * `row_header_separator_width` - B列の幅。空列
            * `node_width` - 例：C, F, I ...列の幅。ノードの箱の幅
            * `parent_side_edge_width` - 例：D, G, J ...列の幅。エッジの水平線のうち、親ノードの方
            * `child_side_edge_width` - 例：E, H, K ...列の幅。エッジの水平線のうち、子ノードの方

            行の高さ設定。height の単位はポイント。既定値 8。昔のアメリカ人が椅子に座ってディスプレイを見たとき 1/72 インチに見える大きさが 1ポイント らしいが、そんなんワカラン。目視確認してほしい
            * `header_height` - 第１行。ヘッダー
            * `column_header_separator_height` - 第２行。空行

            ヘッダー関連
            * `header_bgcolor_1` - ヘッダーの背景色その１
            * `header_bgcolor_2` - ヘッダーの背景色その２
            * `header_fgcolor_1` - ヘッダーの文字色その１
            * `header_fgcolor_2` - ヘッダーの文字色その２

            * 色の参考： 📖 [Excels 56 ColorIndex Colors](https://www.excelsupersite.com/what-are-the-56-colorindex-colors-in-excel/)

            ノード関連
            * `node_horizontal_alignment` - 文字の水平方向の寄せ。規定値 None。'left', 'fill', 'centerContinuous', 'center', 'right', 'general', 'justify', 'distributed' のいずれか。指定しないなら None
            * `node_vertical_alignment` - 文字の垂直方向の寄せ。規定値 None。'bottom', 'center', 'top', 'justify', 'distributed' のいずれか。指定しないなら None
        """

        # 既定のディクショナリー
        self._dictionary = {
            # 列の幅
            'no_width':                         4,
            'row_header_separator_width':       3,
            'node_width':                       20,
            'parent_side_edge_width':           2,
            'child_side_edge_width':            4,

            # 行の高さ
            'header_height':                    13,
            'column_header_separator_height':   13,

            # ヘッダー関連
            'header_bgcolor_1':                 'CCCCCC',
            'header_bgcolor_2':                 '333333',
            'header_fgcolor_1':                 '111111',
            'header_fgcolor_2':                 'EEEEEE',

            # ノード関連
            'node_horizontal_alignment':        None,
            'node_vertical_alignment':          None,
        }

        # 上書き
        if dictionary is not None:
            for key, value in dictionary.items():
                self._dictionary[key] = value


    @property
    def dictionary(self):
        return self._dictionary


class WorkbookControl():
    """ワークブック制御"""


    def __init__(self, target, mode, settings=Settings(), debug_write=False):
        """初期化

        Parameters
        ----------
        target : str
            ワークブック（.xlsx）へのファイルパス
        mode : str
            既存のワークブックが有ったときの挙動。 'w' は新規作成して置換え、 'a' は追記
        settings : Settings
            各種設定
        """
        self._wb_file_path = target
        self._mode = mode
        self._settings = settings
        self._debug_write = debug_write
        self._wb = None
        self._ws = None


    @property
    def workbook_file_path(self):
        return self._wb_file_path


    def render_worksheet(self, target, based_on, debug_write=False):
        """ワークシート描画

        Parameters
        ----------
        target : str
            シート名
        based_on : str
            CSVファイルパス
        debug_write : bool
            デバッグライト
        """

        if self._wb is None:
            self.ready_workbook()

        self.ready_worksheet(target=target)

        # CSV読込
        tree_table = TreeTable.from_csv(file_path=based_on)

        # ツリードロワーを用意、描画（都合上、要らない罫線が付いています）
        tree_drawer = TreeDrawer(tree_table=tree_table, ws=self._ws, settings=self._settings, debug_write=debug_write)
        tree_drawer.render()


        # 要らない罫線を消す
        # DEBUG_TIPS: このコードを不活性にして、必要な線は全部描かれていることを確認してください
        if True:
            tree_eraser = TreeEraser(tree_table=tree_table, ws=self._ws, debug_write=debug_write)
            tree_eraser.render()
        else:
            if self._debug_write:
                print(f"[{datetime.datetime.now()}] eraser disabled")


    def remove_worksheet(self, target):
        """存在すれば、指定のワークシートの削除。存在しなければ無視

        Parameters
        ----------
        target : str
            シート名
        """

        if self.exists_sheet(target=target):
            if self._debug_write:
                print(f"[{datetime.datetime.now()}] remove `{target}` sheet...")

            self._wb.remove(self._wb[target])


    def save_workbook(self):
        """ワークブックの保存"""

        if self._debug_write:
            print(f"[{datetime.datetime.now()}] save `{self._wb_file_path}` file...")

        # ワークブックの保存            
        self._wb.save(self._wb_file_path)


    def ready_workbook(self):
        """ワークブックを準備する"""

        # 既存のファイルが有ったときの挙動
        if os.path.isfile(self._wb_file_path):
            # 既存のファイルへ追記
            if self._mode == 'a':
                if self._debug_write:
                    print(f"[{datetime.datetime.now()}] `{self._wb_file_path}` file exists, read.")

                self._wb = xl.load_workbook(filename=self._wb_file_path)

                return
                    
        # ワークブックを新規生成
        if self._debug_write:
            print(f"[{datetime.datetime.now()}] `{self._wb_file_path}` file not exists, create.")

        self._wb = xl.Workbook()


    def exists_sheet(self, target):
        """シートの存在確認
        
        Parameters
        ----------
        target : str
            シート名
        """
        return target in self._wb.sheetnames


    def ready_worksheet(self, target):
        """ワークシートを準備する
        
        Parameters
        ----------
        target : str
            シート名
        """

        # シートを作成
        if not self.exists_sheet(target):
            if self._debug_write:
                print(f"[{datetime.datetime.now()}] create `{target}` sheet...")

            self._wb.create_sheet(target)


        self._ws = self._wb[target]
