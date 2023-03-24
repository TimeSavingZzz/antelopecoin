from hashlib import sha256

import random
from datetime import datetime
pow2, sum1 = 1, 0
mx = 0
mi = 10000
for pow1 in range(1, 100001):
    while True:
        random_year = random.randint(2000, 2023)
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)  # 为简单起见，我们假设每个月都有 28 天
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        # 使用 datetime 库创建一个 datetime 对象
        random_datetime = datetime(random_year, random_month, random_day, random_hour, random_minute, random_second)

        # 将 datetime 对象转换为 "%Y-%m-%d-%H:%M:%S" 格式的字符串
        formatted_datetime = random_datetime.strftime("%Y-%m-%d-%H:%M:%S")

        sha = sha256(f'{formatted_datetime}{pow2}'.encode()).hexdigest()
        if sha[:1] == "0":
            sum1 += pow2
            if pow2 < mi:
                mi = pow2
            if pow2 > mx:
                mx = pow2
            pow2 = 1
            break
        pow2 += 1
print(sum1 // 100000)
print(mi, mx)