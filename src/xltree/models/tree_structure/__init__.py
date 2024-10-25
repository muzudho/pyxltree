from ...library import INDENT


################
# REMARK: Forest
################
class Forest():
    """森"""


    def __init__(self):
        self._multiple_root_entry = {}

        # 探索時に使用する一時変数
        self._temp_leaf_th = None


    @property
    def multiple_root_entry(self):
        return self._multiple_root_entry


    def tree_root(self, edge_text, node_text):
        """TODO 根ノードでのエッジテキストは未対応するか？"""
        root_entry = TreeEntry(parent_entry=None, edge_text=edge_text, node_text=node_text, child_entries={}, leaf_th=None)

        if root_entry._pack_key() in self._multiple_root_entry:
            raise ValueError(f"key exists  {root_entry._pack_key()=}")

        self._multiple_root_entry[root_entry._pack_key()] = root_entry

        return root_entry


    def renumbering(self):
        """番号の振り直し"""

        self._temp_leaf_th = 1

        for root_entry in self._multiple_root_entry.values():
            self.renumbering_child(root_entry)


    def renumbering_child(self, node):
        # 葉
        if len(node.child_entries) == 0:
            node.leaf_th = self._temp_leaf_th
            self._temp_leaf_th += 1
            return

        for child_entry in node._child_entries.values():
            self.renumbering_child(child_entry)  # 再帰


    def _stringify_like_tree(self, indent):
        items = []
        
        for root_entry in self._multiple_root_entry.values():
            items.append(root_entry._stringify_like_tree(indent=indent, as_root=True))

        return f"""\
{''.join(items)}"""


###############
# REMARK: Entry
###############
class TreeEntry():
    """ツリー・エントリー

    エッジとノードのペア
    
    イミュータブルにすると生成が難しいので、ミュータブルとする
    """


    def __init__(self, parent_entry, edge_text, node_text, child_entries, leaf_th=None, remainder_columns=None):
        """初期化
        
        Parameters
        ----------
        parent_entry : TreeEntry
            親ノード
        edge_text : str
            エッジのテキスト
        node_text : str
            ノードのテキスト
        child_entries : dict<tuple(str, str), TreeEntry>
            子ノードを格納した辞書。キーはエッジテキストとノードテキストのタプル
            FIXME キーがメモリを消費しすぎていないか？仕方ない？
        leaf_th : int
            有れば１から始まる葉番号、無ければナン
        remainder_columns : dict
            有れば、ツリー構造に含まれなかった列の辞書。無ければナン
        """
        self._parent_entry = parent_entry
        self._edge_text = edge_text
        self._node_text = node_text
        self._child_entries = child_entries
        self._leaf_th = leaf_th
        self._remainder_columns = remainder_columns


    @property
    def parent_entry(self):
        """親ノード"""
        return self._parent_entry


    @property
    def edge_text(self):
        """エッジのテキスト"""
        return self._edge_text


    @property
    def node_text(self):
        """ノードのテキスト"""
        return self._node_text


    @property
    def child_entries(self):
        """子ノードを格納した辞書。キーはエッジテキストとノードテキストのタプル
        FIXME キーがメモリを消費しすぎていないか？仕方ない？"""
        return self._child_entries


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


    def leaf(self, edge_text, node_text, remainder_columns):
        """葉要素を生やします"""
        leaf_entry = self.grow(edge_text=edge_text, node_text=node_text)

        leaf_entry.remainder_columns = remainder_columns

        return leaf_entry


    def grow(self, edge_text, node_text):
        """子要素を生やします"""
        child_entry = TreeEntry(parent_entry=self, edge_text=edge_text, node_text=node_text, child_entries={})

        if child_entry._pack_key() in self._child_entries:
            raise ValueError(f"key exists  {child_entry._pack_key()=}")

        self._child_entries[child_entry._pack_key()] = child_entry

        return child_entry


    def _pack_key(self):
        return (self._edge_text, self._node_text)


    def _stringify_like_tree(self, indent, as_root=False):
        succ_indent = indent + INDENT


        if as_root:
            et = '──'
        else:
            et = '└─'


        if self._edge_text is not None:
            et += f"{self._edge_text}─"


        if len(self._child_entries) == 0:
            icon = f'📄 ({self._leaf_th})'
        else:
            icon = '📁'


        if self._remainder_columns is not None:
            remander_columns_text = f"  {self._remainder_columns}"
        else:
            remander_columns_text = ''


        items = []
        for child_entry in self._child_entries.values():
            items.append(child_entry._stringify_like_tree(indent=succ_indent))


        return f"""\
{indent}{et} {icon} {self._node_text}{remander_columns_text}
{''.join(items)}"""


    def _stringify_dump(self, indent):
        succ_indent = indent + INDENT

        items = []
        for child_entry in self._child_entries.values():
            items.append(child_entry._stringify_dump(indent=succ_indent))

        return f"""\
{indent}TreeEntry
{indent}---------
{succ_indent}{self._edge_text=}
{succ_indent}{self._node_text=}
{succ_indent}{self._remainder_columns=}
{''.join(items)}"""
