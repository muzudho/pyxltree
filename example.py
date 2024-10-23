#
# python example.py all
#
# 例を実行しよう
#

import traceback
import datetime
import sys


########################################
# コマンドから実行時
########################################
if __name__ == '__main__':
    """コマンドから実行時"""

    try:
        args = sys.argv

        if 1 < len(args):
            if args[1] == 'all':
                from examples.o1o0 import *
                from examples.o2o0 import *
                from examples.o3o0 import *

            elif args[1] == '1':
                from examples.o1o0 import *

            elif args[1] == '2':
                from examples.o2o0 import *

            elif args[1] == '3':
                from examples.o3o0 import *

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
