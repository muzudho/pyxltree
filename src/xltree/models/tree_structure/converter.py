from collections import deque
from . import TreeEntry


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
        multiple_root_entry : dict<TreeEntry>
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
                self._pre_parent_tree_entry = None
        
        context = Context()


        def set_node(self, context, leaf_th, depth, node_in_record):
#             print(f"""[set_node] {depth=}
# {node_in_record._stringify_dump('')}""")

            # 既存のマルチ根かもしれない
            if depth==0 and node_in_record.text in self._multiple_root:
                tree_entry = self._multiple_root[node_in_record.text]

            # 未作成のノードなら
            elif context._pre_parent_tree_entry is None or node_in_record._pack_key() not in context._pre_parent_tree_entry.child_entries:
                tree_entry = TreeEntry(
                        parent_entry=context._pre_parent_tree_entry,
                        edge_text=node_in_record.edge_text,
                        node_text=node_in_record.text,
                        child_entries={},     # 子要素は、子から戻ってきたときじゃないと分からない
                        leaf_th=leaf_th)
            
            # 既存のノードなら
            else:
                tree_entry = context._pre_parent_tree_entry.child_entries[node_in_record._pack_key()]


            context._pre_parent_tree_entry = tree_entry
            context._stack.append(tree_entry)


        # if row_number == 0:
        #     print("最初のレコードは、根ノードから葉ノードまで全部揃ってる")

        def get_leaf_th(record, depth):
            if depth<record.len_of_path_from_root_to_leaf:
                return record.no
            return None

        record.for_each_node_in_path(set_node=lambda depth, node_in_record: set_node(self=self, context=context, leaf_th=get_leaf_th(record=record, depth=depth), depth=depth, node_in_record=node_in_record))


        prev_child_tree_entry = None

        # 葉から根に向かってノードを読取
        while 0 < len(context._stack):
            tree_entry = context._stack.pop()

            # 子を、子要素として追加
            if prev_child_tree_entry is not None:
                tree_entry.child_entries[prev_child_tree_entry._pack_key()] = prev_child_tree_entry

            #print(f"逆読み  {tree_entry.edge_text=}  {tree_entry.node_text=}")
            prev_child_tree_entry = tree_entry


        if len(context._stack) != 0:
            raise ValueError(f"スタックのサイズが0でないのはおかしい  {len(context._stack)=}")


        # ルートノードを記憶
        self._multiple_root[tree_entry.node_text] = tree_entry


#         print(f"""レコード読取  {row_number=}
# root_entry:
# {tree_entry._stringify_dump('')}
# record:
# {record._stringify_dump('')}""")
