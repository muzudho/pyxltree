from collections import deque
from ..library import INDENT


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

        class Context():
            def __init__(self):
                self._stack = deque()
                self._pre_parent_tree_node = None
        
        context = Context()


        def set_node(self, context, depth, node):
            print(f"""[set_node] {depth=}
{node.stringify_dump('')}""")

            tree_node = TreeNode(
                    parent_node=context._pre_parent_tree_node,
                    edge_text=node.edge_text,
                    text=node.text,
                    child_nodes=[])    # 子要素は、子から戻ってきたときじゃないと分からない
            context._pre_parent_tree_node = tree_node
            context._stack.append(tree_node)


        if row_number == 0:
            print("最初のレコードは、根ノードから葉ノードまで全部揃ってる")


        record.for_each_node_in_path(set_node=lambda depth, node: set_node(self, context, depth, node))


        prev_child_tree_node = None

        # 葉から根に向かってノードを読取
        while 0 < len(context._stack):
            tree_node = context._stack.pop()

            # 子を、子要素として追加
            if prev_child_tree_node is not None:
                tree_node.child_nodes.append(prev_child_tree_node)

            print(f"逆読み  {tree_node.edge_text=}  {tree_node.text=}")
            prev_child_tree_node = tree_node


        if len(context._stack) != 0:
            raise ValueError(f"スタックのサイズが0でないのはおかしい  {len(context._stack)=}")


        print(f"""レコード読取  {row_number=}
root_node:
{tree_node.stringify_dump('')}
record:
{record.stringify_dump('')}""")
        pass


##############
# REMARK: Node
##############
class TreeNode():
    """ツリーノード
    
    イミュータブルにすると生成が難しいので、ミュータブルとする
    """


    def __init__(self, parent_node, edge_text, text, child_nodes):
        """初期化
        
        Parameters
        ----------
        parent_node : TreeNode
            親ノード
        edge_text : str
            エッジのテキスト
        text : str
            テキスト
        child_nodes : list<TreeNode>
            子ノード
        """
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


    def stringify_dump(self, indent):
        succ_indent = indent + INDENT

        items = []
        for node in self._child_nodes:
            items.append(node.stringify_dump(indent=succ_indent))

        return f"""\
{indent}TreeNode
{indent}--------
{succ_indent}{self._edge_text=}
{succ_indent}{self._text=}
{''.join(items)}
"""
