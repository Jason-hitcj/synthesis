import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


class TransactionGeneratorLegal:
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

    def generate_small_transfers(self, sender, receiver, risk=0, num_transactions=None):
        """
        生成小额频繁转账模式
        适用场景：日常生活支付、租金、水电费等

        Args:
            sender (Person): 发送方
            receiver (Person): 接收方
            num_transactions (int, optional): 交易数量, 默认随机20-50笔
            risk (str): 交易风险等级
        """
        if num_transactions is None:
            num_transactions = random.randint(20, 50)

        transactions = []
        for _ in range(num_transactions):
            amount = round(random.uniform(100, 2000), 2)  # 100-2000元的小额转账
            timestamp = self._generate_timestamp()

            sender_id = sender.person_id
            receiver_id = receiver.person_id
            sender_card = random.choice(sender.cards) if sender.cards else None
            receiver_card = random.choice(receiver.cards) if receiver.cards else None

            if amount > sender_card.balance and sender_card.balance > 0:
                continue

            sender_card_balance_old = sender_card.balance
            sender_card.balance = sender_card.balance - amount
            receiver_card_balance_old = receiver_card.balance if receiver_card.card_type == 'C' else 0
            receiver_card.balance = receiver_card.balance + amount
            receiver_card_balance_new = receiver_card.balance if receiver_card.card_type == 'C' else 0

            transaction = {
                'sender_id': sender_id,
                'sender_card_bank': sender_card.bank_name,
                'sender_card_number': sender_card.account_number,
                'sender_card_balance_old': sender_card_balance_old,
                'sender_card_balance_new': sender_card.balance,
                'receiver_id': receiver_id,
                'receiver_card_bank': receiver_card.bank_name,
                'receiver_card_number': receiver_card.account_number,
                'receiver_card_balance_old': receiver_card_balance_old,
                'receiver_card_balance_new': receiver_card_balance_new,
                'amount': round(amount, 2),
                'timestamp': timestamp,
                'transaction_type': 'small_transfer',
                'risk_level': risk
            }
            transactions.append(transaction)

        return pd.DataFrame(transactions) if num_transactions > 1 else transactions[0]

    def generate_medium_transfers(self, sender, receiver, risk=0, num_transactions=None):
        """
        生成中等金额转账模式
        适用场景：购物、装修、购买电子产品等

        Args:
            sender (Person): 发送方
            receiver (Person): 接收方
            num_transactions (int, optional): 交易数量, 默认随机5-15笔
            risk (str): 交易风险等级
        """
        if num_transactions is None:
            num_transactions = random.randint(5, 15)

        transactions = []
        for _ in range(num_transactions):
            amount = round(random.uniform(2000, 20000), 2)  # 2000-20000元的中额转账
            timestamp = self._generate_timestamp()

            sender_id = sender.person_id
            receiver_id = receiver.person_id
            sender_card = random.choice(sender.cards) if sender.cards else None
            receiver_card = random.choice(receiver.cards) if receiver.cards else None

            if amount > sender_card.balance and sender_card.balance > 0:
                continue

            sender_card_balance_old = sender_card.balance
            sender_card.balance = sender_card.balance - amount
            receiver_card_balance_old = receiver_card.balance if receiver_card.card_type == 'C' else 0
            receiver_card.balance = receiver_card.balance + amount
            receiver_card_balance_new = receiver_card.balance if receiver_card.card_type == 'C' else 0

            transaction = {
                'sender_id': sender_id,
                'sender_card_bank': sender_card.bank_name,
                'sender_card_number': sender_card.account_number,
                'sender_card_balance_old': sender_card_balance_old,
                'sender_card_balance_new': sender_card.balance,
                'receiver_id': receiver_id,
                'receiver_card_bank': receiver_card.bank_name,
                'receiver_card_number': receiver_card.account_number,
                'receiver_card_balance_old': receiver_card_balance_old,
                'receiver_card_balance_new': receiver_card_balance_new,
                'amount': round(amount, 2),
                'timestamp': timestamp,
                'transaction_type': 'medium_transfer',
                'risk_level': risk
            }
            transactions.append(transaction)

        return pd.DataFrame(transactions) if num_transactions > 1 else transactions[0]

    def generate_large_transfers(self, sender, receiver, risk=0, num_transactions=None):
        """
        生成大额转账模式
        适用场景：购房首付、购车等

        Args:
            sender (Person): 发送方
            receiver (Person): 接收方
            num_transactions (int, optional): 交易数量, 默认随机1-3笔
            risk (str): 交易风险等级
        """
        if num_transactions is None:
            num_transactions = random.randint(1, 3)

        transactions = []
        for _ in range(num_transactions):
            amount = round(random.uniform(20000, 200000), 2)  # 20000-200000元的大额转账
            timestamp = self._generate_timestamp()

            sender_id = sender.person_id
            receiver_id = receiver.person_id
            sender_card = random.choice(sender.cards) if sender.cards else None
            receiver_card = random.choice(receiver.cards) if receiver.cards else None

            if amount > sender_card.balance and sender_card.balance > 0:
                continue

            sender_card_balance_old = sender_card.balance
            sender_card.balance = sender_card.balance - amount
            receiver_card_balance_old = receiver_card.balance if receiver_card.card_type == 'C' else 0
            receiver_card.balance = receiver_card.balance + amount
            receiver_card_balance_new = receiver_card.balance if receiver_card.card_type == 'C' else 0

            transaction = {
                'sender_id': sender_id,
                'sender_card_bank': sender_card.bank_name,
                'sender_card_number': sender_card.account_number,
                'sender_card_balance_old': sender_card_balance_old,
                'sender_card_balance_new': sender_card.balance,
                'receiver_id': receiver_id,
                'receiver_card_bank': receiver_card.bank_name,
                'receiver_card_number': receiver_card.account_number,
                'receiver_card_balance_old': receiver_card_balance_old,
                'receiver_card_balance_new': receiver_card_balance_new,
                'amount': round(amount, 2),
                'timestamp': timestamp,
                'transaction_type': 'large_transfer',
                'risk_level': risk
            }
            transactions.append(transaction)

        return pd.DataFrame(transactions) if num_transactions >= 1 else transactions[0]

    def generate_investment_transfers(self, sender, receiver, risk=0, num_transactions=None):
        """
        生成投资类大额转账模式
        适用场景：理财产品、股票投资、基金投资等

        Args:
            sender (Person): 发送方
            receiver (Person): 接收方
            num_transactions (int, optional): 交易数量, 默认随机3-8笔
            risk (str): 交易风险等级
        """
        if num_transactions is None:
            num_transactions = random.randint(3, 8)

        transactions = []
        for _ in range(num_transactions):
            # 使用对数正态分布生成投资金额，使其更符合真实投资场景
            amount = round(np.random.lognormal(mean=11, sigma=1) , 2) # 生成较多50000-200000之间的金额
            timestamp = self._generate_timestamp()

            sender_id = sender.person_id
            receiver_id = receiver.person_id
            sender_card = random.choice(sender.cards) if sender.cards else None
            receiver_card = random.choice(receiver.cards) if receiver.cards else None

            if amount > sender_card.balance and sender_card.balance > 0:
                continue

            sender_card_balance_old = sender_card.balance
            sender_card.balance = sender_card.balance - amount
            receiver_card_balance_old = receiver_card.balance if receiver_card.card_type == 'C' else 0
            receiver_card.balance = receiver_card.balance + amount
            receiver_card_balance_new = receiver_card.balance if receiver_card.card_type == 'C' else 0

            transaction = {
                'sender_id': sender_id,
                'sender_card_bank': sender_card.bank_name,
                'sender_card_number': sender_card.account_number,
                'sender_card_balance_old': sender_card_balance_old,
                'sender_card_balance_new': sender_card.balance,
                'receiver_id': receiver_id,
                'receiver_card_bank': receiver_card.bank_name,
                'receiver_card_number': receiver_card.account_number,
                'receiver_card_balance_old': receiver_card_balance_old,
                'receiver_card_balance_new': receiver_card_balance_new,
                'amount': round(amount, 2),
                'timestamp': timestamp,
                'transaction_type': 'investment_transfer',
                'risk_level': risk
            }
            transactions.append(transaction)

        return pd.DataFrame(transactions) if num_transactions > 1 else transactions[0]

    def generate_frequent_large_transfers(self, sender, receiver, risk=0, num_transactions=None):
        """
        生成频繁大额转账模式
        适用场景：商业经营、企业资金往来等
        注意：这种模式可能需要特别关注，因为可能涉及洗钱风险

        Args:
            sender (Person): 发送方
            receiver (Person): 接收方
            num_transactions (int, optional): 交易数量, 默认随机15-30笔
            risk (str): 交易风险等级
        """
        if num_transactions is None:
            num_transactions = random.randint(15, 30)

        transactions = []
        for _ in range(num_transactions):
            amount = round(random.uniform(50000, 500000), 2)  # 50000-500000元的大额频繁转账
            timestamp = self._generate_timestamp()

            sender_id = sender.person_id
            receiver_id = receiver.person_id
            sender_card = random.choice(sender.cards) if sender.cards else None
            receiver_card = random.choice(receiver.cards) if receiver.cards else None

            if amount > sender_card.balance and sender_card.balance > 0:
                continue

            sender_card_balance_old = sender_card.balance
            sender_card.balance = sender_card.balance - amount
            receiver_card_balance_old = receiver_card.balance if receiver_card.card_type == 'C' else 0
            receiver_card.balance = receiver_card.balance + amount
            receiver_card_balance_new = receiver_card.balance if receiver_card.card_type == 'C' else 0

            transaction = {
                'sender_id': sender_id,
                'sender_card_bank': sender_card.bank_name,
                'sender_card_number': sender_card.account_number,
                'sender_card_balance_old': sender_card_balance_old,
                'sender_card_balance_new': sender_card.balance,
                'receiver_id': receiver_id,
                'receiver_card_bank': receiver_card.bank_name,
                'receiver_card_number': receiver_card.account_number,
                'receiver_card_balance_old': receiver_card_balance_old,
                'receiver_card_balance_new': receiver_card_balance_new,
                'amount': round(amount, 2),
                'timestamp': timestamp,
                'transaction_type': 'frequent_large_transfer',
                'risk_level': risk
            }
            transactions.append(transaction)

        return pd.DataFrame(transactions) if num_transactions > 1 else transactions[0]

    def generate_aa_payments(self, participants, total_amount, risk=0):
        """
        生成AA制交易模式
        适用场景：聚餐、团建、集体活动等场景的费用分摊

        Args:
            participants (list): 参与AA的用户列表
            total_amount (float): 活动总费用

        Returns:
            list: 包含所有AA制相关交易的列表
        """
        transactions = []

        timestamp = self._generate_timestamp()

        # 每人应付金额
        per_person_amount = total_amount

        # 随机选择收款人
        payer = random.choice(participants)
        receiver_id = payer.person_id
        receiver_card = random.choice(payer.cards) if payer.cards else None

        # 生成转账记录
        for participant in participants:
            if participant != payer:  # 不包括付款方自己
                sender_id = participant.person_id
                sender_card = random.choice(participant.cards) if participant.cards else None

                if per_person_amount > sender_card.balance and sender_card.balance > 0:
                    continue

                sender_card_balance_old = sender_card.balance
                sender_card.balance = sender_card.balance - per_person_amount
                receiver_card_balance_old = receiver_card.balance if receiver_card.card_type == 'C' else 0
                receiver_card.balance = receiver_card.balance + per_person_amount
                receiver_card_balance_new = receiver_card.balance if receiver_card.card_type == 'C' else 0

                transaction = {
                    'sender_id': sender_id,
                    'sender_card_bank': sender_card.bank_name,
                    'sender_card_number': sender_card.account_number,
                    'sender_card_balance_old': sender_card_balance_old,
                    'sender_card_balance_new': sender_card.balance,
                    'receiver_id': receiver_id,
                    'receiver_card_bank': receiver_card.bank_name,
                    'receiver_card_number': receiver_card.account_number,
                    'receiver_card_balance_old': receiver_card_balance_old,
                    'receiver_card_balance_new': receiver_card_balance_new,
                    'amount': per_person_amount,
                    'timestamp': timestamp + timedelta(minutes=random.randint(1, 60)),  # 添加随机延迟
                    'transaction_type': 'aa_payment',
                    'risk_level': risk,
                    # 'group_id': f'aa_{timestamp.strftime("%Y%m%d_%H%M")}',  # 添加群组ID以关联同一活动的交易
                    # 'total_amount': total_amount,
                    # 'participants_count': len(participants)
                }
                transactions.append(transaction)

        return pd.DataFrame(transactions)

    # def generate_mixed_pattern(self, sender, receiver, pattern_weights=None):
    #     """
    #     更新后的混合交易模式，加入AA制场景
    #
    #     Args:
    #         sender (Person): 发送方
    #         receiver (Person): 接收方
    #         pattern_weights (dict, optional): 各种模式的权重字典
    #     """
    #     if pattern_weights is None:
    #         pattern_weights = {
    #             'small': 0.4,
    #             'medium': 0.2,
    #             'large': 0.1,
    #             'investment': 0.1,
    #             'frequent_large': 0.05,
    #             'aa_payment': 0.15
    #         }
    #
    #     all_transactions = []
    #
    #     # 生成小额转账
    #     num_small = int(50 * pattern_weights['small'])
    #     all_transactions.extend(self.generate_small_transfers(sender, receiver, num_small, 'low'))
    #
    #     # 生成中额转账
    #     num_medium = int(15 * pattern_weights['medium'])
    #     all_transactions.extend(self.generate_medium_transfers(sender, receiver, num_medium, 'medium'))
    #
    #     # 生成大额转账
    #     num_large = int(3 * pattern_weights['large'])
    #     all_transactions.extend(self.generate_large_transfers(sender, receiver, num_large, 'medium'))
    #
    #     # 生成投资转账
    #     num_investment = int(8 * pattern_weights['investment'])
    #     all_transactions.extend(self.generate_investment_transfers(sender, receiver, num_investment, 'medium'))
    #
    #     # 生成频繁大额转账
    #     num_frequent_large = int(30 * pattern_weights['frequent_large'])
    #     all_transactions.extend(self.generate_frequent_large_transfers(sender, receiver, num_frequent_large, 'high'))
    #
    #     # 生成AA制转账
    #     num_aa = int(15 * pattern_weights['aa_payment'])
    #     for _ in range(num_aa):
    #         # 随机选择参与人数（3-8人）
    #         num_participants = random.randint(3, 8)
    #         participants = random.sample([sender, receiver] + [Person() for _ in range(num_participants - 2)],
    #                                      num_participants)
    #         total_amount = random.uniform(200, 10000)
    #         all_transactions.extend(self.generate_aa_payments(participants, total_amount, self._generate_timestamp()))
    #
    #     # 按时间排序
    #     all_transactions.sort(key=lambda x: x['timestamp'])
    #
    #     return all_transactions


if __name__ == "__main__":
    pass
