################
# REMARK: Reader
################
class TableReaderLikeTree():
    """木構造のようにテーブル構造を読むもの"""


    def __init__(self, table):
        """初期化
        
        Parameters
        ----------
        table : Table
            データテーブル
        """
        self._table = table


    def read(self):
        """TODO テーブル読取
        
        Returns
        -------
        root_node : TreeNode        
        """

        # 上のレコードから順に読み込んでいけば作れる
        self._table.for_each(self.on_record_read)

        return None # FIXME


    def on_record_read(self, row_number, record):
        """TODO レコード読取"""

        if row_number == 0:
            print("最初のレコードは、根ノードから葉ノードまで全部揃ってる")
            
        print(f"""レコード読取  {row_number=}
{record.stringify_dump('')}""")
        pass


##############
# REMARK: Node
##############
class TreeNode():
    """ツリーノード"""


    def __init__(self, parent_node, edge_text, text, child_nodes):
        """初期化"""
        self._parent_node = parent_node
        self._edge_text = edge_text
        self._text = text
        self._child_nodes = child_nodes


    @property
    def parent_node(self):
        """親ノード"""
        return self._parent_node


    @property
    def edge_text(self):
        """エッジ・テキスト"""
        return self._edge_text


    @property
    def text(self):
        """テキスト"""
        return self._text
    

    @property
    def child_nodes(self):
        """子ノードのリスト"""
        return self._child_nodes
