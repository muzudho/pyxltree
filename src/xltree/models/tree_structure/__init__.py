import pandas as pd
from ...library import INDENT


##############
# MARK: Forest
##############
class Forest():
    """森"""


    def __init__(self):
        self._multiple_root_entry = {}

        self._remainder_column_name_list = []

        # 探索時に使用する一時変数
        self._temp_leaf_th = None


    @property
    def multiple_root_entry(self):
        return self._multiple_root_entry


    @property
    def remainder_column_name_list(self):
        """ツリー構造には含まないテーブル列の並び順を指定するのに使います"""
        return self._remainder_column_name_list
    

    @remainder_column_name_list.setter
    def remainder_column_name_list(self, value):
        self._remainder_column_name_list = value


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
        if not node.has_children():
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


    def to_csv(self, csv_file_path):
        """CSV形式でファイルへ出力します"""

        # # 葉要素に番号を振っていく
        # self.renumbering()


        class Context():
            def __init__(self):
                self._cur_depth = 0
                self._max_depth = 0
                self._leaf_entries = []
                

        context = Context()


        def find_leaf(context, entry):
            """葉を収集する。葉の最大深さも調べる"""

            context._cur_depth += 1


            # 最大深さ
            if context._max_depth < context._cur_depth:
                context._max_depth = context._cur_depth


            # 葉要素
            if not entry.has_children():
                context._leaf_entries.append(entry)
            else:
                for child_entry in entry.child_entries.values():
                    find_leaf(context, child_entry) # 再帰


            context._cur_depth -= 1


        # 全ての葉を収集
        for root_entry in self.multiple_root_entry.values():
            find_leaf(context, root_entry)


        # 余り列の名前
        # ------------
        remainder_column_name_set = set()

        for leaf in context._leaf_entries:
            if leaf.remainder_columns is not None:
                for name, value in leaf.remainder_columns.items():
                    remainder_column_name_set.add(name)

        # 順序が指定されているものは消す
        for name in self.remainder_column_name_list:
            if name in remainder_column_name_set:
                remainder_column_name_set.remove(name)

        # 順序を固定する
        remainder_column_name_list = self.remainder_column_name_list.copy()
        remainder_column_name_list.extend(list(remainder_column_name_set))
        #print(f"余り列の順序指定：{self.remainder_column_name_list=}")
        #print(f"余り列の名前　　：{remainder_column_name_list=}")



        #print(f"最大深さ：{context._max_depth=}")

        # テーブルの列を作成する
        #
        #   TODO 余り列を作成したい
        #
        column_names = ['no']

        for i in range(0, context._max_depth + 1):
            column_names.append(f'edge{i}')
            column_names.append(f'node{i}')

        # 余り列を追加
        for remainder_column_name in remainder_column_name_list:
            column_names.append(remainder_column_name)

        # print(f"列名：{column_names=}")
        # print(f"列名の要素数：{len(column_names)=}")


        df = pd.DataFrame(columns=column_names)
        df.set_index('no', inplace=True)
#       print(f"""\
# new df:
# {df}
# """)


        # TODO 葉のすべての親を出力
        for leaf_th, leaf in enumerate(context._leaf_entries, 1):


            cur_entry = leaf
            path = [cur_entry]

            while cur_entry.parent_entry is not None:
                # 逆順で親エントリーが入っていく
                cur_entry = cur_entry.parent_entry
                path.append(cur_entry)


            # エッジ、ノードを交互に入れたリストを作る
            #
            #   TODO 余り列を作成したい
            #
            column_values = [None] * ((context._max_depth + 1) * 2 + len(remainder_column_name_list))
            for entry_no, entry in enumerate(reversed(path)):
                column_values[entry_no * 2] = entry.edge_text
                column_values[entry_no * 2 + 1] = entry.node_text

            # 余り列を追加
            column_no = (context._max_depth + 1) * 2
            for remainder_column_name in remainder_column_name_list:
                if remainder_column_name in leaf.remainder_columns:
                    value = leaf.remainder_columns[remainder_column_name]
                else: 
                    value = None

                column_values[column_no] = value
                column_no += 1

#           print(f"""\
# 列名の要素数：{len(column_names[1:])=}
# 値の要素数　：{len(column_values)=}
# 列名　　　　：{column_names[1:]=}
# 値　　　　　：{column_values=}
# """)

            # 行の追加
            # if len(df) == 0:
            #     new_row_no = 0
            # else:
            #     new_row_no = -1

            df.loc[leaf_th] = column_values


        # 全部欠損している列を削除
        df.dropna(how='all', axis=1, inplace=True)

#        print(f"""\
# df:
# {df}
# """)

        # テーブルをCSV形式でファイルへ保存
        df.to_csv(csv_file_path, encoding='utf8')



#############
# MARK: Entry
#############
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


    def has_children(self):
        """子エントリーを持つか？"""
        return 0 < len(self._child_entries)


    def leaf(self, edge_text, node_text, remainder_columns=None):
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


        if not self.has_children():
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
