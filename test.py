import random
from datetime import timedelta


class IncrementalTimestampGenerator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.last_timestamp = start_date  # 初始化时使用开始时间

    def _generate_weighted_time(self):
        """生成加权随机时间（白天权重高）"""
        hour_weights = [1]*24
        for h in range(9, 18):  # 9AM-6PM权重高
            hour_weights[h] = 3
        hour = random.choices(range(24), weights=hour_weights)[0]
        return hour, random.randint(0, 59), random.randint(0, 59)

    def generate(self):
        """生成严格递增的时间戳"""
        # 计算剩余时间范围
        remaining_duration = self.end_date - self.last_timestamp
        if remaining_duration.total_seconds() <= 0:
            raise ValueError("No more timestamps can be generated")

        # 在剩余时间中随机选择一个增量（至少1秒）
        max_increment = remaining_duration.total_seconds()
        increment = random.randint(1, int(max_increment))

        # 生成新时间戳
        new_timestamp = self.last_timestamp + timedelta(seconds=increment)

        # 应用加权时间（只修改时间部分，保持日期递增）
        hour, minute, second = self._generate_weighted_time()
        new_timestamp = new_timestamp.replace(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=0
        )

        # 确保不会超出结束时间
        if new_timestamp > self.end_date:
            new_timestamp = self.end_date

        self.last_timestamp = new_timestamp
        return new_timestamp



if __name__ == "__main__":

