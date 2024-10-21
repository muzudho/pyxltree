import datetime
import pandas as pd
from .library import TableControl


class ColumnsSorting():
    """列ソート"""


    def sort_columns(df):
        """列ソート

        TODO 列名をソートしたい。no,node0,edge1,node1,edge2,node2,remaining_a,remaining_b,... のような感じに
        """

        # 'no' はインデックスなので、列名にはない
        last_end_th_of_node, last_end_th_of_edge, others_name_list = TableControl.sort_out_column_names_node_edge_others(df)

        # 'no' 列を含まないようにしてください
        column_name_list = []

        if last_end_th_of_node < 0:
            raise ValueError(f'node0 列がありませんでした  {last_end_th_of_edge=}  {last_end_th_of_node=}  {others_name_list=}')
        
        # node0 列を追加
        column_name_list.append('node0')

        for i in range(1, last_end_th_of_node + 1):

            # あれば edge{i} 列を追加
            if i <= last_end_th_of_edge:
                column_name_list.append(f'edge{i}')

            # node{i} 列を追加
            column_name_list.append(f'node{i}')

        # 残りの列名を追加
        column_name_list.extend(others_name_list)

        return df[column_name_list]


class InputCompletion():
    """入力補完"""


    @staticmethod
    def fill_directory(df, end_node_th, debug_write=False):
        """ディレクトリーの空欄を埋めます
        
        Before:
            a,b,c,d,e,f,g,h,i
                ,j,k,l, ,m,n,o
                , ,p,      q
        
        After:
            a,b,c,d,e,f,g,h,i
            a,j,k,l,e,m,n,o
            a,j,p,l,e,m,n
        """

        last_node_th = end_node_th - 1

        if debug_write:
            print(f"[{datetime.datetime.now()}] このテーブルは{end_node_th}個のノードがある。最終ノードは {last_node_th}")

        row_size = len(df)

        # ２行目から、１行ずつ行う
        for row_th in range(2, row_size + 1):

            # この行について、最終ノード列を調べる
            actual_last_node_th = last_node_th   # 最終ノードから開始
            for node_th in reversed(range(0, end_node_th)):
                column_name = f'node{node_th}'

                # 縮めていく
                actual_last_node_th = node_th

                if not pd.isnull(df.at[row_th, column_name]):
                    break


            if debug_write:
                print(f"[{datetime.datetime.now()}] 第{row_th}行は第{actual_last_node_th}ノードまで")

            # この行について、最終ノード列まで、ノードの空欄は上行をコピーする
            for node_th in range(0, actual_last_node_th + 1):

                column_name = f'node{node_th}'

                if pd.isnull(df.at[row_th, column_name]):
                    df.at[row_th, column_name] = df.at[row_th - 1, column_name]
