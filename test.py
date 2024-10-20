#
# python test.py 2
#
# エクセルで樹形図を描こう
#

import traceback
import datetime
import sys

from tests.manual import execute as execute_manual
from tests.no_1 import execute as execute_no_1
from tests.no_2 import execute as execute_no_2
from tests.o3o1o0 import execute as execute_o3o1o0
from tests.o3o2o0_do_not_merge_cells import execute as execute_o3o2o0
from tests.no_4 import execute as execute_no_4
from tests.no_5 import execute as execute_no_5


########################################
# コマンドから実行時
########################################
if __name__ == '__main__':
    """コマンドから実行時"""

    try:
        args = sys.argv

        if 1 < len(args):

            if args[1] == 'all':
                execute_no_1()
                execute_no_2()
                execute_o3o1o0()
                execute_o3o2o0()
                execute_no_4()
                execute_no_5()

            elif args[1] == '1':
                execute_no_1()

            elif args[1] == '2':
                execute_no_2()

            elif args[1] == 'o3o1o0':
                execute_o3o1o0()

            elif args[1] == 'o3o2o0':
                execute_o3o2o0()

            elif args[1] == '4':
                execute_no_4()

            elif args[1] == '5':
                execute_no_5()
            
            else:
                raise ValueError(f'unsupported {args[1]=}')
        
        else:
            execute_manual()


    except Exception as err:
        print(f"""\
[{datetime.datetime.now()}] おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")
