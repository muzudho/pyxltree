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
