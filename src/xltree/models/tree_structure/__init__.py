from ...library import INDENT


################
# REMARK: Forest
################
class Forest():
    """TODO 森"""


    def __init__(self):
        self._multiple_root = {}
        self._temp_leaf_th = None


    def tree_root(self, edge_text, text):
        """TODO 根ノードでのエッジテキストは未対応するか？"""
        root_node = TreeNode(parent_node=None, edge_text=edge_text, text=text, child_nodes={}, leaf_th=None)

        if root_node._pack_key() in self._multiple_root:
            raise ValueError(f"key exists  {root_node._pack_key()=}")

        self._multiple_root[root_node._pack_key()] = root_node

        return root_node


    def renumbering(self):
        """番号の振り直し"""

        self._temp_leaf_th = 1

        for root_node in self._multiple_root.values():
            self.renumbering_child(root_node)


    def renumbering_child(self, node):
        # 葉
        if len(node.child_nodes) == 0:
            node.leaf_th = self._temp_leaf_th
            self._temp_leaf_th += 1
            return

        for child_node in node._child_nodes.values():
            self.renumbering_child(child_node)  # 再帰


    def _stringify_like_tree(self, indent):
        succ_indent = indent + INDENT

        items = []
        
        for root_node in self._multiple_root.values():
            items.append(root_node._stringify_like_tree(indent=succ_indent))

        return f"""\
{''.join(items)}"""


##############
# REMARK: Node
##############
class TreeNode():
    """ツリーノード
    
    イミュータブルにすると生成が難しいので、ミュータブルとする
    """


    def __init__(self, parent_node, edge_text, text, child_nodes, leaf_th=None, remainder_columns=None):
        """初期化
        
        Parameters
        ----------
        parent_node : TreeNode
            親ノード
        edge_text : str
            エッジのテキスト
        text : str
            テキスト
        child_nodes : dict<tuple(str, str), TreeNode>
            子ノードを格納した辞書。キーはエッジテキストとノードテキストのタプル
            FIXME キーがメモリを消費しすぎていないか？仕方ない？
        leaf_th : int
            有れば１から始まる葉番号、無ければナン
        remainder_columns : dict
            有れば、ツリー構造に含まれなかった列の辞書。無ければナン
        """
        self._parent_node = parent_node
        self._edge_text = edge_text
        self._text = text
        self._child_nodes = child_nodes
        self._leaf_th = leaf_th
        self._remainder_columns = remainder_columns


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
        """子ノードを格納した辞書。キーはエッジテキストとノードテキストのタプル
        FIXME キーがメモリを消費しすぎていないか？仕方ない？"""
        return self._child_nodes


    @property
    def leaf_th(self):
        """有れば１から始まる葉番号、無ければナン"""
        return self._leaf_th


    @leaf_th.setter
    def leaf_th(self, value):
        """有れば１から始まる葉番号、無ければナン"""
        self._leaf_th = value


    @property
    def remainder_columns(self):
        """有れば、ツリー構造に含まれなかった列の辞書。無ければナン"""
        return self._remainder_columns


    @remainder_columns.setter
    def remainder_columns(self, value):
        """有れば、ツリー構造に含まれなかった列の辞書。無ければナン"""
        self._remainder_columns = value


    def leaf(self, edge_text, text, remainder_columns):
        """葉要素を生やします"""
        leaf_node = self.grow(edge_text=edge_text, text=text)

        leaf_node.remainder_columns = remainder_columns

        return leaf_node


    def grow(self, edge_text, text):
        """子要素を生やします"""
        child_node = TreeNode(parent_node=self, edge_text=edge_text, text=text, child_nodes={})

        if child_node._pack_key() in self._child_nodes:
            raise ValueError(f"key exists  {child_node._pack_key()=}")

        self._child_nodes[child_node._pack_key()] = child_node

        return child_node


    def _pack_key(self):
        return (self._edge_text, self._text)


    def _stringify_like_tree(self, indent):
        succ_indent = indent + INDENT


        if self._edge_text is not None:
            et = f"└─{self._edge_text}─"
        else:
            et = "└──"


        if len(self._child_nodes) == 0:
            icon = f'📄 ({self._leaf_th}) '
        else:
            icon = '📁'


        if self._remainder_columns is not None:
            remander_columns_text = f"  {self._remainder_columns}"
        else:
            remander_columns_text = ''


        items = []
        for child_node in self._child_nodes.values():
            items.append(child_node._stringify_like_tree(indent=succ_indent))


        return f"""\
{indent}{et} {icon} {self._text}{remander_columns_text}
{''.join(items)}"""


    def _stringify_dump(self, indent):
        succ_indent = indent + INDENT

        items = []
        for child_node in self._child_nodes.values():
            items.append(child_node._stringify_dump(indent=succ_indent))

        return f"""\
{indent}TreeNode
{indent}--------
{succ_indent}{self._edge_text=}
{succ_indent}{self._text=}
{''.join(items)}"""
