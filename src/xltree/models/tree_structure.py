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

        # マルチ根
        self._multi_root = {}

        # 現在ノード
        self._cur_tree_node = None


    def read(self):
        """TODO テーブル読取
        
        Returns
        -------
        root_node : TreeNode        
        """

        # 上のレコードから順に読み込んでいけば作れる
        self._table.for_each(self.on_record_read)

        # ダンプ
        print("[read] マルチ根")
        for root in self._multi_root.values():
            print(f"{root.stringify_like_tree('    ')}")

        return None # FIXME


    def on_record_read(self, row_number, record):
        """TODO レコード読取
        
        例えば ^ をマルチ根の親とするとき、
        ^, A, B, C
        ^, A, B, D
        という２レコードを読込むとき、 
        ２行目では A, B というパスは既存。

        """

        class Context():
            def __init__(self):
                self._stack = deque()
                self._pre_parent_tree_node = None
        
        context = Context()


        def set_node(self, context, depth, node):
#             print(f"""[set_node] {depth=}
# {node.stringify_dump('')}""")

            # 既存のマルチ根かもしれない
            if depth==0 and node.text in self._multi_root:
                tree_node = self._multi_root[node.text]

            # 未作成のノードなら
            elif context._pre_parent_tree_node is None or node.text not in context._pre_parent_tree_node.child_nodes:
                tree_node = TreeNode(
                        parent_node=context._pre_parent_tree_node,
                        edge_text=node.edge_text,
                        text=node.text,
                        child_nodes={})    # 子要素は、子から戻ってきたときじゃないと分からない
            
            # 既存のノードなら
            else:
                tree_node = context._pre_parent_tree_node.child_nodes[node.text]

            self._cur_tree_node = tree_node

            context._pre_parent_tree_node = tree_node
            context._stack.append(tree_node)


        # if row_number == 0:
        #     print("最初のレコードは、根ノードから葉ノードまで全部揃ってる")


        record.for_each_node_in_path(set_node=lambda depth, node: set_node(self, context, depth, node))


        prev_child_tree_node = None

        # 葉から根に向かってノードを読取
        while 0 < len(context._stack):
            tree_node = context._stack.pop()
            self._cur_tree_node = tree_node

            # 子を、子要素として追加
            if prev_child_tree_node is not None:
                tree_node.child_nodes[prev_child_tree_node.text] = prev_child_tree_node

            #print(f"逆読み  {tree_node.edge_text=}  {tree_node.text=}")
            prev_child_tree_node = tree_node


        if len(context._stack) != 0:
            raise ValueError(f"スタックのサイズが0でないのはおかしい  {len(context._stack)=}")


        # ルートノードを記憶
        self._multi_root[tree_node.text] = tree_node


#         print(f"""レコード読取  {row_number=}
# root_node:
# {tree_node.stringify_dump('')}
# record:
# {record.stringify_dump('')}""")


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
        child_nodes : dict<text, TreeNode>
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
        """子ノードの辞書"""
        return self._child_nodes


    def get_child_by_text(self, text):
        return self._child_nodes.get(text)


    def stringify_like_tree(self, indent):
        succ_indent = indent + INDENT

        items = []
        for child_node in self._child_nodes.values():
            items.append(child_node.stringify_like_tree(indent=succ_indent))

        if self._edge_text is not None:
            edge_arrow = f"--{self._edge_text}-->"
        else:
            edge_arrow = "---->"

        return f"""\
{indent}{edge_arrow}{self._text}
{''.join(items)}"""


    def stringify_dump(self, indent):
        succ_indent = indent + INDENT

        items = []
        for child_node in self._child_nodes.values():
            items.append(child_node.stringify_dump(indent=succ_indent))

        return f"""\
{indent}TreeNode
{indent}--------
{succ_indent}{self._edge_text=}
{succ_indent}{self._text=}
{''.join(items)}"""
