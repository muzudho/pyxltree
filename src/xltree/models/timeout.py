import time


class Timeout():
    """時間のかかる処理をタイムアップさせるためのタイマー"""


    def __init__(self, seconds=864000.0):
        """初期化、および開始
        
        Parameters
        ----------
        seconds : float
            この時間（秒）を経過すると中止
        """
        self._start_time = time.time()
        self._seconds = seconds
        self._message = None


    @property
    def message(self):
        """str タイムアウトの原因"""
        return self._message


    def is_expired(self, message):
        """タイムアウトしたか

        Parameters
        ----------
        message : str
            タイムアウトした原因。既に設定されていた場合は上書きされません
        """
        end_time = time.time()
        erapsed_time = end_time - self._start_time
        is_expired = self._seconds <= erapsed_time

        if is_expired and self._message is None:
            self._message = message

        return is_expired


    def remaining(self):
        """残り時間（秒）"""
        end_time = time.time()
        erapsed_time = end_time - self._start_time
        secs = self._seconds - erapsed_time

        if secs < 0:
            secs = 0

        return secs
