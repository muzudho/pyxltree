from ...library import INDENT


################
# REMARK: Forest
################
class Forest():
    """TODO 森"""


    def __init__(self):
        self._multiple_root = {}


    def tree_root(self, edge_text, text):
        """TODO 根ノードでのエッジテキストは未対応するか？"""
        root_node = TreeNode(parent_node=None, edge_text=edge_text, text=text, child_nodes={}, leaf_th=None)

        if root_node._pack_key() in self._multiple_root:
            raise ValueError(f"key exists  {root_node._pack_key()=}")

        self._multiple_root[root_node._pack_key()] = root_node

        return root_node


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


    def __init__(self, parent_node, edge_text, text, child_nodes, leaf_th=None):
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
        """
        self._parent_node = parent_node
        self._edge_text = edge_text
        self._text = text
        self._child_nodes = child_nodes
        self._leaf_th = leaf_th


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
    

    def grow(self, edge_text, text):
        """子要素を生やします"""
        child_node = TreeNode(parent_node=self, edge_text=edge_text, text=text, child_nodes={})

        if child_node._pack_key() in self._child_nodes:
            raise ValueError(f"key exists  {child_node._pack_key()=}")

        self._child_nodes[child_node._pack_key()] = child_node


    def _pack_key(self):
        return (self._edge_text, self._text)


    def _stringify_like_tree(self, indent):
        succ_indent = indent + INDENT

        items = []
        for child_node in self._child_nodes.values():
            items.append(child_node._stringify_like_tree(indent=succ_indent))

        if self._edge_text is not None:
            edge_arrow = f"--{self._edge_text}-->"
        else:
            edge_arrow = "---->"

        return f"""\
{indent}{edge_arrow}{self._text}
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
