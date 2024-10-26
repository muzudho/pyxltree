import gc
import time
import pandas as pd
from ...library import INDENT
from ...models.timeout import Timeout


##############
# MARK: Forest
##############
class Forest():
    """森"""


    def __init__(self):
        self._multiple_root_entry = {}

        self._order_of_remainder_columns = []

        # 探索時に使用する一時変数
        self._temp_leaf_th = None


    @property
    def multiple_root_entry(self):
        return self._multiple_root_entry


    @property
    def order_of_remainder_columns(self):
        """ツリー構造には含まないテーブル列の並び順を指定するのに使います"""
        return self._order_of_remainder_columns
    

    @order_of_remainder_columns.setter
    def order_of_remainder_columns(self, value):
        self._order_of_remainder_columns = value


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


    def to_csv(self, csv_file_path, timeout=Timeout(seconds=864000.0)):
        """CSV形式でファイルへ出力します
        
        Parameters
        ----------
        csv_file_path : str
            CSVファイルへのパス
        timeout : Timeout
            指定秒を経過したら中止します
        
        Returns
        -------
        result : dict
            * `timeup` - bool
            * `timeup_location` - タイムアップが発生した箇所のデバッグ用情報
        """

        # # 葉要素に番号を振っていく
        # self.renumbering()


        start = time.time()


        def look_time(start):
            end = time.time()
            return end - start


        def make_return_value(timeout):
            """戻り値の作成
            
            Parameters
            ----------
            timeout : Timeout
                タイムアウト
            """
            return {'timeout':timeout}


        class Context():
            def __init__(self):
                self._cur_depth = 0
                self._max_depth = 0
                self._leaf_entries = []
                

        context = Context()


        def find_leaf(context, entry):
            """葉を収集する。葉の最大深さも調べる"""

            if timeout.is_expired('recursive find_leaf > head of function'):
                return make_return_value(timeout=timeout)

            context._cur_depth += 1


            # 最大深さ
            if context._max_depth < context._cur_depth:
                context._max_depth = context._cur_depth


            # 葉要素
            if not entry.has_children():
                context._leaf_entries.append(entry)

            else:
                for child_entry in entry.child_entries.values():

                    if timeout.is_expired('recursive find_leaf > child in loop'):
                        return make_return_value(timeout=timeout)

                    find_leaf(context, child_entry) # 再帰


            context._cur_depth -= 1


        # 全ての葉を収集
        for root_entry in self.multiple_root_entry.values():

            if timeout.is_expired('root_entry in loop'):
                return make_return_value(timeout=timeout)

            find_leaf(context, root_entry)


        # 余り列の名前
        # ------------
        remainder_column_name_set = set()

        for leaf in context._leaf_entries:

            if timeout.is_expired('leaf_entry in loop for find remainder columns'):
                return make_return_value(timeout=timeout)

            if leaf.remainder_columns is not None:
                for name, value in leaf.remainder_columns.items():

                    if timeout.is_expired('remainder column in loop'):
                        return make_return_value(timeout=timeout)

                    remainder_column_name_set.add(name)


        # 順序が指定されているものは消す
        for name in self.order_of_remainder_columns:

            if timeout.is_expired('order of remainder column in loop'):
                return make_return_value(timeout=timeout)

            if name in remainder_column_name_set:
                remainder_column_name_set.remove(name)


        # 順序を固定する
        order_of_remainder_columns = self.order_of_remainder_columns.copy()
        order_of_remainder_columns.extend(list(remainder_column_name_set))
        #print(f"余り列の順序指定：{self.order_of_remainder_columns=}")
        #print(f"余り列の名前　　：{order_of_remainder_columns=}")



        #print(f"最大深さ：{context._max_depth=}")

        # 出力する順番に列名を並べる（存在しない列が含まれても構わない。存在する列が含まれていなくても構わない）
        order_of_column_names = ['no']

        for i in range(0, context._max_depth + 1):

            if timeout.is_expired('search depth'):
                return make_return_value(timeout=timeout)

            order_of_column_names.append(f'edge{i}')
            order_of_column_names.append(f'node{i}')


        # 余り列を追加
        for remainder_column_name in order_of_remainder_columns:

            if timeout.is_expired('append remainder column'):
                return make_return_value(timeout=timeout)

            order_of_column_names.append(remainder_column_name)


        # print(f"列名の並び順：{order_of_column_names=}")
        # print(f"列名の並び順の要素数：{len(order_of_column_names)=}")

        df = pd.DataFrame()


        # 葉のすべての親を出力
        for leaf_th, leaf in enumerate(context._leaf_entries, 1):

            if timeout.is_expired('leaf entry in loop for make record'):
                return make_return_value(timeout=timeout)

            cur_entry = leaf
            path = [cur_entry]

            while cur_entry.parent_entry is not None:
                # 逆順で親エントリーが入っていく
                cur_entry = cur_entry.parent_entry
                path.append(cur_entry)

                if timeout.is_expired('find parent entry'):
                    return make_return_value(timeout=timeout)


            record = {'no':leaf_th}

            # * `entry_no` - 根を 0 とする連番
            for entry_no, entry in enumerate(reversed(path)):

                if timeout.is_expired('entry in path'):
                    return make_return_value(timeout=timeout)

                if entry.edge_text is not None:
                    record[f'edge{entry_no}'] = entry.edge_text
                
                if entry.node_text is not None:
                    record[f'node{entry_no}'] = entry.node_text


            # 余り列を追加
            if leaf.remainder_columns is not None:
                for name, value in leaf.remainder_columns.items():

                    if timeout.is_expired('append remainder column to record'):
                        return make_return_value(timeout=timeout)

                    record[name] = value

