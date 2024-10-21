import re


class TableControl():


    _pattern_of_column_name_of_node = re.compile(r'node(\d+)')
    _pattern_of_column_name_of_edge = re.compile(r'edge(\d+)')


    @classmethod
    @property
    def pattern_of_column_name_of_node(clazz):
        return clazz._pattern_of_column_name_of_node


    @classmethod
    @property
    def pattern_of_column_name_of_edge(clazz):
        return clazz._pattern_of_column_name_of_edge


    @staticmethod
    def get_column_location_by_column_name(df, column_name):
        return df.columns.get_loc(column_name)


    @staticmethod
    def sort_out_column_names_node_edge_others(df):
        """列名を edge, node, それ以外の３つに分けます。
        edge と node は最後の要素の数字を返します。要素がなければ -1 を返します"""
        edge_th_set = set()
        node_th_set = set()
        others_name_list = []

        # 'no' はインデックスなので、列には含まれない
        for column_name in df.columns.values:
            result = TableControl.pattern_of_column_name_of_edge.match(column_name)
            if result:
                edge_th_set.add(int(result.group(1)))
                continue

            result = TableControl.pattern_of_column_name_of_node.match(column_name)
            if result:
                node_th_set.add(int(result.group(1)))
                continue
            
            others_name_list.append(column_name)
        
        # node 列は 0 から連番で続いているところまで有効にします
        last_node_th = -1
        for i in range(0, len(node_th_set)):
            if i not in node_th_set:
                break

            node_th_set.remove(i)
            last_node_th = i

        # 残っている node 列は others リストに入れます
        for node_th in node_th_set:
            others_name_list.append(f'node{node_th}')

        # edge 列は 1 から last_node_th まで連番で続いているところだけ有効にします
        last_edge_th = -1
        for i in range(1, last_node_th + 1):
            if i not in node_th_set:
                break

            edge_th_set.remove(i)
            last_edge_th = i

        # 残っている edge 列は others リストに入れます
        for edge_th in edge_th_set:
            others_name_list.append(f'edge{edge_th}')


        return last_node_th, last_edge_th, others_name_list


    @staticmethod
    def find_end_th_of_column(df, prefix, start_number):
        """'prefix{n}'列を数える。nは0から始まる
        
        列名を左から見ていくと、 node0, node1, node2 といった形で 0から始まる昇順の連番が付いている "node数" 形式の列名が見つかるものとします

        TODO TableControl.sort_out_column_names_node_edge_others() を使って列名を振り分けてからこのメソッドを使うと高速化できそう

        Parameters
        ----------
        df : DataFrame
            データフレーム
        prefix : str
            列名の数字の前の部分。 'node' または 'edge'
        start_number : int
            開始番号。エッジなら 1、ノードなら 0
        """

        if prefix == 'node':
            pattern_of_column_name = TableControl._pattern_of_column_name_of_node

        elif prefix == 'edge':
            pattern_of_column_name = TableControl._pattern_of_column_name_of_edge

        else:
            raise ValueError(f'{prefix}')

        expected_item_th = start_number    # 次は 'node{0}' を期待する
        for column_name in df.columns.values:
            result = pattern_of_column_name.match(column_name)
            if result:
                item_th = int(result.group(1))
                if expected_item_th == item_th:
                    expected_item_th += 1

        # テーブルにあるノード数
        #print(f"[{datetime.datetime.now()}] Table has {expected_item_th} nodes root node included")

        return expected_item_th     # end 番号に相当
