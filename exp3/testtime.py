from datetime import datetime, time
from time import sleep

Dt = [datetime(2022, 3, 2, 14, 59),  # 最前面的位置是当前bar的开始时间
                   datetime(2022, 3, 2, 14, 58),  # 前一个bar的开始时间
                   datetime(2022, 3, 2, 14, 57),
                   datetime(2022, 3, 2, 14, 56),
                   datetime(2022, 3, 2, 14, 55)]

cur_time = datetime.now()
while time(9, 30) < cur_time.time() < time(14, 42,30):
    print("ok")
    sleep(5)
    cur_time = datetime.now()
print("finish")