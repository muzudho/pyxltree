import os
import datetime
import openpyxl as xl
from .settings import Settings
from .worksheet_control import WorksheetControl


class WorkbookControl():
    """ワークブック制御"""


    def __init__(self, target, mode, settings={}, debug_write=False):
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
        self._settings_obj = Settings(dictionary=settings)
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
            
            elif self._mode == 'w':
                pass
            
            else:
                raise ValueError(f"unsupported {self._mode=}")

                    
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


    def get_worksheet(self, sheet_name):
        """ワークシートの取得"""
        return self._wb[sheet_name]
