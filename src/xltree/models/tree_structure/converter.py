from collections import deque
from . import TreeNode


#######################
# REMARK: TreeStructure
#######################
class TreeStructureBasedOnTable():
    """テーブル構造を読み込んだ、マルチ根を持つ木構造"""


    @staticmethod
    def read_multiple_root(table):
        """テーブル読取

        Parameters
        ----------
        table : Table
            データテーブル

        Returns
        -------
        multiple_root_node : dict<TreeNode>
            マルチ根
        """

        tree_structure = TreeStructureBasedOnTable()

        # 先頭のレコードから順に読み込んでいけば作れる
        table.for_each(tree_structure.on_record_read)

        # # ダンプ
        # print("[read] マルチ根")
        # for root in tree_structure._multiple_root.values():
        #     print(f"{root._stringify_like_tree('    ')}")

        return tree_structure._multiple_root


    def __init__(self):
        """初期化"""

        # マルチ根
        self._multiple_root = {}


    def on_record_read(self, row_number, record):
        """レコード読取
        
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


        def set_node(self, context, leaf_th, depth, node_in_record):
#             print(f"""[set_node] {depth=}
# {node_in_record._stringify_dump('')}""")

            # 既存のマルチ根かもしれない
            if depth==0 and node_in_record.text in self._multiple_root:
                tree_node = self._multiple_root[node_in_record.text]

            # 未作成のノードなら
            elif context._pre_parent_tree_node is None or node_in_record._pack_key() not in context._pre_parent_tree_node.child_nodes:
                tree_node = TreeNode(
                        parent_node=context._pre_parent_tree_node,
                        edge_text=node_in_record.edge_text,
                        text=node_in_record.text,
                        child_nodes={},     # 子要素は、子から戻ってきたときじゃないと分からない
                        leaf_th=leaf_th)
            
            # 既存のノードなら
            else:
                tree_node = context._pre_parent_tree_node.child_nodes[node_in_record._pack_key()]


            context._pre_parent_tree_node = tree_node
            context._stack.append(tree_node)


        # if row_number == 0:
        #     print("最初のレコードは、根ノードから葉ノードまで全部揃ってる")

        def get_leaf_th(record, depth):
            if depth<record.len_of_path_from_root_to_leaf:
                return record.no
            return None

        record.for_each_node_in_path(set_node=lambda depth, node_in_record: set_node(self=self, context=context, leaf_th=get_leaf_th(record=record, depth=depth), depth=depth, node_in_record=node_in_record))


        prev_child_tree_node = None

        # 葉から根に向かってノードを読取
        while 0 < len(context._stack):
            tree_node = context._stack.pop()

            # 子を、子要素として追加
            if prev_child_tree_node is not None:
                tree_node.child_nodes[prev_child_tree_node._pack_key()] = prev_child_tree_node

            #print(f"逆読み  {tree_node.edge_text=}  {tree_node.text=}")
            prev_child_tree_node = tree_node


        if len(context._stack) != 0:
            raise ValueError(f"スタックのサイズが0でないのはおかしい  {len(context._stack)=}")


        # ルートノードを記憶
        self._multiple_root[tree_node.text] = tree_node


#         print(f"""レコード読取  {row_number=}
# root_node:
# {tree_node._stringify_dump('')}
# record:
# {record._stringify_dump('')}""")