#                   print(f"""\
# df:
# {df}
# {leaf_th=}
# 列名の並び順の要素数：{len(order_of_column_names[1:])=}
# 列名の並び順　　　　：{order_of_column_names[1:]=}
# レコード　　　　　　：{record}
# """)

            # テーブルに存在しない列は追加する
            for column_name in record.keys():

                if timeout.is_expired('append column to data frame'):
                    return make_return_value(timeout=timeout)

                if column_name not in df.columns.values:
                    df[column_name] = None


            #
            #   NOTE ここで、空テーブルや、空列と連結すると、 pandas から警告が出ることがある
            #   FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
            #
            # NOTE 以下、エラーの状況を分ける
            #
            # データフレームが空のとき
            if df.empty:
                # データフレームにレコード追加
                df.loc[leaf_th] = record

            elif record == {}:
                # 空の辞書を追加しようとしたとき
                df.loc[leaf_th] = record

            # データフレームが空でないとき
            else:
                # NOTE ここで警告が出る？
                # データフレームにレコード追加
                df.loc[leaf_th] = record


        # 全部欠損している列を削除
        df.dropna(how='all', axis=1, inplace=True)


#         print(f"""\
# df:
# {df}
# 実際の列名の要素数　：{len(df.columns.values)}
# 実際の列名一覧　　　：{df.columns.values}
# 列名の並び順の要素数：{len(order_of_column_names[1:])}
# 列名の並び順　　　　：{order_of_column_names[1:]}
# """)

        # ［実際の列名一覧］をコピーして［順序の指定されていない列名一連］を作る
        no_order_of_column_names = list(df.columns.values)
        # print(f"(1) ［実際の列名一覧］={df.columns.values}")
        # print(f"(2) ［列名の並び順］={order_of_column_names}")

        # ［列名の並び順］に有る列名が、［順序の指定されていない列名一連］にあれば、［順序の指定されていない列名一連］から削除する
        for column_name in order_of_column_names:

            if timeout.is_expired('remove column name from no order column names'):
                return make_return_value(timeout=timeout)

            if column_name in no_order_of_column_names:
                no_order_of_column_names.remove(column_name)
        #print(f"(3) ［順序の指定されていない列名一連］={no_order_of_column_names}")


        # ［列名の並び順］から、［実際の列名一覧］に有る列名だけを残し、［再：列名の並び順］とする。このとき 'no' インデックスが消える
        reorder_of_column_names = []
        for column_name in order_of_column_names:

            if timeout.is_expired('append column name to reorder of column names'):
                return make_return_value(timeout=timeout)

            if column_name in df.columns.values:
                reorder_of_column_names.append(column_name)
        #print(f"(4) ［再：列名の並び順］={reorder_of_column_names}")

        # ［再：列名の並び順］と［順序の指定されていない列名一連］を連結して、［出力する列名一連］とする
        output_column_names = reorder_of_column_names + no_order_of_column_names
        #print(f"(5) ［出力する列名一連］={output_column_names}")


#         print(f"""\
# f:
# {df}""")

        # テーブルをCSV形式でファイルへ保存
        df.to_csv(
                csv_file_path,
                encoding='utf8',
                columns=output_column_names,
                index=False)


        # オブジェクトの破棄
        del df
        # メモリ解放
        gc.collect()

        return make_return_value(timeout=timeout)


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


    def get_child(self, edge_text, node_text, default=None):
        """子要素を取得。無ければデフォルト値を返します"""
        pack_key = TreeEntry._pack_key_static(edge_text=edge_text, node_text=node_text)
        if self.has_child(edge_text=edge_text, node_text=node_text):
            return self.child_entries[pack_key]
        else:
            return default


    def has_child(self, edge_text, node_text):
        """子要素が既存か？"""
        pack_key = TreeEntry._pack_key_static(edge_text=edge_text, node_text=node_text)
        return pack_key in self._child_entries


    @staticmethod
    def _pack_key_static(edge_text, node_text):
        return (edge_text, node_text)


    def _pack_key(self):
        return TreeEntry._pack_key_static(edge_text=self._edge_text, node_text=self._node_text)


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
