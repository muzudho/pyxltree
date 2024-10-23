import os
import datetime
import openpyxl as xl
from .settings import Settings
from .worksheet_control import WorksheetControl


@staticmethod
def prepare_workbook(target, mode, settings={}, debug_write=False):
    """ワークブックを用意します
    
    Returns
    -------
    target : str
        ワークブック（.xlsx）へのファイルパス
    mode : str
        既存のワークブックが有ったときの挙動。 'w' は新規作成して置換え、 'a' は追記
    settings : dict
        各種設定    
    debug_write : bool
        デバッグライト
    """

    wb = None

    # 既存のファイルが有ったときの挙動
    if os.path.isfile(target):
        # 既存のファイルへ追記
        if mode == 'a':
            if debug_write:
                print(f"[{datetime.datetime.now()}] `{target}` file exists, read.")

            # ワークブックを開く
            wb = xl.load_workbook(filename=target)
        
        elif mode == 'w':
            pass
        
        else:
            raise ValueError(f"unsupported {mode=}")

                
    # ワークブックを新規生成
    if wb is None:
        if debug_write:
            print(f"[{datetime.datetime.now()}] `{target}` file not exists, create.")

        wb = xl.Workbook()


    return WorkbookControl(target=target, mode=mode, wb=wb, settings=settings, debug_write=debug_write)


class XltreeInSrc():
    """テストで使う仕組み

    テストでは

        import xltree as tr

    のように書けないので、
    テストでは以下のように書く

        from src.xltree import xltree_in_src as tr
    
    """

    @staticmethod
    def prepare_workbook(target, mode, settings={}, debug_write=False):
        """グローバル関数の prepare_workbook() を呼び出す
        
        Returns
        -------
        target : str
            ワークブック（.xlsx）へのファイルパス
        mode : str
            既存のワークブックが有ったときの挙動。 'w' は新規作成して置換え、 'a' は追記
        settings : dict
            各種設定    
        debug_write : bool
            デバッグライト
        """
        global prepare_workbook

        return prepare_workbook(target=target, mode=mode, settings=settings, debug_write=debug_write)


xltree_in_src = XltreeInSrc()


class WorkbookControl():
    """ワークブック制御"""




    def __init__(self, target, mode, wb, settings={}, debug_write=False):
        """初期化

        Parameters
        ----------
        target : str
            ワークブック（.xlsx）へのファイルパス
        mode : str
            既存のワークブックが有ったときの挙動。 'w' は新規作成して置換え、 'a' は追記
        settings : dict
            各種設定
        """
        self._wb_file_path = target
        self._mode = mode
        self._wb = wb
        self._settings_obj = Settings(dictionary=settings)
        self._debug_write = debug_write
        self._ws = None


    @property
    def workbook_file_path(self):
        return self._wb_file_path


    def open_worksheet(self, target, based_on, debug_write=False):
        """TODO ワークシート読取"""

        # ワークシートの準備
        self.ready_worksheet(target=target)

        # ワークシート制御の生成
        return WorksheetControl.instantiate(target=target, based_on=based_on, ws=self._ws, settings_obj=self._settings_obj, debug_write=debug_write)



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

        # ワークシートの準備
        self.ready_worksheet(target=target)

        # ワークシート制御の生成
        wsc = WorksheetControl.instantiate(target=target, based_on=based_on, ws=self._ws, settings_obj=self._settings_obj, debug_write=debug_write)

        # 木の描画
        wsc.render_tree()


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


    def get_worksheet(self, sheet_name):
        """ワークシートの取得"""
        return self._wb[sheet_name]
