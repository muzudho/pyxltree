#
# python example.py all
#
# 例を実行しよう
#

import traceback
import datetime
import sys

from examples.e_o1o0 import execute as execute_e_o1o0
from examples.e_o2o0 import execute as execute_e_o2o0
from examples.e_o3o0 import execute as execute_e_o3o0


########################################
# コマンドから実行時
########################################
if __name__ == '__main__':
    """コマンドから実行時"""

    try:
        args = sys.argv

        if 1 < len(args):
            if args[1] == 'all':
                execute_e_o1o0()
                execute_e_o2o0()
                execute_e_o3o0()

            elif args[1] == '1':
                execute_e_o1o0()

            elif args[1] == '2':
                execute_e_o2o0()

            elif args[1] == '3':
                execute_e_o3o0()

            else:
                raise ValueError(f'unsupported {args[1]=}')
        
        else:
            raise ValueError(f'unsupported {len(args)=}')


    except Exception as err:
        print(f"""\
[{datetime.datetime.now()}] おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")
