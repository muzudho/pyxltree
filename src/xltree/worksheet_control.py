import datetime
from .models.database import Table
from .models.tree_structure import TreeStructureBasedOnTable
from .settings import Settings
from .workbooks import TreeDrawer, TreeEraser


class WorksheetControl():
    """ワークシート制御"""


    @staticmethod
    def instantiate(target, based_on, ws, settings_obj, debug_write=False):
        """生成

        Parameters
        ----------
        target : str
            シート名
        based_on : str
            CSVファイルパス
        ws : Worksheet
            ワークシート
        settings_obj : Settings
            各種設定
        debug_write : bool
            デバッグライト
        """

        # CSV読込
        table = Table.from_csv(file_path=based_on)

        # table からツリー構造を作成
        #
        #   NOTE マルチ根にも対応していることに注意してください
        #
        tree_structure = TreeStructureBasedOnTable.read(table=table)

        return WorksheetControl(target=target, based_on=based_on, ws=ws, settings_obj=settings_obj, table=table, tree_structure=tree_structure, debug_write=debug_write)


    def __init__(self, target, based_on, ws, settings_obj, table, tree_structure, debug_write=False):
        """初期化

        Parameters
        ----------
        target : str
            シート名
        based_on : str
            CSVファイルパス
        ws : Worksheet
            ワークシート
        settings_obj : Settings
            各種設定
        table : Table
            データテーブル
        tree_structure : TreeStructureBasedOnTable
            木構造
        debug_write : bool
            デバッグライト
        """
        self._target = target
        self._based_on = based_on
        self._ws = ws
        self._settings_obj = settings_obj
        self._table = table
        self._tree_structure = tree_structure
        self._debug_write = debug_write


    @property
    def tree_structure(self):
        """ツリー構造。マルチ根に対応していることに注意してください"""
        return self._tree_structure


    def render_tree(self):
        """木の描画"""

        # ツリードロワーを用意、描画（都合上、要らない罫線が付いています）
        tree_drawer = TreeDrawer(table=self._table, ws=self._ws, settings_obj=self._settings_obj, debug_write=self._debug_write)
        tree_drawer.render()


        # 要らない罫線を消す
        # DEBUG_TIPS: このコードを不活性にして、必要な線は全部描かれていることを確認してください
        if True:
            tree_eraser = TreeEraser(table=self._table, ws=self._ws, settings_obj=self._settings_obj, debug_write=self._debug_write)
            tree_eraser.render()
        else:
            if self._debug_write:
                print(f"[{datetime.datetime.now()}] eraser disabled")
