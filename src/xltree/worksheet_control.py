import os
import datetime
import openpyxl as xl
from .models.database import Table
from .settings import Settings
from .workbooks import TreeDrawer, TreeEraser


class WorksheetControl():
    """ワークシート制御"""


    def __init__(self, target, based_on, ws, debug_write=False):
        """初期化

        Parameters
        ----------
        target : str
            シート名
        based_on : str
            CSVファイルパス
        ws : Worksheet
            ワークシート
        debug_write : bool
            デバッグライト
        """
        self._target = target
        self._based_on = based_on
        self._ws = ws
        self._debug_write = debug_write
