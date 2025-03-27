import random
from datetime import timedelta, datetime
import numpy as np
import pandas as pd

"""
    生成异常交易模式
    
"""
class TransactionGeneratorIllegal:
    def __init__(self, start_date, end_date):
        """
        初始化交易生成器

        Args:
            start_date (datetime): 交易开始日期
            end_date (datetime): 交易结束日期
        """
        self.start_date = start_date
        self.end_date = end_date

    def _generate_weighted_random_time(self):
        """生成加权随机时间，精确到秒"""
        # 定义时间段及其权重
        time_slots = [
            (9, 18, 5),  # 白天正常交易时间 9:00 - 18:00，权重为5
            (0, 6, 1),   # 凌晨异常交易时间 00:00 - 6:00，权重为1
            (6, 9, 2),   # 早上 6:00 - 9:00，权重为2
            (18, 24, 2)  # 晚上 18:00 - 24:00，权重为2
        ]

        # 计算总权重
        total_weight = sum(slot[2] for slot in time_slots)

        # 生成一个随机数
        rand_num = random.uniform(0, total_weight)

        # 累计权重，找到对应的时段
        cumulative_weight = 0
        for start_hour, end_hour, weight in time_slots:
            cumulative_weight += weight
            if rand_num < cumulative_weight:
                hour = random.randint(start_hour, end_hour - 1)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                return hour, minute, second

    def _generate_timestamp(self):
        """生成随机时间戳，具体到秒"""
        time_between_dates = self.end_date - self.start_date
        total_seconds = int(time_between_dates.total_seconds())
        random_seconds = random.randint(0, total_seconds)
        random_date = self.start_date + timedelta(seconds=random_seconds)

        # 生成加权随机时间
        hour, minute, second = self._generate_weighted_random_time()
        random_date = random_date.replace(hour=hour, minute=minute, second=second, microsecond=0)
        return random_date

    def generate_regular_pattern_transfers(self, sender, receiver, base_amount=10000,
                                           risk=2, num_cycles=6, x_threshold=3000,
                                           y_threshold=3):
        """
        生成具有明显规律性的异常转账模式
        特征：
        1. 入账金额相同且<=X元(默认3000)
        2. 半年内相同金额入账
        3. 相邻交易间隔差异<=Y天(默认3天)
        4. 最早入账前2个月有万元整数倍的转出
        5. 金额呈倍数关系

        Args:
            sender: 发送方(资金转出方)
            receiver: 接收方(资金转入方)
            base_amount: 基础金额(通常为万元)
            risk: 风险等级
            num_cycles: 交易周期数(半年约6次)
            x_threshold: 入账金额阈值(元)
            y_threshold: 时间间隔差异阈值(天)
        """
        # 确保入账金额<=X元
        transfer_amount = min(base_amount * 0.3, x_threshold)  # 示例按基础金额的30%计算

        # 生成交易时间序列(确保间隔规律)
        time_intervals = [random.randint(28, 31) for _ in range(num_cycles)]  # 每月一次，间隔28-31天
        # 确保最大最小间隔差<=Y天
        while max(time_intervals) - min(time_intervals) > y_threshold:
            time_intervals = [random.randint(28, 31) for _ in range(num_cycles)]

        # 生成交易时间(从当前往前推180天)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        current_date = start_date

        # 最早入账前2个月(60天)的转出交易(万元整数倍)
        initial_out_date = current_date - timedelta(days=60)
        initial_out_amount = base_amount * random.randint(1, 5)  # 1-5万元的整数倍

        # 生成初始转出交易
        transactions = []
        sender_card = self._select_valid_card(sender, initial_out_amount)
        if sender_card:
            initial_trans = self._execute_transfer(
                sender, receiver, sender_card, random.choice(receiver.cards),
                initial_out_amount, initial_out_date.strftime("%Y-%m-%d %H:%M:%S"),
                'regular_pattern_initial', risk
            )
            transactions.append(initial_trans)

        # 生成规律性入账交易
        for interval in time_intervals:
            current_date += timedelta(days=interval)
            timestamp = current_date.strftime("%Y-%m-%d %H:%M:%S")

            # 随机选择倍数关系(1-3倍)
            multiple = random.randint(1, 3)
            amount = round(transfer_amount * multiple, 2)

            sender_card = self._select_valid_card(sender, amount)
            if not sender_card:
                continue

            trans = self._execute_transfer(
                sender, receiver, sender_card, random.choice(receiver.cards),
                amount, timestamp, 'regular_pattern_in', risk
            )
            transactions.append(trans)

        # 添加一些倍数关系的返利交易
        for _ in range(int(num_cycles * 0.5)):  # 约50%的返利交易
            current_date += timedelta(days=random.randint(5, 10))
            timestamp = current_date.strftime("%Y-%m-%d %H:%M:%S")

            # 返利金额与之前交易呈倍数关系
            reference_amount = random.choice([t['amount'] for t in transactions if t['amount'] <= x_threshold])
            rebate_amount = round(reference_amount * random.uniform(0.5, 1.5), 2)  # 0.5-1.5倍的返利

            sender_card = self._select_valid_card(sender, rebate_amount)
            if sender_card:
                trans = self._execute_transfer(
                    sender, receiver, sender_card, random.choice(receiver.cards),
                    rebate_amount, timestamp, 'regular_pattern_rebate', risk
                )
                transactions.append(trans)

        df = pd.DataFrame(transactions)

        # 按时间排序
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        df['timestamp'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        return df


if __name__ == "__main__":
    pass